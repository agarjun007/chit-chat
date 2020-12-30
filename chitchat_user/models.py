from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField (null=True,blank=True)
    profile_picture = models.ImageField(null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    open_chat = models.BooleanField(null=True,blank=True)
    dob = models.DateField(null=True, blank=True)