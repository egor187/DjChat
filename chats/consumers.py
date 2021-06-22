import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chats.models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    """
    Handler for 'ws' connection
    """
    def connect(self):
        self.chat_room_number = f"chatroom_{self.scope['url_route']['kwargs']['pk']}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_room_number,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_room_number,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """
        Receives messages from JS and echo it back
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        chat_pk = self.scope['url_route']['kwargs']['pk']
        user = self.scope["user"]
        chat_obj = Chat.objects.get(pk=chat_pk)
        message_obj = Message.objects.create(chat=chat_obj, sender=user, text=message)


        async_to_sync(self.channel_layer.group_send)(
            self.chat_room_number,
            {
                'type': 'chat_message',
                'message': message_obj.text
            }
        )

    # Receive message from group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
