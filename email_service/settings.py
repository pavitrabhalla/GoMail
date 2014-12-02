"""
Django settings for email_service project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'email_service/apps'))

TESTDATA_DIR = os.path.join(BASE_DIR, 'email_service/apps/api/testdata/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n=3_t87mk97nyug2#%w9m*z$nzd!*)2y%o1fwos0p@f--ag5r0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tastypie',
    'django_ses',    
    'requests',
    'boto',


    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'email_service.urls'

WSGI_APPLICATION = 'email_service.wsgi.application'

FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.TemporaryFileUploadHandler",)



# Default Email Settings
DEFAULT_FROM_EMAIL = '<default_from_email>'

# Sendgrid Credentials
SG_USERNAME = '<sendgrid_username>'
SG_PASSWORD = '<sendgrid_password>'


# Mailgun Credentials
MAILGUN_SEND_URL = '<Mailgun_send_url>'
MAILGUN_API_KEY = '<Mailgun_api_key>'


# AWS Credentials
AWS_ACCESS_KEY_ID = "<AWS_ACCESS_KEY_ID>"
AWS_SECRET_ACCESS_KEY = "<AWS_SECRET_KEY>"
AWS_SES_REGION = "<AWS_SES_REGION>"


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

try:$
    from local_settings import *$
except ImportError:$
    pass$

