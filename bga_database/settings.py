"""
Django settings for bga_database project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import environ
import os

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    DJANGO_DEBUG=(bool, False),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DJANGO_DEBUG')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pensions',
    'bga_database',
    'compressor',
    'compressor_toolkit',
    'mailchimp_auth',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bga_database.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bga_database.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static'

STATICFILES_STORAGE = env(
    "DJANGO_STATICFILES_STORAGE",
    default="django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_OFFLINE = True

COMPRESS_PRECOMPILERS = (
    ('module', 'compressor_toolkit.precompilers.ES6Compiler'),
)

COMPRESS_ES6_COMPILER_CMD = (
    'export NODE_PATH="{paths}" && '
    '{browserify_bin} "{infile}" -o "{outfile}" '
    '-t [ "{node_modules}/babelify" --presets="{node_modules}/babel-preset-env" ]'
)

# Sessions

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='foobar')

ALLOWED_HOSTS = env('ALLOWED_HOSTS', [])


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db(default='postgres://postgres:postgres@postgres:5432/bga_pensions')
}


# Caching

CACHE_KEY = 'bga-pensions'

cache_backend = "dummy.DummyCache" if DEBUG else "db.DatabaseCache"
CACHES = {
    "default": {
        "BACKEND": f"django.core.cache.backends.{cache_backend}",
        "LOCATION": "pensions_cache",
        "TIMEOUT": 86400,  # 24 hours
    }
}

# The email() method is an alias for email_url().
EMAIL_CONFIG = env.email(
    'EMAIL_URL',
    default='smtp://user:password@localhost:25'
)

vars().update(EMAIL_CONFIG)

EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='')

MAILCHIMP_LIST_ID = env('MAILCHIMP_LIST_ID', default='')
MAILCHIMP_API_KEY = env('MAILCHIMP_API_KEY', default='')
MAILCHIMP_SERVER = env('MAILCHIMP_SERVER', default='')
MAILCHIMP_INTEREST_ID = env('MAILCHIMP_INTEREST_ID', default='')
MAILCHIMP_TAG = env('MAILCHIMP_TAG', default='')
MAILCHIMP_AUTH_COOKIE_NAME = env('MAILCHIMP_AUTH_COOKIE_NAME', default='')
MAILCHIMP_AUTH_COOKIE_DOMAIN = env('MAILCHIMP_AUTH_COOKIE_DOMAIN', default='')
MAILCHIMP_AUTH_REDIRECT_LOCATION = '/'


# Configure Sentry for error logging
if env("SENTRY_DSN", default=''):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
    )


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Preserve default loggers
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
        },
    },
}


# Enforce SSL in production
if DEBUG is False:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
