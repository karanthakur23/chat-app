from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, max_length=100)
    online_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class ChatRoom(models.Model):
    ROOM_TYPES = (
        ('personal', 'Personal'),
        ('group', 'Group'),
    )

    roomId = models.CharField(max_length=100, unique=True, blank=True, null=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='personal', null=True, blank=True)
    group_name = models.CharField(max_length=50, null=True, blank=True)
    member = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        if self.room_type == 'group':
            return self.group_name
        else:
            return self.roomId

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return 'Notification created'

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'message': self.message.message,
            'read': self.read
        }

    def mark_as_read(self):
        self.read = True
        self.save()