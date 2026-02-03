from pathlib import Path
import environ
from django.core.management.utils import get_random_secret_key

env = environ.Env()

SITE_ID = 1

#variable settings
PFP_WIDTH_HEIGHT = 250 #width and height of profile pictures
BAND_WIDTH_HEIGHT = 500 #width and height of band/label profile pictures
SHOW_MAX_WIDTH_HEIGHT = 800 #max width and/or height of show posters
CHAT_LOAD = 20 #how many chat messages are loaded at a time



BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env', overwrite=True)
DEBUG = env.bool('DEBUG')

# HTPPS stuff
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_NAME = 'plum'


#important!! 
SECRET_KEY = env.str('SECRET_KEY', default=get_random_secret_key())
DATABASE_URL = env.str('DATABASE_URL')


#hosts
ALLOWED_HOSTS = ["omahaunderground-wispy-meadow-6277.fly.dev", 'localhost', 'omahaunderground.net']
if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')

CSRF_TRUSTED_ORIGINS = ['https://omahaunderground-wispy-meadow-6277.fly.dev', 'https://omahaunderground.net']


# Database
if DEBUG and (not DATABASE_URL or DATABASE_URL == 'None'): #if debug=True but no database URL is provided (development)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': env.db(),
    }


AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_ENDPOINT_URL_S3 = env('AWS_ENDPOINT_URL_S3')
AWS_ENDPOINT_URL_IAM = env('AWS_ENDPOINT_URL_IAM')
AWS_REGION = None
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static/'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_ADDRESSING_STYLE = 'virtual'


#if not in development (production), use s3 static storage
if not DEBUG:
    MEDIA_URL = 'https://omaha-underground.t3.storage.dev/static/'
    STATIC_URL = 'https://omaha-underground.t3.storage.dev/static/'
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
        }
    }
else:
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    MEDIA_ROOT = BASE_DIR / 'media'



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



WSGI_APPLICATION = 'planetapplication.wsgi.application'
ROOT_URLCONF = 'planetapplication.urls'

#Custom User Logic
LOGIN_REDIRECT_URL = '/'
CSRF_FAILURE_VIEW = 'planetplum.views.csrf_failure'
AUTH_USER_MODEL = "users.CustomUser"
AUTHENTICATION_BACKENDS = ['users.authentication.BackendAuth']

#EMAIL SHTUFF
ADMIN_EMAIL = env('ADMIN_EMAIL')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#template processing
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


# Password validation
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