"""Postman App — models for Postman collections and environments stored in S3."""

from django.db import models
from django.utils import timezone


class PostmanCollection(models.Model):
    """A Postman Collection JSON (v2.1.0) uploaded to S3."""

    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, default="")
    postman_id = models.CharField(
        max_length=200, blank=True, default="", help_text="_postman_id from info block"
    )
    schema_version = models.CharField(max_length=100, blank=True, default="v2.1.0")
    s3_bucket_id = models.CharField(max_length=300)
    s3_file_key = models.CharField(
        max_length=500, help_text="Relative key, e.g. json/<uuid>.json"
    )
    item_count = models.PositiveIntegerField(
        default=0, help_text="Top-level item count parsed on upload"
    )
    request_count = models.PositiveIntegerField(
        default=0, help_text="Total request count (recursive)"
    )
    size_bytes = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.CharField(max_length=254, blank=True, default="")

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Postman Collection"
        verbose_name_plural = "Postman Collections"

    def __str__(self):
        return self.name

    @property
    def full_s3_key(self) -> str:
        return f"{self.s3_bucket_id}/{self.s3_file_key}"


class PostmanEnvironment(models.Model):
    """A Postman Environment JSON uploaded to S3."""

    name = models.CharField(max_length=300)
    postman_id = models.CharField(
        max_length=200, blank=True, default="", help_text="id from environment JSON"
    )
    s3_bucket_id = models.CharField(max_length=300)
    s3_file_key = models.CharField(
        max_length=500, help_text="Relative key, e.g. json/<uuid>.json"
    )
    variable_count = models.PositiveIntegerField(
        default=0, help_text="Number of variables in environment"
    )
    size_bytes = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.CharField(max_length=254, blank=True, default="")

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Postman Environment"
        verbose_name_plural = "Postman Environments"

    def __str__(self):
        return self.name

    @property
    def full_s3_key(self) -> str:
        return f"{self.s3_bucket_id}/{self.s3_file_key}"
