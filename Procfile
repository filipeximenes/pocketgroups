web: cd pocket_groups; gunicorn pocket_groups.wsgi
worker: celery -A pocket_groups worker -B -l info
