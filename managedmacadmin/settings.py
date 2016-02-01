"""
Django settings for managedmacadmin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#
# Change these settings to reflect your configuration.
# ORGANIZATION - Name of your organization to use for display purposes
# PUSH_TOPIC - Apple assigned, com.apple.mgmt.External.<GUID>
# MANAGED_PROFILE_UUID - Generate a custom UUID and put it in here
# IDENTIFIER - Prefix to use with profiles (e.g. com.yourorganization)
# DEFAULT_DEVICE_GROUP - UUID of the device group to put all new devices in (create a device group first)
# ENROLL_PIN - The Pin code to use to enroll new devices
# USE_CERTIFICATE - True/False (If True and a certificate was provided by the client, use it. Recommended: False)
# REQUIRE_CERTIFICATE - True/False (If True, require the client to provide a valid certificate. Recommended: False)

ORGANIZATION = 'Your Organization'
PUSH_TOPIC = 'com.apple.mgmt.External.GUID'
MANAGED_PROFILE_UUID = 'GUID'
IDENTIFIER = 'com.yourorganization'
DEFAULT_DEVICE_GROUP=''
ENROLL_PIN='0000'
USE_CERTIFICATE = False
REQUIRE_CERTIFICATE = False

LOGIN_URL='/login/'
LOGIN_REDIRECT_URL='/mdm/'
MANAGED_PROFILE_IDENTIFIER = IDENTIFIER + '.' + MANAGED_PROFILE_UUID


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7wdk^m+rf^zerj3#=d5^e77zf(_ys)=(+p(&$3k(_^e5vm!mzf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'reports',
    'mdm',
    'config',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'managedmacadmin.urls'

WSGI_APPLICATION = 'managedmacadmin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
#    'default': {
#	'ENGINE': 'django.db.backends.mysql',
#	'NAME': 'django',
#	'USER': 'django',
#	'PASSWORD': 'password',
#	'HOST': 'localhost',
#	'PORT': '3306',
#    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'site_static'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

