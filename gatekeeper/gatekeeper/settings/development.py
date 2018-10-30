# Development settings for Gatekeeper project

import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.postgresql',
        'NAME'      : os.environ.get("DJANGO_DB_NAME"),
        'USER'      : os.environ.get("DJANGO_DB_USER"),
        'PASSWORD'  : os.environ.get("DJANGO_DB_PASSWORD"),
        'HOST'      : os.environ.get("DJANGO_DB_HOST"),
        'PORT'      : os.environ.get("DJANGO_DB_PORT")
    }
}
