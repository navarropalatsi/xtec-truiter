from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Post
from .forms import PostForm


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sessió automàticament després del registre
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def home(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"posts": posts})


def profile(request, username):
    watched_user = User.objects.get(username=username)
    if watched_user.profile.followers.filter(id=watched_user.id).exists():
        watched_user.profile.followers.remove(watched_user)  # Elimina l'usuari de si mateix si és seguidor

    posts = watched_user.posts.all().order_by("-created_at")
    return render(
        request, "profile.html", {"watched_user": watched_user, "posts": posts, 'is_following': request.user in watched_user.profile.followers.all() if request.user.is_authenticated else False}
    )

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "post.html", {"post": post})

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "home.html", {"form": form})


def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Si ja li agrada, elimina el like
    else:
        post.likes.add(request.user)
    next = request.POST.get("next", "/")
    return redirect(next)

def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        if comment_text:
            post.comments.create(author=request.user, text=comment_text)
    return redirect("post", post_id=post_id)

def follow_user(request, username):
    user_to_follow = User.objects.get(username=username)
    user_to_follow.profile.followers.add(request.user)
    return redirect("profile", username=username)


def unfollow_user(request, username):
    user_to_unfollow = User.objects.get(username=username)
    user_to_unfollow.profile.followers.remove(request.user)
    return redirect("profile", username=username)

def repost_post(request, post_id):
    original_post = Post.objects.get(id=post_id)
    if request.method == "POST":
        repost = Post.objects.create(
            author=request.user,
            content=original_post.content,
            repost=original_post
        )
        return redirect("post", post_id=repost.id)
    return redirect("post", post_id=post_id)