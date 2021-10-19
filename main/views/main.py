from django.views import generic, View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count

from main.forms import CommentForm, SubredditUpdateForm
from main.models import Subreddit, Post, Comment, Notifications

from datetime import timedelta


class IndexListView(generic.ListView):
    model = Post
    template_name = "main/index.html"
    paginate_by = 10
    context_object_name = "posts"
    # default sorting
    sort = "new"

    def get_queryset(self):
        qs = super().get_queryset()
        # .select_related() TO REDUCE THE NUMBER OF QUERIES
        qs = qs.select_related("sub", "creator")
        # .prefetch_related() TO REDUCE THE NUMBER OF QUERIES
        qs = qs.prefetch_related("post_upvote", "post_downvote")
        # .only() TO REDUCE MEMORY CONSUMPTION OF THE QUERY
        qs = qs.only(
            "pk",
            "title",
            "text",
            "image",
            "post_type",
            "created_at",
            "creator__id",
            "creator__username",
            "sub__id",
            "sub__name",
            "sub__image",
        )
        qs = qs.annotate(num_comments=Count("comment", distinct=True))
        # SORTING
        if self.sort == "top":
            timeRange = self.request.GET.get("t", None)
            if timeRange:
                if timeRange == "week":
                    qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=7))
                elif timeRange == "month":
                    qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=30))
                elif timeRange == "year":
                    qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=365))
                elif timeRange == "all":
                    qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=365))
            else:
                # today's case
                qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=1))

            qs = qs.annotate(
                vote=Count("post_upvote", distinct=True)
                - Count("post_downvote", distinct=True)
            ).order_by("-vote")
        else:
            qs = qs.order_by("-created_at")
        return qs

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        user = self.request.user
        # sort context
        context["sorting"] = self.sort
        if self.sort == "top":
            context["top_sort_parameter"] = self.request.GET.get("t", None)
        # sub context
        context["sub_list"] = (
            Subreddit.objects.prefetch_related("members")
            .annotate(num_members=Count("members"))
            .order_by("-num_members")
            .only("name")[:5]
        )
        return context


class SubredditListPage(generic.ListView):
    queryset = Subreddit.objects.annotate(num_members=Count("members")).order_by(
        "-num_members"
    )
    template_name = "main/subredditlist.html"
    paginate_by = 10
    context_object_name = "subs"


class SubredditDetailPage(generic.ListView):
    """DETAIL PAGE FOR SUBREDDIT, BUT CHOOSE ListView TO LIST POSTS"""

    template_name = "main/subredditdetail.html"
    paginate_by = 10
    context_object_name = "posts"

    def get_queryset(self):
        sub = Subreddit.objects.get(name=self.kwargs["name"])
        return (
            sub.posts.select_related("creator")
            .annotate(num_comments=Count("comment"))
            .prefetch_related("post_upvote", "post_downvote")
            .all()
        )

    def get_context_data(self, **kwargs):
        context = super(SubredditDetailPage, self).get_context_data(**kwargs)
        context["subreddit"] = Subreddit.objects.get(name=self.kwargs["name"])
        return context


class PostDetailPage(View):
    def get(self, request, name, pk, *args, **kwargs):
        form = CommentForm()
        user = request.user
        subreddit = Subreddit.objects.get(name=name)
        post = get_object_or_404(subreddit.posts, pk=pk)
        comments = (
            post.comment_set.all()
            .prefetch_related("comment_upvote", "comment_downvote")
            .select_related("commentator")
        )

        context = {
            "subreddit": subreddit,
            "post": post,
            "comments": comments,
            "form": form,
        }
        return render(request, "main/post-detail.html", context)

    def post(self, request, name, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.commentator = request.user
            new_comment.post_id = pk
            new_comment.save()
            return HttpResponseRedirect(reverse("main:post-detail", args=(name, pk)))


# NOTOFICATION VIEWS
class NotificationListPage(generic.ListView):
    template_name = "main/notification-list.html"
    paginate_by = 15
    context_object_name = "nots"

    def get_queryset(self):
        return self.request.user.notofication_to.select_related(
            "post", "comment", "from_user", "post__sub", "comment__post__sub"
        ).order_by("-created_at")


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


# SUBREDDIT SETTINGS
class SubredditSettings(LoginRequiredMixin, View):
    def get(self, request, sub, *args, **kwargs):
        subreddit = Subreddit.objects.get(name=sub)
        form = SubredditUpdateForm()
        context = {"form": form, "sub": subreddit}
        return render(request, "main/subredditsettings.html", context)

    def post(self, request, sub, *args, **kwargs):
        subreddit = Subreddit.objects.get(name=sub)
        form = SubredditUpdateForm(request.POST, request.FILES, instance=subreddit)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes saved")
            return redirect(reverse("main:subreddit-detail", args=[sub]))
        else:
            messages.error(request, "Invalid data.")
            return render(request, "main/subredditsettings.html", {"sub": subreddit})


# delete comment
def DeletePost(request, name, pk):
    user = request.user
    post = Post.objects.get(pk=pk)

    if post.creator.username == user.username:
        post.delete()
    return redirect(reverse("main:subreddit-detail", args=[name]))
