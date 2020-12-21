from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout

def user_login(request):
    if request.user.is_authenticated:
        return redirect(user_home)     
    else:        
        return render(request, 'chitchat_user/user_login.html')

def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(user_login)

def user_registration(request):
    if request.user.is_authenticated:
        return redirect(user_home)  
    otp_field = 0
    return render(request, 'chitchat_user/user_registration.html',{'otp_field':otp_field})  

def verify_otp(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    otp_field = 1
    return render(request, 'chitchat_user/user_registration.html',{'otp_field':otp_field})

def user_signup(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    return render(request, 'chitchat_user/user_signup.html')    

def user_home(request):
    if request.user.is_authenticated:
        return render(request, 'chitchat_user/user_home.html')     
    else:
        return redirect(user_login)