"""
Django settings for pocket_groups project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AUTH_USER_MODEL = 'accounts.UserAccount'

LOGIN_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='abc')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',
    'gunicorn',
    'south',

    'core',
    'accounts',
    'groups',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pocket_groups.urls'

WSGI_APPLICATION = 'pocket_groups.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
from dj_database_url import parse as db_url

DATABASES = {
    'default': config(
        'DATABASE_URL', 
        # default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        cast=db_url
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Pocket
POCKET_CONSUMER_KEY = config('POCKET_CONSUMER_KEY', default='23252-73547210af1d70d949daf5be')

# Templated email
TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django'

# CELERY
CELERY_TIMEZONE = TIME_ZONE
BROKER_URL = config('BROKER_URL', default='amqp://@localhost:5672//')

# Email
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='pocketgroupsemail@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='c0azML1FvKwCdr28iTJH3n1a57lRU2')
