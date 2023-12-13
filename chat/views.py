from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from hashlib import sha256
from django.http import HttpResponseForbidden


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
        room_id_hash = room_id_hash[:6]

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

    try:
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:10]

        for notification in notifications:
            notification.read = True
            notification.save()
        unread_count = notifications.count()

    except Notification.DoesNotExist:
        notifications = []
        unread_count = 0

    return render(request, 'index.html', {'users': users, 'notifications': notifications, 'unread_count': unread_count})


@login_required
def chat_detail(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)

    users = User.objects.exclude(username=request.user.username)

    if request.user.id < receiver_id:
        roomId = f'chat_{request.user.id}_{receiver_id}'
    else:
        roomId = f'chat_{receiver_id}_{request.user.id}'

    chat_rooms = ChatRoom.objects.filter(
        room_type='personal',
        member=request.user,
        roomId=roomId
    )

    chat_room_instance = chat_rooms.first()

    messages_in_room = Message.objects.filter(chat_room=chat_room_instance)

    # try:
    #     notifications = Notification.objects.filter(user=request.user).order_by('-id')[:3]

    #     unread_noti = Notification.objects.filter(user=request.user, read=False)
    #     unread_noti.update(read=True)

    #     unread_count = unread_noti.count()

    # except Notification.DoesNotExist:
    #     notifications = []
    #     unread_count = 0

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


@login_required
def group_chat(request, chat_room_id=None):
    if chat_room_id:
        print (chat_room_id)
        print(type(chat_room_id), "TYPE OF CR ID")
        # Handle the case when a specific chat room is selected
        group_chat_room = get_object_or_404(ChatRoom, roomId=chat_room_id, room_type='group')

        if request.user in group_chat_room.member.all():
            messages_in_room = Message.objects.filter(chat_room=group_chat_room)
            print(messages_in_room, "<<<<<MESSAGES>>>>>>_____:")
            # Filter group chat rooms based on the user's membership
            group_list = ChatRoom.objects.filter(room_type='group', member=request.user)
            return render(request, 'group_chat.html', {'chat_room_id': chat_room_id, 'group_list': group_list, 'messages_in_room': messages_in_room, 'group_chat_room': group_chat_room})
        else:
            # User is not a member of the group chat, handle as needed (e.g., show an error message)
            return HttpResponseForbidden("You are not a member of this group chat.")
    else:
        # Handle the case when no specific chat room is selected (display list of group chat rooms)
        # Filter group chat rooms based on the user's membership
        group_list = ChatRoom.objects.filter(room_type='group', member=request.user)
        return render(request, 'group_chat.html', {'group_list': group_list})