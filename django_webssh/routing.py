from django.conf.urls import url
from django.urls import path, re_path
from django_webssh.tools.channel import websocket

websocket_urlpatterns = {
    re_path(r'room/(?P<group>\w+)/$', websocket.WebSSH.as_asgi()),
    re_path(r'webssh/host=$', websocket.WebSSH.as_asgi()),
    re_path(r'ws_webssh/', websocket.WebSSH.as_asgi()),
}

