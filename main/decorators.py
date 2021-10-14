from functools import wraps
from django.http.response import JsonResponse


def ajaxAuthCheck(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "unauth"})

    return wrap
