import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from openwisp_notifications.api.serializers import NotificationListSerializer
from openwisp_notifications.signals import notify
from openwisp_notifications.swapper import load_model
from tests.openwisp2.routing import application

Notification = load_model('Notification')
User = get_user_model()


@database_sync_to_async
def create_notification(admin_user):
    n = notify.send(sender=admin_user, type='default').pop()
    return n[1].pop()


@database_sync_to_async
def notification_operation(notification, mark_read=False, delete=False):
    if mark_read:
        notification.mark_as_read()
    if delete:
        notification.delete()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestNotificationSockets:
    async def _get_communicator(self, admin_client):
        communicator = WebsocketCommunicator(
            application,
            path="ws/notifications/",
            headers=[
                (
                    b'cookie',
                    f'sessionid={admin_client.cookies["sessionid"].value}'.encode(
                        'ascii'
                    ),
                )
            ],
        )
        connected, subprotocol = await communicator.connect()
        assert connected is True
        return communicator

    async def test_new_notification_created(self, admin_user, admin_client):
        communicator = await self._get_communicator(admin_client)
        n = await create_notification(admin_user)
        response = await communicator.receive_json_from()
        response = await communicator.receive_json_from()
        exp_res = {
            'notification_count': 1,
            'reload_widget': True,
            'notification': NotificationListSerializer(n).data,
        }
        assert response == exp_res
        await communicator.disconnect()

    async def test_read_notification(self, admin_user, admin_client):
        n = await create_notification(admin_user)
        communicator = await self._get_communicator(admin_client)
        await notification_operation(n, mark_read=True)
        response = await communicator.receive_json_from(timeout=2)
        exp_response = {
            'notification_count': 0,
            'reload_widget': False,
            'notification': None,
        }
        assert response == exp_response
        await communicator.disconnect()

    async def test_delete_notification(self, admin_user, admin_client):
        n = await create_notification(admin_user)
        communicator = await self._get_communicator(admin_client)
        await notification_operation(n, delete=True)
        response = await communicator.receive_json_from()
        exp_response = {
            'notification_count': 0,
            'reload_widget': True,
            'notification': None,
        }
        assert response == exp_response
        await communicator.disconnect()

    async def test_unauthenticated_user(self, client):
        client.cookies["sessionid"] = "random"
        with pytest.raises(AssertionError):
            await self._get_communicator(client)
