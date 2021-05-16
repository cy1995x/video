from django.urls import path

from search import views

urlpatterns = [
    # 查询用户
    path('user/', views.SearchUserView.as_view())
]
