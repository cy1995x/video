"""video URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from btoken import views as token_views
from classification import views as c_view
from history import views as h_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户模块
    path('v1/users/', include('users.urls')),
    # 登陆
    path('v1/btoken', token_views.TokenView.as_view()),
    # 电影模块
    path('v1/movies/', include('movies.urls')),
    # 点赞模块
    path('v1/like/', include('like.urls')),
    # 评论模块
    path('v1/comments/', include('comments.urls')),
    # 分类模块
    path('v1/classifications/', c_view.classification_view),
    # 历史记录
    path('v1/history/', h_view.HistoryView.as_view()),
    # 查询模块
    path('v1/search/', include('search.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
