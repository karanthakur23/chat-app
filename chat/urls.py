from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_chat_list, name='home'),
    path('chat/<int:receiver_id>/', views.chat_detail, name='chat'),
    path('chat/global/', views.global_chat, name='global'),
]
