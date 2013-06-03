# Django settings for pyvideo project.
from richard.settings import *

ALLOWED_HOSTS = ['pyvideo.ru']
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
SECRET_KEY = 'this_is_not_production_so_who_cares'

ROOT_URLCONF = 'pyvideo.urls'

WSGI_APPLICATION = 'pyvideo.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(ROOT, 'templates'),
)

INSTALLED_APPS = INSTALLED_APPS + (
)
