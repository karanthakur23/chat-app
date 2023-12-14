from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


@receiver(pre_save, sender=Notification)
def create_notification(sender, instance, **kwargs):
    if instance.pk is None:
        print("Notification created:", instance)
        print("Instance sender:", instance.user)

        channel_layer = get_channel_layer()

        notification = Notification.objects.filter(read=False, user__username=instance.user).order_by('-id')
        print ("notification : ", notification)

        notification_list = [noti.message.to_dict() for noti in notification]
        print("Notification list:", notification_list)

        user_id = str(instance.user.id)

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

        print("Sending WebSocket notification...")


        # # Create a new Notification instance
        # notification = Notification.objects.create(
        #     message=instance,  # Assuming you have a ForeignKey relation to Message
        #     read=False,
        #     user=instance.sender
        # )

        # # You can now use 'notification' as needed

        # # For example, if you want to send a notification to a specific channel
        # async def send_notification():
        #     group_name = f"user_{instance.sender.id}"
        #     await channel_layer.group_add(group_name, instance.channel_name)
        #     await channel_layer.group_send(
        #         group_name,
        #         {
        #             "type": "chat.notification",
        #             "message": "New notification!",
        #         },
        #     )
        #     await channel_layer.group_discard(group_name, instance.channel_name)

        # # Call the asynchronous function
        # async_to_sync(send_notification)()

