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
    user = User.objects.get(username=username)
    posts = user.posts.all().order_by("-created_at")
    return render(request, "profile.html", {"username": username, 'posts': posts})


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
    post.likes.add(request.user)
    return redirect("home")
