from django.contrib import admin
from .models import UserProfile, BannerInfo, EmailVerifyCode


# Register your models here.
@admin.register(EmailVerifyCode)
class EmailVerifyCodeAdmin(admin.ModelAdmin):
    list_display = ['code','email','send_type','add_time']
    search_fields = ['code', 'email']
    list_filter = ['code', 'email']



@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','nick_name','gender','birthday','phone','address','add_time','image']
    #list_display = [field.name for field in UserProfile._meta.get_fields()]
    search_fields = ['nick_name', 'phone']
    list_filter = ['nick_name', 'phone']


@admin.register(BannerInfo)
class BannerInfoAdmin(admin.ModelAdmin):
    list_display = ['image', 'url',  'add_time']
    search_fields = ['url']
    list_filter = ['url']