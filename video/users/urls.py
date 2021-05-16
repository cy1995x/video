from django.urls import path

from users import views

urlpatterns = [
    # sms验证路由：http://127.0.0.1/v1/users/sms
    path('sms', views.sms_view),

    # 注册路由：http://127.0.0.1/v1/users/
    path('', views.UserView.as_view()),

    path('<str:username>', views.UserInfoView.as_view()),

    # 个人空间
    path('<str:username>/space', views.space_view),

    # 图像上传
    path('<str:username>/avatar', views.AvatarView.as_view()),

    # 粉丝路由
    path('<str:username>/fans', views.FansView.as_view()),

    # 关注路由
    path('<str:username>/attention', views.AttentionView.as_view()),

    path('<str:username>/attention/info', views.AttentionInfoView.as_view()),
    path('<str:username>/fans/info', views.FansInfoView.as_view()),
]
