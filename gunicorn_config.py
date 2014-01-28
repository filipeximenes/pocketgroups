
# import server_config

# command = server_config.VIRTUALENV_FOLDER + '/bin/gunicorn'
# pythonpath = server_config.DJANGO_PROJECT_FOLDER

command = '/home/ubuntu/venvs/virtualenv/bin/gunicorn'
pythonpath = '/home/ubuntu/sites/pocket_groups'
bind = '127.0.0.1:8001'
workers = 3
user = 'ubuntu'
