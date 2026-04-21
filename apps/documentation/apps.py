"""
Django app for the documentation portal (Phase 0–4 docs UX + REST under ``/docs/``).

GraphQL: ``docs.*`` (pages, relationships) where wired; see views under ``apps/documentation``.
"""

from django.apps import AppConfig


class DocumentationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.documentation"
