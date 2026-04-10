"""
Durgasflow Models — n8n-compatible workflow automation.

Stores workflow metadata (pointer to S3 JSON) + full execution history in PostgreSQL.
"""

import uuid

from django.db import models
from django.utils import timezone


class WorkflowStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    ARCHIVED = "archived", "Archived"


class TriggerType(models.TextChoices):
    MANUAL = "manual", "Manual"
    WEBHOOK = "webhook", "Webhook"
    SCHEDULE = "schedule", "Schedule"
    EVENT = "event", "Event"


class ExecutionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    RUNNING = "running", "Running"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class N8nWorkflow(models.Model):
    """Uploaded n8n workflow — metadata in DB, full JSON stored on S3."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, default="")

    # n8n identifiers from the exported JSON
    n8n_id = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="id / workflow_id from n8n JSON",
    )
    n8n_version_id = models.CharField(max_length=200, blank=True, default="")

    # Status / trigger
    status = models.CharField(
        max_length=20, choices=WorkflowStatus.choices, default=WorkflowStatus.DRAFT
    )
    is_active = models.BooleanField(default=False)
    trigger_type = models.CharField(
        max_length=20, choices=TriggerType.choices, default=TriggerType.MANUAL
    )

    # Metadata from JSON
    tags = models.JSONField(default=list, blank=True)
    settings = models.JSONField(default=dict, blank=True)

    # In-DB graph override (edits made in the visual editor are written here;
    # merged over the S3 JSON when loading in the editor)
    graph_data = models.JSONField(default=dict, blank=True)

    # S3 storage pointer
    s3_bucket_id = models.CharField(max_length=300, blank=True, default="")
    s3_file_key = models.CharField(
        max_length=500, blank=True, default="", help_text="e.g. json/<uuid>.json"
    )

    # Counts
    node_count = models.PositiveIntegerField(default=0)
    size_bytes = models.PositiveIntegerField(default=0)

    # Execution stats (denormalised for fast dashboard queries)
    execution_count = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    failure_count = models.PositiveIntegerField(default=0)
    last_executed_at = models.DateTimeField(null=True, blank=True)

    # Ownership
    created_by = models.CharField(max_length=254, blank=True, default="")

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "N8n Workflow"
        verbose_name_plural = "N8n Workflows"

    def __str__(self):
        return f"{self.name} ({self.status})"

    @property
    def full_s3_key(self):
        if self.s3_bucket_id and self.s3_file_key:
            return f"{self.s3_bucket_id}/{self.s3_file_key}"
        return ""

    @property
    def success_rate(self):
        if self.execution_count == 0:
            return None
        return round(self.success_count / self.execution_count * 100, 1)

    def increment_execution(self, success: bool):
        self.execution_count += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        self.last_executed_at = timezone.now()
        self.save(
            update_fields=[
                "execution_count",
                "success_count",
                "failure_count",
                "last_executed_at",
                "updated_at",
            ]
        )


class N8nExecution(models.Model):
    """Single execution run of an N8nWorkflow."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(
        N8nWorkflow, on_delete=models.CASCADE, related_name="executions"
    )

    status = models.CharField(
        max_length=20, choices=ExecutionStatus.choices, default=ExecutionStatus.PENDING
    )
    trigger_type = models.CharField(
        max_length=20, choices=TriggerType.choices, default=TriggerType.MANUAL
    )
    trigger_data = models.JSONField(default=dict, blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    result_data = models.JSONField(default=dict, blank=True)
    node_results = models.JSONField(default=dict, blank=True)

    error_message = models.TextField(blank=True, default="")
    error_stack = models.TextField(blank=True, default="")

    retry_count = models.PositiveIntegerField(default=0)
    triggered_by = models.CharField(max_length=254, blank=True, default="")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "N8n Execution"
        verbose_name_plural = "N8n Executions"

    def __str__(self):
        return f"Exec {self.id} [{self.status}] — {self.workflow.name}"

    @property
    def duration_seconds(self):
        if self.started_at and self.finished_at:
            return round((self.finished_at - self.started_at).total_seconds(), 2)
        return None

    def start(self):
        self.status = ExecutionStatus.RUNNING
        self.started_at = timezone.now()
        self.save(update_fields=["status", "started_at", "updated_at"])

    def complete(self, result_data=None, node_results=None):
        self.status = ExecutionStatus.COMPLETED
        self.finished_at = timezone.now()
        if result_data is not None:
            self.result_data = result_data
        if node_results is not None:
            self.node_results = node_results
        self.save(
            update_fields=[
                "status",
                "finished_at",
                "result_data",
                "node_results",
                "updated_at",
            ]
        )
        self.workflow.increment_execution(success=True)

    def fail(self, error_message: str, error_stack: str = ""):
        self.status = ExecutionStatus.FAILED
        self.finished_at = timezone.now()
        self.error_message = error_message
        self.error_stack = error_stack
        self.save(
            update_fields=[
                "status",
                "finished_at",
                "error_message",
                "error_stack",
                "updated_at",
            ]
        )
        self.workflow.increment_execution(success=False)


class N8nExecutionLog(models.Model):
    """Per-node log entry within an execution."""

    LEVEL_CHOICES = [
        ("debug", "Debug"),
        ("info", "Info"),
        ("warning", "Warning"),
        ("error", "Error"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    execution = models.ForeignKey(
        N8nExecution, on_delete=models.CASCADE, related_name="logs"
    )

    node_id = models.CharField(max_length=200, blank=True, default="")
    node_name = models.CharField(max_length=300, blank=True, default="")
    node_type = models.CharField(max_length=200, blank=True, default="")

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="info")
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Execution Log"
        verbose_name_plural = "Execution Logs"

    def __str__(self):
        return f"[{self.level}] {self.node_name}: {self.message[:60]}"

    @property
    def duration_ms(self):
        if self.started_at and self.finished_at:
            return round((self.finished_at - self.started_at).total_seconds() * 1000)
        return None


class N8nCredential(models.Model):
    """Credential used by workflow nodes to authenticate with external services."""

    CREDENTIAL_TYPES = [
        ("api_key", "API Key"),
        ("bearer_token", "Bearer Token"),
        ("basic_auth", "Basic Auth"),
        ("oauth2", "OAuth 2.0"),
        ("custom", "Custom"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    credential_type = models.CharField(
        max_length=20, choices=CREDENTIAL_TYPES, default="api_key"
    )
    service_name = models.CharField(max_length=100, blank=True, default="")

    # Stored as JSON — in production use django-encrypted-model-fields
    data = models.JSONField(default=dict)

    created_by = models.CharField(max_length=254, blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "N8n Credential"
        verbose_name_plural = "N8n Credentials"

    def __str__(self):
        return f"{self.name} ({self.credential_type})"

    def mark_used(self):
        self.last_used_at = timezone.now()
        self.save(update_fields=["last_used_at"])
