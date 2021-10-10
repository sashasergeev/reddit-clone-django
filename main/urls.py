from django.conf.urls import url
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import (
    IndexListView,
    CreatePost,
    CreatePostIn,
    CreateSubreddit,
    PostCommentReplyNotification,
    CommentNotifications,
    subredditDetailPage,
    PostDetailPage,
    SubredditListPage,
)

from .ajax_views import (
    PostVoteHandle,
    CommentVoteHandle,
    ClearNotifications,
    SubJoin,
    SearchSubreddit,
    DeleteComment,
    DeletePost,
)

app_name = "main"
urlpatterns = [
    # index - subreddit - post
    path("", IndexListView.as_view(), name="index"),
    path("subreddits/", SubredditListPage, name="subreddit-list"),
    path("r/<slug:name>/", subredditDetailPage, name="subreddit-detail"),
    path("r/<slug:name>/<int:pk>/", PostDetailPage, name="post-detail"),
    # create post
    path("create-post/", CreatePost.as_view(), name="create-post"),
    path("r/<slug:name>/create-post/", CreatePostIn.as_view(), name="create-post-in"),
    # create community
    path("subreddits/create", CreateSubreddit.as_view(), name="create-subreddit"),
    # POST upvote / downvote - used with fetch API
    path("post/vote/<int:pk>/<slug:voteType>/", PostVoteHandle, name="post-vote"),
    # COMMENT upvote / downvote - used with fetch API
    path(
        "comment/vote/<int:pk>/<slug:voteType>/", CommentVoteHandle, name="comment-vote"
    ),
    # SEARCH SUBREDDITS - used with fetch API
    path("subreddits/search/", SearchSubreddit, name="Search"),
    # JOIN / LEAVE SUBREDDIT - used with fetch API
    path("join/<int:pk>/", SubJoin, name="sub-join"),
    # delete post
    path("r/<slug:name>/<int:pk>/delete/", DeletePost, name="delete-sub"),
    # delete comment -- used with fetch API
    path("comment/<int:pk>/", DeleteComment, name="delete-comment"),
    # Post Notifications - votes - comments
    path(
        "notifications/<int:notification_pk>/post/<int:post_pk>/",
        PostCommentReplyNotification.as_view(),
        name="post-notification",
    ),
    path(
        "notifications/<int:notification_pk>/comment/<int:comment_pk>/",
        CommentNotifications.as_view(),
        name="comment-notification",
    ),
    path("notifications/clear/", ClearNotifications.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
