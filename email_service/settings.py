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

# Mailgun Credentials
MAILGUN_MIME_SEND_URL = "https://api.mailgun.net/v2/sandbox85e18cde4adf4d3b8f4ed689bbb9e1a0.mailgun.org/messages.mime"
MAILGUN_DEFAULT_FROM_EMAIL = 'Pavitra Bhalla <pavitra@sandbox85e18cde4adf4d3b8f4ed689bbb9e1a0.mailgun.org>'
MAILGUN_API_KEY = 'key-16a1b7363b2e177454b069bb451ca562'

# AWS Credentials
AWS_ACCESS_KEY_ID = "AKIAJ3RFPYCM3HSDJISA"
AWS_SECRET_ACCESS_KEY = "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"
AWS_SES_REGION = "us-east-1"
AWS_DEFAULT_FROM_EMAIL = 'Pavitra Bhalla <pavitrabhalla@gmail.com>'


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
