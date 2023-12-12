# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification when a new message is created
        Notification.objects.create(user=instance.chat_room.member.exclude(id=instance.sender.id).first(),
        message=f'New message from {instance.sender.username}')
