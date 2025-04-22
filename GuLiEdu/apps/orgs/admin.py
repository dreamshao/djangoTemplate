from django.contrib import admin
from .models import CityInfo, OrgInfo, TeacherInfo


# Register your models here.
@admin.register(CityInfo)
class CityInfoCodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'add_time']
    search_fields = ['name', 'add_time']
    # list_filter = ['code', 'email']


@admin.register(OrgInfo)
class OrgInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_num', 'study_num', 'address','desc','detail','category','cityinfo','image','add_time']
    search_fields = ['name', 'course_num']
    # list_filter = ['code', 'email']


@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'age','image','work_year', 'work_position', 'work_style','work_company','add_time']
    search_fields = ['name', 'work_year']
    # list_filter = ['code', 'email']
