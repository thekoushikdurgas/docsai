"""
Admin operations views — users, jobs, logs, billing, storage, system status, settings, statistics.
All views require admin or super_admin role.
"""
import json
import logging
import re
import uuid
from typing import Any, Dict

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.core.decorators import require_admin_or_super_admin, require_login, require_super_admin
from apps.core.exceptions import LambdaAPIError

from .services.admin_client import (
    AdminGraphQLError,
    adjust_credits,
    approve_payment,
    decline_payment,
    delete_log,
    delete_storage_artifact,
    delete_user_account,
    find_admin_user,
    get_download_url,
    get_job_detail,
    get_jobs,
    get_logs,
    get_payment_instructions,
    get_pending_payments,
    get_storage_artifacts,
    get_system_health,
    get_users_with_buckets,
    get_user_activity_for_user,
    get_user_stats,
    get_users,
    promote_to_admin,
    promote_to_super_admin,
    retry_job,
    update_payment_instructions,
    update_user_role,
)
from .services.logs_api_client import LogsApiClient
from .services.s3storage_client import S3StorageClient
from .utils import time_range_to_iso

logger = logging.getLogger(__name__)

LOGS_API_ENABLED = getattr(settings, "LOGS_API_ENABLED", bool(getattr(settings, "LOGS_API_URL", "")))
S3STORAGE_ENABLED = bool(getattr(settings, "S3STORAGE_API_URL", ""))


def _request_trace_id(request) -> str:
    return (
        request.META.get("HTTP_X_REQUEST_ID")
        or request.META.get("HTTP_X_CORRELATION_ID")
        or str(uuid.uuid4())
    )


def _is_idempotent_noop_error(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None)
    if status_code in (404, 409):
        return True
    message = str(exc).lower()
    markers = ("not found", "already deleted", "already declined", "already approved")
    return any(marker in message for marker in markers)


def _validate_billing_settings_input(
    upi_id: str,
    phone_number: str,
    email: str,
    qr_code_s3_key: str | None,
) -> list:
    errors = []
    if not upi_id:
        errors.append("UPI ID is required.")
    elif not re.match(r"^[A-Za-z0-9._-]{2,256}@[A-Za-z]{2,64}$", upi_id):
        errors.append("UPI ID format is invalid.")
    if phone_number:
        normalized = phone_number.replace(" ", "").replace("-", "")
        if normalized.startswith("+"):
            normalized = normalized[1:]
        if not normalized.isdigit() or not (8 <= len(normalized) <= 15):
            errors.append("Phone number must be 8-15 digits (optional leading +).")
    if email:
        try:
            validate_email(email)
        except DjangoValidationError:
            errors.append("Email format is invalid.")
    if qr_code_s3_key:
        key = qr_code_s3_key.strip()
        if ".." in key or key.startswith("/") or key.endswith("/"):
            errors.append("QR key path is invalid.")
        if key and not key.startswith("photo/"):
            errors.append("QR key must be under photo/ prefix.")
    return errors


def _token(request) -> str:
    return request.session.get("operator", {}).get("token", "")


def _get_payment_qr_bucket(request) -> str | None:
    bucket = getattr(settings, "PAYMENT_QR_BUCKET_ID", None) or ""
    if bucket:
        return bucket
    try:
        data = get_users(_token(request), limit=10, offset=0)
        for u in data.get("items", []):
            b = u.get("uuid") or ""
            if b:
                return b
    except Exception:
        pass
    return None


# ===== Users =====

def _users_page_querystring(request, page_num: int) -> str:
    q = request.GET.copy()
    if page_num <= 1:
        q.pop("page", None)
    else:
        q["page"] = str(page_num)
    return q.urlencode()


