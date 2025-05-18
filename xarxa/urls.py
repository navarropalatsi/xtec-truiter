from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("u/<str:username>/", views.profile, name="profile"),
    path("p/new/", views.create_post, name="create_post"),
    path("p/<int:post_id>/like/", views.like_post, name="like_post"),
]
