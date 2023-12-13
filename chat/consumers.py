import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import *
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
import logging
logger = logging.getLogger(__name__)


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


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the chat room ID from the URL parameters
        chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        print(chat_room_id, "---------------------chat_room_id")

        self.room_group_name = f'group_chat_{chat_room_id}'  # Assign it at the class level
        print(self.room_group_name, "---------------------room_group_name")

        # Validate that the user is a member of the specified group chat
        if await self.is_user_member(chat_room_id):
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            # User is not a member of the group chat, close the connection
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']

        # Save the message and broadcast to the group
        await self.save_message(username, message, chat_room_id)
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
    def is_user_member(self, chat_room_id):
        user = self.scope['user']
        return ChatRoom.objects.filter(roomId=chat_room_id, member=user).exists()

    @database_sync_to_async
    def save_message(self, username, message, chat_room_id):
        sender = User.objects.get(username=username)
        chat_room = ChatRoom.objects.get(roomId=chat_room_id)
        saved_message_obj = Message.objects.create(sender=sender, chat_room=chat_room, message=message)
        return saved_message_obj




















class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        self.room_group_name = f'{my_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        try:
            data = json.loads(event.get('value'))
            count = data['count']
            notifications = data['notifications']

            await self.send(
                text_data=json.dumps({
                    'count': count,
                    'notifications': notifications
                })
            )

            logger.info(f"Notification sent: {count} notifications")
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")