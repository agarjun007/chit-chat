from django.shortcuts import render
from django.http import HttpResponse


def user_login(request):
    return render(request, 'chitchat_user/user_login.html')

def user_registration(request):  
    otp_field = 0
    return render(request, 'chitchat_user/user_registration.html',{'otp_field':otp_field})  

def verify_otp(request):
    otp_field = 1
    return render(request, 'chitchat_user/user_registration.html',{'otp_field':otp_field})

def user_signup(request):
    return render(request, 'chitchat_user/user_signup.html')    

def user_home(request):
    return render(request, 'chitchat_user/user_home.html')     