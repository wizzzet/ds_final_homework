from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from snippets.api.swagger.schema import SimpleAutoSchema


class PublicViewMixin(object):
    permission_classes = (AllowAny,)


class BaseAPIViewMixin(object):
    swagger_schema = SimpleAutoSchema


class PublicAPIViewMixin(PublicViewMixin, BaseAPIViewMixin):
    pass


class BaseListAPIView(ListAPIView):

    @method_decorator(cache_page(60 * 2))
    def get(self, request, *args, **kwargs):
        return super(BaseListAPIView, self).get(request, *args, **kwargs)


class BaseRetrieveAPIView(RetrieveAPIView):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class PageRetrieveAPIView(RetrieveAPIView):
    """
    Позволяет получать объекты "страниц"
    """

    @method_decorator(cache_page(60 * 2))
    def get(self, request, *args, **kwargs):
        return super(PageRetrieveAPIView, self).get(request, *args, **kwargs)

    def get_object(self):
        return self.queryset.model.get_solo()


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 200
    limit_query_param = 'limit'
    offset_query_param = 'offset'


class PaginationMixin:
    pagination_class = CustomLimitOffsetPagination
