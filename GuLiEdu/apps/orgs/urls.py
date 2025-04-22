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
from django.urls import path, re_path
from django.conf.urls import url, include
from .views import org_list, org_detail,org_detail_course,org_detail_desc,org_detail_teacher,teacher_list,teacher_detail

urlpatterns = [
    path('org_list/', org_list, name="org_list"),
    re_path('org_detail/(\d+)', org_detail, name="org_detail"),
    re_path('org_detail_course/(\d+)', org_detail_course, name="org_detail_course"),
    re_path('org_detail_desc/(\d+)', org_detail_desc, name="org_detail_desc"),
    re_path('org_detail_teacher/(\d+)', org_detail_teacher, name="org_detail_teacher"),
    path('teacher_list/', teacher_list, name="teacher_list"),
    re_path('teacher_detail/(\d+)', teacher_detail, name="teacher_detail"),

]
