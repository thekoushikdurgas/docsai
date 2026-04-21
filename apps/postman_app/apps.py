"""Deprecated — use ``apps.durgasman``; kept for migrations/data only."""

from django.apps import AppConfig


class PostmanAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.postman_app"
    label = "postman_app"
