from pathlib import Path
import os
import sys
from base64 import b64decode

import environ
import sentry_sdk
from django.urls import reverse_lazy
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.

test = os.path.dirname(__file__)

TEST_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read environment variables using `django-environ`, use `.env` if it exists
env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")

if os.path.exists(env_file):
    env.read_env(env_file)

VCAP_SERVICES = env.json("VCAP_SERVICES", {})

# Set required configuration from environment
APP_ENV = env.str("APP_ENV", "local")

#  Staff SSO
AUTHBROKER_URL = env("AUTHBROKER_URL")
AUTHBROKER_CLIENT_ID = env("AUTHBROKER_CLIENT_ID")
AUTHBROKER_CLIENT_SECRET = env("AUTHBROKER_CLIENT_SECRET")
LOGIN_URL = reverse_lazy("authbroker_client:login")
LOGIN_REDIRECT_URL = reverse_lazy("test")

AUTH_USER_MODEL = "user.User"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

# Allow all hosts
# (this application will always be run behind a PaaS router or locally)
ALLOWED_HOSTS = ["*"]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = ["core", "user", "workflow", "chartofaccount"]

THIRD_PARTY_APPS = [
    "authbroker_client",
    "simple_history",
    "webpack_loader",
    "django_tables2",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "authbroker_client.middleware.ProtectAllViewsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if "postgres" in VCAP_SERVICES:
    DATABASE_URL = VCAP_SERVICES["postgres"][0]["credentials"]["uri"]
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {"default": env.db()}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django webpack loader config
STATICFILES_DIRS = (os.path.join(BASE_DIR, "assets"),)

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # "user.backends.CustomAuthbrokerBackend",
]

# Application paths outside of SSO protection
AUTHBROKER_ANONYMOUS_PATHS = [
    "/pingdom/ping.xml",
]

# Google Tag Manager
GTM_CODE = env("GTM_CODE", default=None)
GTM_AUTH = env("GTM_AUTH", default=None)

# Settings to expose in templates
SETTINGS_EXPORT = [
    "DEBUG",
    "GTM_CODE",
    "GTM_AUTH",
]

# Notify
GOVUK_NOTIFY_API_KEY = env("GOVUK_NOTIFY_API_KEY")
# Notify templates
HIRING_MANAGER_NEW_REQUEST_TEMPLATE_ID = env("HIRING_MANAGER_NEW_REQUEST_TEMPLATE_ID")
CHIEF_APPROVAL_REQUEST_TEMPLATE_ID = env("CHIEF_APPROVAL_REQUEST_TEMPLATE_ID")
HIRING_MANAGER_CHANGES_REQUESTED_TEMPLATE_ID = env(
    "HIRING_MANAGER_CHANGES_REQUESTED_TEMPLATE_ID"
)
BUS_OPS_APPROVAL_REQUEST_TEMPLATE_ID = env("BUS_OPS_APPROVAL_REQUEST_TEMPLATE_ID")