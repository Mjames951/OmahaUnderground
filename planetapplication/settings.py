from pathlib import Path
import os
import environ
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.management.utils import get_random_secret_key

DEBUG = False


env = environ.Env()

SITE_ID = 1

#variable settings
PFP_WIDTH_HEIGHT = 250 #width and height of profile pictures
BAND_WIDTH_HEIGHT = 500 #width and height of band/label profile pictures
SHOW_MAX_WIDTH_HEIGHT = 800 #max width and/or height of show posters
CHAT_LOAD = 20 #how many chat messages are loaded at a time

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

# HTPPS stuff
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

SECRET_KEY = env.str('SECRET_KEY', default=get_random_secret_key())
DATABASE_URL = env.str('DATABASE_URL')

ALLOWED_HOSTS = ["omahaunderground-wispy-meadow-6277.fly.dev", 'localhost', 'omahaunderground.net']
if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')

CSRF_TRUSTED_ORIGINS = ['https://omahaunderground-wispy-meadow-6277.fly.dev', 'https://omahaunderground.net']

# Application definition

INSTALLED_APPS = [
    'django.contrib.sessions',
    'storages',
    'planetplum.apps.PlanetplumConfig',
    'users',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'colorfield',
    'django_extensions',
    'tz_detect',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'planetapplication.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'planetapplication.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
if not DEBUG:
    DATABASES = {
        'default': env.db()
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = ['users.authentication.BackendAuth']


#EMAIL SHTUFF
ADMIN_EMAIL = env("ADMIN_EMAIL")
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_ENDPOINT_URL_S3 = env('AWS_ENDPOINT_URL_S3')
AWS_ENDPOINT_URL_IAM = env('AWS_ENDPOINT_URL_IAM')
AWS_REGION = env('AWS_REGION')
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static/' 
AWS_QUERYSTRING_AUTH = False


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

MEDIA_URL = 'https://omaha-underground.t3.storage.dev/static/'

#if not in development (production), use s3 static storage
if not DEBUG:
    STATIC_URL = 'https://omaha-underground.t3.storage.dev/static/'
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {

            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {

            },
        }
    }
else:
    STATIC_URL = '/static/'