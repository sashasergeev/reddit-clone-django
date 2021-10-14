from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from django.core.files.storage import default_storage as storage
from PIL import Image
import math
from io import BytesIO


# FUNCTIONS AND MIXINS
def upload_image_rename(instance, filename):
    print(filename)
    filebase, extenstion = filename.rsplit(".", 1)
    return "images/subreddit/%s.%s" % (instance.name, extenstion)


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

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


# MODELS
class Subreddit(models.Model):
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(User, related_name="sub_members")
    creator = models.ForeignKey(
        User, related_name="sub_admin", on_delete=models.CASCADE
    )
    creation_data = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to="images/subreddit/",
        default="images/subreddit/default.png",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def members_count(self):
        return self.members.count()

    def get_absolute_url(self):
        return f"/r/{self.name}/"

    def save(self):
        super().save()
        memfile = BytesIO()
        img = Image.open(self.image)
        if img.height > 250 or img.width > 250:
            new_img = (250, 250)
            img.thumbnail(new_img, Image.ANTIALIAS)
            img.save(memfile, "png", quality=80)
            storage.save(self.image.name, memfile)
            memfile.close()
            img.close()


class Post(TimeStampMixin):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subreddit, related_name="posts", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/post/", null=True, blank=True)
    saved_by = models.ManyToManyField(User, related_name="saved_posts")

    # CHOICES FOR POST TYPE
    class PostType(models.TextChoices):
        TEXT_POST = "TP", _("Text")
        IMAGE_POST = "IP", _("Image")

    post_type = models.CharField(
        max_length=2, choices=PostType.choices, default=PostType.TEXT_POST
    )

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

    def get_absolute_url(self):
        return f"/r/{self.sub.name}/{self.id}/"


class Comment(MPTTModel, TimeStampMixin):
    text = models.TextField()
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    saved_by = models.ManyToManyField(User, related_name="saved_comments")

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    def __str__(self):
        return f"{self.post} - {self.commentator}"

    def votes_count(self):
        upvotes = self.comment_upvote.count()
        downvotes = self.comment_downvote.count()
        return upvotes - downvotes


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


class Notifications(TimeStampMixin):
    # 1 = like 2 = dislike, 3 = post comment - reply
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(
        User, related_name="notofication_to", on_delete=models.CASCADE, null=True
    )
    from_user = models.ForeignKey(
        User, related_name="notofication_from", on_delete=models.CASCADE, null=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True
    )
    user_has_seen = models.BooleanField(default=False)
