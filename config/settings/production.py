"""Production settings."""

from django.core.exceptions import ImproperlyConfigured

from decouple import config

from ._env import bootstrap_layered_env, resolve_secret_key

# Load `.env` then `.env.prod` into the process env (exported vars win). Must run
# before ``base`` so DATABASE_URL, Redis, and other keys match SECRET_KEY resolution.
bootstrap_layered_env()

from .base import *  # noqa: F403

# Prefer HTTPS `GRAPHQL_URL` (e.g. https://api.contact360.io/graphql) when this site is served over HTTPS.
# Set via environment / .env.prod — see README.md.

DEBUG = False

_secret = resolve_secret_key()
if not _secret:
    raise ImproperlyConfigured(
        "SECRET_KEY must be set for production (environment, .env.prod, or .env)."
    )
SECRET_KEY = _secret

USE_HTTPS = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SECURE_SSL_REDIRECT = USE_HTTPS
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_COOKIE_SECURE = USE_HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

if USE_HTTPS:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SILENCED_SYSTEM_CHECKS = [
        "security.W004",
        "security.W008",
        "security.W012",
        "security.W016",
    ]
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "unsafe-none"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

LOGGING["handlers"]["console"]["level"] = "WARNING"  # noqa: F405
LOGGING["root"]["level"] = "INFO"  # noqa: F405

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# GraphQL-only auth in production: keep ``false`` so operators use gateway JWT only.
AUTH_FALLBACK_LOCAL = config("AUTH_FALLBACK_LOCAL", default=False, cast=bool)

if SENTRY_DSN:  # noqa: F405
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,  # noqa: F405
        integrations=[DjangoIntegration()],
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,  # noqa: F405
        environment="production",
        send_default_pii=False,
    )
