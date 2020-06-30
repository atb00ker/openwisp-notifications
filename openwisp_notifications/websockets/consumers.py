import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope['user'].is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                "ow_notification", self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "ow_notification", self.channel_name
        )

    def notification_update_widget(self, event):
        user = self.scope['user']
        unread_notifications = user.notifications.unread().count()
        self.send(
            json.dumps(
                {
                    'notification_count': unread_notifications,
                    'reload_widget': event['reload_widget'],
                }
            )
        )
