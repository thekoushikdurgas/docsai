"""
Backward-compatible settings entry point.

Prefer ``DJANGO_SETTINGS_MODULE=config.settings`` (see ``config/settings/__init__.py``).
"""

from config.settings import *  # noqa: F403
