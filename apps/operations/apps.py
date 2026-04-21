"""Operations hub app (links and landing; gateway work lives under ``admin_ops``)."""

from django.apps import AppConfig


class OperationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.operations"
    label = "operations"
