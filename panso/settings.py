"""Django settings for panso project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from __future__ import annotations

import os
from pathlib import Path

from django.utils import timezone
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), verbose=True)

DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
BASE_DIR: Path = Path(__file__).resolve().parent.parent
SECRET_KEY: str = os.getenv("SECRET_KEY", "django-insecure")
ALLOWED_HOSTS: list[str] = [".panso.se", ".localhost", "127.0.0.1"]
INTERNAL_IPS: list[str] = ["127.0.0.1", "localhost", "192.168.1.143"]
USE_X_FORWARDED_HOST = True
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
ROOT_URLCONF = "panso.urls"
WSGI_APPLICATION = "panso.wsgi.application"
SITE_ID = 1

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Stockholm"
USE_I18N = True
USE_TZ = True
DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = " "

ADMINS: list[tuple] = [("TheLovinator", "tlovinator@gmail.com")]
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER: str = os.getenv(key="EMAIL_HOST_USER", default="webmaster@localhost")
EMAIL_HOST_PASSWORD: str = os.getenv(key="EMAIL_HOST_PASSWORD", default="")
EMAIL_SUBJECT_PREFIX = "[Panso] "
EMAIL_USE_LOCALTIME = True
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL: str = os.getenv(key="EMAIL_HOST_USER", default="webmaster@localhost")
SERVER_EMAIL: str = os.getenv(key="EMAIL_HOST_USER", default="webmaster@localhost")

STATIC_URL = "static/"
STATIC_ROOT: Path = BASE_DIR / "staticfiles"
STATICFILES_DIRS: list[Path] = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Application definition
INSTALLED_APPS: list[str] = [
    "panso.apps.PansoConfig",
    "django.contrib.admin",
    "django.contrib.sitemaps",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
database_folder: Path = BASE_DIR / "data"
database_folder.mkdir(parents=True, exist_ok=True)
DATABASES: dict[str, dict[str, str | Path | bool]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": database_folder / "panso.sqlite3",
        "ATOMIC_REQUESTS": True,
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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

if not DEBUG:
    CACHES: dict[str, dict[str, str]] = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "cache_table",
        },
    }
else:
    CACHES: dict[str, dict[str, str]] = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        },
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "data" / "logs" / f"{timezone.now().strftime('%Y%m%d')}.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
