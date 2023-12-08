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
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='personal')
    group_name = models.CharField(max_length=50, null=True, blank=True)
    member = models.ManyToManyField(User, related_name='chat_rooms')

    # def __str__(self):
    #     return self.roomId

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
