# Generated by Django 3.1.2 on 2021-01-14 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chitchat_user', '0005_auto_20210114_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='status',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
