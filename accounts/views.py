from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator

from django.urls import reverse
from itertools import chain
from django.views import View

from main.models import Post
from .forms import ProfileUpdateForm


# AUTH VIEWS
class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You've logged in successfuly!")
            return redirect("main:index")
        else:
            return render(request, "registration/login.html", {"form": form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        form = UserCreationForm()
        return render(request, "registration/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, "You've successfully created an account!")
            return redirect("main:index")
        else:
            return render(request, "registration/register.html", {"form": form})


def LogoutView(request):
    logout(request)
    return redirect("main:index")


# USER PROFILE
class ProfileSettings(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ProfileUpdateForm()
        return render(request, "profile/settings.html", {"form": form})

    def post(self, request, *args, **kwargs):
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
            messages.error(request, "Invalid data.")
            return render(request, "registration/register.html", {"form": form})


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
