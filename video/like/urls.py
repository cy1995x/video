from django.urls import path

from like import views

urlpatterns = [
    path('', views.like_view),
    path('is_up', views.LikeView.as_view())
]
