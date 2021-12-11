from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.views import View
from rest_framework.decorators import api_view

from snippets.http.response import error_response


@api_view()
def e400(request, exception=None, *args, **kwargs):
    return error_response(status=400)


@api_view()
def e403(request, exception=None, *args, **kwargs):
    return error_response(status=403)


@api_view()
def e404(request, exception=None, *args, **kwargs):
    return error_response(status=404)


def e500(request, *args, **kwargs):
    return error_response(status=500, only_json=True)


class HomeView(View):
    @staticmethod
    def get(request, **kwargs):
        return HttpResponseRedirect('/swagger')


class CacheClearView(View):
    @staticmethod
    def post(request, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, 'Доступ запрещен')
            return HttpResponseRedirect('/')

        cache.clear()
        messages.success(request, 'Кэш очищен')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
