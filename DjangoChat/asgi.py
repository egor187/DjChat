"""
ASGI config for DjangoChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoChat.settings')
django_asgi_app = get_asgi_application()  # this method should be called BEFORE any middleware (such as
                                          # AuthMiddlewareStack) that get access to users.models

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chats.routing

application = ProtocolTypeRouter(
    {
        "https": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(chats.routing.websocket_urlpatterns)),
    }
)
