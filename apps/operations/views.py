"""Operations views."""
import uuid
from django.db import connection
from django.conf import settings
from django.shortcuts import render
from apps.core.decorators.auth import require_super_admin
from apps.core.middleware.request_id_middleware import REQUEST_ID_ATTR
from apps.admin.services.admin_client import AdminGraphQLClient
from apps.admin.services.logs_api_client import LogsApiClient
from apps.admin.services.s3storage_client import S3StorageClient
from apps.admin.services.tkdjob_client import TkdJobClient


def _request_trace_id(request=None):
    if request is None:
        return str(uuid.uuid4())
    cached = getattr(request, REQUEST_ID_ATTR, None)
    if cached:
        return cached
    return (
        request.META.get("HTTP_X_REQUEST_ID")
        or request.META.get("HTTP_X_CORRELATION_ID")
        or str(uuid.uuid4())
    )


def _probe_graphql_health(request):
    try:
        health = AdminGraphQLClient(request).get_api_health()
        if health and str(health.get("status", "")).lower() in {"ok", "healthy", "up"}:
            return "operational"
        if health:
            return "degraded"
        return "down"
    except Exception:
        return "down"


def _probe_db_health():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
        return "operational" if row and row[0] == 1 else "degraded"
    except Exception:
        return "down"


def _probe_logs_health():
    if not getattr(settings, "LOGS_API_ENABLED", False):
        return "degraded"
    try:
        LogsApiClient(request_id=str(uuid.uuid4())).get_statistics(time_range="1h", period="hourly")
        return "operational"
    except Exception:
        return "down"


def _probe_storage_health(request):
    if not getattr(settings, "S3STORAGE_ENABLED", False):
        return "degraded"
    try:
        users = AdminGraphQLClient(request).list_users_with_buckets(limit=1)
        bucket = (users[0].get("bucket") if users else None) or ""
        if not bucket:
            return "degraded"
        # Best-effort lightweight call.
        S3StorageClient(request_id=_request_trace_id(request)).list_objects(bucket_id=bucket, prefix="")
        return "operational"
    except Exception:
        return "down"


def _probe_lambda_health():
    statuses = []
    statuses.append(_probe_logs_health())
    statuses.append(_probe_job_scheduler_health())
    if getattr(settings, "S3STORAGE_ENABLED", False):
        statuses.append("operational")
    else:
        statuses.append("degraded")
    if "down" in statuses:
        return "down"
    if "degraded" in statuses:
        return "degraded"
    return "operational"


def _probe_job_scheduler_health():
    if not getattr(settings, "JOB_SCHEDULER_ENABLED", False):
        return "degraded"
    try:
        TkdJobClient(request_id=str(uuid.uuid4())).list_jobs(limit=1, offset=0)
        return "operational"
    except Exception:
        return "down"


def _build_release_gate(service_states):
    """Compute dependency release gate from current probe states."""
    total_services = len(service_states) if service_states else 1
    operational_count = sum(1 for state in service_states if state == "operational")
    degraded_count = sum(1 for state in service_states if state == "degraded")
    down_count = sum(1 for state in service_states if state == "down")
    weighted_uptime = ((operational_count * 1.0) + (degraded_count * 0.5)) / total_services
    gate_pass = down_count == 0 and weighted_uptime >= 0.90
    return {
        "pass": gate_pass,
        "state": "pass" if gate_pass else "block",
        "weighted_uptime_pct": f"{weighted_uptime * 100:.1f}%",
        "down_services": down_count,
        "degraded_services": degraded_count,
        "policy": "Pass requires zero down services and weighted uptime >= 90.0%.",
    }


@require_super_admin
def operations_view(request):
    """Operations hub: stats and links to analyze/validate/generate/upload/workflow."""
    stats = {'total_operations': 0, 'successful': 0, 'failed': 0, 'uptime': '0.0%'}
    try:
        from apps.documentation.services.pages_service import PagesService
        from apps.documentation.services.endpoints_service import EndpointsService
        ps = PagesService()
        es = EndpointsService()
        pr = ps.list_pages(limit=1, offset=0)
        er = es.list_endpoints(limit=1, offset=0)
        stats['total_pages'] = pr.get('total', 0)
        stats['total_endpoints'] = er.get('total', 0)
    except Exception:
        stats['total_pages'] = 0
        stats['total_endpoints'] = 0

    system_status = {
        "s3": _probe_storage_health(request),
        "lambda": _probe_lambda_health(),
        "graphql": _probe_graphql_health(request),
        "database": _probe_db_health(),
        "logs": _probe_logs_health(),
    }
    service_states = list(system_status.values())
    operational_count = sum(1 for state in service_states if state == "operational")
    degraded_count = sum(1 for state in service_states if state == "degraded")
    down_count = sum(1 for state in service_states if state == "down")
    total_services = len(service_states) if service_states else 1
    # Weighted uptime proxy for admin dashboard: operational=1.0, degraded=0.5, down=0.
    uptime_ratio = ((operational_count * 1.0) + (degraded_count * 0.5)) / total_services
    release_gate = _build_release_gate(service_states)
    stats["successful"] = operational_count
    stats["failed"] = down_count
    stats["total_operations"] = total_services
    stats["uptime"] = f"{uptime_ratio * 100:.1f}%"
    context = {
        'system_status': system_status,
        'recent_operations': [],
        'stats': stats,
        'release_gate': release_gate,
    }
    return render(request, 'operations/dashboard.html', context)
