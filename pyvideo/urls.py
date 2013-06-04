from django.conf.urls import patterns, url
from django.conf import settings

from richard.urls import urlpatterns


urlpatterns += patterns('',
    url(r'^(robots.txt)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^(favicon.ico)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': False,}),
)