"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-5d0!#bp$+*_i)6y7x12-+i)r^(s79o=-68dh^)0k69ro+wkp+n"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['https://localhost:8000','*']
CSRF_TRUSTED_ORIGINS = ['https://localhost:8000']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'users',
    'rest_framework_simplejwt',
    'oauth2_provider',
    # 'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'oauth2_provider.middleware.OAuth2TokenMiddleware', #added
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'postgres',
       'USER': 'postgres.eqzdqqudnrlrroimvdon',
       'PASSWORD': 'Transcender_78!',
       'HOST': 'aws-0-eu-central-1.pooler.supabase.com',
       'PORT': '5432',
   }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # 'rest_framework.authentication.SessionAuthentication', # To keep the Browsable API
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SIGNING_KEY': "kmoutaou",
    # custom
    "AUTH_COOKIE": "access_token",  # cookie name
    "AUTH_COOKIE_DOMAIN": None,  # specifies domain for which the cookie will be sent
    # "AUTH_COOKIE_SECURE": False,  # restricts the transmission of the cookie to only occur over secure (HTTPS) connections. 
    # "AUTH_COOKIE_HTTP_ONLY": True,  # prevents client-side js from accessing the cookie
    "AUTH_COOKIE_PATH": "/",  # URL path where cookie will be sent
    # "AUTH_COOKIE_SAMESITE": "Lax",  # specifies whether the cookie should be sent in cross site requests
}

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
# #     'ROTATE_REFRESH_TOKENS': True,
# #     'BLACKLIST_AFTER_ROTATION': True,
# #     'UPDATE_LAST_LOGIN': False,

# #     'ALGORITHM': 'HS256',

# #     'VERIFYING_KEY': None,
# #     'AUDIENCE': None,
# #     'ISSUER': None,
# #     'JWK_URL': None,
# #     'LEEWAY': 0,

# #     'AUTH_HEADER_TYPES': ('Bearer',),
# #     'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
# #     'USER_ID_FIELD': 'id',
# #     'USER_ID_CLAIM': 'user_id',
# #     'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

# #     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
# #     'TOKEN_TYPE_CLAIM': 'token_type',
# #     'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

# #     'JTI_CLAIM': 'jti',

# #     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
# #     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
# #     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
# }

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}

}

# 42 OAuth2 settings
OAUTH42_CLIENT_ID = 'u-s4t2ud-110e6a72c470ea3b61e2a1bc09acbd391dbb5fa23ecb37d0c8b88d513aa3865a'
OAUTH42_CLIENT_SECRET = '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'
OAUTH42_REDIRECT_URI = 'https://upgraded-dollop-q65pjww6654c67pp-8000.app.github.dev/auth42_callback&response_type=code'

ALLOWED_HOSTS = ['https://localhost:8000','*']
CSRF_TRUSTED_ORIGINS = ['https://localhost:8000']

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"