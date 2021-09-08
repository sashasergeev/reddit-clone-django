from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from django.contrib.auth.models import User
from .models import Profile
from main.models import PostsUpVotes, PostsDownVotes, CommentUpVote, CommentDownVote


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=PostsUpVotes)
@receiver(post_save, sender=PostsDownVotes)
@receiver(post_save, sender=CommentUpVote)
@receiver(post_save, sender=CommentDownVote)
def karma_post_upvote_add(sender, instance, created, **kwargs):
    if isinstance(instance, PostsUpVotes) or isinstance(instance, PostsDownVotes):
        if instance.user == instance.post.creator:
            return
        profile = instance.post.creator.profile
    else:
        if instance.user == instance.comment.commentator:
            return
        profile = instance.comment.commentator.profile

    if isinstance(instance, PostsUpVotes):
        profile.karma += 1
        profile.save()
    elif isinstance(instance, CommentUpVote):
        profile.karma += 1
        profile.save()
    elif isinstance(instance, PostsDownVotes):
        profile.karma -= 1
        profile.save()
    elif isinstance(instance, CommentDownVote):
        profile.karma -= 1
        profile.save()


@receiver(post_delete, sender=PostsUpVotes)
@receiver(post_delete, sender=PostsDownVotes)
@receiver(post_delete, sender=CommentUpVote)
@receiver(post_delete, sender=CommentDownVote)
def karma_post_upvote_delete(sender, instance, **kwargs):
    if isinstance(instance, PostsUpVotes) or isinstance(instance, PostsDownVotes):
        if instance.user == instance.post.creator:
            return
        profile = instance.post.creator.profile
    else:
        if instance.user == instance.comment.commentator:
            return
        profile = instance.comment.commentator.profile

    if isinstance(instance, PostsUpVotes):
        profile.karma -= 1
        profile.save()
    elif isinstance(instance, CommentUpVote):
        profile.karma -= 1
        profile.save()
    elif isinstance(instance, PostsDownVotes):
        profile.karma += 1
        profile.save()
    elif isinstance(instance, CommentDownVote):
        profile.karma += 1
        profile.save()
