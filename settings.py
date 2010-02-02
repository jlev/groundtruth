from settings_local import *

ROOT_URLCONF = 'groundtruth.urls'
APPEND_SLASH = True

TEMPLATE_DIRS = (
    SITE_ROOT + 'templates/',
    SITE_ROOT + 'olwidget/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'django_evolution',
    'olwidget',
    'groundtruth.geo',
    'groundtruth.info'
)