def _users_list_auth_message(exc: AdminGraphQLError) -> str:
    msg = str(exc)
    if msg == "Authentication required" or "Authentication required" in msg:
        return (
            "The API did not accept any signed-in user (missing or invalid JWT). "
            "Sign out and sign in with your Contact360 email and password so an access token is stored. "
            "If you used local Django sign-in only, set GRAPHQL_INTERNAL_TOKEN or use gateway login. "
            "This directory requires a Super Admin account on the gateway."
        )
    if "Insufficient permissions" in msg or msg == "SuperAdmin role required":
        return (
            "Listing users requires Super Admin on the gateway. "
            "Ask a Super Admin to promote your account, or use a Super Admin login."
        )
    return f"Failed to load users: {msg}"


@require_super_admin
def users_view(request):
    search = request.GET.get("search", "")
    plan = request.GET.get("plan", "")
    role = request.GET.get("role", "")
    active = request.GET.get("active", "")
    page = max(1, int(request.GET.get("page", 1)))
    limit = 25
    offset = (page - 1) * limit

    filters = {}
    if search:
        filters["search"] = search
    if plan:
        filters["subscriptionPlan"] = plan
    if role:
        filters["role"] = role
    if active:
        filters["isActive"] = active == "true"

    filters_active = bool(search or plan or role or active)
    users_data: dict = {}
    users_load_failed = False

    session_tok = (_token(request) or "").strip()
    internal_tok = (getattr(settings, "GRAPHQL_INTERNAL_TOKEN", None) or "").strip()
    if not session_tok and not internal_tok:
        users_load_failed = True
        messages.error(
            request,
            "No gateway credentials available for this browser session (empty JWT and no "
            "GRAPHQL_INTERNAL_TOKEN). Sign in with Contact360 email/password, or configure "
            "GRAPHQL_INTERNAL_TOKEN for server-to-server access.",
        )
    else:
        try:
            users_data = get_users(_token(request), filters=filters, limit=limit, offset=offset)
        except AdminGraphQLError as exc:
            users_load_failed = True
            logger.error("users_view GraphQL error: %s", exc)
            messages.error(request, _users_list_auth_message(exc))
        except Exception as exc:
            users_load_failed = True
            logger.error("users_view error: %s", exc)
            messages.error(request, "Failed to load users. Check gateway connection.")

    page_info = users_data.get("pageInfo", {}) if isinstance(users_data, dict) else {}
    items = users_data.get("items", []) if isinstance(users_data, dict) else []

    if users_load_failed:
        users_subtitle_mode = "error"
        users_total = None
    elif isinstance(page_info, dict) and "total" in page_info and page_info.get("total") is not None:
        users_subtitle_mode = "count"
        try:
            users_total = int(page_info["total"])
        except (TypeError, ValueError):
            users_subtitle_mode = "unknown"
            users_total = None
    else:
        users_subtitle_mode = "unknown"
        users_total = None

    pagination_query_prev = ""
    pagination_query_next = ""
    if not users_load_failed and isinstance(page_info, dict):
        total = page_info.get("total")
        try:
            total_n = int(total) if total is not None else 0
        except (TypeError, ValueError):
            total_n = 0
        if total_n > limit:
            if page_info.get("hasPrevious"):
                pagination_query_prev = _users_page_querystring(request, page - 1)
            if page_info.get("hasNext"):
                pagination_query_next = _users_page_querystring(request, page + 1)

    return render(request, "admin_ops/users.html", {
        "users": items,
        "page_info": page_info if isinstance(page_info, dict) else {},
        "search": search, "plan": plan, "role": role, "active": active,
        "current_page": page, "page_title": "Users",
        "filters_active": filters_active,
        "users_load_failed": users_load_failed,
        "users_subtitle_mode": users_subtitle_mode,
        "users_total": users_total,
        "pagination_query_prev": pagination_query_prev,
        "pagination_query_next": pagination_query_next,
    })


