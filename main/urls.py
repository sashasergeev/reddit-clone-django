from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import (
    IndexListView,
    CreatePost,
    CreatePostIn,
    CreateSubreddit,
    NotificationListPage,
    PostCommentReplyNotification,
    CommentNotifications,
    SubredditDetailPage,
    SubredditSettings,
    PostDetailPage,
    SubredditListPage,
    Search,
    DeletePost,
)

from .ajax_views import (
    PostVoteHandle,
    CommentVoteHandle,
    ClearNotifications,
    SavePostOrComment,
    SubJoin,
    SearchSubreddit,
    DeleteComment,
)

app_name = "main"
urlpatterns = [
    # index - subreddit - post
    path("", IndexListView.as_view(), name="index"),
    path("subreddits/", SubredditListPage.as_view(), name="subreddit-list"),
    path("r/<slug:name>/", SubredditDetailPage.as_view(), name="subreddit-detail"),
    path("r/<slug:name>/<int:pk>/", PostDetailPage.as_view(), name="post-detail"),
    # create post
    path("create-post/", CreatePost.as_view(), name="create-post"),
    path("r/<slug:name>/create-post/", CreatePostIn.as_view(), name="create-post-in"),
    # create community
    path("subreddits/create", CreateSubreddit.as_view(), name="create-subreddit"),
    # Community settings
    path(
        "r/<slug:sub>/settings/", SubredditSettings.as_view(), name="subreddit-settings"
    ),
    # FULL BLOWN NOTIFICATIONS
    path("notifications/", NotificationListPage.as_view(), name="notification-list"),
    # NAVBAR Notifications - votes - comments
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
    # SEARCH
    path("search/", Search, name="Search"),
    # DELETE POST
    path("r/<slug:name>/<int:pk>/delete/", DeletePost, name="delete-post"),
    ## AJAX URLS
    path("save/<slug:oType>/<int:pk>/", SavePostOrComment),
    # POST - COMMENT upvote / downvote - used with fetch API
    path("post/vote/<int:pk>/<slug:voteType>/", PostVoteHandle),
    path("comment/vote/<int:pk>/<slug:voteType>/", CommentVoteHandle),
    # LIVE SEARCH SUBREDDITS - used with fetch API
    path("subreddits/live-search/", SearchSubreddit),
    # JOIN / LEAVE SUBREDDIT - used with fetch API
    path("join/<int:pk>/", SubJoin),
    # delete comment -- used with fetch API
    path("comment/<int:pk>/", DeleteComment),
    # clear notifications
    path("notifications/clear/", ClearNotifications),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
