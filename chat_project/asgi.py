import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import PersonalChatConsumer, GlobalChatConsumer, GroupChatConsumer, NotificationConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', PersonalChatConsumer.as_asgi()),
            path('ws/global/', GlobalChatConsumer.as_asgi()),
            path('ws/group_chat/<str:chat_room_id>/', GroupChatConsumer.as_asgi()),
            path('ws/notify/', NotificationConsumer.as_asgi()),
        ])
    ),
})
