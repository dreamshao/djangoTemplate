from django.contrib import admin
from .models import CourseInfo, LessonInfo, VideoInfo, SourceInfo


# Register your models here.
@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacherinfo', 'level', 'desc', 'detail', 'category', 'course_notice', 'course_need',
                    'teacher_tell', 'orginfo', 'image', 'add_time']
    search_fields = ['name', 'teacherinfo']
    # list_filter = ['code', 'email']


@admin.register(LessonInfo)
class LessonInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'courseinfo', 'add_time']
    search_fields = ['name', 'courseinfo']
    # list_filter = ['code', 'email']


@admin.register(VideoInfo)
class VideoInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'study_time', 'url', 'lessoninfo', 'add_time']
    search_fields = ['name', 'lessoninfo']


@admin.register(SourceInfo)
class SourceInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'down_load', 'courseinfo', 'add_time']
    search_fields = ['name', 'courseinfo']
