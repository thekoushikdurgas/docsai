"""Local development settings."""

from decouple import config

from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = config("SECRET_KEY", default="insecure-dev-key-change-me")

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING["handlers"]["console"]["level"] = "DEBUG"  # noqa: F405
LOGGING["root"]["level"] = "DEBUG"  # noqa: F405

try:
    import debug_toolbar  # noqa: F401

    INSTALLED_APPS = ["debug_toolbar"] + list(INSTALLED_APPS)  # noqa: F405
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + list(MIDDLEWARE)  # noqa: F405
    INTERNAL_IPS = ["127.0.0.1", "localhost"]
except ImportError:
    pass

if SENTRY_DSN:  # noqa: F405
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,  # noqa: F405
        integrations=[DjangoIntegration()],
        traces_sample_rate=min(SENTRY_TRACES_SAMPLE_RATE, 0.2),  # noqa: F405
        environment="development",
        send_default_pii=False,
    )
