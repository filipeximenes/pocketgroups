
from fabric.api import *
from fabvenv import virtualenv, make_virtualenv
import server_config


env.roledefs = {
    'django': server_config.DJANGO_HOSTS,
    'django_provision': server_config.PROVISION_DJANGO_HOSTS,
}


def server():
    env.user = 'ubuntu'
    env.key_filename = 'deploy/pem_key.pem'


def setup_config_files():
    with cd(server_config.DJANGO_PROJECT_FOLDER):
        run('sudo rm -rf /etc/supervisor/conf.d/' + server_config.PROJECT_NAME + '.conf')
        run('sudo rm -rf /etc/nginx/sites-available/' + server_config.PROJECT_NAME)
        run('sudo rm -rf /etc/nginx/sites-enabled/' + server_config.PROJECT_NAME)

        run('sudo cp -fT supervisor.conf /etc/supervisor/conf.d/' + server_config.PROJECT_NAME + '.conf')
        run('sudo cp -fT nginx.conf /etc/nginx/sites-available/' + server_config.PROJECT_NAME)
        run('sudo ln -fs /etc/nginx/sites-available/' + server_config.PROJECT_NAME + ' '+
            '/etc/nginx/sites-enabled/' + server_config.PROJECT_NAME
            )

        with settings(warn_only=True):
            run('sudo service supervisor start')
            run('sudo supervisorctl reread')
            run('sudo supervisorctl update')
            run('sudo supervisorctl start ' + server_config.PROJECT_NAME)


def restart_services():
    run('sudo supervisorctl restart ' + server_config.PROJECT_NAME)
    run('sudo service nginx restart')


# def push_key():
#     # keyfile = '/tmp/%s.pub' % env.user
#     # run('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
#     # put('~/.ssh/id_rsa.pub', keyfile)
#     # run('cat %s >> ~/.ssh/authorized_keys' % keyfile)
#     # run('rm %s' % keyfile)
#     key = '~/.ssh/' + server_config.PROJECT_NAME
#     keypub = '~/.ssh/' + server_config.PROJECT_NAME + '.pub'
#     run('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
#     put(key, '~/.ssh/id_rsa')
#     put(keypub, '~/.ssh/id_rsa.pub')


# def push():
#     env.roles = ['django_provision']
#     server()
#     execute('push_key')


def prepare_server():
    run('sudo apt-get update')
    run('sudo apt-get install -y python-virtualenv python-pip fabric')
    run('sudo apt-get install -y python-software-properties')
    run('sudo apt-get install -y build-essential python2.7-dev')
    run('sudo apt-get install -y libsqlite3-dev git supervisor')

    run('sudo add-apt-repository -y ppa:nginx/stable')
    run('sudo apt-get update')
    run('sudo apt-get install -y nginx')

    run('sudo mkdir -p ' + server_config.DJANGO_PROJECT_FOLDER)
    run('sudo git clone ' + server_config.HTTPS_GIT_REPO + ' ' + server_config.DJANGO_PROJECT_FOLDER)

    make_virtualenv(server_config.VIRTUALENV_FOLDER)


def provision_django():
    env.roles = ['django_provision']
    server()
    execute('prepare_server')
    execute('start_deploy_django')
    execute('setup_config_files')
    execute('restart_services')


def start_deploy_django():
    with virtualenv(server_config.VIRTUALENV_FOLDER):
        with cd(server_config.DJANGO_PROJECT_FOLDER):
            run('sudo git pull origin')
            run('pip install -r requirements.txt')

    execute('setup_config_files')
    execute('restart_services')


def deploy_django():
    env.roles = ['django']
    server()
    execute('start_deploy_django')






