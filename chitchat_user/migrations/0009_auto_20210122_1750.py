# Generated by Django 3.1.2 on 2021-01-22 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chitchat_user', '0008_auto_20210119_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneToOneChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_1', models.CharField(blank=True, max_length=100, null=True)),
                ('user_2', models.CharField(blank=True, max_length=100, null=True)),
                ('room_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='room_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
