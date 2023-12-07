import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import PersonalChatConsumer, GlobalChatConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', PersonalChatConsumer.as_asgi()),
            path('ws/global/', GlobalChatConsumer.as_asgi()),
        ])
    ),
})
