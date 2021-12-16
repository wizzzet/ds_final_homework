from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.static import serve

from project.views import CacheClearView

admin.autodiscover()

urlpatterns = tuple()

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
    path('', admin.site.urls),
    path(
        'cache/clear/',
        CacheClearView.as_view(),
        name='cache_clear'
    )
)
