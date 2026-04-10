"""JSON Store — persists uploaded JSON documents (Postman collections, configs, etc.)."""

from django.db import models
from django.utils import timezone


class JsonDocument(models.Model):
    """A JSON document uploaded to S3 and tracked in the database."""

    key = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-safe identifier, auto-generated from label",
    )
    label = models.CharField(max_length=300, help_text="Human-readable name")
    s3_bucket_id = models.CharField(max_length=300)
    s3_file_key = models.CharField(
        max_length=500, help_text="Relative key, e.g. json/<uuid>.json"
    )
    size_bytes = models.PositiveIntegerField(default=0)
    content_type = models.CharField(max_length=100, default="application/json")
    tags = models.CharField(
        max_length=500, blank=True, default="", help_text="Comma-separated tags"
    )
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.CharField(max_length=254, blank=True, default="")

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "JSON Document"
        verbose_name_plural = "JSON Documents"

    def __str__(self):
        return self.label

    @property
    def full_s3_key(self) -> str:
        return f"{self.s3_bucket_id}/{self.s3_file_key}"

    @property
    def size_display(self) -> str:
        if self.size_bytes < 1024:
            return f"{self.size_bytes} B"
        if self.size_bytes < 1024 * 1024:
            return f"{self.size_bytes / 1024:.1f} KB"
        return f"{self.size_bytes / (1024 * 1024):.1f} MB"
