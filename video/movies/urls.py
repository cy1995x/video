from django.urls import path

from movies import views

urlpatterns = [
    path('', views.MoviesView.as_view()),
    path('control', views.MovieControlView.as_view()),
    # 详情页路由
    path('<int:m_rank>', views.DetailView.as_view()),
    # 短视频get
    path('shortvideo', views.short_video_view),

]
