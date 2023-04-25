"""
Django settings for scrubbers_backend project.

Generated by 'django-admin startproject' using Django 4.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from .discord_webhook_handler import DiscordWebhookHandler
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n72^h9zigpr59^p)+n99w*t#yb793s89rboma3hjqjx_z46bk-'

PORT = os.environ.get('PORT', 8000)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', None) or 'False'

REST_KNOX = {'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512', 'AUTH_TOKEN_CHARACTER_LENGTH': 64,
             'TOKEN_TTL': timedelta(days=5), 'USER_SERIALIZER': 'scheduling.serializers.auth.UserSerializer',
             'MIN_REFRESH_INTERVAL': 3600, 'TOKEN_LIMIT_PER_USER': None, 'AUTO_REFRESH': True, }

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'rest_framework', 'knox',
                  'django.contrib.staticfiles', 'transactions', 'django_crontab', 'drf_yasg',

                  'authorization', 'corsheaders', 'scheduling', 'django_filters', 'graphene_django', 'search',
                  'analytics', 'capacity', 'available']

FIREBASE_CONFIG = os.path.join(BASE_DIR, 'firebase-config.json')
REST_FRAMEWORK = {'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
                  'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
                  'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
                  'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',}
CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware', 'common.DisableCSRFMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
'request_logging.middleware.LoggingMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware', 'corsheaders.middleware.CorsMiddleware', ]


ROOT_URLCONF = 'scrubbers_backend.urls'

TEMPLATES = [
	{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
	 'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
	                                    'django.template.context_processors.request',
	                                    'django.contrib.auth.context_processors.auth',
	                                    'django.contrib.messages.context_processors.messages', ], }, }, ]

WSGI_APPLICATION = 'scrubbers_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
USE_SQLITE = os.environ.get('USE_SQLITE', None) or 'False'
if USE_SQLITE == 'True':
	DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3', }}
else:

	DATABASES = {
		'default':
			{
				'ENGINE': 'django.db.backends.postgresql',
				'NAME': os.environ['DB_NAME'],
				'USER': os.environ['DB_USER'],
				'PASSWORD': os.environ['DB_PASSWORD'],
				'HOST': os.environ['DB_HOST'],
				'PORT': os.environ['DB_PORT'],
			}
	}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.authorization.password_validation.UserAttributeSimilarityValidator', },
	{'NAME': 'django.contrib.authorization.password_validation.MinimumLengthValidator', },
	{'NAME': 'django.contrib.authorization.password_validation.CommonPasswordValidator', },
	{'NAME': 'django.contrib.authorization.password_validation.NumericPasswordValidator', }, ]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = 'static/'

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRONJOBS = [('* * * * *', 'transactions.utils.delete_old_transactions'), ]

# Mailchimp API key
MAILCHIMP_API_KEY = '<e8a0bc3c49bf95ddc6347c8c4641c9a8-us9>'

# Mailchimp API base URL
MAILCHIMP_API_URL = 'https://us9.api.mailchimp.com/3.0'

# Default from email address for transactional emails
DEFAULT_FROM_EMAIL = '<support@quicker.com>'

# Mailchimp template name for transactional emails
MAILCHIMP_TEMPLATE_NAME = '<Quicker-Reset-Password>'

# Configure the mailchimp_transactional package to use your Mailchimp API key and base URL
MAILCHIMP_TRANSACTIONAL_API_KEY = MAILCHIMP_API_KEY
MAILCHIMP_TRANSACTIONAL_API_BASE_URL = MAILCHIMP_API_URL



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "webhook": {
	        "level": "DEBUG",
            "class":"scrubbers_backend.discord_webhook_handler.DiscordWebhookHandler",
	        "webhook_url": "https://discord.com/api/webhooks/1094364223959740486/9W69d8AHC0HWe67lpzyKVXos1Z07xxr5lyr_L9QKnxuNzQ4aJa4t5SfsiX5FPCpyx1tB"
        },
    },
    'loggers': {
	    "django.request":{
            'handlers': ['webhook'],
            'level': 'DEBUG',
		    "propagate": False,
	    }
    },
	'formatters': {
	        'verbose': {
	            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
	        },
	    },
}

TEST = {
    'ATOMIC_REQUESTS': True,
}