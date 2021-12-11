from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from project import views

handler400 = 'views.e400'
handler403 = 'views.e403'
handler404 = 'views.e404'
handler500 = 'views.e500'


api_info = openapi.Info(
    title='DataScience Final Homework API',
    default_version='v1.0',
    description='AskUbuntu Q&A',
    contact=openapi.Contact(email='wizzzet@gmail.com'),
)

schema_view = get_schema_view(
    api_info,
    url=settings.API_BASE_URL,
    validators=['flex'],
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = (
    path(
        'swagger/docs/',
        schema_view.as_view()
    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    )
)

# API urlpatterns
api_urlpatterns = []
for app in settings.API_APPS:
    namespace = app.replace('.', '_')
    api_urlpatterns.append(
        path(
            'api/<str:lang>/%s/' % app,
            include('%s.api.urls' % app, namespace=namespace)
        )
    )
urlpatterns += tuple(api_urlpatterns)

# MEDIA urlpatterns
if settings.DEBUG is True:
    urlpatterns += (
        re_path(
            r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT}
        ),
    )

if getattr(settings, 'ENV', 'production') == 'dev':
    urlpatterns += tuple(staticfiles_urlpatterns())

urlpatterns += (
    path(
        '',
        views.HomeView.as_view(),
        name='home'
    ),
)
