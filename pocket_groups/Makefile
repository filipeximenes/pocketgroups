
setup:
	rm -rf db.sqlite3
	./manage.py syncdb --noinput
	./manage.py createsuperuser --pocket_username=superuser

hk-config:
	heroku config --app pocketgroups

hk-config-push:
	heroku config:push --overwrite --app pocketgroups

hk-config-pull:
	heroku config:pull --overwrite --app pocketgroups
