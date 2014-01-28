
from fabric.api import *
from fabvenv import virtualenv, make_virtualenv
import server_config


env.roledefs = {
    'django': server_config.DJANGO_HOSTS,
    'django_provision': server_config.PROVISION_DJANGO_HOSTS,
}


def server():
    # env.host_string = '999.999.999.999'
    env.user = 'ubuntu'
    env.key_filename = 'deploy/pem_key.pem'

def start_provisioning():
    pass
    # run('sudo apt-get update')
    # run('sudo apt-get install -y python-virtualenv python-pip fabric')
    # run('sudo apt-get install -y python-software-properties')
    # run('sudo apt-get install -y build-essential python2.7-dev')
    # run('sudo apt-get install -y libsqlite3-dev')
    
    # run('sudo add-apt-repository ppa:nginx/stable')
    # run('sudo apt-get update')
    # run('sudo apt-get install -y nginx')
    
    # run('sudo apt-get install -y git')

    # make_virtualenv(server_config.VIRTUALENV_FOLDER)

    # run('sudo mkdir -p ' + server_config.DJANGO_PROJECT_FOLDER)
    # run('sudo git clone ' + server_config.HTTPS_GIT_REPO + ' ' + server_config.DJANGO_PROJECT_FOLDER)



def provision_django():
    env.roles = ['django_provision']
    server()
    execute('start_provisioning')


def start_deploy_django():
    with virtualenv(server_config.VIRTUALENV_FOLDER):
        with cd(server_config.DJANGO_PROJECT_FOLDER):
            run('sudo git pull origin')
            run('pip install -r requirements.txt')

            run('sudo cp nginx.conf /etc/nginx/sites-enabled/' + server_config.PROJECT_NAME)

            run('sudo rm -rf /etc/nginx/sites-available/' + server_config.PROJECT_NAME)
            run('sudo ln -fs /etc/nginx/sites-available/' + server_config.PROJECT_NAME + ' '+
                '/etc/nginx/sites-enabled/' + server_config.PROJECT_NAME
                )

            run('gunicorn -c ' + server_config.DJANGO_PROJECT_FOLDER + 
                '/gunicorn_config.py ' + server_config.PROJECT_NAME + '.wsgi')
            run('sudo service nginx restart')


def deploy_django():
    env.roles = ['django']
    server()
    execute('start_deploy_django')






