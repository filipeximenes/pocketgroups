
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


hk-deploy:
	git push heroku master
	heroku run python manage.py syncdb
	heroku run python manage.py migrate
	heroku run python manage.py collecticstatic

# python pip install -r requirements.txt; manage.py syncdb; python manage.py migrate;
