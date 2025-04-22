"""GuLiEdu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path  # 移除 url
from .views import user_register,UserLoginView,user_logout,user_activate,user_forget,user_reset,user_info,user_changeimage,user_changeinfo,user_changeemail,user_resetemail,user_course,user_loveorg,user_deletelove,user_loveteacher, user_lovecourse,\
user_message,user_deletemessage

urlpatterns = [
    path('user_register/', user_register, name="user_register"),
    #path('user_login/', user_login, name="user_login"),
    path('user_login/', UserLoginView.as_view(), name="user_login"),
    path('user_logout/', user_logout, name="user_logout"),
    re_path('user_activate/(\w+)', user_activate, name="user_activate"),
    path('user_forget/', user_forget, name="user_forget"),
    re_path('user_reset/(\w+)', user_reset, name="user_reset"),
    path('user_info/', user_info, name="user_info"),
    path('user_changeimage/',user_changeimage,name="user_changeimage"),
    path('user_changeinfo/', user_changeinfo, name="user_changeinfo"),
    path('user_changeemail/', user_changeemail, name="user_changeemail"),
    path('user_resetemail', user_resetemail, name="user_resetemail"),
    path('user_course', user_course, name="user_course"),
    path('user_loveorg', user_loveorg, name="user_loveorg"),
    path('user_loveteacher', user_loveteacher, name="user_loveteacher"),
    path('user_lovecourse', user_lovecourse, name="user_lovecourse"),
    path('user_deletelove', user_deletelove, name="user_deletelove"),
    path('user_message', user_message, name="user_message"),
    path('user_deletemessage', user_deletemessage, name="user_deletemessage"),


]