@require_admin_or_super_admin
def user_detail_view(request, user_id):
    if request.method == "POST":
        action = request.POST.get("action")
        tok = _token(request)
        try:
            if action == "adjust_credits":
                amount = int(request.POST.get("amount", 0))
                reason = request.POST.get("reason", "Admin adjustment")
                result = adjust_credits(tok, user_id, amount, reason)
                if result.get("success"):
                    messages.success(request, f"Credits updated (delta {amount:+d}).")
                else:
                    messages.error(request, result.get("error", "Failed to adjust credits."))
            elif action == "update_role":
                role = (request.POST.get("role") or "").strip()
                result = update_user_role(tok, user_id, role)
                if result.get("success"):
                    messages.success(request, f"Role set to {role}.")
                else:
                    messages.error(request, result.get("error", "Failed to update role."))
            elif action == "delete_user":
                result = delete_user_account(tok, user_id)
                if result.get("success"):
                    messages.success(request, "User deleted.")
                    return redirect("admin_ops:users")
                messages.error(request, result.get("error", "Failed to delete user."))
            elif action == "promote_admin":
                result = promote_to_admin(tok, user_id)
                if result.get("success"):
                    messages.success(request, "User promoted to Admin.")
                else:
                    messages.error(request, result.get("error", "Promote to Admin failed."))
            elif action == "promote_super":
                result = promote_to_super_admin(tok, user_id)
                if result.get("success"):
                    messages.success(request, "User promoted to SuperAdmin.")
                else:
                    messages.error(request, result.get("error", "Promote to SuperAdmin failed."))
            else:
                messages.error(request, "Unknown action.")
        except Exception as exc:
            messages.error(request, f"Error: {exc}")
        return redirect("admin_ops:user_detail", user_id=user_id)

    user_row = None
    try:
        user_row = find_admin_user(_token(request), user_id)
    except Exception as exc:
        logger.warning("user_detail find_admin_user: %s", exc)

    return render(request, "admin_ops/user_detail.html", {
        "user_id": user_id,
        "user_row": user_row,
        "page_title": "User Detail",
        "valid_roles": ["FreeUser", "ProUser", "Admin", "SuperAdmin"],
    })


# ===== Jobs =====

def _jobs_page_querystring(request, page_num: int) -> str:
    q = request.GET.copy()
    if page_num <= 1:
        q.pop("page", None)
    else:
        q["page"] = str(page_num)
    return q.urlencode()


@require_admin_or_super_admin
def jobs_view(request):
    status_filter = request.GET.get("status", "")
    source_filter = (request.GET.get("source") or "").strip()
    if source_filter not in ("email_server", "sync_server"):
        source_filter = ""
    page = max(1, int(request.GET.get("page", 1)))
    limit = 25
    offset = (page - 1) * limit

    jobs_data: dict = {}
    jobs_load_failed = False
    try:
        jobs_data = get_jobs(
            _token(request),
            status=status_filter or None,
            limit=limit,
            offset=offset,
            source_service=source_filter or None,
        )
    except Exception as exc:
        jobs_load_failed = True
        logger.error("jobs_view error: %s", exc)
        messages.error(request, "Failed to load jobs.")

    page_info = jobs_data.get("pageInfo", {}) if isinstance(jobs_data, dict) else {}
    pagination_query_prev = ""
    pagination_query_next = ""
    if not jobs_load_failed and isinstance(page_info, dict):
        try:
            total_n = int(page_info.get("total") or 0)
        except (TypeError, ValueError):
            total_n = 0
        if total_n > limit:
            if page_info.get("hasPrevious"):
                pagination_query_prev = _jobs_page_querystring(request, page - 1)
            if page_info.get("hasNext"):
                pagination_query_next = _jobs_page_querystring(request, page + 1)

    # Tab IDs match ``scheduler_job_status`` / gateway DB (not legacy "running"/"queued" aliases).
    status_tabs = [
        {"id": "", "label": "All"},
        {"id": "open", "label": "Open"},
        {"id": "in_queue", "label": "In queue"},
        {"id": "processing", "label": "Processing"},
        {"id": "completed", "label": "Completed"},
        {"id": "failed", "label": "Failed"},
        {"id": "retry", "label": "Retry"},
    ]
    return render(request, "admin_ops/jobs.html", {
        "jobs": jobs_data.get("items", []),
        "page_info": page_info,
        "status_filter": status_filter,
        "source_filter": source_filter,
        "status_tabs": status_tabs,
        "current_page": page,
        "page_title": "Jobs",
        "jobs_load_failed": jobs_load_failed,
        "pagination_query_prev": pagination_query_prev,
        "pagination_query_next": pagination_query_next,
    })


