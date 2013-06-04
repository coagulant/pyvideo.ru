# Django settings for production instance of pyvideo.ru
import os
from .settings import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ.get('BONSAI_URL'),
        'INDEX_NAME': 'pyvideo',
    },
}