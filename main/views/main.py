from django.views import generic, View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count

from main.forms import CommentForm, SubredditUpdateForm
from main.models import Subreddit, Post, Comment, Notifications


class IndexListView(generic.ListView):
    model = Post
    template_name = "main/index.html"
    paginate_by = 10
    context_object_name = "posts"

    def get_queryset(self):
        qs = super().get_queryset()
        return (
            # .select_related() TO REDUCE THE NUMBER OF QUERIES
            qs.annotate(num_comments=Count("comment")).select_related("sub", "creator")
            # .only() TO REDUCE MEMORY CONSUMPTION OF THE QUERY
            .only(
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
            # .prefetch_related() TO REDUCE THE NUMBER OF QUERIES
            .prefetch_related("post_upvote", "post_downvote")
        )

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        user = self.request.user
        context["sub_list"] = (
            Subreddit.objects.prefetch_related("members")
            .annotate(num_members=Count("members"))
            .order_by("-num_members")
            .only("name")[:5]
        )
        if user.is_authenticated:
            # DECIDED TO CHECK WHETHER THE USER HAS INTERACTED WITH CONTENT
            # BY MAKING QUERY VALUES, AND NOT USING TEMPLATETAGS TO CHECK RELATIONS
            context["upvoted_posts"] = user.upvote_user_post.values_list(
                "post_id", flat=True
            )
            context["downvoted_posts"] = user.downvote_user_post.values_list(
                "post_id", flat=True
            )
            context["saved_posts"] = user.saved_posts.values_list("id", flat=True)
            context["joined_subs"] = user.sub_members.values_list("id", flat=True)
        return context


class SubredditListPage(generic.ListView):
    queryset = Subreddit.objects.annotate(num_members=Count("members")).order_by(
        "-num_members"
    )
    template_name = "main/subredditlist.html"
    paginate_by = 10
    context_object_name = "subs"

    def get_context_data(self, **kwargs):
        context = super(SubredditListPage, self).get_context_data(**kwargs)
        context["joined_subs"] = self.request.user.sub_members.values_list(
            "id", flat=True
        )
        return context


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
        user = self.request.user
        if user.is_authenticated:
            context["upvoted_posts"] = user.upvote_user_post.values_list(
                "post_id", flat=True
            )
            context["downvoted_posts"] = user.downvote_user_post.values_list(
                "post_id", flat=True
            )
            context["saved_posts"] = user.saved_posts.values_list("id", flat=True)
            context["joined_subs"] = user.sub_members.values_list("id", flat=True)
            context["user"] = user
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

        context = {}
        context["subreddit"] = subreddit
        context["post"] = post
        context["comments"] = comments
        context["form"] = form
        if request.user.is_authenticated:
            context["comment_ups"] = user.upvote_user_comment.values_list(
                "comment_id", flat=True
            )
            context["comment_downs"] = user.downvote_user_comment.values_list(
                "comment_id", flat=True
            )
            context["comment_saved"] = user.saved_comments.values_list("id", flat=True)
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
