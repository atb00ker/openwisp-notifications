import openwisp_notifications.websockets.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        'websocket': AuthMiddlewareStack(
            URLRouter(openwisp_notifications.websockets.routing.websocket_urlpatterns)
        ),
    }
)
