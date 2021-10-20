def user_activity_context(request):
    context = {}
    if request.user.is_authenticated:
        context["upvoted_posts"] = request.user.upvote_user_post.values_list(
            "post_id", flat=True
        )
        context["downvoted_posts"] = request.user.downvote_user_post.values_list(
            "post_id", flat=True
        )
        context["saved_posts"] = request.user.saved_posts.values_list("id", flat=True)
        context["joined_subs"] = request.user.sub_members.values_list("id", flat=True)
        context["comment_saved"] = request.user.saved_comments.values_list(
            "id", flat=True
        )
        context["comment_ups"] = request.user.upvote_user_comment.values_list(
            "comment_id", flat=True
        )
        context["comment_downs"] = request.user.downvote_user_comment.values_list(
            "comment_id", flat=True
        )
        return context
    return context
