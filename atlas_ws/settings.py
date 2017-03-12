"""
Django settings for atlas_ws project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from __future__ import absolute_import
# ^^^ The above is required if you want to import from the celery
# library.  If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from django.conf.global_settings import MEDIA_ROOT
from mongoengine import connection

# from kombu import serialization
# serialization.registry._decoders.pop("application/x-python-serialize")

# Celery settings
# TODO : Change the settings when AMQP cluster is used.
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see user guide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
USERAPP_DIR = "%s/%s/" % (BASE_DIR, 'userapp')
MEDIAAPP_DIR = "%s/%s/" % (BASE_DIR, 'mediacontentapp')
MODELLER_DIR = "%s/%s/" % (BASE_DIR, 'modeller')
SEARCHAPP_DIR = "%s/%s/" % (BASE_DIR, 'mediaresearchapp')
MEDIA_ROOT = os.path.dirname(os.path.dirname(__file__))
GCM_APIKEY = "AIzaSyB_LJhGIT0hkh6I54znllGZ2pi1Y7Nl2Jo"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'da50pwk)13@(d=u2j24g5_n=vj_js(fpder#63-cr#nnooz%t0'
FIREBASE_KEY = 'key=AAAAK1uBcGw:APA91bHiD-hvGL694Kx-kTujH5XRRs8eeH_xDxjAofPmWLy-Lx51iHmTXqIt_9MsYQBJPzvmbRrc7MnC5Aohj2s-TjoJos7asbSfZROOn80zJrFkGnjdgbwZrPtdDT3ZHU2G8-S6W1Ng'
FIREBASE_URL = 'fcm.googleapis.com'
FIREBASE_PROJECT_ID = 'research-154014'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'rest_framework',
    'rest_framework_mongoengine',
    'rest_framework_swagger',
    'userapp',
    'mediacontentapp',
    'mediaresearchapp',
    'mediaetlapp',
    'modeller',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'atlas_ws.urls'

WSGI_APPLICATION = 'atlas_ws.wsgi.application'

_MONGODB_NAME = 'my_database'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
   'default' : {
      'ENGINE' : 'django_mongodb_engine',
      'NAME' : 'my_database',
      'HOST' : '172.31.41.248'
   }
}
connection.connect(_MONGODB_NAME, host='172.31.41.248')

# Required for Basic authentication
# AUTHENTICATION_BACKENDS = (
#     'mongoengine.django.auth.MongoEngineBackend',
# )
# SESSION_ENGINE = 'mongoengine.django.sessions'
# SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
#    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#    ]
     'DEFAULT_PARSER_CLASSES': (
    'rest_framework.parsers.JSONParser',
     )
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],    # List URL namespaces to ignore
    "api_version": '0.1.10',  # Specify your API's version (optional)
    "enabled_methods": [  # Methods to enable in UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "is_authenticated": False
}

LOGGING = {
 'version': 1,
 'disable_existing_loggers': False,
 'handlers': {
   'console': {
     'level': 'ERROR',
     'class': 'logging.StreamHandler',
     'stream': sys.stderr
   },
  },
 'loggers': {
   'django.request': {
     'handlers': ['console'],
     'propogate': True,
     'level': 'ERROR',
   }
 }
}
