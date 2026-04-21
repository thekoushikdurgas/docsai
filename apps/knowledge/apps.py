"""Knowledge base app (Phase 5 — gateway ``knowledge.*`` TBD)."""

from django.apps import AppConfig


class KnowledgeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.knowledge"
    label = "knowledge"
