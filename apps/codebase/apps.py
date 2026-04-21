"""Codebase scanner app (local UI; external scanner TBD)."""

from django.apps import AppConfig


class CodebaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.codebase"
    label = "codebase"
