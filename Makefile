
setup:
	rm -rf db.sqlite3
	./manage.py syncdb --noinput
	./manage.py migrate
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
	git push heroku master
	heroku run python manage.py syncdb --app pocketgroups
	heroku run python manage.py migrate --app pocketgroups
	git push heroku-wk master

hk-open:
	heroku open --app pocketgroups

hk-logs:
	heroku logs --app pocketgroups

hk-wk-logs:
	heroku logs --app pocketgroups-wk

hk-wk-restart:
	heroku restart --app pocketgroups-wk

# python pip install -r requirements.txt; manage.py syncdb; python manage.py migrate;
