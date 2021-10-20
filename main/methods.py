from django.utils import timezone
from datetime import timedelta
from django.db.models import Count


def topFilterRange(request, qs):
    timeRange = request.GET.get("t", None)
    if timeRange:
        if timeRange == "week":
            qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=7))
        elif timeRange == "month":
            qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=30))
        elif timeRange == "year":
            qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=365))
        elif timeRange == "all":
            qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=365))
    else:
        # today's case
        qs = qs.filter(created_at__gte=timezone.now() - timedelta(days=1))
    return qs


# TOP sorting posts
def topSorting(request, qs):
    qs = topFilterRange(request, qs)
    qs = qs.annotate(
        vote=Count("post_upvote", distinct=True) - Count("post_downvote", distinct=True)
    ).order_by("-vote")
    return qs


# TOP sorting comments
def topCommentSorting(request, qs):
    qs = topFilterRange(request, qs)
    qs = qs.annotate(
        vote=Count("comment_upvote", distinct=True)
        - Count("comment_downvote", distinct=True)
    ).order_by("-vote")
    return qs
