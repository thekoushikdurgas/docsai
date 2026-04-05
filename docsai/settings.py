"""
Contact360 DocsAI Admin — Django settings
"""
import os
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from decouple import config, Csv


def _normalize_graphql_url(url: str) -> str:
    """
    Public API root is JSON-only; GraphQL POST must go to /graphql (see api.contact360.io).
    If GRAPHQL_URL is set to the site root (path / or empty), append /graphql.
    """
    u = (url or "").strip()
    if not u:
        return u
    p = urlparse(u)
    path = (p.path or "/").rstrip("/") or "/"
    if path == "/":
        return urlunparse((p.scheme, p.netloc, "/graphql", "", "", ""))
    return u

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="insecure-dev-key-change-me")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "drf_spectacular",
    "debug_toolbar",
    # Local apps
    "apps.core",
    "apps.admin_ops",
    "apps.documentation",
    "apps.analytics",
    "apps.ai_agent",
    "apps.graph",
    "apps.roadmap",
    "apps.architecture",
    "apps.durgasflow",
    "apps.durgasman",
    "apps.codebase",
    "apps.knowledge",
    "apps.operations",
    "apps.postman_app",
    "apps.json_store",
    "apps.page_builder",
    "apps.templates_app",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "docsai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.sidebar_context",
                "apps.core.context_processors.user_context",
                "apps.core.context_processors.system_info",
            ],
        },
    },
]

WSGI_APPLICATION = "docsai.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", default=86400, cast=int)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Service URLs
GRAPHQL_URL = _normalize_graphql_url(config("GRAPHQL_URL", default="http://localhost:8001/graphql"))
GRAPHQL_INTERNAL_TOKEN = config("GRAPHQL_INTERNAL_TOKEN", default="")
LOGS_API_URL = config("LOGS_API_URL", default="")
LOGS_API_KEY = config("LOGS_API_KEY", default="")
S3STORAGE_API_URL = config("S3STORAGE_API_URL", default="")
S3STORAGE_API_KEY = config("S3STORAGE_API_KEY", default="")
SCHEDULER_URL = config("SCHEDULER_URL", default="")
AI_API_URL = config("AI_API_URL", default="")
AI_API_KEY = config("AI_API_KEY", default="")
EMAILCAMPAIGN_URL = config("EMAILCAMPAIGN_URL", default="")

DOCS_AGENT_VERSION = config("DOCS_AGENT_VERSION", default="1.0.0")

# When True and GraphQL sign-in fails due to network (gateway down), fall back to
# django.contrib.auth (staff/superuser). Disable in production if you require GraphQL-only auth.
AUTH_FALLBACK_LOCAL = config("AUTH_FALLBACK_LOCAL", default=True, cast=bool)

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Contact360 DocsAI Admin API",
    "DESCRIPTION": "Internal admin and documentation API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

INTERNAL_IPS = ["127.0.0.1"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}
