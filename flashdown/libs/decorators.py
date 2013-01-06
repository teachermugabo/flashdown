from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse

from functools import wraps


class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')


def ajax_request(func):
    """
    If view returned serializable dict, returns JsonResponse with this dict as content.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, dict):
            return JsonResponse(response)
        else:
            return response
    return wrapper


def login_required(func, login_url, append=''):
    """
    Require user authentication. If unauthenticated, redirect to the login page and
    show the login forms.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            request.session['lform_errors'] = ['You need to sign in to do that.']
            return HttpResponseRedirect(reverse(login_url) + append)
        return func(request, *args, **kwargs)

    return wrapper


