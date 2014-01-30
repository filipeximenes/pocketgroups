web: python pip install -r requirements.txt; manage.py syncdb; python manage.py migrate; gunicorn pocket_groups.wsgi
worker: celery -A pocket_groups worker -B -l info
