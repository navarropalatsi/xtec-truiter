from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", views.home, name="home"),
    
    path("u/<str:username>/", views.profile, name="profile"),
    path("u/<str:username>/update_profile/", views.update_profile_form, name="update_profile_form"),
    path("u/<str:username>/update_profile/submit/", views.update_profile, name="update_profile"),
    path("u/<str:username>/update_profile_picture/", views.update_profile_picture, name="update_profile_picture"),
    
    path("u/<str:username>/follow/", views.follow_user, name="follow_user"),
    path("u/<str:username>/unfollow/", views.unfollow_user, name="unfollow_user"),

    path("p/new/", views.create_post, name="create_post"),
    path("p/<int:post_id>", views.post, name="post"),
    path("p/<int:post_id>/like/", views.like_post, name="like_post"),
    path("p/<int:post_id>/add_comment/", views.add_comment, name="add_comment"),
    path("p/<int:post_id>/repost_post/", views.repost_post, name="repost_post"),

    path("signup/", views.signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
