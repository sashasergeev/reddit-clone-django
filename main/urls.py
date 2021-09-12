from django.conf.urls import url
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import (
    IndexListView,
    CreatePost,
    CreatePostIn,
    CreateSubreddit,
    subredditDetailPage,
    SubJoin,
    PostDetailPage,
    PostUpvoteHandle,
    PostDownvoteHandle,
    CommentUpvoteHandle,
    CommentDownvoteHandle,
    DeletePost,
    DeleteComment,
)

app_name = "main"
urlpatterns = [
    # index - subreddit - post
    path("", IndexListView.as_view(), name="index"),
    path("r/<slug:name>/", subredditDetailPage, name="subreddit-detail"),
    path("r/<slug:name>/<int:pk>/", PostDetailPage, name="post-detail"),
    # create post
    path("create-post/", CreatePost.as_view(), name="create-post"),
    path("r/<slug:name>/create-post/", CreatePostIn.as_view(), name="create-post-in"),
    # create community
    path("subreddits/create", CreateSubreddit.as_view(), name="create-subreddit"),
    # POST upvote / downvote - used with fetch API
    path("vote/<int:pk>/", PostUpvoteHandle, name="upvote-post"),
    path("downvote/<int:pk>/", PostDownvoteHandle, name="downvote-post"),
    # COMMENT upvote / downvote - used with fetch API
    path("comment-vote/<int:pk>/", CommentUpvoteHandle, name="upvote-comment"),
    path("comment-downvote/<int:pk>/", CommentDownvoteHandle, name="downvote-comment"),
    # JOIN / LEAVE SUBREDDIT - used with fetch API
    path("join/<int:pk>/", SubJoin, name="sub-join"),
    # delete post
    path("r/<slug:name>/<int:pk>/delete/", DeletePost, name="delete-sub"),
    # delete comment -- used with fetch API
    path("comment/<int:pk>/", DeleteComment, name="delete-comment"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
