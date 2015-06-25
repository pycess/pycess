"""
Django settings for pycess project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c-e2f6t1=c%^h8pb=y=scp8(szq(q=7-18$36$oyf@*b9x)@n^'

# Will need to change soon as per http://jxqdjango.readthedocs.org/en/latest/ref/templates/upgrading.html
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
    # dependancies
    'crispy_forms',
    # our app
    'process',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pycess.urls'

WSGI_APPLICATION = 'pycess.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# REFACT should this go into local_settings?
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'process/static/')


# django-crispy-forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Modeled after http://stackoverflow.com/questions/1406892/elegantly-handle-site-specific-settings-configuration-in-svn-hg-git-etc
# REFACT: I would like to replace this with a config file loader that loads a yml or ini file
# it could default to development.ini in the root file and be overridden by something. Most likely an environment variable?

import os
if 'DJANGO_ADD_CONFIG' in os.environ:
    try:
        exec("from pycess.%s_settings import *" % os.environ['DJANGO_ADD_CONFIG'])
    except ImportError:
        pass

# Pull in the local changes.
try:
    from pycess.local_settings import *
except ImportError:
    pass
