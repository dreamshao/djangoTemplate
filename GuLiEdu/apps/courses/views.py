from django.shortcuts import render
from .models import CourseInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from operations.models import UserLove, UserCourse, UserComment
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tools.decorators import login_decorator


# Create your views here.
def course_list(request):
    all_courses = CourseInfo.objects.all()
    recommend_courses = all_courses.order_by('-add_time')[:3]

    # 全局搜索功能的过滤
    keywords = request.GET.get("keywords", "")
    if keywords:
        all_courses = all_courses.filter(
            Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))  # 查找包含的内容 不区分大小写

    sort = request.GET.get('sort', '')
    if sort:
        all_courses = all_courses.order_by('-' + sort)

    # 分页
    """
        pa.page(pagenum)：
        pagenum 是整数且有效 → 返回对应页数据。
        pagenum 不是整数 → 返回第一页。
        pagenum 超出范围 → 返回最后一页。
        """
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_courses, 3)  # 实例化 Paginator，每页显示 3 条数据
    try:
        pages = pa.page(pagenum)  # 尝试获取 pagenum 指定的页码，如果 pagenum 是有效的页码，则返回该页的数据。
    except PageNotAnInteger:
        pages = pa.page(1)  # pagenum 不是整数（如 pagenum="abc"）如果 pagenum 不是整数，则默认返回 第 1 页 的数据。
    except EmptyPage:
        pages = pa.page(pa.num_pages)  # pagenum 超出有效范围（如 pagenum=100，但总共只有 10 页） 如果 pagenum 超出范围，则返回 最后一页 的数据。
    return render(request, 'courses/course-list.html',
                  {'all_courses': all_courses, "recommend_courses": recommend_courses, "pages": pages, 'sort': sort,
                   "keywords": keywords})


# def course_detail(request, course_id):
#     if course_id:
#         print(f"course_id+={course_id}")
#         course = CourseInfo.objects.filter(id=int(course_id))[0]
#         print("here")
#         relate_course = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))  # 去除自己
#         print("here")
#         # 根据下面的状态展示是收藏还是取消收藏
#         lovecourse = False  # 收藏状态
#         loveorg = False
#         if request.user.is_authenticated: # django2.0 后改了不需要加（）
#             love = UserLove.objects.filter(love_id=int(course_id), love_type=2, love_status=True, love_man=request.user)
#             if love:
#                 lovecourse = True
#
#             lovel = UserLove.objects.filter(love_id=course.orginfo.id, love_type=1, love_status=True,
#                                            love_man=request.user)
#             if lovel:
#                 loveorg = True
#
#         return render(request, 'courses/course-detail.html',
#                       {"course": course, "relate_course": relate_course, "lovecourse": lovecourse, "loveorg": loveorg})
#     else:
#         return JsonResponse({"status":"fail"})

def course_detail(request, course_id):
    if course_id:
        # 根据id查询课程信息
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        print("her")

        # 课程详情页访问一次 访问量+1
        course.click_num += 1
        course.save()

        # 根据类别查看相关课程信息
        relate_course = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))[0]

        # lovecourse和loveorg 用来存储用户收藏这个东西的状态，在模板当中根据这个状态来确定页面加载时候，显示的是收藏还是取消收藏
        lovecourse = False  # 课程的收藏状态(页面显示)
        loveorg = False  # 机构的收藏状态(页面显示)
        if request.user.is_authenticated:  # 验证用户是否登录
            # 根据要课程id,课程类型,登录用户查询收藏表中是否存在这条记录
            love = UserLove.objects.filter(love_id=int(course_id), love_type=2, love_status=True, love_man=request.user)
            if love:
                lovecourse = True
            # 根据要机构id,机构类型,登录用户查询收藏表中是否存在这条记录
            love = UserLove.objects.filter(love_id=course.orginfo.id, love_type=1, love_status=True,
                                           love_man=request.user)
            if love:
                loveorg = True

        return render(request, 'courses/course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'lovecourse': lovecourse,
            'loveorg': loveorg,
        })


# @login_required(login_url="users/user_login/")
@login_decorator
def course_video(request, course_id):
    course_list = []
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        # 当用户点击开始学习的时候代表用户学习了这个课程，需要判断当前是否学习过，没有则创建
        usercourse_list = UserCourse.objects.filter(study_man=request.user, study_course=course)
        if not usercourse_list:
            a = UserCourse()
            a.study_man = request.user
            a.study_course = course
            a.save()
            print("学习人数")
            print(course.study_num)
            course.study_num += 1  # 学习人数
            print(course.study_num)
            print("学习人数")
            course.save()

            # 学习过这个课程的人也属于学习过这个机构的人

            # 从学习课程的表中找去当前这个人学习的所有课程

            usercourse_list = UserCourse.objects.filter(study_man=request.user)
            course_list = [usercourse.study_course for usercourse in usercourse_list]
            # 根据拿到的所有课程，找到每个课程的机构
            org_list = list(set([course.orginfo for course in course_list]))
            if course.orginfo not in org_list:
                course.orginfo.study_num += 1
                course.orginfo.save()

            # 学过这个课程的学生还学过什么课程？
            # 根据中间表课程表中找到学生学过该课的所有人

            usercourse_list = UserCourse.objects.filter(study_course=course)

            # 根据找到的用户学习课程列表，遍历拿到学过这门课程的用户列表

            user_list = [usercourse.study_man for usercourse in usercourse_list]

            # 根据找到的用户，从中间表用户学习表中，找到用户学习其他课程的整个对象

            # study_man__in in 是否包含在范围内 pk in= [1,2,3,4,5]或者 id in=[1,2.3,4,5] 去除当前已经学习过的课程

            usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)

            # 从获取到的用户课程列表中，拿到我们需要的其他课程

            course_list = list(set([usercourse.study_course for usercourse in usercourse_list]))

        return render(request, "courses/course-video.html", {"course": course, "course_list": course_list})


# def course_comment(request, courese_id):
#     if courese_id:
#         course = CourseInfo.objects.filter(id=int(courese_id))
#         all_comments = course.usercomment_set.all()[:10]  # 根据中间表获取评论信息
#         return render(request, "courses/course-comment.html", {"all_comments", all_comments})

# 公开课课程视频-评论
def course_comment(request, course_id):
    if course_id:
        # 查询要评论的课程
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        # 根据课程查询该课程下的所有评论   commnet_course
        all_comment = UserComment.objects.filter(commnet_course=course).order_by('-add_time')

        # 学过该课程的用户还学过哪些课程???(指当前用户还是学习该课程的所有用户)
        # 1.从用户课程表(UserCourse)中查找到所有学习过该课程的 所有对象(用户课程)
        usercourse_list = UserCourse.objects.filter(study_course=course)
        # 2.根据查询得到的所有用户课程对象获取对应的用户信息列表
        user_list = [usercourse.study_man for usercourse in usercourse_list]
        # 3.根据获取到的用户信息列表查询用户学习的其他课程的 所有对象(用户课程)
        usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)
        # 4.从获取到的用户课程列表中获取所有课程列表
        course_list = list(set([usercourse.study_course for usercourse in usercourse_list]))

        return render(request, 'courses/course-comment.html', {
            'course': course,
            'all_comment': all_comment,
            'course_list': course_list,
        })
