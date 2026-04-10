"""Page Builder — persisted page spec metadata (JSON stored in S3)."""

from django.db import models
from django.utils import timezone


class PageSpec(models.Model):
    """A `page_spec` JSON document (e.g. docs/frontend/pages/*.json) tracked in DB + S3."""

    page_id = models.SlugField(max_length=200, unique=True, db_index=True)
    title = models.CharField(max_length=300)
    page_type = models.CharField(max_length=100, blank=True, default="")
    codebase = models.CharField(max_length=100, blank=True, default="")
    surface = models.CharField(max_length=200, blank=True, default="")
    flow_id = models.CharField(max_length=200, blank=True, default="")
    era_tags = models.JSONField(default=list, blank=True)
    route = models.CharField(max_length=500, blank=True, default="")
    status = models.CharField(max_length=50, blank=True, default="")
    auth_required = models.BooleanField(default=False)
    purpose = models.TextField(blank=True, default="")
    section_count = models.PositiveIntegerField(default=0)
    component_count = models.PositiveIntegerField(default=0)
    endpoint_count = models.PositiveIntegerField(default=0)
    s3_bucket_id = models.CharField(max_length=300)
    s3_file_key = models.CharField(
        max_length=500, help_text="Relative key, e.g. json/<uuid>.json"
    )
    size_bytes = models.PositiveIntegerField(default=0)
    sections_override = models.JSONField(
        default=list,
        blank=True,
        help_text="Edited sections; merged over S3 spec in editor",
    )
    uploaded_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.CharField(max_length=254, blank=True, default="")

    class Meta:
        ordering = ["-updated_at", "title"]
        verbose_name = "Page spec"
        verbose_name_plural = "Page specs"

    def __str__(self):
        return self.title

    @property
    def full_s3_key(self) -> str:
        return f"{self.s3_bucket_id}/{self.s3_file_key}"
