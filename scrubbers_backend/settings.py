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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n72^h9zigpr59^p)+n99w*t#yb793s89rboma3hjqjx_z46bk-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
DEBUG = True

REST_KNOX = {'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512', 'AUTH_TOKEN_CHARACTER_LENGTH': 64,
             'TOKEN_TTL': timedelta(days=5), 'USER_SERIALIZER': 'scheduling.serializers.AuthUserSerializer',
             'MIN_REFRESH_INTERVAL': 3600, 'TOKEN_LIMIT_PER_USER': None, 'AUTO_REFRESH': True, }

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'rest_framework',
                  'knox',
					'website',
                  'authorization', 'corsheaders', 'scheduling', 'django_filters', ]

FIREBASE_CONFIG = os.path.join(BASE_DIR, 'firebase-config.json')
REST_FRAMEWORK = {'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
                  'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
                  'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',), }
CORS_ORIGIN_ALLOW_ALL = True

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static',]

MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware', 'common.DisableCSRFMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
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

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3', }}

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

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
