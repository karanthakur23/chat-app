from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from hashlib import sha256

# Create your views here.

@login_required
def user_chat_list(request):
    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        selected_user_ids = request.POST.get('selectedUserIds', '').split(',')
        selected_user_ids = [int(user_id) for user_id in selected_user_ids if user_id]

        selected_user_ids.append(request.user.id)
        selected_user_ids.sort()

        room_id_hash = sha256(','.join(map(str, selected_user_ids)).encode()).hexdigest()

        existing_chatroom = ChatRoom.objects.filter(
            room_type='group',
            roomId=room_id_hash
        ).distinct()

        if existing_chatroom.exists():
            print(f"Existing Chat Room ID: {existing_chatroom.first().id}")
            return redirect('chat', receiver_id=existing_chatroom.first().id)

        new_group_chat = ChatRoom.objects.create(
            room_type='group',
            roomId=room_id_hash,
            group_name='Group Chat',
        )
        new_group_chat.member.set(selected_user_ids)
        print(f"New Chat Room ID: {new_group_chat.id}")
        return redirect('chat', receiver_id=new_group_chat.id)

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

@login_required
def add_group(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'add_group.html', {'users': users})
