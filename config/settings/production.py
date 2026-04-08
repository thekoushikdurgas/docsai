"""Production settings."""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = False

_secret = (os.environ.get("SECRET_KEY") or "").strip()
if not _secret:
    raise ImproperlyConfigured("SECRET_KEY must be set in the environment for production.")
SECRET_KEY = _secret

# HTTPS: mirror contact360.io/2 — SECURE_SSL_REDIRECT=true when behind TLS
USE_HTTPS = os.getenv("SECURE_SSL_REDIRECT", "false").lower() == "true"
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
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

LOGGING["handlers"]["console"]["level"] = "WARNING"  # noqa: F405
LOGGING["root"]["level"] = "INFO"  # noqa: F405

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# GraphQL-only auth in production (local staff fallback is for dev / break-glass only)
AUTH_FALLBACK_LOCAL = os.getenv("AUTH_FALLBACK_LOCAL", "false").lower() == "true"

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
