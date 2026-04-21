"""Phase 0 — Architecture blueprint (static registry + docs index rows; live health TBD)."""

from django.apps import AppConfig


class ArchitectureConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.architecture"
    label = "architecture"
