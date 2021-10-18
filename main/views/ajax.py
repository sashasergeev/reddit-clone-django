from django.http.response import JsonResponse
from django.db.models import Count

import json
from main.decorators import ajaxAuthCheck
from main.models import (
    CommentDownVote,
    CommentUpVote,
    Subreddit,
    Post,
    PostsUpVotes,
    PostsDownVotes,
    Comment,
    Notifications,
)


def ClearNotifications(request):
    notifications = Notifications.objects.filter(to_user=request.user)
    for n in notifications:
        n.user_has_seen = True
        n.save()
    return JsonResponse({"Status": "Removed"})


# POST VOTES - JavaScript
@ajaxAuthCheck
def PostVoteHandle(request, pk, voteType):
    post = Post.objects.get(pk=pk)
    user = request.user

    upvote = PostsUpVotes.objects.filter(post=post, user=user)
    downvote = PostsDownVotes.objects.filter(post=post, user=user)

    if voteType == "upvote":
        response = {"action": "post upvoted", "downvote_existed": False}
        if upvote.exists():
            upvote.delete()
            response["action"] = "post upvote unvoted"
            return JsonResponse(response)
        elif downvote.exists():
            downvote.delete()
            response["downvote_existed"] = True
        PostsUpVotes.objects.create(post=post, user=user)
    elif voteType == "downvote":
        response = {"action": "post downvoted", "upvote_existed": False}
        if downvote.exists():
            downvote.delete()
            response["action"] = "post downvote unvoted"
            return JsonResponse(response)
        if upvote.exists():
            upvote.delete()
            response["upvote_existed"] = True
        PostsDownVotes.objects.create(post=post, user=user)
    return JsonResponse(response)


# COMMENT VOTES - JavaScript
@ajaxAuthCheck
def CommentVoteHandle(request, pk, voteType):
    comment = Comment.objects.get(pk=pk)
    user = request.user

    upvote = CommentUpVote.objects.filter(comment=comment, user=user)
    downvote = CommentDownVote.objects.filter(comment=comment, user=user)

    if voteType == "upvote":
        response = {"action": "comment upvoted", "downvote_existed": False}
        if upvote.exists():
            upvote.delete()
            response["action"] = "comment upvote unvoted"
            return JsonResponse(response)
        if downvote.exists():
            downvote.delete()
            response["downvote_existed"] = True
        CommentUpVote.objects.create(comment=comment, user=user)
        return JsonResponse(response)
    elif voteType == "downvote":
        response = {"action": "comment downvoted", "upvote_existed": False}
        if downvote.exists():
            downvote.delete()
            response["action"] = "comment downvote unvoted"
            return JsonResponse(response)
        if upvote.exists():
            upvote.delete()
            response["upvote_existed"] = True
        CommentDownVote.objects.create(comment=comment, user=user)
        return JsonResponse(response)


# JOIN / LEAVE SUBREDDIT - JavaScript
@ajaxAuthCheck
def SubJoin(request, pk):
    # obtaining needed data
    sub = Subreddit.objects.get(pk=pk)
    user = request.user
    response = {"action": "joined"}

    # checks if sub joined, if so, deletes it
    is_joined = user.sub_members.filter(name=sub.name)
    if is_joined.exists():
        sub.members.remove(user)
        response["action"] = "left"
        return JsonResponse(response)

    # joins subreddit
    user.sub_members.add(sub)
    return JsonResponse(response)


# delete comment - JavaScript
@ajaxAuthCheck
def DeleteComment(request, pk):
    # obtaining needed data
    comment = Comment.objects.get(pk=pk)
    user = request.user

    # check if this comment is done by the same user
    if not comment.commentator == user:
        return JsonResponse({"action": "user error"})

    # deleting comment
    comment.delete()
    return JsonResponse({"action": "deleted"})


# live search subreddits - JavaScript
def SearchSubreddit(request):
    res = "No subreddits found..."

    data = json.load(request)
    query = data.get("query")
    if len(query) > 0:
        qs = (
            Subreddit.objects.filter(name__icontains=query)
            .annotate(num_members=Count("members"))
            .order_by("-num_members")
        )[:5]
        if len(qs) > 0:
            data = []
            for pos in qs:
                item = {
                    "pk": pos.pk,
                    "name": pos.name,
                    "img": pos.image.url,
                    "num_members": pos.num_members,
                }
                data.append(item)
            res = data
    return JsonResponse({"data": res})


@ajaxAuthCheck
def SavePostOrComment(request, oType, pk):
    user = request.user
    response = {"action": "saved"}

    if oType == "post":
        post = Post.objects.get(pk=pk)
        is_saved = user.saved_posts.filter(pk=pk)
        if is_saved.exists():
            post.saved_by.remove(user)
            response["action"] = "unsaved"
        else:
            post.saved_by.add(user)
    elif oType == "comment":
        comment = Comment.objects.get(pk=pk)
        is_saved = user.saved_comments.filter(pk=pk)
        if is_saved.exists():
            comment.saved_by.remove(user)
            response["action"] = "unsaved"
        else:
            comment.saved_by.add(user)
    return JsonResponse(response)
