from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import UserRegisterForm, UserLoginForm, UserForgetForm, UserResetForm, UserChangeImageForm, \
    UserChangeInfoForm, UserChangeEmailForm, UserResetEmailForm
from .models import UserProfile, EmailVerifyCode, BannerInfo
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from tools.send_email_tool import send_email_code
from django.http import JsonResponse
import datetime
from orgs.models import OrgInfo, TeacherInfo
from operations.models import UserLove, UserMessage
from courses.models import CourseInfo
from django.views.generic import View


# 类模式

class IndexView(View):
    def get(self, request):
        all_banners = BannerInfo.objects.all().order_by("-add_time")[:5]
        banner_courses = CourseInfo.objects.filter(is_banner=True)[:3]
        all_courses = CourseInfo.objects.filter(is_banner=False)[:6]
        all_orgs = OrgInfo.objects.all()[:15]
        return render(request, 'index.html',
                      {"all_banners": all_banners, "banner_courses": banner_courses, "all_courses": all_courses,
                       "all_orgs": all_orgs})


# Create your views here.
# def index(request):
#     all_banners = BannerInfo.objects.all().order_by("-add_time")[:5]
#     banner_courses = CourseInfo.objects.filter(is_banner=True)[:3]
#     all_courses = CourseInfo.objects.filter(is_banner=False)[:6]
#     all_orgs = OrgInfo.objects.all()[:15]
#     return render(request, 'index.html',
#                   {"all_banners": all_banners, "banner_courses": banner_courses, "all_courses": all_courses,
#                    "all_orgs": all_orgs})


def user_register(request):
    if request.method == "GET":
        # 这里实例化forms类，不是为了验证，而是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html', {'user_register_form': user_register_form})
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']
            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'users/register.html', {'msg': '用户已经存在'})
            else:
                # a = UserProfile
                # a.username = email
                # a.set_password(password)
                # a.email = email
                a = UserProfile(username=email, email=email)  # ✅ 先创建实例
                a.set_password(password)  # ✅ 确保 `password` 被加密
                a.save()
                # 注册发送激活码到邮箱
                send_email_code(email=email, send_type=1)
                return HttpResponse("请尽快前往您的邮箱激活，否则无法登录！")
                # return redirect(reverse('index')) # 注册成功回到首页
        else:
            return render(request, 'users/register.html', {'user_register_form': user_register_form})


class UserLoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            user = authenticate(username=email, password=password)  # 验证登录
            if user:
                # 验证是否激活邮箱
                if user.is_start:
                    login(request, user)
                    # 登录成功就发布一条消息给到用户
                    a = UserMessage()
                    a.message_man = user.id
                    a.message_content = "欢迎登录"
                    a.save()
                    url = request.COOKIES.get("url", "/")  # 获取当前cookie 中由于未登录后导致跳转index 路由 登录后获取该路由进行访问
                    ret = redirect(url)
                    ret.delete_cookie("url")
                    return ret
                else:
                    return HttpResponse("please go your email to activate account")
            else:
                return render(request, 'users/login.html', {'msg': 'email or password is wrong, please try again!'})
        else:
            return render(request, 'users/login.html', {'user_register_form': user_login_form})


# def user_login(request):
#     if request.method == "GET":
#         return render(request, 'users/login.html')
#     else:
#         user_login_form = UserLoginForm(request.POST)
#         if user_login_form.is_valid():
#             email = user_login_form.cleaned_data['email']
#             password = user_login_form.cleaned_data['password']
#             user = authenticate(username=email, password=password)  # 验证登录
#             if user:
#                 # 验证是否激活邮箱
#                 if user.is_start:
#                     login(request, user)
#                     # 登录成功就发布一条消息给到用户
#                     a = UserMessage()
#                     a.message_man = user.id
#                     a.message_content = "欢迎登录"
#                     a.save()
#                     url = request.COOKIES.get("url", "/")  # 获取当前cookie 中由于未登录后导致跳转index 路由 登录后获取该路由进行访问
#                     ret = redirect(url)
#                     ret.delete_cookie("url")
#                     return ret
#                 else:
#                     return HttpResponse("please go your email to activate account")
#             else:
#                 return render(request, 'users/login.html', {'msg': 'email or password is wrong, please try again!'})
#         else:
#             return render(request, 'users/login.html', {'user_register_form': user_login_form})


