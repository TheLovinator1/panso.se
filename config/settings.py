from __future__ import annotations

import os
import sys
from pathlib import Path

import hishel
from dotenv import load_dotenv
from platformdirs import user_data_dir

load_dotenv(verbose=True)

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = Path(user_data_dir(appname="Panso", appauthor="TheLovinator", roaming=True, ensure_exists=True))

SECRET_KEY: str | None = os.getenv("DJANGO_SECRET_KEY")
DEBUG: bool = os.getenv(key="DJANGO_DEBUG", default="False").lower() == "true"

ALLOWED_HOSTS: list[str] = [] if DEBUG else [".panso.se"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ADMINS: list[tuple[str, str]] = [("Joakim Hellsén", "tlovinator@gmail.com")]
SITE_ID = 1
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
INTERNAL_IPS: list[str] = ["127.0.0.1", "::1"]
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

LANGUAGE_CODE = "sv-se"
TIME_ZONE = "Europe/Stockholm"
DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = " "
USE_I18N = False
USE_TZ = False

STATIC_URL = "static/"
STATIC_ROOT: Path = Path(os.getenv(key="STATIC_ROOT", default=DATA_DIR / "static"))
MEDIA_URL = "media/"
MEDIA_ROOT: Path = Path(os.getenv(key="MEDIA_ROOT", default=DATA_DIR / "media"))

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
ACCOUNT_EMAIL_VERIFICATION = "none"

INSTALLED_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_browser_reload",
    "django_filters",
    "django_htmx",
    "ninja",
    "pictures",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "panso.apps.PansoConfig",
    "webhallen.apps.WebhallenConfig",
    "inet.apps.InetConfig",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "panso"),
        "USER": os.getenv("POSTGRES_USER", "panso"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST", "192.168.1.2"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "OPTIONS": {
            "pool": True,
        },
    },
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": DATA_DIR / "panso.sqlite3",
    #     "OPTIONS": {
    #        "init_command": "PRAGMA journal_mode=wal; PRAGMA synchronous=1; PRAGMA mmap_size=134217728; PRAGMA journal_size_limit=67108864; PRAGMA cache_size=2000;",  # noqa: E501
    #     },
    # },
}


AUTHENTICATION_BACKENDS: list[str] = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "asyncio": {  # Hide "Using selector: SelectSelector" spam
            "level": "WARNING",
        },
    },
}

# Only enable the toolbar when we're in debug mode and we're
# not running tests. Django will change DEBUG to be False for
# tests, so we can't rely on DEBUG alone.
ENABLE_DEBUG_TOOLBAR: bool = DEBUG and "test" not in sys.argv
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    # Customize the config to support turbo and htmx boosting.
    DEBUG_TOOLBAR_CONFIG: dict[str, str] = {"ROOT_TAG_EXTRA_ATTRS": "data-turbo-permanent hx-preserve"}

# Store HTTP responses in a cache.
storage = hishel.FileStorage(
    base_path=DATA_DIR / "cache",
)
controller = hishel.Controller(
    cacheable_methods=["GET", "HEAD", "OPTIONS"],
    cacheable_status_codes=[200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501],
)
HISHEL_CLIENT = hishel.CacheClient(
    storage=storage,
    controller=controller,
    follow_redirects=True,
    http2=True,
)
