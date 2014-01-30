web: gunicorn -w 1 pocket_groups.wsgi
worker: celery -A pocket_groups worker -B -l info
