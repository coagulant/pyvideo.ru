# Django settings for pyvideo project.
import os
from richard.settings import *

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ALLOWED_HOSTS = ['pyvideo.ru', 'www.pyvideo.ru', 'pyvideoru.herokuapp.com', '127.0.0.1',]
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
SECRET_KEY = 'this_is_not_production_so_who_cares'

ROOT_URLCONF = 'pyvideo.urls'
WSGI_APPLICATION = 'pyvideo.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)
JINGO_EXCLUDE_APPS += (
    'suit',
)
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
    'suit',
) + INSTALLED_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
    }
}

API = True