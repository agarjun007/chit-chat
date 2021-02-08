from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
import requests
import json
from .models import UserDetails, User, Message,OneToOneChat
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files import File
import datetime
from django.db.models import Q
from django.contrib import messages
from django.core import serializers
import uuid 
from django.contrib import messages


def user_login(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        if user is not None and check_password(password, user.password):
            if user.is_active == False:
                return JsonResponse('blocked', safe=False)
            else:
                auth.login(request, user,
                           backend='django.contrib.auth.backends.ModelBackend')
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

            response = requests.request(
                "POST", url, headers=headers, data=payload, files=files)

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

            response = requests.request(
                "POST", url, headers=headers, data=payload, files=files)

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
        users = User.objects.all()
        if UserDetails.objects.filter(user=request.user).exists():
            user_details = UserDetails.objects.get(user=request.user)
            if user_details.state == 'All':
                users_details = UserDetails.objects.filter(~Q(user=request.user)) 
            else:
                users_details = UserDetails.objects.filter(~Q(user=request.user),state=user_details.state,
                                                         district= user_details.district,open_chat=1 ) 
            context= {'users': users, 'user_details': user_details,'users_details': users_details }               
            return render(request, 'chitchat_user/user_home.html',context )
        else:
            user_details = UserDetails.objects.create(user=request.user, open_chat=1, show_propic='Everyone',
                                                      show_profile='Everyone', show_mobile='Everyone',
                                                      state='kerala', district= 'Kozhikode')
            users_details = UserDetails.objects.filter(~Q(user=request.user),state=user_details.state,
                                                        district= user_details.district,open_chat=1)
            user_details = UserDetails.objects.get(user=request.user)
            context= {'users': users, 'user_details': user_details,'users_details': users_details,'status': 'new' }               
            return render(request, 'chitchat_user/user_home.html',context )
    else:
        return redirect(user_login)


def room(request, room_name):
    if request.user.is_authenticated:
        users = User.objects.all()
        if UserDetails.objects.filter(user=request.user).exists():
            user_details = UserDetails.objects.get(user=request.user)
            users_details = UserDetails.objects.filter(~Q(user=request.user))
            return render(request, 'chitchat_user/chat_room_trial.html',
                          {'room_name_json': mark_safe(json.dumps(room_name)),
                           'username': mark_safe(json.dumps(request.user.username)),
                           'users': users,
                           'user_details': user_details,
                           'users_details': users_details
                           })
        else:
            users_details = UserDetails.objects.filter(~Q(user=request.user))
            return render(request, 'chitchat_user/chat_room_trial.html',
                          {'room_name_json': mark_safe(json.dumps(room_name)),
                           'username': mark_safe(json.dumps(request.user.username)),
                           'users': users,
                           'users_details': users_details,
                           'status': 'new'
                           })

    else:
        return redirect(user_login)


def user_profile(request):
    if request.user.is_authenticated:

        if UserDetails.objects.filter(user=request.user).exists():
            user_details = UserDetails.objects.get(user=request.user)
        else:
            user_details = UserDetails.objects.create(user=request.user, open_chat=1, show_propic='Everyone',
                                                      show_profile='Everyone', show_mobile='Everyone')
        content = {'user_details': user_details}

        return render(request, 'chitchat_user/user_profile.html', content)

    else:
        return redirect(user_login)


def edit_profile(request):
    if request.user.is_authenticated:

        if UserDetails.objects.filter(user=request.user).exists():
            user_details = UserDetails.objects.get(user=request.user)

            if user_details.dob is not None:
                dob = user_details.dob.strftime('%Y-%m-%d')
                context = {'user_details': user_details, 'dob': dob}
            else:
                context = {'user_details': user_details}
        else:
            user_details = UserDetails.objects.create(user=request.user, open_chat=1, show_propic='Everyone',
                                                      show_profile='Everyone', show_mobile='Everyone')
            context = {'user_details': user_details}

        return render(request, 'chitchat_user/user_profile_edit.html', context)

    else:
        return redirect(user_login)


def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            user_details = UserDetails.objects.get(user=user)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user_details.phone = request.POST['phone']
            user_details.dob = request.POST['dob']
            user_details.state = request.POST['state']
            user_details.disrict = request.POST['district']
            user_details.martial_status = request.POST['martialstatus']
            user_details.status = request.POST['status']
            user_details.bio = request.POST['bio']

            if 'profile-image-upload' not in request.POST:
                profile_picture = request.FILES.get('profile-image-upload')
                print('not post', profile_picture)
            else:
                profile_picture = user_details.profile_picture
                print('post', profile_picture)

            user_details.profile_picture = profile_picture
            user.save()
            user_details.save()
            return redirect(user_profile)
        else:
            return render(request, 'chitchat_user/user_profile_edit.html')
    else:
        return redirect(user_login)


def user_settings(request):
    if request.user.is_authenticated:
        if UserDetails.objects.filter(user=request.user).exists():
            user_details = UserDetails.objects.get(user=request.user)
        else:
            user_details = UserDetails.objects.create(user=request.user, open_chat=1, show_propic='Everyone',
                                                      show_profile='Everyone', show_mobile='Everyone')

        context = {'user_details': user_details}

        if request.method == 'POST':
            user_details.show_propic = request.POST['propic']
            print(request.POST['propic'])
            user_details.show_profile = request.POST['profile']
            print(request.POST['profile'])
            user_details.show_mobile = request.POST['mobile']
            print(request.POST['mobile'])
            open_chat = request.POST['open_chat']

            if open_chat == 'yes':
                user_details.open_chat = 1
            else:
                user_details.open_chat = 0

            user_details.save()
            user_details = UserDetails.objects.get(user=request.user)
            context = {'user_details': user_details}
            return render(request, 'chitchat_user/user_settings.html', context)
        else:
            return render(request, 'chitchat_user/user_settings.html', context)
    else:
        return redirect(user_login)


def chat_location(request):
    if request.user.is_authenticated:
        user_details = UserDetails.objects.get(user=request.user)
        if request.method == 'POST':
            user_details.state = request.POST['state']
            if user_details.state != 'All':
                user_details.district = request.POST['district']
            else:
                user_details.district = ''
            user_details.save()
            return redirect(user_home)
        else:
            context={'user_details':user_details}
            return render (request,'chitchat_user/chat_location.html', context)   
    else:     
        return redirect(user_login)


def user_profile_view(request, user_id):
    if request.user.is_authenticated:
        user_details = UserDetails.objects.get(id=user_id)
        if user_details.show_profile == 'Everyone':
            return JsonResponse('success',safe=False)
        else:
            return JsonResponse('failed',safe=False)
    else:
        return redirect(user_login)        

def user_profile_show(request,user_id):
    if request.user.is_authenticated:
        user_details = UserDetails.objects.get(id=user_id)
        if user_details.show_profile == 'Everyone':
            context = {'user_details': user_details}
            return render(request, 'chitchat_user/user_profile_view.html', context)
        else:
            return redirect(user_home) 
    else:
        return redirect(user_login)     


def user_chat_details(request):
    if request.user.is_authenticated:
        user_id = request.GET.get('user_id')
        print(user_id)
        user_details = UserDetails.objects.filter(id=user_id)
        user = [user_details[0].user]
        user_2 = user[0].username
        print(user[0].username)
        print(user)
        if OneToOneChat.objects.filter(user_1 = request.user.username , user_2 = user_2 ).exists(): 
            one_to_one = OneToOneChat.objects.get(user_1 = request.user.username  , user_2 = user_2 ) 
            room_name = one_to_one.room_name
            print(room_name, 'get room_nameeeeeeeeee1111')
        elif OneToOneChat.objects.filter(user_1 = user_2 , user_2 =  request.user.username ).exists():
            one_to_one =  OneToOneChat.objects.get(user_1 = user_2 , user_2 =  request.user.username )
            room_name = one_to_one.room_name
            print(room_name, 'get room_nameeeeeeeeee222222')      
        else: 
            room_name = uuid.uuid1()   
            OneToOneChat.objects.create(user_1 = request.user.username, user_2 = user_2,room_name=room_name)
            print(room_name, 'newwwwwwwwwww room_nameeeeeeeeee')
        
        print(room_name, 'databaseeeee room_nameeeeeeeeee')

        for user_detail in user_details:
            user_detail.imageurl = user_detail.ImageURL
        print(user_details[0].imageurl)
        response_data = {'user_details': serializers.serialize(
            'json', user_details), 'user': serializers.serialize('json', user),
            'room_name':room_name,'imageurl':user_detail.imageurl}

        return JsonResponse(response_data)
