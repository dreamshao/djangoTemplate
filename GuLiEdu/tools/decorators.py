"""
Author: WangXing
Time: 2025/4/9 20:03
Description: 未登录下的装饰器
"""
from django.shortcuts import redirect, reverse
from django.http import JsonResponse


def login_decorator(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():  # 判断当前请求是否是ajax
                return JsonResponse({"status": "nologin"})

            url = request.get_full_path()  # 获取当前访问的路由信息(完整的url)
            ret = redirect(reverse('users:user_login'))
            ret.set_cookie("url", url)  # 登录后可以回到之前的页面
            return ret

    return inner
