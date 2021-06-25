from django.urls import path

from chats.consumers import ChatConsumer


websocket_urlpatterns = [
    path("wss/chat/<int:pk>/", ChatConsumer.as_asgi(), name="ws_chat_detail"),
]