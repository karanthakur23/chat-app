# Generated by Django 4.2.8 on 2023-12-08 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_chatroom_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='group_name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='room_type',
            field=models.CharField(choices=[('personal', 'Personal'), ('group', 'Group')], default='personal', max_length=10),
        ),
    ]