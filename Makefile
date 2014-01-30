
setup:
	rm -rf db.sqlite3
	./manage.py syncdb --noinput
	./manage.py createsuperuser --pocket_username=superuser

hk-config:
	heroku config --app pocketgroups
	heroku config --app pocketgroups-wk

hk-config-push:
	heroku config:push --overwrite --app pocketgroups
	heroku config:push --overwrite --app pocketgroups-wk

hk-config-pull:
	heroku config:pull --overwrite --app pocketgroups

hk-deploy:
	git push heroku-wk master
	git push heroku master
	heroku run python manage.py syncdb --app pocketgroups
	heroku run python manage.py migrate --app pocketgroups


hk-open:
	heroku open --app pocketgroups

hk-logs:
	heroku logs --app pocketgroups

# python pip install -r requirements.txt; manage.py syncdb; python manage.py migrate;
