from __future__ import absolute_import

import os

from django.conf import settings
from datetime import timedelta

from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pocket_groups.settings')

app = Celery('pocket_groups')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if settings.DEBUG:
    schedule = timedelta(seconds=15)
else:
    schedule = timedelta(minutes=2)

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'share-urls':{
            'schedule': schedule,
            'task': 'core.tasks.fetch_groups'
        }
    })
