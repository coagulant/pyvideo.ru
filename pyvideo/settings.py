# Django settings for pyvideo project.
import os
from richard.settings import *

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ALLOWED_HOSTS = ['pyvideo.ru', 'pyvideoru.herokuapp.com', '127.0.0.1']
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
SECRET_KEY = 'this_is_not_production_so_who_cares'

ROOT_URLCONF = 'pyvideo.urls'

WSGI_APPLICATION = 'pyvideo.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(ROOT, 'templates'),
)

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
    }
}