@require_admin_or_super_admin
def job_detail_view(request, job_id):
    if request.method == "POST" and request.POST.get("action") == "retry":
        try:
            result = retry_job(_token(request), job_id)
            if result.get("idempotent"):
                messages.info(request, "Job is already in a terminal state or currently running.")
            elif result.get("success"):
                detail = (result.get("detail") or "").strip()
                messages.success(
                    request,
                    detail or "Retry recorded on the gateway (sync jobs: local status reset to open).",
                )
            else:
                messages.error(request, result.get("error", "Retry failed."))
        except Exception as exc:
            messages.error(request, f"Retry error: {exc}")
        return redirect("admin_ops:job_detail", job_id=job_id)

    job = None
    try:
        job = get_job_detail(_token(request), job_id)
    except Exception as exc:
        messages.error(request, f"Failed to load job: {exc}")

    return render(request, "admin_ops/job_detail.html", {
        "job": job, "job_id": job_id,
        "page_title": f"Job {job_id[:8]}…" if job_id else "Job Detail",
    })


# ===== Logs =====

def _logs_page_querystring(request, page_num: int) -> str:
    q = request.GET.copy()
    if page_num <= 1:
        q.pop("page", None)
    else:
        q["page"] = str(page_num)
    return q.urlencode()


@require_super_admin
def logs_view(request):
    """
    Log.server data is loaded via GraphQL ``admin.logs`` (same path as API ``LogsServerClient``).
    Requires Super Admin on the gateway — matches ``admin.queries.AdminQuery.logs``.
    """
    service = request.GET.get("service", "")
    level = (request.GET.get("level") or "").strip().upper() or ""
    if level and level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "WARN"):
        level = ""
    if level == "WARN":
        level = "WARNING"
    page = max(1, int(request.GET.get("page", 1)))
    limit = 50
    offset = (page - 1) * limit

    log_payload: Dict[str, Any] = {"items": [], "pageInfo": {}}
    logs_load_failed = False
    try:
        log_payload = get_logs(
            _token(request),
            logger=service or None,
            level=level or None,
            limit=limit,
            offset=offset,
        )
    except Exception as exc:
        logs_load_failed = True
        logger.error("logs_view error: %s", exc)
        messages.error(
            request,
            "Failed to load logs from the gateway. "
            "Use a Super Admin session, or check GraphQL and log.server configuration.",
        )

    page_info = log_payload.get("pageInfo") or {}
    pagination_query_prev = ""
    pagination_query_next = ""
    if not logs_load_failed and isinstance(page_info, dict):
        try:
            total_n = int(page_info.get("total") or 0)
        except (TypeError, ValueError):
            total_n = 0
        if total_n > limit:
            if page_info.get("hasPrevious"):
                pagination_query_prev = _logs_page_querystring(request, page - 1)
            if page_info.get("hasNext"):
                pagination_query_next = _logs_page_querystring(request, page + 1)

    services = [
        "gateway",
        "sync",
        "email",
        "jobs",
        "s3storage",
        "logs",
        "ai",
        "extension",
        "emailcampaign",
        "mailvetter",
    ]
    return render(request, "admin_ops/logs.html", {
        "logs": log_payload.get("items", []),
        "service": service,
        "level_filter": level,
        "services": services,
        "current_page": page,
        "page_title": "Logs",
        "page_info": page_info,
        "logs_load_failed": logs_load_failed,
        "pagination_query_prev": pagination_query_prev,
        "pagination_query_next": pagination_query_next,
    })


