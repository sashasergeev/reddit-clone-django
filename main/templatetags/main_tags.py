from django import template

register = template.Library()

from ..models import Notifications, Comment, Post

## OPTIMIZATION ISSUE with using templatetags for checking relation:
## it creates new queryset, therefore it makes .prefetch_related() on its view useless

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


# CHECK IF OBJECT IS SAVED
@register.filter(name="is_saved")
def is_saved(feedObj, user):
    if isinstance(feedObj, Post):
        return feedObj.saved_by.filter(username=user.username).exists()
    else:
        return feedObj.saved_by.filter(pk=feedObj.pk).exists()


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
        # .select_related() TO REDUCE THE NUMBER OF QUERIES
        .select_related("from_user", "post__sub", "comment__post__sub")
        # .only() TO REDUCE MEMORY CONSUMPTION OF THE QUERY
        .only(
            "pk",
            "notification_type",
            "from_user__username",
            "created_at",
            "to_user__username",
            # POST NOTIF
            "post__id",
            "post__title",
            "post__sub__name",
            # COMMENT NOTIF
            "comment__post__sub__name",
            "comment__text",
        )
    )
    return {
        "notification_count": notifications.count(),
        "notifications": notifications[:3],
    }
