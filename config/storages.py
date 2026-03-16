"""
Custom S3 storage backends for static and media (separate bucket locations).

NOTE: Asset static/media are always served from local folders in all environments;
these classes are unused for asset serving. They are kept in case other parts of
the project need S3-backed static/media. Documentation data (pages, endpoints,
postman, relationships) uses S3 via apps.documentation.repositories, not these storages.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticS3Storage(S3Boto3Storage):
    """S3 storage for static files (collectstatic). Uses AWS_STATIC_LOCATION."""

    def get_default_settings(self):
        base = super().get_default_settings()
        base["location"] = getattr(settings, "AWS_STATIC_LOCATION", "static")
        return base


class MediaS3Storage(S3Boto3Storage):
    """S3 storage for media uploads. Uses AWS_MEDIA_LOCATION."""

    def get_default_settings(self):
        base = super().get_default_settings()
        base["location"] = getattr(settings, "AWS_MEDIA_LOCATION", "media")
        return base
