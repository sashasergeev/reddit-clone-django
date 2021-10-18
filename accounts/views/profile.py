from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator

from django.urls import reverse
from itertools import chain
from django.views import View
from django.db.models import Count

from main.models import Post
from accounts.forms import ProfileUpdateForm


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


# DRY QUERIES
def postsQuery(quo):
    return (
        quo.annotate(num_comments=Count("comment"))
        .prefetch_related("post_upvote", "post_downvote")
        .select_related("creator", "sub")
        .all()
    )


def commentsQuery(quo):
    return (
        quo.select_related("commentator", "post", "post__sub", "post__creator")
        .prefetch_related("comment_upvote", "comment_downvote")
        .all()
    )


# CONTEXT
def postsContext(context, request):
    if request.user.is_authenticated:
        context["upvoted_posts"] = request.user.upvote_user_post.values_list(
            "post_id", flat=True
        )
        context["downvoted_posts"] = request.user.downvote_user_post.values_list(
            "post_id", flat=True
        )
        context["saved_posts"] = request.user.saved_posts.values_list("id", flat=True)
    return context


def commentsContext(context, request):
    if request.user.is_authenticated:
        context["comment_saved"] = request.user.saved_comments.values_list(
            "id", flat=True
        )
    return context


def subsContext(context, request):
    if request.user.is_authenticated:
        context["joined_subs"] = request.user.sub_members.values_list("id", flat=True)
    return context


def pagination(request, pagObj, pagNum=10):
    paginator = Paginator(pagObj, pagNum)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


# VIEWS
def MainProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts = postsQuery(user.post_set)
    comments = commentsQuery(user.comment_set)

    feed = sorted(
        chain(posts, comments), key=lambda data: data.created_at, reverse=True
    )
    page_obj = pagination(request, feed)

    context = {"user": user, "feed": page_obj, "current": "overview"}
    context = postsContext(context, request)
    context = commentsContext(context, request)
    context = subsContext(context, request)
    return render(request, "profile/main.html", context)


def PostsProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts = postsQuery(user.post_set).order_by("-created_at")

    page_obj = pagination(request, posts)

    context = {"user": user, "feed": page_obj, "current": "posts"}
    context = postsContext(context, request)
    return render(request, "profile/main.html", context)


def CommentsProfile(request, username):
    user = get_object_or_404(User, username=username)
    comments = commentsQuery(user.comment_set).order_by("-created_at")

    page_obj = pagination(request, comments)

    context = {"user": user, "feed": page_obj, "current": "comments"}
    context = commentsContext(context, request)
    return render(request, "profile/main.html", context)


def UpvotedProfile(request, username):
    user = get_object_or_404(User, username=username)
    upvoted = postsQuery(
        Post.objects.filter(post_upvote__user__username=username)
    ).order_by("-created_at")

    page_obj = pagination(request, upvoted)

    context = {"user": user, "feed": page_obj, "current": "upvoted"}
    context = postsContext(context, request)
    return render(request, "profile/main.html", context)


def DownvotedProfile(request, username):
    user = get_object_or_404(User, username=username)
    downvoted = postsQuery(
        Post.objects.filter(post_downvote__user__username=username)
    ).order_by("-created_at")

    page_obj = pagination(request, downvoted)

    context = {"user": user, "feed": page_obj, "current": "downvoted"}
    context = postsContext(context, request)
    return render(request, "profile/main.html", context)


@login_required
def SavedProfile(request, username):
    user = get_object_or_404(User, username=username)
    posts = postsQuery(user.saved_posts)
    comments = commentsQuery(user.saved_comments)
    feed = sorted(
        chain(posts, comments), key=lambda data: data.created_at, reverse=True
    )
    page_obj = pagination(request, feed)

    context = {"user": user, "feed": page_obj, "current": "saved"}
    context = postsContext(context, request)
    context = commentsContext(context, request)
    context = subsContext(context, request)
    return render(request, "profile/main.html", context)
