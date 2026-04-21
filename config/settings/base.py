"""
Shared Django settings for Contact360 DocsAI Admin.

Environment-specific overrides live in development.py, production.py, staging.py, testing.py.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse, urlunparse

from decouple import Csv, config


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


def _parse_database_url(url: str) -> dict:
    """Minimal DATABASE_URL parser for postgres:// and postgresql:// (no extra deps)."""
    p = urlparse(url)
    if p.scheme not in ("postgres", "postgresql"):
        raise ValueError(f"Unsupported DATABASE_URL scheme: {p.scheme}")
    name = (p.path or "").lstrip("/")
    cfg: dict = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": name,
        "USER": p.username or "",
        "PASSWORD": p.password or "",
        "HOST": p.hostname or "",
        "PORT": str(p.port or 5432),
    }
    return cfg


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Production must set SECRET_KEY via environment (validated in production.py)
SECRET_KEY = config("SECRET_KEY", default="")
DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# Trusted origins for CSRF on HTTPS (e.g. https://admin.contact360.io). Empty in local HTTP dev.
_csrf_origins = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins if o.strip()]

INSTALLED_APPS = [
    "mathfilters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
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
    "apps.json_store",
    "apps.page_builder",
    "apps.templates_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "apps.documentation.middleware.api_tracking_middleware.ApiTrackingMiddleware",
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

# Database: DATABASE_URL for PostgreSQL, else SQLite (see .env.example)
_database_url = config("DATABASE_URL", default="").strip()
if _database_url:
    DATABASES = {"default": _parse_database_url(_database_url)}
    DATABASES["default"]["CONN_MAX_AGE"] = config("CONN_MAX_AGE", default=60, cast=int)
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    DATABASES["default"]["CONN_MAX_AGE"] = config("CONN_MAX_AGE", default=0, cast=int)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
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

GRAPHQL_URL = _normalize_graphql_url(
    config("GRAPHQL_URL", default="http://localhost:8001/graphql")
)
GRAPHQL_INTERNAL_TOKEN = config("GRAPHQL_INTERNAL_TOKEN", default="")
LOGS_API_URL = config("LOGS_API_URL", default="")
LOGS_API_KEY = config("LOGS_API_KEY", default="")
S3STORAGE_API_URL = config("S3STORAGE_API_URL", default="")
S3STORAGE_API_KEY = config("S3STORAGE_API_KEY", default="")
# When True, prefer gateway ``s3.deleteFile`` for JSON store / page builder deletes (operator JWT).
# Uploads still use direct s3storage until a generic JSON upload exists on ``s3.*``.
ADMIN_STORAGE_VIA_GATEWAY = config(
    "ADMIN_STORAGE_VIA_GATEWAY", default=False, cast=bool
)
# Optional CSV of allowed request hosts for Durgasman (e.g. ``api.stripe.com,.mycompany.com``).
# Empty = only SSRF blocks (private IPs, non-http(s), etc.). See ``durgasman.services.url_guard``.
DURGASMAN_ALLOWED_REQUEST_HOSTS = config(
    "DURGASMAN_ALLOWED_REQUEST_HOSTS", default="", cast=Csv()
)
SCHEDULER_URL = config("SCHEDULER_URL", default="")
AI_API_URL = config("AI_API_URL", default="")
AI_API_KEY = config("AI_API_KEY", default="")
EMAILCAMPAIGN_URL = config("EMAILCAMPAIGN_URL", default="")

# Direct AWS S3 (documentation JSON store, S3Service). Optional locally; set in env for prod.
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_REGION = config("AWS_REGION", default="us-east-1")
S3_BUCKET_NAME = config("S3_BUCKET_NAME", default="")
S3_DATA_PREFIX = config("S3_DATA_PREFIX", default="")
S3_DOCUMENTATION_PREFIX = config("S3_DOCUMENTATION_PREFIX", default="")

DOCS_AGENT_VERSION = config("DOCS_AGENT_VERSION", default="1.0.0")

AUTH_FALLBACK_LOCAL = config("AUTH_FALLBACK_LOCAL", default=True, cast=bool)

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

API_TRACKING_ENABLED = config("API_TRACKING_ENABLED", default=True, cast=bool)
API_TRACKING_USER_TYPE_ENABLED = config(
    "API_TRACKING_USER_TYPE_ENABLED", default=True, cast=bool
)
API_TRACKING_PATH_PREFIX = config("API_TRACKING_PATH_PREFIX", default="/api/v1/")

# Cache: optional Redis (USE_REDIS_CACHE=true + REDIS_URL or host/port)
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
REDIS_DB = config("REDIS_DB", default=0, cast=int)
REDIS_URL = config("REDIS_URL", default="")
USE_REDIS_CACHE = config("USE_REDIS_CACHE", default=False, cast=bool)

_redis_location = None
if USE_REDIS_CACHE and (REDIS_URL or REDIS_HOST):
    _redis_location = REDIS_URL or f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

if _redis_location:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _redis_location,
            "OPTIONS": {
                "socket_connect_timeout": 5,
            },
            "KEY_PREFIX": "docsai_admin",
            "TIMEOUT": 300,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "docsai-admin-default",
            "TIMEOUT": 300,
        }
    }

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

# Sentry (initialized in production/development when SENTRY_DSN is set)
SENTRY_DSN = config("SENTRY_DSN", default="").strip()
SENTRY_TRACES_SAMPLE_RATE = config("SENTRY_TRACES_SAMPLE_RATE", default=0.1, cast=float)
