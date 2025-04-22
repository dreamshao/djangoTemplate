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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include  # 移除 url
# from users.views import index
from users.views import IndexView

urlpatterns = [
    # path('xadmin/', xadmin.site.urls),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),  # 验证码请求
    # path('ueditor/', include("DjangoUeditor.urls")),  # 富文本编辑器
    path('ckeditor/', include('ckeditor_uploader.urls')), # 富文本编辑器
    # path('', index, name="index"),
    path("", IndexView.as_view(), name="index"),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('orgs/', include(('orgs.urls', 'orgs'), namespace='orgs')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('operations/', include(('operations.urls', 'operations'), namespace='operations')),
    # path('orgs/', include(('orgs.urls', 'orgs'), namespace='orgs')),
    # path('operations/', include(('operations.urls', 'operations'), namespace='operations')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "星仔教育管理系统"  # 设置管理后台的标题
admin.site.site_title = "星仔教育管理系统"
admin.site.index_title = "星仔教育管理系统"

handler404 = "users.views.handler_404"
handler400 = 'users.views.handler_400'
handler403 = 'users.views.handler_403'
handler500 = "users.views.handler_500"
