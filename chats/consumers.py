import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chats.models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    """
    Handler for 'ws' connection
    """
    def connect(self):
        self.chat_room_number = str(self.scope['url_route']['kwargs']['pk'])

        # Checks for user-chat-member
        if int(self.chat_room_number) in self.scope["user"].get_chats_membership().values_list("pk", flat=True):
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.chat_room_number,
                self.channel_name
            )
            self.accept()

        else:
            self.close()

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
        message = f"{self.scope['user'].username} at {datetime.time(datetime.now().replace(microsecond=0))}:" \
                  f" \n{text_data_json['message']}"  # add username to each message from frontend


        #  for case with message save to db
        # chat_pk = self.scope['url_route']['kwargs']['pk']
        # user = self.scope["user"]
        # chat_obj = Chat.objects.get(pk=chat_pk)
        # message_obj = Message.objects.create(chat=chat_obj, sender=user, text=message)


        async_to_sync(self.channel_layer.group_send)(
            self.chat_room_number,
            {
                'type': 'chat_message',
                # 'message': message_obj.text
                'message': message
            }
        )

    # Receive message from group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
