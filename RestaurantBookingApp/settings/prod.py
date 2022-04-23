import os
from .base import *

import dj_database_url


DEBUG = False

if not SECRET_KEY:
    SECRET_KEY = os.environ.get("SECRET_KEY")

INSTALLED_APPS += [
    "whitenoise.runserver_nostatic",
]

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


ALLOWED_HOSTS = ["0.0.0.0", "prince-booking.herokuapp.com"]


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
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

# Make sure to use production ready smtp server for sending emails
# Set the email backend to 'django.core.mail.backends.smtp.EmailBackend'
# Set the following environ variales for the email server
# EMAIL_HOST = os.environ.get("EMAIL_HOST")
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = os.environ.get("EMAIL_PORT")
# EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")

# This is just for test purpose to avoid sending emails
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}
