from asgiref.sync import async_to_sync
from channels import layers


def update_widget(reload_widget=False):
    channel_layer = layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "ow_notification",
        {"type": "notification.update_widget", "reload_widget": reload_widget},
    )
