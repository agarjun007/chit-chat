from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('user-registration/', views.user_registration, name='user_registration'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('user-signup/', views.user_signup, name='user_signup'),
    path('user-home/', views.user_home, name='user_home'),


]
