import json
import uuid

from django.test import RequestFactory

from apps.documentation.views import operations
from apps.operations.models import OperationLog


def _unwrap_view(view_func):
    current = view_func
    while hasattr(current, "__wrapped__"):
        current = current.__wrapped__
    return current


def test_analyze_progress_reads_persisted_job_state_when_memory_empty():
    job_id = uuid.uuid4()
    OperationLog.objects.create(
        operation_id=job_id,
        operation_type="documentation_sync",
        name="Docs background job (analyze)",
        status="completed",
        progress=100,
        metadata={
            "runtime_job_kind": "analyze",
            "done": True,
            "report": {"summary": {"total_files": 3}},
            "error": None,
        },
    )
    operations._analyze_jobs.clear()
    request = RequestFactory().get(f"/docs/api/operations/analyze-progress/{job_id}/")
    response = _unwrap_view(operations.analyze_progress_api)(request, str(job_id))
    payload = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert payload["done"] is True
    assert payload["report"]["summary"]["total_files"] == 3


def test_generate_json_progress_reads_persisted_job_state_when_memory_empty():
    job_id = uuid.uuid4()
    OperationLog.objects.create(
        operation_id=job_id,
        operation_type="documentation_sync",
        name="Docs background job (generate_json)",
        status="completed",
        progress=100,
        metadata={
            "runtime_job_kind": "generate_json",
            "done": True,
            "report": {"results": {"pages": {"success": True}}},
            "error": None,
        },
    )
    operations._generate_json_jobs.clear()
    request = RequestFactory().get(f"/docs/api/operations/generate-json-progress/{job_id}/")
    response = _unwrap_view(operations.generate_json_progress_api)(request, str(job_id))
    payload = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert payload["done"] is True
    assert payload["report"]["results"]["pages"]["success"] is True


def test_upload_progress_reads_persisted_job_state_when_memory_empty():
    job_id = uuid.uuid4()
    OperationLog.objects.create(
        operation_id=job_id,
        operation_type="documentation_sync",
        name="Docs background job (upload)",
        status="completed",
        progress=100,
        metadata={
            "runtime_job_kind": "upload",
            "done": True,
            "report": {"results": {"postman": {"synced": 2}}},
            "error": None,
        },
    )
    operations._upload_jobs.clear()
    request = RequestFactory().get(f"/docs/api/operations/upload-progress/{job_id}/")
    response = _unwrap_view(operations.upload_progress_api)(request, str(job_id))
    payload = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert payload["done"] is True
    assert payload["report"]["results"]["postman"]["synced"] == 2

