# Generated by Django 3.1.2 on 2021-02-05 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chitchat_user', '0010_message_chat_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chat_icon',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
