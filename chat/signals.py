# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        notification = Notification.objects.filter(read=False, user=instance.sender)

        notification_list = [noti.message for noti in notification]

        user_id = str(instance.sender.id)

        data = {
            'count': notification.count(),
            'notifications': notification_list
        }

        async_to_sync(channel_layer.group_send)(
            user_id, {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )

