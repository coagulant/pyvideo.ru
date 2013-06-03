# Django settings for production instance of pyvideo.ru
from .settings import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')