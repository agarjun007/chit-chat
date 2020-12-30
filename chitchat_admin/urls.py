from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel-users/', views.admin_panel_users, name='admin_panel-users'),
    path('block-user/<int:id>', views.block_user, name='block-user'),
    path('delete-user/<int:id>', views.delete_user, name='delete-user'),


]