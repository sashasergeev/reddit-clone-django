from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Count

from main.models import Subreddit, Post

# LIVE SEARCH VIEW IS LOCATED IN .ajax

# FUNCTIONS TO GET QUERIES
def subsQuery(query, current):
    if current is None:
        return (
            Subreddit.objects.filter(name__icontains=query)
            .annotate(num_members=Count("members"))
            .order_by("-num_members")[:3]
        )
    else:
        return (
            Subreddit.objects.filter(name__icontains=query)
            .annotate(num_members=Count("members"))
            .order_by("-num_members")
        )


def usersQuery(query, current):
    if current is None:
        return User.objects.filter(username__icontains=query).prefetch_related(
            "profile"
        )[:3]
    else:
        return User.objects.filter(username__icontains=query).prefetch_related(
            "profile"
        )


def postsQuery(query):
    return (
        Post.objects.filter(title__icontains=query)
        .annotate(num_comments=Count("comment"))
        .select_related("creator", "sub")
        .prefetch_related("post_upvote", "post_downvote")
    )


def pagination(request, pagObj, pagNum=10):
    paginator = Paginator(pagObj, pagNum)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


# FUNCTIONS FOR GETTING CONTEXT
# SEARCH PAGE WHERE USER CAN SEE QUERY RESULTS ON COMMUNITIES, USERS, POSTS
def overviewContext(request, query, current=None):
    subs = subsQuery(query, current)
    users = usersQuery(query, current)
    posts = postsQuery(query)
    page_obj = pagination(request, posts)
    context = {
        "subs": subs,
        "users": users,
        "page_obj": page_obj,
        "searchQ": query,
        "current": None,
    }
    return context


# PAGE WITH POST RESULTS
def postsContext(request, query, current):
    posts = postsQuery(query)
    page_obj = pagination(request, posts)
    context = {
        "page_obj": page_obj,
        "searchQ": query,
        "current": current,
    }
    return context


# PAGE WITH SUB RESULTS
def subsContext(request, query, current):
    subs = subsQuery(query, current)
    page_obj = pagination(request, subs)
    context = {
        "subs": page_obj,
        "searchQ": query,
        "current": current,
    }
    return context


# PAGE WITH USER RESULTS
def usersContext(request, query, current):
    users = usersQuery(query, current)
    page_obj = pagination(request, users)
    context = {
        "users": page_obj,
        "searchQ": query,
        "current": current,
    }
    return context


# MAIN VIEW
def Search(request):
    query = request.GET.get("q")
    current = request.GET.get("subpage")
    user = request.user

    if current is None:
        context = overviewContext(request, query)
    elif current == "posts":
        context = postsContext(request, query, current)
    elif current == "subs":
        context = subsContext(request, query, current)
    elif current == "users":
        context = usersContext(request, query, current)

    if user.is_authenticated:
        context["upvoted_posts"] = user.upvote_user_post.values_list(
            "post_id", flat=True
        )
        context["downvoted_posts"] = user.downvote_user_post.values_list(
            "post_id", flat=True
        )
        context["saved_posts"] = user.saved_posts.values_list("id", flat=True)
        context["joined_subs"] = user.sub_members.values_list("id", flat=True)

    return render(request, "main/search.html", context)
