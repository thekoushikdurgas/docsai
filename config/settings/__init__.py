"""
Django settings package.

This module loads settings based on the DJANGO_ENV environment variable.
Default is 'config.settings.development' for local development.

When running `manage.py check --deploy`, production settings are used automatically
so the deploy check validates the actual production configuration.
"""

import os
import sys

# Use production settings for deploy check so security warnings are validated against prod config
if 'check' in sys.argv and '--deploy' in sys.argv:
    _env = 'production'
else:
    _env = os.getenv('DJANGO_ENV', 'development').lower()

# Determine which settings module to use
DJANGO_ENV = _env

if DJANGO_ENV == 'production':
    from .production import *  # noqa
elif DJANGO_ENV == 'staging':
    from .staging import *  # noqa
elif DJANGO_ENV == 'testing' or 'test' in DJANGO_ENV:
    from .testing import *  # noqa
else:
    from .development import *  # noqa
