from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic, View
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Count

from .forms import CommentForm
from .models import (
    Subreddit,
    Post,
    Comment,
    Notifications,
)


# Create your views here.


class IndexListView(generic.ListView):
    model = Post
    template_name = "main/index.html"
    paginate_by = 10
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        context["sub_list"] = Subreddit.objects.annotate(
            num_members=Count("members")
        ).order_by("-num_members")[:5]
        return context


def SubredditListPage(request):
    subs = Subreddit.objects.annotate(num_members=Count("members")).order_by(
        "-num_members"
    )

    paginator = Paginator(subs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "main/subredditlist.html", {"page_obj": page_obj})


def subredditDetailPage(request, name):
    subreddit = Subreddit.objects.get(name=name)
    posts = subreddit.posts.prefetch_related("post_upvote", "post_downvote").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"subreddit": subreddit, "posts": page_obj}
    return render(request, "main/subredditdetail.html", context)


def PostDetailPage(request, name, pk):
    # comment purposes
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.commentator = request.user
            new_comment.post_id = pk
            new_comment.save()
            return HttpResponseRedirect(reverse("main:post-detail", args=(name, pk)))
    else:
        form = CommentForm()

    # main page rendering
    subreddit = Subreddit.objects.get(name=name)
    post = get_object_or_404(subreddit.posts, pk=pk)
    comments = post.comment_set.filter(parent=None)
    comments = comments.get_descendants(include_self=True).prefetch_related(
        "comment_upvote", "comment_downvote"
    )
    context = {"subreddit": subreddit, "post": post, "comments": comments, "form": form}
    return render(request, "main/post-detail.html", context)


# NOTOFICATION VIEWS
class PostCommentReplyNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notifications.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()
        return redirect(reverse("main:post-detail", args=(post.sub.name, post_pk)))


class CommentNotifications(View):
    def get(self, request, notification_pk, comment_pk, *args, **kwargs):
        notification = Notifications.objects.get(pk=notification_pk)
        comment = Comment.objects.get(pk=comment_pk)

        notification.user_has_seen = True
        notification.save()
        return redirect(
            reverse("main:post-detail", args=(comment.post.sub.name, comment.post.pk))
        )


# CREATE POST
class CreatePost(LoginRequiredMixin, generic.edit.CreateView):
    login_url = "/accounts/login/"
    model = Post
    fields = ["post_type", "sub", "title", "text", "image"]
    template_name = "main/create_post.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.creator = user
        return super(CreatePost, self).form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(CreatePost, self).get_form(form_class)
        form.fields["sub"].widget.attrs = {
            "placeholder": "Choose a community",
            "class": "someclass",
        }
        form.fields["post_type"].widget.attrs = {
            "class": "form_inputs",
        }
        form.fields["title"].widget.attrs = {
            "placeholder": "Title",
            "class": "form_inputs",
        }
        form.fields["text"].widget.attrs = {
            "placeholder": "Text",
            "class": "form_inputs",
        }
        form.fields["image"].widget.attrs = {
            "class": "form_inputs",
        }
        form.fields["text"].required = False
        form.fields["image"].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context["form"].fields["sub"].empty_label = "Choose a community"
        return context


# CREATE POST IN A CURRENT COMMUNITY
class CreatePostIn(LoginRequiredMixin, generic.edit.CreateView):
    login_url = "/accounts/login/"
    model = Post
    fields = ["post_type", "title", "text", "image"]
    template_name = "main/create-post-in.html"

    def form_valid(self, form):
        user = self.request.user
        subname = self.kwargs["name"]
        form.instance.creator = user
        form.instance.sub = Subreddit.objects.get(name=subname)
        return super(CreatePostIn, self).form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(CreatePostIn, self).get_form(form_class)
        form.fields["title"].widget.attrs = {
            "placeholder": "Title",
            "class": "form_inputs",
        }
        form.fields["text"].widget.attrs = {
            "placeholder": "Text",
            "class": "form_inputs",
        }
        form.fields["image"].widget.attrs = {
            "class": "form_inputs",
        }
        form.fields["post_type"].widget.attrs = {
            "class": "form_inputs",
        }
        form.fields["text"].required = False
        form.fields["image"].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super(CreatePostIn, self).get_context_data(**kwargs)
        context["subreddit"] = Subreddit.objects.get(name=self.kwargs["name"])
        return context


# CREATE SUBREDDIT
class CreateSubreddit(LoginRequiredMixin, generic.edit.CreateView):
    login_url = "/accounts/login/"
    model = Subreddit
    fields = ["name", "description", "image"]
    template_name = "main/create-subreddit.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.creator = user
        return super(CreateSubreddit, self).form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(CreateSubreddit, self).get_form(form_class)
        form.fields["image"].required = False
        return form