def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def user_activate(request, code):
    if code:
        email_ver_list = EmailVerifyCode.objects.filter(code=code)
        if email_ver_list:
            email_ver = email_ver_list[0]
            email = email_ver.email
            user_list = UserProfile.objects.filter(username=email)
            if user_list:
                user = user_list[0]
                user.is_start = True
                user.save()
                return redirect(reverse('users:user_login'))  # 重定向到users下的user_login 函数中
            else:
                return HttpResponse("User is not register!")
        else:
            return HttpResponse("Email is not register!")
    else:
        return HttpResponse("please input right code!")


def user_forget(request):
    if request.method == "GET":
        # 这里实例化forms类，不是为了验证，而是为了使用验证码
        user_forget_form = UserForgetForm()
        return render(request, 'users/forgetpwd.html', {'user_forget_form': user_forget_form})
    else:
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(username=email)
            if user_list:
                send_email_code(email=email, send_type=2)
                return HttpResponse("请尽快去您的邮箱重置密码！")
            else:
                return render(request, 'users/forgetpwd.html', {'msg': "user is not exists"})
        else:
            return render(request, 'users/forgetpwd.html', {'msg': "user is not exists"})


def user_reset(request, code):
    if code:
        if request.method == "GET":
            return render(request, 'users/password_reset.html', {'code': code})
        else:
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password1 = user_reset_form.cleaned_data['password1']
                if password == password1:
                    email_ver_list = EmailVerifyCode.objects.filter(code=code)
                    if email_ver_list:
                        email_ver = email_ver_list[0]
                        email = email_ver.email
                        user_list = UserProfile.objects.filter(username=email)
                        if user_list:
                            user = user_list[0]
                            user.set_password(password1)
                            user.save()
                            return redirect(reverse('users:user_login'))  # 重定向到users下的user_login 函数中
                        else:
                            return HttpResponse("User is not register!")
                    else:
                        return HttpResponse("Email is not register!")
                else:
                    return render(request, 'users/password_reset.html', {'msg': '两次密码不一致', 'code': code})
            else:
                return render(request, 'users/password_reset.html', {'user_reset_form': user_reset_form, 'code': code})


def user_info(request):
    return render(request, 'users/usercenter-info.html')


def user_changeimage(request):
    # 上传图片
    # instance 指明实例是什么，做修改的时候，我们需要知道是给哪个对象实例进行修改#如果不指明，那么就会被当作创建对象去执行，而我们只有一个图片，就一定会报错
    user_changeimage_form = UserChangeImageForm(request.POST, request.FILES, instance=request.user)  # 验证的字段来自实例的user
    if user_changeimage_form.is_valid():
        user_changeimage_form.save(commit=True)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'fail'})


def user_changeinfo(request):
    user_changeinfo_form = UserChangeInfoForm(request.POST, instance=request.user)
    if user_changeinfo_form.is_valid():
        user_changeinfo_form.save(commit=True)
        return JsonResponse({"status": "ok", "msg": "修改成功"})
    else:
        return JsonResponse({'status': 'fail', "msg": "修改失败"})


def user_changeemail(request):
    user_chnageemail_form = UserChangeEmailForm(request.POST, instance=request.user)
    if user_chnageemail_form.is_valid():
        email = user_chnageemail_form.cleaned_data['email']
        result = UserProfile.objects.filter(Q(email=email) | Q(username=email))
        if result:
            return JsonResponse({"status": "fail", "msg": "the email is used"})
        else:
            email_ver_list = EmailVerifyCode.objects.filter(email=email, send_type=3)
            if email_ver_list:
                # 找出最近的一次发送的记录时间
                email_ver = email_ver_list.order_by('-add_time')[0]
                # 判断当前时间与最近一次时间相差大于1分钟则再次发送验证码
                if (datetime.datetime.now() - email_ver.add_time).seconds > 60:
                    send_email_code(email=email, send_type=3)
                    # 如果重新发了，则以前发的就被清除
                    email_ver.delete()
                    return JsonResponse({"status": "ok", "msg": "please to your email to check code"})
                else:
                    return JsonResponse({"status": "fail", "msg": "please don't send again! wait for some time"})
            else:
                send_email_code(email=email, send_type=3)
                return JsonResponse({"status": "ok", "msg": "please to your email to check code"})
        # user_chnageemail_form.save(commit=True)
    else:
        return JsonResponse({"status": "fail", "msg": "please input right type email"})


