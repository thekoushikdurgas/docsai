"""Staging — same security posture as production with shorter HSTS."""

from django.core.exceptions import ImproperlyConfigured

from decouple import Csv, config

from ._env import bootstrap_layered_env, resolve_secret_key

bootstrap_layered_env()

from .base import *  # noqa: F403

DEBUG = False

_secret = resolve_secret_key()
if not _secret:
    raise ImproperlyConfigured(
        "SECRET_KEY must be set for staging (.env.prod, .env, or environment)."
    )
SECRET_KEY = _secret

USE_HTTPS = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SECURE_SSL_REDIRECT = USE_HTTPS
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_COOKIE_SECURE = USE_HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

if USE_HTTPS:
    SECURE_HSTS_SECONDS = 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

ALLOWED_HOSTS = [
    h.strip()
    for h in config("ALLOWED_HOSTS", default="staging.example.com", cast=Csv())
    if h.strip()
]

AUTH_FALLBACK_LOCAL = config("AUTH_FALLBACK_LOCAL", default=False, cast=bool)

if SENTRY_DSN:  # noqa: F405
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,  # noqa: F405
        integrations=[DjangoIntegration()],
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,  # noqa: F405
        environment="staging",
        send_default_pii=False,
    )
