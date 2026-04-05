"""
Admin operations views — users, jobs, logs, billing, storage, system status, settings, statistics.
All views require admin or super_admin role.
"""
import json
import logging
import re
import uuid

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
    adjust_credits,
    approve_payment,
    decline_payment,
    delete_log,
    delete_storage_artifact,
    get_download_url,
    get_job_detail,
    get_jobs,
    get_logs,
    get_payment_instructions,
    get_pending_payments,
    get_storage_artifacts,
    get_system_health,
    get_user_activity_for_user,
    get_user_stats,
    get_users,
    retry_job,
    update_payment_instructions,
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

@require_admin_or_super_admin
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

    users_data = {}
    try:
        users_data = get_users(_token(request), filters=filters, limit=limit, offset=offset)
    except Exception as exc:
        logger.error("users_view error: %s", exc)
        messages.error(request, "Failed to load users. Check gateway connection.")

    return render(request, "admin_ops/users.html", {
        "users": users_data.get("items", []),
        "page_info": users_data.get("pageInfo", {}),
        "search": search, "plan": plan, "role": role, "active": active,
        "current_page": page, "page_title": "Users",
    })


@require_admin_or_super_admin
def user_detail_view(request, user_id):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "adjust_credits":
            amount = int(request.POST.get("amount", 0))
            reason = request.POST.get("reason", "Admin adjustment")
            try:
                result = adjust_credits(_token(request), user_id, amount, reason)
                if result.get("success"):
                    messages.success(request, f"Credits adjusted by {amount}.")
                else:
                    messages.error(request, result.get("error", "Failed to adjust credits."))
            except Exception as exc:
                messages.error(request, f"Error: {exc}")
        return redirect("admin_ops:user_detail", user_id=user_id)

    return render(request, "admin_ops/user_detail.html", {
        "user_id": user_id,
        "page_title": "User Detail",
    })


# ===== Jobs =====

@require_admin_or_super_admin
def jobs_view(request):
    status_filter = request.GET.get("status", "")
    page = max(1, int(request.GET.get("page", 1)))
    limit = 25
    offset = (page - 1) * limit

    jobs_data = {}
    try:
        jobs_data = get_jobs(_token(request), status=status_filter or None, limit=limit, offset=offset)
    except Exception as exc:
        logger.error("jobs_view error: %s", exc)
        messages.error(request, "Failed to load jobs.")

    status_tabs = [
        {"id": "", "label": "All"},
        {"id": "running", "label": "Running"},
        {"id": "queued", "label": "Queued"},
        {"id": "completed", "label": "Completed"},
        {"id": "failed", "label": "Failed"},
        {"id": "cancelled", "label": "Cancelled"},
    ]
    return render(request, "admin_ops/jobs.html", {
        "jobs": jobs_data.get("items", []),
        "page_info": jobs_data.get("pageInfo", {}),
        "status_filter": status_filter,
        "status_tabs": status_tabs,
        "current_page": page,
        "page_title": "Jobs",
    })


@require_admin_or_super_admin
def job_detail_view(request, job_id):
    if request.method == "POST" and request.POST.get("action") == "retry":
        try:
            result = retry_job(_token(request), job_id)
            if result.get("idempotent"):
                messages.info(request, "Job is already in a terminal state or currently running.")
            elif result.get("success"):
                messages.success(request, "Job retry queued successfully.")
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

@require_admin_or_super_admin
def logs_view(request):
    service = request.GET.get("service", "")
    page = max(1, int(request.GET.get("page", 1)))
    limit = 50
    offset = (page - 1) * limit

    log_entries = []
    try:
        log_entries = get_logs(service=service or None, limit=limit, offset=offset)
    except Exception as exc:
        messages.error(request, f"Failed to load logs: {exc}")

    services = ["gateway", "sync", "email", "jobs", "s3storage", "logs", "ai", "extension", "emailcampaign", "mailvetter"]
    return render(request, "admin_ops/logs.html", {
        "logs": log_entries,
        "service": service,
        "services": services,
        "current_page": page,
        "page_title": "Logs",
    })


@require_super_admin
@require_http_methods(["POST"])
def delete_log_view(request, log_id):
    success = delete_log(log_id)
    if success:
        messages.success(request, "Log entry deleted.")
    else:
        messages.error(request, "Failed to delete log entry.")
    return redirect("admin_ops:logs")


# ===== Billing =====

@require_admin_or_super_admin
def billing_view(request):
    payments = []
    try:
        payments = get_pending_payments(_token(request))
    except Exception as exc:
        messages.error(request, f"Failed to load payments: {exc}")

    return render(request, "admin_ops/billing.html", {
        "payments": payments,
        "page_title": "Billing — Pending Payments",
    })


@require_admin_or_super_admin
@require_http_methods(["POST"])
def approve_payment_view(request, payment_id):
    reason = request.POST.get("reason", "")
    try:
        result = approve_payment(_token(request), payment_id, reason)
        if result.get("success"):
            messages.success(request, "Payment approved and credits applied.")
        else:
            messages.error(request, result.get("error", "Approval failed."))
    except Exception as exc:
        messages.error(request, f"Error: {exc}")
    return redirect("admin_ops:billing")


@require_admin_or_super_admin
@require_http_methods(["POST"])
def decline_payment_view(request, payment_id):
    reason = request.POST.get("reason", "")
    if not reason:
        messages.error(request, "Reason is required to decline a payment.")
        return redirect("admin_ops:billing")
    try:
        result = decline_payment(_token(request), payment_id, reason)
        if result.get("success"):
            messages.success(request, "Payment declined.")
        else:
            messages.error(request, result.get("error", "Decline failed."))
    except Exception as exc:
        messages.error(request, f"Error: {exc}")
    return redirect("admin_ops:billing")


# ===== Storage =====

@require_admin_or_super_admin
def storage_view(request):
    prefix = request.GET.get("prefix", "")
    artifacts = []
    try:
        artifacts = get_storage_artifacts(prefix=prefix)
    except Exception as exc:
        messages.error(request, f"Failed to load storage: {exc}")

    return render(request, "admin_ops/storage.html", {
        "artifacts": artifacts,
        "prefix": prefix,
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
    if not key:
        messages.error(request, "No key specified.")
        return redirect("admin_ops:storage")
    success = delete_storage_artifact(key)
    if success:
        messages.success(request, f"Deleted: {key}")
    else:
        messages.error(request, "Delete failed.")
    return redirect("admin_ops:storage")


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
    uptime_pct = round((up_count / total) * 100) if total else 0

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
    stats = {}
    try:
        stats = get_user_stats(_token(request))
    except Exception as exc:
        messages.error(request, f"Failed to load statistics: {exc}")

    by_plan = stats.get("usersBySubscription", [])
    chart_data = {
        "labels": [p["subscriptionPlan"] for p in by_plan],
        "values": [p["count"] for p in by_plan],
    }
    return render(request, "admin_ops/statistics.html", {
        "stats": stats,
        "chart_data": chart_data,
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
            messages.success(request, "Job retry queued successfully.")
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
