from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import CommentDownVote, CommentUpVote, Subreddit, Post, PostsUpVotes, PostsDownVotes, Comment
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import CommentForm

# Create your views here.


class IndexListView(generic.ListView):
    model = Post
    template_name = "main/index.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        context["sub_list"] = Subreddit.objects.order_by("name")[:5]
        return context


def subredditDetailPage(request, name):
    subreddit = Subreddit.objects.get(name=name)
    posts = subreddit.posts.all()

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

    # generic page rendering
    subreddit = Subreddit.objects.get(name=name)
    post = get_object_or_404(subreddit.posts, pk=pk)

    context = {"subreddit": subreddit, "post": post, "form": form}

    return render(request, "main/post-detail.html", context)


# POST VOTES
def PostUpvoteHandle(request, pk):
    # obtaining needed data
    post = Post.objects.get(pk=pk)
    user = request.user
    response = {"action": "post upvoted", "downvote_existed": False}

    # auth check
    if not user.is_authenticated:
        return redirect("accounts:login")

    # checks if upvote exists, if so, deletes it
    upvote = PostsUpVotes.objects.filter(post=post, user=user)
    if upvote.exists():
        upvote.delete()
        response["action"] = "post upvote unvoted"
        return JsonResponse(response)

    # checks if downvote on an object exists, if exists deletes it
    downvote = PostsDownVotes.objects.filter(post=post, user=user)
    if downvote.exists():
        downvote.delete()
        response["downvote_existed"] = True

    # creates upvote
    if request.method == "POST":
        PostsUpVotes.objects.create(post=post, user=user)
    return JsonResponse(response)


def PostDownvoteHandle(request, pk):
    # obtaining needed data
    post = Post.objects.get(pk=pk)
    user = request.user
    response = {"action": "post downvoted", "upvote_existed": False}

    # auth check
    if not user.is_authenticated:
        return redirect("accounts:login")

    # checks if downvote exists, if so, deletes it
    downvote = PostsDownVotes.objects.filter(post=post, user=user)
    if downvote.exists():
        downvote.delete()
        response["action"] = "post downvote unvoted"
        return JsonResponse(response)

    # checks if upvote on an object exists, if exists deletes it
    upvote = PostsUpVotes.objects.filter(post=post, user=user)
    if upvote.exists():
        upvote.delete()
        response["upvote_existed"] = True

    # creates downvote
    if request.method == "POST":
        PostsDownVotes.objects.create(post=post, user=user)
    return JsonResponse(response)


def CommentUpvoteHandle(request, pk):
    # obtaining needed data
    comment = Comment.objects.get(pk=pk)
    user = request.user
    response = {"action": "comment upvoted", "downvote_existed": False}

    # auth check
    if not user.is_authenticated:
        return redirect("accounts:login")

    # checks if upvote on an object exists, if exists deletes it
    upvote = CommentUpVote.objects.filter(comment=comment, user=user)
    if upvote.exists():
        upvote.delete()
        response["action"] = "comment upvote unvoted"
        return JsonResponse(response)

    # checks if downvote exists, if so, deletes it
    downvote = CommentDownVote.objects.filter(comment=comment, user=user)
    if downvote.exists():
        downvote.delete()
        response["downvote_existed"] = True

    # creates upvote
    if request.method == "POST":
        CommentUpVote.objects.create(comment=comment, user=user)
    return JsonResponse(response)


def CommentDownvoteHandle(request, pk):
    # obtaining needed data
    comment = Comment.objects.get(pk=pk)
    user = request.user
    response = {"action": "comment downvoted", "upvote_existed": False}

    # auth check
    if not user.is_authenticated:
        return redirect("accounts:login")
    
    # checks if downvote exists, if so, deletes it
    downvote = CommentDownVote.objects.filter(comment=comment, user=user)
    if downvote.exists():
        downvote.delete()
        response["action"] = "comment downvote unvoted"
        return JsonResponse(response)

    # checks if upvote on an object exists, if exists deletes it
    upvote = CommentUpVote.objects.filter(comment=comment, user=user)
    if upvote.exists():
        upvote.delete()
        response["upvote_existed"] = True

    # creates downvote
    if request.method == "POST":
        CommentDownVote.objects.create(comment=comment, user=user)
    return JsonResponse(response)


# JOIN / LEAVE SUBREDDIT
def SubJoin(request, pk):
    # obtaining needed data
    sub = Subreddit.objects.get(pk=pk)
    user = request.user
    response = {"action": "joined"}

    # auth check
    if not user.is_authenticated:
        return redirect("accounts:login")

    # checks if sub joined, if so, deletes it
    is_joined = user.sub_members.filter(name=sub.name)
    if is_joined.exists():
        sub.members.remove(user)
        response["action"] = "left"
        return JsonResponse(response)

    # joins subreddit
    user.sub_members.add(sub)
    return JsonResponse(response)


# CREATE POST
class CreatePost(LoginRequiredMixin, generic.edit.CreateView):
    login_url = "/accounts/login/"
    model = Post
    fields = ["sub", "title", "text"]
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
        form.fields["title"].widget.attrs = {
            "placeholder": "Title",
            "class": "form_inputs",
        }
        form.fields["text"].widget.attrs = {
            "placeholder": "Text",
            "class": "form_inputs",
        }
        return form

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context["form"].fields["sub"].empty_label = "Choose a community"
        return context


# CREATE POST IN A CURRENT COMMUNITY
class CreatePostIn(LoginRequiredMixin, generic.edit.CreateView):
    login_url = "/accounts/login/"
    model = Post
    fields = ["title", "text"]
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
        return form

    def get_context_data(self, **kwargs):
        context = super(CreatePostIn, self).get_context_data(**kwargs)
        context["subreddit"] = Subreddit.objects.get(name=self.kwargs["name"])
        return context


# CREATE SUBREDDIT
class CreateSubreddit(LoginRequiredMixin, generic.edit.CreateView):
    login_url = "/accounts/login/"
    model = Subreddit
    fields = ["name", "description"]
    template_name = "main/create-subreddit.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.creator = user
        return super(CreateSubreddit, self).form_valid(form)


# delete comment
def DeleteComment(request, pk):
    # obtaining needed data
    comment = Comment.objects.get(pk=pk)
    user = request.user

    # auth check
    if not user.is_authenticated:
        return JsonResponse({"action": "auth"})

    # check if this comment is done by the same user
    if not comment.commentator == user:
        return JsonResponse({"action": "user error"})

    # deleting comment
    if request.method == "POST":
        comment.delete()
    return JsonResponse({"action": "deleted"})