"""Documentation relationship graph (``docs.relationships``)."""

from django.apps import AppConfig


class GraphConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.graph"
    label = "graph"
