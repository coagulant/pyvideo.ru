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
    # exclude unwanted richard apps
) + tuple(app for app in INSTALLED_APPS if app not in ('grappelli',))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
    }
}

API = True
SUIT_CONFIG = {
    'LIST_PER_PAGE': 100
}
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/admin/'
ENABLE_METRICS = False

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