@require_super_admin
@require_http_methods(["POST"])
def delete_log_view(request, log_id):
    success = delete_log(_token(request), log_id)
    if success:
        messages.success(request, "Log entry deleted.")
    else:
        messages.error(request, "Failed to delete log entry.")
    return redirect("admin_ops:logs")


# ===== Billing =====

@require_admin_or_super_admin
def billing_view(request):
    status_filter = request.GET.get("status", "pending")
    try:
        page = max(0, int(request.GET.get("page", 0)))
    except (ValueError, TypeError):
        page = 0
    limit = 25
    offset = page * limit

    payment_data = {"items": [], "total": 0, "hasNext": False, "hasPrevious": False}
    try:
        payment_data = get_pending_payments(
            _token(request), status=status_filter or None, limit=limit, offset=offset
        )
    except Exception as exc:
        messages.error(request, f"Failed to load payments: {exc}")

    return render(request, "admin_ops/billing.html", {
        "payments": payment_data["items"],
        "total": payment_data["total"],
        "has_next": payment_data["hasNext"],
        "has_previous": payment_data["hasPrevious"],
        "page": page,
        "status_filter": status_filter,
        "status_tabs": [
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("declined", "Declined"),
            ("", "All"),
        ],
        "page_title": "Billing — Payment Submissions",
    })


@require_admin_or_super_admin
@require_http_methods(["POST"])
def approve_payment_view(request, payment_id):
    try:
        result = approve_payment(_token(request), payment_id)
        if result.get("id"):
            messages.success(request, f"Payment approved. Credits: {result.get('creditsToAdd', '—')}")
        else:
            messages.error(request, "Approval failed — no response from gateway.")
    except Exception as exc:
        messages.error(request, f"Error: {exc}")
    return redirect("admin_ops:billing")


@require_admin_or_super_admin
@require_http_methods(["POST"])
def decline_payment_view(request, payment_id):
    reason = request.POST.get("reason", "").strip()
    if not reason:
        messages.error(request, "Reason is required to decline a payment.")
        return redirect("admin_ops:billing")
    try:
        result = decline_payment(_token(request), payment_id, reason)
        if result.get("id"):
            messages.success(request, "Payment declined.")
        else:
            messages.error(request, "Decline failed — no response from gateway.")
    except Exception as exc:
        messages.error(request, f"Error: {exc}")
    return redirect("admin_ops:billing")


# ===== Storage =====

@require_admin_or_super_admin
def storage_view(request):
    selected_bucket = request.GET.get("bucket", "").strip()
    prefix = request.GET.get("prefix", "").strip()
    try:
        page = max(0, int(request.GET.get("page", 0)))
    except (ValueError, TypeError):
        page = 0
    limit = 50
    offset = page * limit

    users = get_users_with_buckets(_token(request))
    # Map bucket -> user for easy lookup in template
    bucket_to_user = {u["bucket"]: u for u in users if u.get("bucket")}

    artifacts: list = []
    total = 0
    has_next = False
    has_previous = False

    if selected_bucket:
        full_prefix = f"{selected_bucket}/{prefix}".lstrip("/") if prefix else selected_bucket
        try:
            result = get_storage_artifacts(prefix=full_prefix, limit=limit, offset=offset)
            artifacts = result["items"]
            total = result["total"]
            has_next = offset + limit < total
            has_previous = offset > 0
        except Exception as exc:
            messages.error(request, f"Failed to load storage: {exc}")

    # Build breadcrumb segments from prefix
    breadcrumb_parts = []
    if selected_bucket:
        breadcrumb_parts.append({"label": "All", "bucket": "", "prefix": ""})
        selected_user = bucket_to_user.get(selected_bucket)
        user_label = selected_user["email"] if selected_user else selected_bucket[:12]
        breadcrumb_parts.append({"label": user_label, "bucket": selected_bucket, "prefix": ""})
        if prefix:
            segments = [s for s in prefix.split("/") if s]
            for i, seg in enumerate(segments):
                breadcrumb_parts.append({
                    "label": seg,
                    "bucket": selected_bucket,
                    "prefix": "/".join(segments[: i + 1]),
                })

    return render(request, "admin_ops/storage.html", {
        "artifacts": artifacts,
        "total": total,
        "has_next": has_next,
        "has_previous": has_previous,
        "page": page,
        "prefix": prefix,
        "selected_bucket": selected_bucket,
        "users": users,
        "breadcrumbs": breadcrumb_parts,
        "page_title": "Storage",
    })


