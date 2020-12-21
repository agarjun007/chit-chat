from django.shortcuts import render
from django.http import HttpResponse


def admin_login(request):
    return render(request, 'chitchat_admin/admin_login.html')

