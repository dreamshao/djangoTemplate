from django.contrib import admin
from .models import UserAsk, UserLove, UserCourse, UserComment, UserMessage


# Register your models here.
@admin.register(UserAsk)
class UserAskAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'course', 'add_time']
    search_fields = ['name', 'phone']


@admin.register(UserLove)
class UserLoveAdmin(admin.ModelAdmin):
    list_display = ['love_man', 'love_id', 'love_type', 'love_status', 'add_time']
    search_fields = ['love_man', 'love_type']

@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['study_man', 'study_course', 'add_time']
    search_fields = ['study_man', 'study_course']

@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ['commnet_man', 'commnet_course', 'comment_content', 'add_time']
    search_fields = ['commnet_man', 'commnet_course']

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['message_man', 'message_content', 'message_status', 'add_time']
    search_fields = ['message_man', 'message_content']