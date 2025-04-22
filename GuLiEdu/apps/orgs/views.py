from django.shortcuts import render
from .models import OrgInfo, TeacherInfo, CityInfo
from operations.models import UserLove
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


# Create your views here.

def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_citys = CityInfo.objects.all()
    sort_orgs = all_orgs.order_by('-love_num')[:3]

    # 全局搜索功能的过滤
    keywords = request.GET.get("keywords", "")
    if keywords:
        all_orgs = all_orgs.filter(
            Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))  # 查找包含的内容 不区分大小写

    # 按照机构类别进行过滤筛选
    cate = request.GET.get('cate', '')
    if cate:
        all_orgs = all_orgs.filter(category=cate)

    # 按照所在地区进行过滤筛选
    cityid = request.GET.get('cityid', '')
    if cityid:
        all_orgs = all_orgs.filter(cityinfo_id=int(cityid))

    # 排序 传入 学习人数 或者 课程人数 排名
    sort = request.GET.get("sort", '')
    if sort:
        all_orgs = all_orgs.order_by('-' + sort)

    """
    pa.page(pagenum)：
    pagenum 是整数且有效 → 返回对应页数据。
    pagenum 不是整数 → 返回第一页。
    pagenum 超出范围 → 返回最后一页。
    """
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_orgs, 3)  # 实例化 Paginator，每页显示 3 条数据
    try:
        pages = pa.page(pagenum)  # 尝试获取 pagenum 指定的页码，如果 pagenum 是有效的页码，则返回该页的数据。
    except PageNotAnInteger:
        pages = pa.page(1)  # pagenum 不是整数（如 pagenum="abc"）如果 pagenum 不是整数，则默认返回 第 1 页 的数据。
    except EmptyPage:
        pages = pa.page(pa.num_pages)  # pagenum 超出有效范围（如 pagenum=100，但总共只有 10 页） 如果 pagenum 超出范围，则返回 最后一页 的数据。
    return render(request, 'orgs/org-list.html',
                  {"all_orgs": all_orgs,
                   "pages": pages,
                   "all_citys": all_citys,
                   "sort_orgs": sort_orgs,
                   'cate': cate,
                   'cityid': cityid,
                   'sort': sort,
                   "keywords": keywords})


def org_detail(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        org.click_num += 1  # 访问次数
        org.save()

        # 处理用户收藏的信息, 让前端根据状态显示收藏还是取消收藏
        lovestatus = False
        if request.user.is_authenticated:  # Django2.0 以上无需加（）
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        return render(request, 'orgs/org-detail-homepage.html',
                      {'org': org, "detail_type": "home", "lovestaus": lovestatus})


def org_detail_course(request, org_id):
    if org_id:
        if org_id:
            org = OrgInfo.objects.filter(id=int(org_id))[0]
            all_course = org.courseinfo_set.all()
            # 处理用户收藏的信息, 让前端根据状态显示收藏还是取消收藏
            lovestatus = False
            if request.user.is_authenticated():
                love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1,
                                               love_status=True)
                if love:
                    lovestatus = True

            # 分页
            """
                pa.page(pagenum)：
                pagenum 是整数且有效 → 返回对应页数据。
                pagenum 不是整数 → 返回第一页。
                pagenum 超出范围 → 返回最后一页。
                """
            pagenum = request.GET.get('pagenum', '')
            pa = Paginator(all_course, 3)  # 实例化 Paginator，每页显示 3 条数据
            try:
                pages = pa.page(pagenum)  # 尝试获取 pagenum 指定的页码，如果 pagenum 是有效的页码，则返回该页的数据。
            except PageNotAnInteger:
                pages = pa.page(1)  # pagenum 不是整数（如 pagenum="abc"）如果 pagenum 不是整数，则默认返回 第 1 页 的数据。
            except EmptyPage:
                pages = pa.page(pa.num_pages)  # pagenum 超出有效范围（如 pagenum=100，但总共只有 10 页） 如果 pagenum 超出范围，则返回 最后一页 的数据。
            return render(request, 'orgs/org-detail-course.html',
                          {"org": org, "pages": pages, "detail_type": "course", "lovestaus": lovestatus})


def org_detail_desc(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        # 处理用户收藏的信息, 让前端根据状态显示收藏还是取消收藏
        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1,
                                           love_status=True)
            if love:
                lovestatus = True
        return render(request, 'orgs/org-detail-desc.html',
                      {'org': org, "detail_type": "desc", "lovestaus": lovestatus})


def org_detail_teacher(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        # 处理用户收藏的信息, 让前端根据状态显示收藏还是取消收藏
        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1,
                                           love_status=True)
            if love:
                lovestatus = True
        return render(request, 'orgs/org-detail-teachers.html',
                      {'org': org, "detail_type": "teacher", "lovestaus": lovestatus})


def teacher_list(request):
    all_teachers = TeacherInfo.objects.all()
    sort_teachers = all_teachers.order_by('-love_num')[:2]

    # 全局搜索功能的过滤
    keywords = request.GET.get("keywords", "")
    if keywords:
        all_teachers = all_teachers.filter(name__icontains=keywords)  # 查找包含的内容 不区分大小写

    sort = request.GET.get("sort", "")
    if sort:
        all_teachers = all_teachers.order_by("-" + sort)

    # 分页
    """
        pa.page(pagenum)：
        pagenum 是整数且有效 → 返回对应页数据。
        pagenum 不是整数 → 返回第一页。
        pagenum 超出范围 → 返回最后一页。
        """
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_teachers, 3)  # 实例化 Paginator，每页显示 3 条数据
    try:
        pages = pa.page(pagenum)  # 尝试获取 pagenum 指定的页码，如果 pagenum 是有效的页码，则返回该页的数据。
    except PageNotAnInteger:
        pages = pa.page(1)  # pagenum 不是整数（如 pagenum="abc"）如果 pagenum 不是整数，则默认返回 第 1 页 的数据。
    except EmptyPage:
        pages = pa.page(pa.num_pages)  # pagenum 超出有效范围（如 pagenum=100，但总共只有 10 页） 如果 pagenum 超出范围，则返回 最后一页 的数据。

    return render(request, "orgs/teachers-list.html",
                  {"all_teachers": all_teachers, "sort_teachers": sort_teachers, "pages": pages, "sort": sort,"keywords":keywords})


def teacher_detail(request, teacher_id):
    if teacher_id:
        all_teachers = TeacherInfo.objects.all()
        teacher = TeacherInfo.objects.filter(id=int(teacher_id))[0]
        sort_teachers = all_teachers.order_by('-love_num')[:2]

        teacher.click_num += 1  # 访问次数
        teacher.save()

        # # 根据下面的状态展示是收藏还是取消收藏
        loveteacher = False  # 收藏状态
        loveorg = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_id=int(teacher_id), love_type=3, love_status=True,
                                           love_man=request.user)
            if love:
                loveteacher = True

            lovel = UserLove.objects.filter(love_id=teacher.work_company.id, love_type=1, love_status=True,
                                            love_man=request.user)
            if lovel:
                loveorg = True

        return render(request, "orgs/teacher-detail.html",
                      {"teacher": teacher, "sort_teachers": sort_teachers, "loveteacher": loveteacher,
                       "loveorg": loveorg})
        # else:
        #     return JsonResponse({"status": "fail", "msg": "当前用户未登录"})
