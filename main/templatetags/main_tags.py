from django import template

register = template.Library()

from ..models import Notifications


# CHECK IF POST UPVOTED
@register.filter(name="check_relation_upvote")
def check_relation_upvote(post, user):
    return post.post_upvote.filter(user=user.id).exists()


# CHECK IF POST DOWNVOTED
@register.filter(name="check_relation_downvote")
def check_relation_downvote(post, user):
    return post.post_downvote.filter(user=user.id).exists()


# CHECK IF COMMUNITY IS JOINED
@register.filter(name="check_join")
def check_join(sub, user):
    return user.sub_members.filter(name=sub.name).exists()


# CHECK IF COMMENT UPVOTED
@register.filter(name="check_relation_comm_upvote")
def check_relation_comm_upvote(comment, user):
    return comment.comment_upvote.filter(user=user.id).exists()


# CHECK IF COMMENT DOWNVOTED
@register.filter(name="check_relation_comm_downvote")
def check_relation_comm_downvote(comment, user):
    return comment.comment_downvote.filter(user=user.id).exists()


# NOTIFICATIONS
@register.inclusion_tag("base/show_notifications.html", takes_context=True)
def show_notifications(context):
    request_user = context["request"].user
    notifications = (
        Notifications.objects.filter(to_user=request_user)
        .exclude(user_has_seen=True)
        .order_by("-created_at")
    )
    return {
        "notifications": notifications[:3],
        "notification_count": notifications.count(),
    }
