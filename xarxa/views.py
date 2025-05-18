from django.shortcuts import render

from .models import Post
from django.contrib.auth.models import User
from .forms import PostForm
from django.shortcuts import redirect

# Create your views here.
def home(request):
  posts = Post.objects.all().order_by("-created_at")
  return render(request, "home.html", {"posts": posts})

def profile(request, username):
    user = User.objects.get(username=username)
    posts  = user.posts.all().order_by("-created_at")
    return render(request, "profile.html", {"username": username})

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
