from django.http import HttpResponse
from django.test import RequestFactory

from apps.operations import views


def _unwrap_view(view_func):
    current = view_func
    while hasattr(current, "__wrapped__"):
        current = current.__wrapped__
    return current


def test_probe_logs_health_degraded_when_logs_api_disabled(monkeypatch):
    monkeypatch.setattr(views.settings, "LOGS_API_ENABLED", False)
    assert views._probe_logs_health() == "degraded"


def test_probe_job_scheduler_health_down_on_dependency_failure(monkeypatch):
    class _FailClient:
        def list_jobs(self, **kwargs):
            raise RuntimeError("scheduler down")

    monkeypatch.setattr(views.settings, "JOB_SCHEDULER_ENABLED", True)
    monkeypatch.setattr(views, "TkdJobClient", lambda *args, **kwargs: _FailClient())
    assert views._probe_job_scheduler_health() == "down"


def test_probe_storage_health_degraded_when_bucket_missing(monkeypatch):
    request = RequestFactory().get("/operations/")

    class _GraphqlClient:
        def list_users_with_buckets(self, **kwargs):
            return [{"bucket": ""}]

    monkeypatch.setattr(views.settings, "S3STORAGE_ENABLED", True)
    monkeypatch.setattr(views, "AdminGraphQLClient", lambda *args, **kwargs: _GraphqlClient())
    assert views._probe_storage_health(request) == "degraded"


def test_operations_view_renders_even_when_all_probes_fail(monkeypatch):
    request = RequestFactory().get("/operations/")
    captured = {}

    def _fake_render(req, template, context):
        captured["template"] = template
        captured["context"] = context
        return HttpResponse("ok")

    monkeypatch.setattr(views, "_probe_storage_health", lambda req: "down")
    monkeypatch.setattr(views, "_probe_lambda_health", lambda: "down")
    monkeypatch.setattr(views, "_probe_graphql_health", lambda req: "down")
    monkeypatch.setattr(views, "_probe_db_health", lambda: "down")
    monkeypatch.setattr(views, "_probe_logs_health", lambda: "down")
    monkeypatch.setattr(views, "render", _fake_render)

    response = _unwrap_view(views.operations_view)(request)
    assert response.status_code == 200
    assert captured["template"] == "operations/dashboard.html"
    assert captured["context"]["stats"]["total_operations"] == 5
    assert captured["context"]["stats"]["failed"] == 5
    assert captured["context"]["stats"]["uptime"] == "0.0%"
    assert captured["context"]["release_gate"]["pass"] is False
    assert captured["context"]["release_gate"]["state"] == "block"


def test_release_gate_passes_when_all_dependencies_healthy():
    gate = views._build_release_gate(["operational", "operational", "operational", "operational", "operational"])
    assert gate["pass"] is True
    assert gate["state"] == "pass"
    assert gate["down_services"] == 0
    assert gate["weighted_uptime_pct"] == "100.0%"

