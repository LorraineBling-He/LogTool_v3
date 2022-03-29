from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import os
from django_webssh import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LogTool_v3.settings')

# application = ProtocolTypeRouter({
#     "http":get_asgi_application(),
#     'websocket': AuthMiddlewareStack(
#         URLRouter(routing.websocket_urlpatterns)
#     ),
# })

application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    'websocket':URLRouter(routing.websocket_urlpatterns),
})