@require_admin_or_super_admin
def storage_download_url_view(request):
    key = request.GET.get("key", "")
    url = get_download_url(key)
    if url:
        return JsonResponse({"url": url})
    return JsonResponse({"error": "Could not generate download URL"}, status=400)


@require_super_admin
@require_http_methods(["POST"])
def delete_artifact_view(request):
    key = request.POST.get("key", "")
    selected_bucket = request.POST.get("bucket", "")
    prefix = request.POST.get("prefix", "")
    if not key:
        messages.error(request, "No key specified.")
        return redirect("admin_ops:storage")
    success = delete_storage_artifact(key)
    if success:
        messages.success(request, f"Deleted: {key}")
    else:
        messages.error(request, "Delete failed.")
    redirect_url = f"{redirect('admin_ops:storage').url}?bucket={selected_bucket}&prefix={prefix}"
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(redirect_url)


# ===== System status =====

@require_login
def system_status_view(request):
    health = []
    try:
        health = get_system_health()
    except Exception as exc:
        messages.error(request, f"Health probe failed: {exc}")

    up_count = sum(1 for s in health if s.get("status") == "up")
    total = len(health)
    # Uptime % only among services that are actually probed (exclude "not configured")
    probed = [s for s in health if s.get("status") != "not_configured"]
    up_probed = sum(1 for s in probed if s.get("status") == "up")
    uptime_pct = round((up_probed / len(probed)) * 100) if probed else 0

    return render(request, "admin_ops/system_status.html", {
        "health_services": health,
        "up_count": up_count,
        "total_services": total,
        "uptime_pct": uptime_pct,
        "page_title": "System Status",
    })


# ===== Settings =====

@require_super_admin
def settings_view(request):
    from django.conf import settings as dj_settings
    config_snapshot = {
        "GRAPHQL_URL": dj_settings.GRAPHQL_URL,
        "LOGS_API_URL": dj_settings.LOGS_API_URL,
        "S3STORAGE_API_URL": dj_settings.S3STORAGE_API_URL,
        "AI_API_URL": dj_settings.AI_API_URL,
        "EMAILCAMPAIGN_URL": dj_settings.EMAILCAMPAIGN_URL,
        "DEBUG": dj_settings.DEBUG,
        "DOCS_AGENT_VERSION": dj_settings.DOCS_AGENT_VERSION,
    }
    return render(request, "admin_ops/settings.html", {
        "config": config_snapshot,
        "page_title": "Settings (Read-only)",
    })


# ===== Statistics =====

@require_admin_or_super_admin
def statistics_view(request):
    stats: dict = {}
    try:
        stats = get_user_stats(_token(request))
    except Exception as exc:
        messages.error(request, f"Failed to load statistics: {exc}")

    # Gateway AdminUserStats: usersByPlan / usersByRole are JSON objects { "free": 12, ... }
    # Accept camelCase (typical GraphQL JSON) or snake_case.
    by_plan = stats.get("usersByPlan") if isinstance(stats.get("usersByPlan"), dict) else {}
    if not by_plan and isinstance(stats.get("users_by_plan"), dict):
        by_plan = stats["users_by_plan"]
    plan_items = sorted(by_plan.items(), key=lambda x: (-(x[1] or 0), str(x[0]).lower()))
    chart_data = {
        "labels": [str(k) for k, _ in plan_items],
        "values": [int(v or 0) for _, v in plan_items],
    }

    by_role = stats.get("usersByRole") if isinstance(stats.get("usersByRole"), dict) else {}
    if not by_role and isinstance(stats.get("users_by_role"), dict):
        by_role = stats["users_by_role"]
    role_items = sorted(by_role.items(), key=lambda x: (-(x[1] or 0), str(x[0]).lower()))

    return render(request, "admin_ops/statistics.html", {
        "stats": stats,
        "chart_data": chart_data,
        "plan_items": plan_items,
        "role_items": role_items,
        "page_title": "Statistics",
    })


