from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserDetails(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField (null=True,blank=True)
    profile_picture = models.ImageField(null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    open_chat = models.BooleanField(null=True,blank=True)
    dob = models.DateField(null=True, blank=True)
    martial_status = models.CharField(max_length=100,null=True,blank=True)
    bio = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=500,null=True,blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return url

class Message(models.Model):
    author = models.ForeignKey(User,related_name='author_message',on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username 
    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]        