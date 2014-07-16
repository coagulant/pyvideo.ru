from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from richard.videos.sitemaps import CategorySitemap, SpeakerSitemap, VideoSitemap
from sergey.views import SpeakerList


admin.autodiscover()

sitemaps = {
    'category': CategorySitemap,
    'speaker': SpeakerSitemap,
    'video': VideoSitemap
}

urlpatterns = patterns('',
    url(r'^$', 'richard.base.views.home', name='home'),
    url(r'^login-failure$', 'richard.base.views.login_failure', name='login_failure'),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('richard.pages.urls')),
    url(r'^speaker/$', SpeakerList.as_view(), name='videos-speaker-list'),
    url(r'', include('richard.videos.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    url(r'^(robots.txt)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^(favicon.ico)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': False,}),
)
