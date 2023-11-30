from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing
from django.urls import re_path, path

from .customers import ConversationConsumer
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path(r'ws/users', ConversationConsumer.as_asgi()),
]

