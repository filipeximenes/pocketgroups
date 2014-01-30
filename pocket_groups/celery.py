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

app.conf.update(
    BROKER_POOL_LIMIT=1,
    CELERYBEAT_SCHEDULE={
        'share-urls':{
            'schedule': timedelta(minutes=2),
            'task': 'core.tasks.fetch_groups'
        }
    })
