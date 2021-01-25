from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('user-registration/', views.user_registration, name='user_registration'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('user-signup/', views.user_signup, name='user_signup'),
    path('user-home/', views.user_home, name='user_home'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('user-profile-edit/',views.edit_profile,name='user-profile-edit'),
    path('user-profile-update/',views.update_profile,name='user-profile-update'),
    path('user-settings/',views.user_settings,name='user_settings'),
    path('user-profile-view/<int:id>',views.user_profile_view ,name='user-profile-view'),
    path('user-chat-details/',views.user_chat_details,name='user-chat-details'),
]
