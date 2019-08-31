from django.urls import path
from userprofile import views

app_name='userprofile'


urlpatterns = [

    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'register/', views.user_register, name='register'),
    path(r'edit/<int:id>/', views.user_edit, name='edit'),
    path(r'modifypassword/<int:id>/', views.modify_password, name='modify'),


]
