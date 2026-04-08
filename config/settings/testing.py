"""Pytest and CI test settings."""

from .base import *  # noqa: F403

DEBUG = False
SECRET_KEY = "test-secret-key-not-for-production"
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"null": {"class": "logging.NullHandler"}},
    "root": {"handlers": ["null"]},
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

AUTH_FALLBACK_LOCAL = False

# Avoid manifest static storage in tests (login template uses {% static %})
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# django-ratelimit uses cache backend; dummy cache is fine for unit tests
