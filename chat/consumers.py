import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatModel, UserProfileModel, ChatNotification
from django.contrib.auth.models import User
from django.conf import settings

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_project.settings")
import django

django.setup()


class PersonalChatConsumer(AsyncWebsocketConsumer):
    pass