def user_resetemail(request):
    user_resetemail_form = UserResetEmailForm(request.POST)
    if user_resetemail_form.is_valid():
        email = user_resetemail_form.cleaned_data['email']
        code = user_resetemail_form.cleaned_data['code']
        email_ver_list = EmailVerifyCode.objects.filter(email=email, code=code)
        if email_ver_list:
            email_ver = email_ver_list[0]
            if (datetime.datetime.now() - email_ver.add_time).seconds > 60:
                request.user.username = email
                request.user.email = email
                request.user.save()
                return JsonResponse({"status": "ok", "msg": "the email is reset success!"})
            else:
                return JsonResponse({"status": "fail", "msg": "the code is not active, please try again!"})
        else:
            return JsonResponse({"status": "fail", "msg": "the email or code is not right!"})
    else:
        return JsonResponse({"status": "fail", "msg": "the email or code is not right!"})


def user_course(request):
    # 找中间表的operations 里面的usercourse
    usercourese_list = request.user.usercourse_set.all()  # 拿到所有学习的信息
    course_list = [usercourse.study_course for usercourse in usercourese_list]

    return render(request, 'users/usercenter-mycourse.html', {"course_list": course_list})


def user_loveorg(request):
    # 找中间表operations 找到收藏信息
    # userloveorg_list = request.user.userlove_set.all().filter(love_type=1)  # 查找出喜爱的类型是1的信息
    userloveorg_list = UserLove.objects.filter(love_man=request.user, love_type=1, love_status=True)  # 查找出喜爱的类型是1的信息
    org_ids = [userlovorg.love_id for userlovorg in userloveorg_list]
    org_list = OrgInfo.objects.filter(id_in=org_ids)
    return render(request, 'users/usercenter-fav-org.html', {"org_list": org_list})


def user_loveteacher(request):
    # 找中间表operations 找到收藏信息
    # userloveteacher_list = request.user.userlove_set.all().filter(love_type=3)  # 查找出喜爱的类型是3的信息
    userloveteacher_list = UserLove.objects.filter(love_man=request.user, love_type=3, love_status=True)
    teacher_ids = [userloveteacher.love_id for userloveteacher in userloveteacher_list]
    teacher_list = TeacherInfo.objects.filter(id_in=teacher_ids)
    return render(request, 'users/usercenter-fav-teacher.html', {"teacher_list": teacher_list})


def user_lovecourse(request):
    # 找中间表operations 找到收藏信息
    # userlovecourse_list = request.user.userlove_set.all().filter(love_type=2)  # 查找出喜爱的类型是2的信息
    userlovecourse_list = UserLove.objects.filter(love_man=request.user, love_type=2, love_status=True)
    course_ids = [userlovecourse.love_id for userlovecourse in userlovecourse_list]
    course_list = TeacherInfo.objects.filter(id_in=course_ids)
    return render(request, 'users/usercenter-fav-course.html', {"course_list": course_list})


def user_deletelove(request):
    loveid = request.GET.get('loveid', '')
    lovetype = request.GET.get('lovetype', '')
    if loveid and lovetype:
        love = UserLove.objects.filter(love_id=int(loveid), love_type=int(lovetype), love_man=request.user,
                                       love_status=True)
        if love:
            love[0].love_status = False
            love[0].save()
            return JsonResponse({"status": "ok", "msg": "remove love success!"})
        else:
            return JsonResponse({"status": "fail", "msg": "remove love fail!"})
    else:
        return JsonResponse({"status": "fail", "msg": "remove love fail!"})


def user_message(request):
    msg_list = UserMessage.objects.filter(message_man=request.user.id)
    return render(request, 'users/usercenter-message.html', {"msg_list": msg_list})


def user_deletemessage(request):
    delete_id = request.GET.get('delete_id', '')
    if delete_id:
        msg = UserMessage.objects.filter(id=int(delete_id))[0]
        msg.message_status = True
        msg.save()
        return JsonResponse({"status": "ok", "msg": "message is read"})
    else:
        return JsonResponse({"status": "fail", "msg": "message read failed"})


def handler_404(request, exception):
    return render(request, "handler_404.html", status=404)

def handler_400(request, exception):
    return render(request, 'handler_400.html', status=400)

def handler_403(request, exception):
    return render(request, 'handler_403.html', status=403)


def handler_500(request):
    return render(request, "handler_500.html", status=500)
