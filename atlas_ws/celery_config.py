'''
Created on Dec 30, 2015

@author: sonu
'''

from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atlas_ws.settings')

# app = Celery('atlas_ws')
app = Celery('atlas_ws', backend="amqp", broker='amqp://guest@localhost:5672//')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.conf.update(CELERY_ACCEPT_CONTENT=['json'])
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
