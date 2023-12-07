import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import *
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        current_user = self.scope['user'].id
        receiver = self.scope['url_route']['kwargs']['id']

        if current_user > receiver:
            self.room_name = f'{receiver}_{current_user}'
        else:
            self.room_name = f'{current_user}_{receiver}'

        self.room_group_name = f'chat_{self.room_name}'
        print(self.room_group_name, "----------------<<<<<<<<<<")

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
    def save_message(self, username, room_group_name, message):
        sender = User.objects.get(username=username)

        try:
            chat_room = ChatRoom.objects.get(roomId=room_group_name)
        except ChatRoom.DoesNotExist:
            chat_room = ChatRoom.objects.create(roomId=room_group_name)
            chat_room.member.add(sender)

        chat_room = ChatRoom.objects.get(roomId=room_group_name)
        saved_message_obj = Message.objects.create(sender=sender, chat_room=chat_room, message=message)


class GlobalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'global_chat'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_message(username, message)

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
    def save_message(self, username, message):
        sender = User.objects.get(username=username)

        # Save the message to the database (similar logic as before)
        chat_room, _ = ChatRoom.objects.get_or_create(roomId=self.room_group_name)
        saved_message_obj = Message.objects.create(sender=sender, chat_room=chat_room, message=message)
        return saved_message_obj



