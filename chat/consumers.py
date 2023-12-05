import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatModel, UserProfileModel, ChatNotification
from django.contrib.auth.models import User


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logged_in = self.scope['user'].id
        other_user = self.scope['url_route']['kwargs']['id']

        if int(logged_in) > int(other_user):
            self.room_name = f'{logged_in}-{other_user}'
        else:
            self.room_name = f'{other_user}-{logged_in}'

        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        receiver = data['receiver']

        await self.save_message(username, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        saved_message_obj = ChatModel.objects.create(sender=username, message=message, thread_name=thread_name)