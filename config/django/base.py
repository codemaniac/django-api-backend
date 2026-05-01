import os

from config.env import BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",

    "guardian",
    "rest_framework",
    "drf_spectacular",

    "healthz",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": env.db(),
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Auth

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)


# REST

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "accounts.authentication.ClerkAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "accounts.permissions.IsAuthenticatedActiveUser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api",
}


# File Uploads

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Tasks

TASKS = {
    "default": {
        "BACKEND": "django_tasks_db.DatabaseBackend",
        "QUEUES": ["default",],
    }
}


# Cache

CACHES = {
    "default": env.cache(),
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Other Settings

from config.settings.clerk import *  # noqa
