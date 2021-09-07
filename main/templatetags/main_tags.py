from django import template

register = template.Library()

from ..models import PostsUpVotes, PostsDownVotes, CommentUpVote, CommentDownVote


# CHECK IF USER UPVOTED
@register.filter(name="check_relation_upvote")
def check_relation_upvote(post, user):
    return post.post_upvote.filter(user=user.id).exists()


# CHECK IF USER DOWNVOTED
@register.filter(name="check_relation_downvote")
def check_relation_downvote(post, user):
    return post.post_downvote.filter(user=user.id).exists()


# CHECK IF COMMENTT IS DONE BY CURRENT USER
@register.filter(name="is_comment")
def is_comment(comment, user):
    return user.comment_set.filter(pk=comment.id).exists()


# CHECK IF COMMUNITY IS JOINED
@register.filter(name="check_join")
def check_join(sub, user):
    return user.sub_members.filter(name=sub.name).exists()


# CHECK IF POST UPVOTED
@register.filter(name="check_relation_comm_upvote")
def check_relation_comm_upvote(comment, user):
    return comment.comment_upvote.filter(user=user.id).exists()


# CHECK IF POST DOWNVOTED
@register.filter(name="check_relation_comm_downvote")
def check_relation_comm_downvote(comment, user):
    return comment.comment_downvote.filter(user=user.id).exists()
