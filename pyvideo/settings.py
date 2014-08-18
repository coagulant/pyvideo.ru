# Django settings for pyvideo project.
import os
from richard.settings import *

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ALLOWED_HOSTS = ['pyvideo.ru', 'www.pyvideo.ru', 'pyvideoru.herokuapp.com', '127.0.0.1',]
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
SECRET_KEY = 'this_is_not_production_so_who_cares'
SITE_TITLE = 'pyvideo.ru'

ROOT_URLCONF = 'pyvideo.urls'
WSGI_APPLICATION = 'pyvideo.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)
STATIC_ROOT = os.path.join(PROJECT_PATH, '../sergey/static')

INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
    'suit',
    'sergey',
    'proposal',
    # exclude unwanted richard apps
) + tuple(app for app in INSTALLED_APPS if app not in ('grappelli', 'django_browserid',))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
    }
}

TEMPLATE_CONTEXT_PROCESSORS += (
    'sergey.context.humor',
)

API = True
SUIT_CONFIG = {
    'LIST_PER_PAGE': 100
}
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/admin/'
ENABLE_METRICS = False

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        # the json, yaml, xml parses are used for parsing video proposals
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.XMLParser',
        'rest_framework.parsers.YAMLParser',

        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        # the json, yaml, xml renderers are used for parsing video proposals
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework.renderers.YAMLRenderer',

        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

EMBEDLY_TIMEOUT = 1.5  # seconds
