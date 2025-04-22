from django.shortcuts import render
from .forms import UserAskForm
from django.http import JsonResponse
from .models import UserAsk, UserLove, UserComment
from .forms import UserCommentForm
from orgs.models import OrgInfo, TeacherInfo
from courses.models import CourseInfo
from tools.decorators import login_decorator


# Create your views here.
def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():
        user_ask_form.save(commit=True)
        # 上面一行代码等同于下面的
        # name = user_ask_form.cleaned_data['name']
        # phone = user_ask_form.cleaned_data['phone']
        # course = user_ask_form.cleaned_data['course']
        #
        # a = UserAsk()
        # a.name = name
        # a.phone = phone
        # a.course = course
        # a.save()
        return JsonResponse({"status": "ok", "msg": "咨询成功"})
    else:
        return JsonResponse({"status": "fail", "msg": "咨询失败"})

@login_decorator
def user_love(request):
    loveid = request.GET.get('loveid', '')
    lovetype = request.GET.get('lovetype', '')
    if loveid and lovetype:
        # 根据类型判断你是机构 老师
        obj = None
        if int(lovetype) == 1:
            obj = OrgInfo.objects.filter(id=int(loveid))[0]
        if int(lovetype) == 2:
            obj = CourseInfo.objects.filter(id=int(loveid))[0]
        if int(lovetype) == 3:
            obj = TeacherInfo.objects.filter(id=int(loveid))[0]

        # 收藏的Id 和 type 同时存在, 那么首先去收藏表中去查找这个用户是否有这个收藏记录
        love = UserLove.objects.filter(love_id=int(loveid), love_type=int(lovetype), love_man=request.user)
        if love:
            # 如果本来已经存在收藏记录，且是True的情况则表示之前是收藏状态，再次点击是取消收藏改为false, 反之亦是
            if love[0].love_status:
                love[0].love_status = False
                love[0].save()
                obj.love_num -= 1  # 收藏数据
                obj.save()

                return JsonResponse({"status": "ok", "msg": "收藏成功"})
            else:
                love[0].love_status = True
                love[0].save()
                obj.love_num += 1
                obj.save()
                return JsonResponse({"status": "ok", "msg": "取消收藏"})
        else:
            # 没有收藏过则创建记录，将status改为True
            a = UserLove()
            a.love_man = request.user
            a.love_status = True
            a.love_id = int(loveid)
            a.love_type = int(lovetype)
            a.save()
            obj.love_num += 1
            obj.save()
            return JsonResponse({"status": "ok", "msg": "收藏成功"})
    else:
        return JsonResponse({"status": "ok", "msg": "收藏失败"})


def user_comment(request):
    user_comment_form = UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        course = user_comment_form.cleaned_data['course']
        content = user_comment_form.cleaned_data['content']
        a = UserComment()
        a.commnet_man = request.user
        a.comment_content = content
        a.commnet_course_id = course
        a.save()
        return JsonResponse({"status": "ok", "msg": "评论成功"})
    else:
        return JsonResponse({"status": "fail", "msg": "评论失败"})
