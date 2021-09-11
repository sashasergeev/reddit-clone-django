from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from itertools import chain
from main.models import Post

# Create your views here.

# AUTH VIEWS
def LoginView(request):
    if request.user.is_authenticated:
        return redirect("main:index")

    if request.method != "POST":
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main:index")

    context = {"form": form}
    return render(request, "registration/login.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("main:index")

    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("main:index")
    context = {"form": form}
    return render(request, "registration/register.html", context)


def LogoutView(request):
    logout(request)
    return redirect("main:index")


# USER PROFILE
def MainProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all()
    comments = user.comment_set.all()

    feed = sorted(
        chain(posts, comments), key=lambda data: data.created_at, reverse=True
    )
    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": feed, "current": "overview"},
    )


def PostsProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.order_by("-created_at")

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": posts, "current": "posts"},
    )


def CommentsProfile(request, username):
    user = get_object_or_404(User, username=username)
    comments = user.comment_set.order_by("-created_at")

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": comments, "current": "comments"},
    )


def UpvotedProfile(request, username):
    user = get_object_or_404(User, username=username)
    upvoted = Post.objects.filter(post_upvote__user__username=username)

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": upvoted, "current": "upvoted"},
    )


def DownvotedProfile(request, username):
    user = get_object_or_404(User, username=username)
    downvoted = Post.objects.filter(post_downvote__user__username=username)

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": downvoted, "current": "downvoted"},
    )
