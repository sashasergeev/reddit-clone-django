from django.contrib import admin
from .models import (
    CommentDownVote,
    CommentUpVote,
    Subreddit,
    Post,
    Comment,
    PostsUpVotes,
    PostsDownVotes,
    Notifications,
)

# Register your models here.

admin.site.register(Subreddit)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostsUpVotes)
admin.site.register(PostsDownVotes)
admin.site.register(CommentUpVote)
admin.site.register(CommentDownVote)
admin.site.register(Notifications)
