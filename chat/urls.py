from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_chat_list, name='home'),
    path('chat/<int:receiver_id>/', views.chat_detail, name='chat'),
    path('chat/global/', views.global_chat, name='global'),
    path('add-group/', views.add_group, name='add_group'),
    path('chat/group/', views.group_chat, name='group'),
    path('chat/group/<str:chat_room_id>/', views.group_chat, name='group_with_id'),
]
