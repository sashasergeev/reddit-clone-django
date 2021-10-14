from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from django.urls import reverse
from itertools import chain

from django.views.generic import edit
from main.models import Post
from .forms import ProfileUpdateForm

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
            messages.success(request, "You've logged in successfuly!")
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
            messages.success(request, "You've successfully created an account!")
            return redirect("main:index")
    context = {"form": form}
    return render(request, "registration/register.html", context)


def LogoutView(request):
    logout(request)
    return redirect("main:index")


# USER PROFILE
@login_required
def ProfileSettings(request):
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()

            messages.success(request, "Changes saved")
            return redirect(
                reverse("accounts:profile-overview", args=[request.user.username])
            )
    else:
        form = ProfileUpdateForm()
    context = {"form": form}
    return render(request, "profile/settings.html", context)


def MainProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all()
    comments = user.comment_set.all()

    feed = sorted(
        chain(posts, comments), key=lambda data: data.created_at, reverse=True
    )
    paginator = Paginator(feed, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": page_obj, "current": "overview"},
    )


def PostsProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.order_by("-created_at")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": page_obj, "current": "posts"},
    )


def CommentsProfile(request, username):
    user = get_object_or_404(User, username=username)
    comments = user.comment_set.order_by("-created_at")

    paginator = Paginator(comments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": page_obj, "current": "comments"},
    )


def UpvotedProfile(request, username):
    user = get_object_or_404(User, username=username)
    upvoted = Post.objects.filter(post_upvote__user__username=username)

    paginator = Paginator(upvoted, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": page_obj, "current": "upvoted"},
    )


def DownvotedProfile(request, username):
    user = get_object_or_404(User, username=username)
    downvoted = Post.objects.filter(post_downvote__user__username=username)

    paginator = Paginator(downvoted, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": page_obj, "current": "downvoted"},
    )


@login_required
def SavedProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.saved_posts.all()
    comments = user.saved_comments.all()
    feed = sorted(
        chain(posts, comments), key=lambda data: data.created_at, reverse=True
    )
    paginator = Paginator(feed, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profile/main.html",
        {"user": user, "feed": page_obj, "current": "saved"},
    )
