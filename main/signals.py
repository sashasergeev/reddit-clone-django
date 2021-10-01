from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from django.contrib.auth.models import User
from .models import (
    Comment,
    Notifications,
    PostsUpVotes,
    PostsDownVotes,
    CommentUpVote,
    CommentDownVote,
)


@receiver(post_save, sender=Comment)
def create_post_comment_orreply_notification(sender, instance, created, **kwargs):
    if instance.commentator != instance.post.creator and instance.parent is None:
        # Post comment notification
        Notifications.objects.create(
            notification_type=3,
            from_user=instance.commentator,
            to_user=instance.post.creator,
            post=instance.post,
        )
    elif instance.parent and instance.commentator != instance.parent.commentator:
        # Comment reply notification
        Notifications.objects.create(
            notification_type=3,
            from_user=instance.commentator,
            to_user=instance.parent.commentator,
            comment=instance,
        )


# LOGIC ON VOTES NOTIFICATIONS:
# if user already voted on this post, comment - notification doesn't count


@receiver(post_save, sender=PostsUpVotes)
@receiver(post_save, sender=CommentUpVote)
@receiver(post_save, sender=PostsDownVotes)
@receiver(post_save, sender=CommentDownVote)
def create_post_vote_notification(sender, instance, created, **kwargs):

    if isinstance(instance, PostsUpVotes) or isinstance(instance, PostsDownVotes):
        if not Notifications.objects.filter(
            notification_type=1 or 2, from_user=instance.user, post=instance.post
        ).exists():
            if instance.user != instance.post.creator:
                if isinstance(instance, PostsUpVotes):
                    Notifications.objects.create(
                        notification_type=1,
                        from_user=instance.user,
                        to_user=instance.post.creator,
                        post=instance.post,
                    )
                else:
                    Notifications.objects.create(
                        notification_type=2,
                        from_user=instance.user,
                        to_user=instance.post.creator,
                        post=instance.post,
                    )
    else:
        if not Notifications.objects.filter(
            notification_type=1 or 2, from_user=instance.user, comment=instance.comment
        ).exists():
            if instance.user != instance.comment.commentator:
                if isinstance(instance, CommentUpVote):
                    Notifications.objects.create(
                        notification_type=1,
                        from_user=instance.user,
                        to_user=instance.comment.commentator,
                        comment=instance.comment,
                    )
                else:
                    Notifications.objects.create(
                        notification_type=2,
                        from_user=instance.user,
                        to_user=instance.comment.commentator,
                        comment=instance.comment,
                    )
