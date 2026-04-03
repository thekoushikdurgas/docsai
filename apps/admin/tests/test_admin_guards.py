import json

import pytest
from django.test import RequestFactory
from django.urls import resolve, reverse

from apps.admin import views
from apps.admin.route_inventory import ADMIN_ROUTE_INVENTORY
from apps.admin.urls import urlpatterns
from apps.core.exceptions import LambdaAPIError


def _unwrap_view(view_func):
    current = view_func
    while hasattr(current, "__wrapped__"):
        current = current.__wrapped__
    return current


def _sample_url(name: str) -> str:
    kwargs = {}
    if name == "log_update" or name == "log_delete":
        kwargs["log_id"] = "log-1"
    if name == "job_detail" or name == "job_retry":
        kwargs["job_uuid"] = "job-1"
    if name == "billing_payment_approve" or name == "billing_payment_decline":
        kwargs["submission_id"] = "sub-1"
    return reverse(f"admin:{name}", kwargs=kwargs)


def test_admin_route_inventory_matches_urlpatterns():
    by_name = {entry["name"]: entry for entry in ADMIN_ROUTE_INVENTORY}
    url_names = {pattern.name for pattern in urlpatterns if pattern.name}
    assert set(by_name) == url_names

    for pattern in urlpatterns:
        if not pattern.name:
            continue
        expected_path = by_name[pattern.name]["path"]
        assert pattern.pattern._route == expected_path


@pytest.mark.parametrize("entry", ADMIN_ROUTE_INVENTORY)
def test_admin_permission_map_decorators(entry):
    if entry["permission"] == "public":
        return
    url = _sample_url(entry["name"])
    callback = resolve(url).func
    assert getattr(callback, "required_role_scope", None) == entry["permission"]


def test_log_delete_is_idempotent_on_not_found(monkeypatch):
    factory = RequestFactory()
    request = factory.post("/admin/logs/log-1/delete/")

    class _Client:
        def delete_log(self, log_id):
            raise LambdaAPIError("Log not found", status_code=404)

    monkeypatch.setattr(views, "LogsApiClient", lambda *args, **kwargs: _Client())
    response = _unwrap_view(views.log_delete_view)(request, "log-1")
    payload = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert payload["success"] is True


def test_storage_delete_is_idempotent_on_not_found(monkeypatch):
    factory = RequestFactory()
    request = factory.post("/admin/storage/delete/", data={"bucket_id": "b1", "file_key": "a.csv"})

    class _Client:
        def delete_object(self, bucket_id, file_key):
            raise LambdaAPIError("Object not found", status_code=404)

    monkeypatch.setattr(views, "S3StorageClient", lambda *args, **kwargs: _Client())
    monkeypatch.setattr(views, "S3STORAGE_ENABLED", True)
    response = _unwrap_view(views.storage_delete_view)(request)
    payload = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert payload["success"] is True


def test_logs_bulk_delete_is_idempotent_on_not_found(monkeypatch):
    factory = RequestFactory()
    request = factory.post(
        "/admin/logs/bulk-delete/",
        data=json.dumps({"level": "INFO"}),
        content_type="application/json",
    )

    class _Client:
        def delete_logs_bulk(self, **kwargs):
            raise LambdaAPIError("No matching logs found", status_code=404)

    monkeypatch.setattr(views, "LogsApiClient", lambda *args, **kwargs: _Client())
    monkeypatch.setattr(views, "LOGS_API_ENABLED", True)
    response = _unwrap_view(views.logs_bulk_delete_view)(request)
    payload = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["deleted_count"] == 0


def test_billing_payment_approve_is_idempotent_on_already_approved(monkeypatch):
    factory = RequestFactory()
    request = factory.post("/admin/billing/payments/sub-1/approve/")

    class _Client:
        def approve_payment_submission(self, submission_id):
            raise LambdaAPIError("Already approved", status_code=409)

    audit_calls = []
    monkeypatch.setattr(views, "_get_client", lambda request: _Client())
    monkeypatch.setattr(
        views,
        "_audit_billing_review_event",
        lambda *args, **kwargs: audit_calls.append(kwargs),
    )
    response = _unwrap_view(views.billing_payment_approve_view)(request, "sub-1")
    assert response.status_code == 302
    assert len(audit_calls) == 1
    assert audit_calls[0]["action"] == "approve"
    assert audit_calls[0]["success"] is True


def test_billing_payment_decline_is_idempotent_on_already_declined(monkeypatch):
    factory = RequestFactory()
    request = factory.post("/admin/billing/payments/sub-1/decline/", data={"reason": "duplicate"})

    class _Client:
        def decline_payment_submission(self, submission_id, reason):
            raise LambdaAPIError("Already declined", status_code=409)

    audit_calls = []
    monkeypatch.setattr(views, "_get_client", lambda request: _Client())
    monkeypatch.setattr(
        views,
        "_audit_billing_review_event",
        lambda *args, **kwargs: audit_calls.append(kwargs),
    )
    response = _unwrap_view(views.billing_payment_decline_view)(request, "sub-1")
    assert response.status_code == 302
    assert len(audit_calls) == 1
    assert audit_calls[0]["action"] == "decline"
    assert audit_calls[0]["success"] is True


def test_job_retry_is_idempotent_on_conflict(monkeypatch):
    factory = RequestFactory()
    request = factory.post(
        "/admin/jobs/job-1/retry/",
        data=json.dumps({"priority": 1}),
        content_type="application/json",
    )

    class _Client:
        def retry_job(self, *args, **kwargs):
            raise LambdaAPIError("Already approved", status_code=409)

    monkeypatch.setattr(views, "JOB_SCHEDULER_ENABLED", True)
    monkeypatch.setattr(views, "TkdJobClient", lambda *args, **kwargs: _Client())
    response = _unwrap_view(views.job_retry_view)(request, "job-1")
    payload = json.loads(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["status"] == "noop"


def test_billing_audit_payload_includes_request_and_actor(monkeypatch):
    factory = RequestFactory()
    request = factory.post(
        "/admin/billing/payments/sub-1/approve/",
        HTTP_X_REQUEST_ID="req-123",
    )

    class _User:
        is_authenticated = True
        pk = "u-42"

    request.user = _User()
    calls = []
    monkeypatch.setattr(views.logger, "info", lambda *args, **kwargs: calls.append(args))

    views._audit_billing_review_event(
        request=request,
        submission_id="sub-1",
        action="approve",
        success=True,
        status_before="pending",
        status_after="approved",
    )

    assert len(calls) == 1
    payload = calls[0][3]
    assert payload["request_id"] == "req-123"
    assert payload["actor_user_id"] == "u-42"
    assert payload["status_before"] == "pending"
    assert payload["status_after"] == "approved"
