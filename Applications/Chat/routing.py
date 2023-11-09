from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing
from django.urls import re_path
from .customers import ConversationConsumer
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    re_path(r'ws/users/(?P<userId>\w+)/chat/$', ConversationConsumer.as_asgi()),
]

