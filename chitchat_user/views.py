from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
import requests
import json
from .models import *


def user_login(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        if user is not None  and check_password(password,user.password):
            if user.is_active == False:
                return JsonResponse('blocked', safe=False)
            else:
                auth.login(request, user)
                return JsonResponse('valid', safe=False)
        else:
            return JsonResponse('invalid', safe=False)
    else:
        return render(request, 'chitchat_user/user_login.html')


def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(user_login)


def user_registration(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    if request.method == 'POST':
        mobile = request.POST['mobile']
        if UserDetails.objects.filter(mobile_number=mobile).exists():
            return JsonResponse('exists', safe=False)
        else:
            request.session['mobile'] = mobile
            mobile = str(91) + mobile
            url = "https://d7networks.com/api/verifier/send"

            payload = {'mobile': mobile,
                       'sender_id': 'SMSINFO',
                       'message': 'Your otp code is {code}',
                       'expiry': '9000'}
            files = [

            ]
            headers = {
                'Authorization': 'Token 4dc831ffc708d93a7287b8846ab5034db634afe0'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print(response.text.encode('utf8'))
            data = response.text.encode('utf8')
            otp_data = json.loads(data.decode('utf-8'))

            otp_id = otp_data['otp_id']
            request.session['id'] = otp_id

            return JsonResponse('valid', safe=False)

    else:
        otp_field = 0
        return render(request, 'chitchat_user/user_registration.html', {'otp_field': otp_field})


def verify_otp(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    if request.session.has_key('id'):
        if request.method == 'POST':
            otp = request.POST['otp']
            otp_id = request.session['id']

            url = "https://d7networks.com/api/verifier/verify"
            
            payload = {'otp_id': otp_id,
                       'otp_code': otp}
            files = [

            ]
            headers = {
                'Authorization': 'Token 4dc831ffc708d93a7287b8846ab5034db634afe0'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            data = response.text.encode('utf8')
            otp_data = json.loads(data.decode('utf-8'))
            status = otp_data['status']

            if status == 'success':
                request.session['status'] = status
                return JsonResponse('valid', safe=False)
            else:
                return JsonResponse('otp_mismatch', safe=False)

        else:
            otp_field = 1
            return render(request, 'chitchat_user/user_registration.html', {'otp_field': otp_field})
    else:
        return redirect(user_login)


def user_signup(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    if request.session.has_key('status'):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            state = request.POST['state']
            district = request.POST['district']
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            mobile = request.session['mobile']
            open_chat = request.POST['open_chat']
            if open_chat == 'yes':
                open_chat = 1
            else:
                open_chat = 0
            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    return JsonResponse('usernamemismatch', safe=False)
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                    password=password)
                    user_details = UserDetails.objects.create(user=user, state=state, district=district,
                                                              mobile_number=mobile, open_chat=open_chat)
                    request.session.flush()
                    return JsonResponse('valid', safe=False)
            else:
                return JsonResponse('invalid', safe=False)
            return render(request, 'chitchat_user/user_signup.html')
        else:
            return render(request, 'chitchat_user/user_signup.html')
    else:
        return redirect(verify_otp)


def user_home(request):
    if request.user.is_authenticated:
        return render(request, 'chitchat_user/user_home.html')
    else:
        return redirect(user_login)
