# Generated by Django 3.1.2 on 2021-01-15 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chitchat_user', '0006_userdetails_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='show_mobile',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='show_profile',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='show_propic',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
