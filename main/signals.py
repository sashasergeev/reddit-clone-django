from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from django.contrib.auth.models import User
from .models import Comment, Notifications


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