# ===== Per-user activity (GraphQL userHistory / userActivity parity) =====


@require_super_admin
def user_history_view(request, user_id: str):
    page = max(1, int(request.GET.get("page", 1)))
    event_type = request.GET.get("event_type", "all")
    per_page = 15
    offset = (page - 1) * per_page
    error = None
    try:
        result = get_user_activity_for_user(
            _token(request),
            user_id,
            limit=per_page,
            offset=offset,
            event_type=event_type if event_type not in ("all", "") else None,
        )
        history = result.get("items", [])
        total = result.get("total", 0)
        err = result.get("error")
        if err:
            error = err
    except Exception as exc:
        logger.exception("user_history_view")
        history, total, error = [], 0, str(exc)

    total_pages = max(1, (total + per_page - 1) // per_page) if total else 1
    return render(
        request,
        "admin_ops/user_history.html",
        {
            "user_id": user_id,
            "history": history,
            "total": total,
            "error": error,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "event_type": event_type,
            "page_title": f"User activity — {user_id[:8]}…",
        },
    )


@require_admin_or_super_admin
@require_http_methods(["POST"])
def logs_bulk_delete_view(request):
    if not LOGS_API_ENABLED:
        return JsonResponse({"success": False, "error": "Logs API is not enabled"}, status=400)
    try:
        body = json.loads(request.body) if request.body else {}
        time_range = (body.get("time_range") or "").strip()
        level = (body.get("level") or "").strip() or None
        logger_filter = (body.get("logger") or "").strip() or None
        user_id = (body.get("user_id") or "").strip() or None
        start_time = body.get("start_time") or None
        end_time = body.get("end_time") or None
        if time_range and not start_time and not end_time:
            start_time, end_time = time_range_to_iso(time_range)
        client = LogsApiClient(request_id=_request_trace_id(request))
        result = client.delete_logs_bulk(
            level=level,
            logger=logger_filter,
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
        )
        return JsonResponse(
            {
                "success": True,
                "deleted_count": result.get("deleted_count"),
                "status": result.get("status"),
                "message": result.get("message"),
            }
        )
    except LambdaAPIError as e:
        if _is_idempotent_noop_error(e):
            return JsonResponse(
                {
                    "success": True,
                    "deleted_count": 0,
                    "status": "noop",
                    "message": "No matching logs to delete",
                }
            )
        return JsonResponse({"success": False, "error": str(e)}, status=getattr(e, "status_code", 500))
    except Exception as e:
        logger.exception("logs_bulk_delete_view")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_admin_or_super_admin
@require_http_methods(["POST"])
def log_update_view(request, log_id: str):
    if not LOGS_API_ENABLED:
        return JsonResponse({"success": False, "error": "Logs API is not enabled"}, status=400)
    try:
        body = json.loads(request.body) if request.body else {}
        message = body.get("message")
        context = body.get("context")
        if message is None and context is None:
            return JsonResponse(
                {"success": False, "error": "Provide at least message or context"},
                status=400,
            )
        client = LogsApiClient(request_id=_request_trace_id(request))
        log = client.update_log(log_id=log_id, message=message, context=context)
        return JsonResponse({"success": True, "data": log})
    except LambdaAPIError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=getattr(e, "status_code", 500))
    except Exception as e:
        logger.exception("log_update_view")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_admin_or_super_admin
