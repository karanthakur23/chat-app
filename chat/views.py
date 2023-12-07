from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required
def user_chat_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'index.html', {'users': users})

@login_required
def chat_detail(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)
    users = User.objects.exclude(username=request.user.username)
    chat_rooms = ChatRoom.objects.filter(member=request.user).filter(member=receiver)
    chat_room_instance = chat_rooms.first()
    messages_in_room = Message.objects.filter(chat_room=chat_room_instance)

    return render(request, 'main_chat.html', {'receiver': receiver, 'users': users, 'messages_in_room': messages_in_room})

@login_required
def global_chat(request):
    chat_room = ChatRoom.objects.get(roomId='global_chat')
    messages_in_room = Message.objects.filter(chat_room=chat_room)
    users = User.objects.exclude(username=request.user.username)

    return render(request, 'global_chat.html', {'users':users, 'messages_in_room': messages_in_room})

