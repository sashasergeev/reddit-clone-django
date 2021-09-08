from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints
from django.db.models.deletion import CASCADE
from django.utils import timezone
import math
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Subreddit(models.Model):
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(User, related_name="sub_members")
    creator = models.ForeignKey(User, related_name="sub_admin", on_delete=CASCADE)
    creation_data = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def members_count(self):
        return self.members.count()

    def get_absolute_url(self):
        return f"/r/{self.name}/"


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subreddit, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.sub}"

    class Meta:
        ordering = ["-created_at"]

    def comment_count(self):
        return self.comment_set.count()

    def votes_count(self):
        upvotes = self.post_upvote.count()
        downvotes = self.post_downvote.count()
        return upvotes - downvotes

    def children(self):
        children_comms = self.comment_set.filter(parent=None)
        children_comms = children_comms.get_descendants(include_self=True)
        return children_comms

    def get_absolute_url(self):
        return f"/r/{self.sub.name}/{self.id}/"

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + " second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Comment(MPTTModel):
    text = models.TextField()
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["commented_at"]

    def __str__(self):
        return f"{self.post} - {self.commentator}"

    def votes_count(self):
        upvotes = self.comment_upvote.count()
        downvotes = self.comment_downvote.count()
        return upvotes - downvotes

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.commented_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + " second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class PostsUpVotes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_upvote")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="upvote_user_post"
    )

    class Meta:
        verbose_name_plural = "Post Upvotes"
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_post_upvote")
        ]

    def __str__(self):
        return f"{self.post} upvoted by {self.user.username}"


class PostsDownVotes(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_downvote"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="downvote_user_post"
    )

    class Meta:
        verbose_name_plural = "Post Downvotes"
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"], name="unique_post_downvote"
            )
        ]

    def __str__(self):
        return f"{self.post} downvoted by {self.user.username}"


class CommentUpVote(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_upvote"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="upvote_user_comment"
    )

    class Meta:
        verbose_name_plural = "Comment Upvotes"
        constraints = [
            models.UniqueConstraint(
                fields=["comment", "user"], name="unique_comment_upvote"
            )
        ]

    def __str__(self):
        return f"{self.comment} upvoted by {self.user.username}"


class CommentDownVote(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_downvote"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="downvote_user_comment"
    )

    class Meta:
        verbose_name_plural = "Comment Downvotes"
        constraints = [
            models.UniqueConstraint(
                fields=["comment", "user"], name="unique_comment_downvote"
            )
        ]

    def __str__(self):
        return f"{self.comment} downvoted by {self.user.username}"