"""
Production settings for docsai project.

These settings are used when DJANGO_ENV=production
"""

from .base import *  # noqa

# Override base settings for production
DEBUG = False

# SSL/HTTPS: Set SECURE_SSL_REDIRECT=True only when serving over HTTPS (domain + SSL).
# For HTTP-only deploy (e.g. IP 34.201.10.84), set SECURE_SSL_REDIRECT=False in .env.prod.
USE_HTTPS = os.getenv('SECURE_SSL_REDIRECT', 'false').lower() == 'true'

# Security settings
SECURE_SSL_REDIRECT = USE_HTTPS
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_COOKIE_SECURE = USE_HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (only when using HTTPS)
if USE_HTTPS:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # Silence expected security checks when intentionally serving HTTP-only (e.g. IP deploy)
    SILENCED_SYSTEM_CHECKS = [
        'security.W004',  # SECURE_HSTS_SECONDS
        'security.W008',  # SECURE_SSL_REDIRECT
        'security.W012',  # SESSION_COOKIE_SECURE
        'security.W016',  # CSRF_COOKIE_SECURE
    ]
    # Avoid browser console warnings about COOP being ignored on non-HTTPS origins.
    # COOP/COEP are "powerful features" that browsers only honor on trustworthy origins (HTTPS/localhost).
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'unsafe-none'

# Email Backend (SMTP for production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Logging - less verbose in production
LOGGING['handlers']['console']['level'] = 'WARNING'  # noqa
LOGGING['root']['level'] = 'INFO'  # noqa

# CORS - restrict in production
CORS_ALLOW_ALL_ORIGINS = False
# CORS_ALLOWED_ORIGINS should be set in environment variables

# Static and media: always use local folders in all environments. S3 is not used for asset
# static/media; only documentation data (pages, endpoints, postman, relationships) uses S3.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_URL = f'/{BASE_PATH}/static/' if BASE_PATH else '/static/'
MEDIA_URL = f'/{BASE_PATH}/media/' if BASE_PATH else '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload limits for production
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
