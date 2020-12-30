from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from chitchat_user.models import *


def admin_login(request):
    if request.session.has_key('password'):
        return redirect(admin_panel)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin' and password == 'admin':
            request.session['password'] = password
            return JsonResponse('valid',safe=False)
        else:
            return JsonResponse('invalid',safe=False)
    else:
        return render(request, 'chitchat_admin/admin_login.html')


def admin_logout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect(admin_login)


def admin_panel(request):
    if request.session.has_key('password'):
        return render(request, 'chitchat_admin/admin_panel.html')
    else:
        return redirect(admin_login)

def admin_panel_users(request):
    if request.session.has_key('password'):
        users = User.objects.all()
        user_data = {}
        for user in users:
            user_details = UserDetails.objects.filter(user=user).first()
            user_data[user.id] =[user,user_details]
        # print(user_data)

        # for x, y in user_data.items():
        #     print(x)
        #     print(y[0].first_name)
        #     if y[1] is not None:
        #         print(y[1].mobile_number)
        #     else:
        #         print('sry ttttttttttt')    
            # for x in y[1]:
            #     print(x.mobile_number)

        return render(request, 'chitchat_admin/admin_panel_users.html',{'users':user_data})
    else:
        return redirect(admin_login)

def block_user(request,id):
    if request.session.has_key('password'):
        user = User.objects.get(id=id)
        if user.is_active:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect(admin_panel_users)
    else:
        return redirect(admin_login)

def delete_user(request,id):
    if request.session.has_key('password'):
        user = User.objects.get(id=id)
        user.delete()
        return redirect(admin_panel_users)
    else:
        return redirect(admin_login)