@require_http_methods(["POST"])
def job_retry_view(request, job_id: str):
    try:
        result = retry_job(_token(request), job_id)
        if result.get("idempotent"):
            messages.info(request, "Job is already in a terminal state or currently running.")
        elif result.get("success"):
            detail = (result.get("detail") or "").strip()
            messages.success(
                request,
                detail or "Retry recorded on the gateway (sync jobs: local status reset to open).",
            )
        else:
            messages.error(request, result.get("error", "Retry failed."))
    except Exception as exc:
        messages.error(request, f"Retry error: {exc}")
    return redirect("admin_ops:job_detail", job_id=job_id)


@require_super_admin
def billing_qr_upload_view(request):
    if request.method == "GET":
        return render(
            request,
            "admin_ops/billing_qr_upload.html",
            {"page_title": "Upload payment QR", "payment_qr_bucket": _get_payment_qr_bucket(request)},
        )
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)
    if not S3STORAGE_ENABLED:
        return JsonResponse({"success": False, "error": "Storage is not configured"}, status=400)
    bucket_id = _get_payment_qr_bucket(request)
    if not bucket_id:
        return JsonResponse(
            {
                "success": False,
                "error": "No bucket available. Set PAYMENT_QR_BUCKET_ID or ensure users have buckets.",
            },
            status=400,
        )
    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"success": False, "error": "No file provided"}, status=400)
    allowed = ("image/png", "image/jpeg", "image/jpg", "image/webp")
    ct = (getattr(file, "content_type", "") or "").lower()
    if ct not in allowed:
        return JsonResponse(
            {"success": False, "error": f"Invalid type. Allowed: {', '.join(allowed)}"},
            status=400,
        )
    try:
        s3_client = S3StorageClient(request_id=_request_trace_id(request))
        result = s3_client.upload_photo(bucket_id=bucket_id, file=file)
        file_key = result.get("fileKey", "")
        return JsonResponse({"success": True, "fileKey": file_key, "bucketId": bucket_id})
    except LambdaAPIError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=getattr(e, "status_code", 500))
    except Exception as e:
        logger.exception("billing_qr_upload_view")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_super_admin
@require_http_methods(["GET", "POST"])
def billing_settings_view(request):
    context = {
        "error": None,
        "success": None,
        "settings": None,
        "s3_enabled": S3STORAGE_ENABLED,
        "payment_qr_bucket": _get_payment_qr_bucket(request),
    }
    if request.method == "POST":
        upi_id = (request.POST.get("upi_id") or "").strip()
        phone_number = (request.POST.get("phone_number") or "").strip()
        email = (request.POST.get("email") or "").strip()
        qr_code_s3_key = (request.POST.get("qr_code_s3_key") or "").strip() or None
        qr_code_bucket_id = (request.POST.get("qr_code_bucket_id") or "").strip() or None
        errors = _validate_billing_settings_input(
            upi_id=upi_id,
            phone_number=phone_number,
            email=email,
            qr_code_s3_key=qr_code_s3_key,
        )
        if errors:
            context["error"] = " ".join(errors)
            return render(request, "admin_ops/billing_settings.html", context)
        payload = {
            "upiId": upi_id,
            "phoneNumber": phone_number,
            "email": email,
            "qrCodeS3Key": qr_code_s3_key,
        }
        if qr_code_bucket_id:
            payload["qrCodeBucketId"] = qr_code_bucket_id
        try:
            updated = update_payment_instructions(_token(request), payload)
            context["settings"] = updated or {}
            context["success"] = "Payment instructions updated."
        except Exception as exc:
            logger.exception("billing_settings_view post")
            context["error"] = str(exc)

    if context["settings"] is None:
        try:
            context["settings"] = get_payment_instructions(_token(request)) or {}
        except Exception as exc:
            logger.exception("billing_settings_view load")
            context["error"] = str(exc)
            context["settings"] = {}

    return render(request, "admin_ops/billing_settings.html", context)
