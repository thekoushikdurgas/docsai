"""
Development settings for docsai project.

These settings are used when DJANGO_ENV=development or when DEBUG=True
"""

from .base import *  # noqa

# Override base settings for development
DEBUG = True
ALLOWED_HOSTS = ['*']  # Allow all hosts in development

# Use non-manifest static storage so {% static %} works without running collectstatic
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Development-specific middleware (optional)
# Install with: pip install django-debug-toolbar django-extensions
try:
    import debug_toolbar  # noqa
    INSTALLED_APPS += ['debug_toolbar']  # noqa
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE  # noqa
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    # RedirectsPanel is deprecated; HistoryPanel provides redirect data. Omit RedirectsPanel to avoid deprecation warning.
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.alerts.AlertsPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.community.CommunityPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]
except ImportError:
    pass  # Debug toolbar not installed

try:
    import django_extensions  # noqa
    INSTALLED_APPS += ['django_extensions']  # noqa
except ImportError:
    pass  # Django extensions not installed

# Email Backend (Console for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging - more verbose in development (Django at DEBUG; httpx/httpcore at WARNING to reduce noise)
LOGGING['handlers']['console']['level'] = 'DEBUG'  # noqa
LOGGING['root']['level'] = 'DEBUG'  # noqa
LOGGING.setdefault('loggers', {})['httpx'] = {'level': 'WARNING', 'propagate': False}  # noqa
LOGGING['loggers']['httpcore'] = {'level': 'WARNING', 'propagate': False}  # noqa

# Session cookies not secure in development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# CORS - allow all in development
CORS_ALLOW_ALL_ORIGINS = True
