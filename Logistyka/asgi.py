"""
ASGI config for Logistyka project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# from Logistyka.Applications.Chat.routing import websocket_urlpatterns
# from Logistyka.Applications.Chat.routing import websocket_urlpatterns
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Logistyka.settings')
django_asgi_app = get_asgi_application()

from Applications.Chat import routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
