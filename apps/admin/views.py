"""Admin views - users, stats, history, logs, system status, settings."""
import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from apps.core.decorators.auth import require_super_admin, require_admin_or_super_admin
from apps.core.clients.appointment360_client import Appointment360Client
from apps.core.exceptions import LambdaAPIError
from apps.core.services.graphql_client import GraphQLError
from .services.admin_client import AdminGraphQLClient
from .services.logs_api_client import LogsApiClient
from .services.tkdjob_client import TkdJobClient
from .services.s3storage_client import S3StorageClient
from .utils import build_logs_query_params, build_jobs_query_params, time_range_to_iso

logger = logging.getLogger(__name__)

LOGS_API_ENABLED = getattr(settings, "LOGS_API_ENABLED", False)
JOB_SCHEDULER_ENABLED = getattr(settings, "JOB_SCHEDULER_ENABLED", False)
S3STORAGE_ENABLED = getattr(settings, "S3STORAGE_ENABLED", False)
VALID_PER_PAGE = (10, 25, 50, 100)
VALID_JOBS_LIMIT = (10, 25, 50, 100)


def _get_client(request):
    return AdminGraphQLClient(request)


@require_super_admin
def billing_payments_view(request):
    status_filter = (request.GET.get("status") or "").strip() or None
    page = max(1, int(request.GET.get("page", 1)))
    per_page = 25
    offset = (page - 1) * per_page

    context = {
        "items": [],
        "total": 0,
        "error": None,
        "page": page,
        "per_page": per_page,
        "total_pages": 0,
        "status": status_filter or "all",
        "s3_enabled": S3STORAGE_ENABLED,
    }

    try:
        client = _get_client(request)
        result = client.list_payment_submissions(
            status=status_filter if status_filter != "all" else None,
            limit=per_page,
            offset=offset,
        )
        context["items"] = result.get("items", [])
        context["total"] = result.get("total", 0)
        context["total_pages"] = max(1, (context["total"] + per_page - 1) // per_page)
    except GraphQLError as e:
        logger.warning("Admin billing payments GraphQL error: %s", e)
        context["error"] = str(e)
    except Exception as e:
        logger.exception("Admin billing payments error")
        context["error"] = str(e)

    return render(request, "admin/billing_payments.html", context)


@require_super_admin
@require_http_methods(["POST"])
def billing_payment_approve_view(request, submission_id: str):
    try:
        client = _get_client(request)
        client.approve_payment_submission(submission_id=submission_id)
    except Exception as e:
        logger.exception("Approve payment submission error")
        # fall through, redirect back with best-effort
    return redirect("/admin/billing/payments/?status=pending")


@require_super_admin
@require_http_methods(["POST"])
def billing_payment_decline_view(request, submission_id: str):
    reason = (request.POST.get("reason") or "").strip()
    if not reason:
        reason = "Declined by admin"
    try:
        client = _get_client(request)
        client.decline_payment_submission(submission_id=submission_id, reason=reason)
    except Exception as e:
        logger.exception("Decline payment submission error")
    return redirect("/admin/billing/payments/?status=pending")


def _get_payment_qr_bucket(request):
    """Resolve bucket for payment QR upload. PAYMENT_QR_BUCKET_ID or first from users."""
    bucket = getattr(settings, "PAYMENT_QR_BUCKET_ID", None) or ""
    if bucket:
        return bucket
    try:
        client = _get_client(request)
        users = client.list_users_with_buckets(limit=10)
        for u in users:
            b = u.get("bucket") or u.get("uuid")
            if b:
                return b
    except Exception:
        pass
    return None


@require_super_admin
@require_http_methods(["POST"])
def billing_qr_upload_view(request):
    """Upload QR image to photo/ folder. Returns JSON {success, fileKey, bucketId, error?}."""
    if not S3STORAGE_ENABLED:
        return JsonResponse(
            {"success": False, "error": "Storage is not configured"},
            status=400,
        )
    bucket_id = _get_payment_qr_bucket(request)
    if not bucket_id:
        return JsonResponse(
            {"success": False, "error": "No bucket available. Configure PAYMENT_QR_BUCKET_ID or ensure users have buckets."},
            status=400,
        )
    file = request.FILES.get("file")
    if not file:
        return JsonResponse(
            {"success": False, "error": "No file provided"},
            status=400,
        )
    allowed = ("image/png", "image/jpeg", "image/jpg", "image/webp")
    ct = getattr(file, "content_type", "") or ""
    if ct.lower() not in allowed:
        return JsonResponse(
            {"success": False, "error": f"Invalid type. Allowed: {', '.join(allowed)}"},
            status=400,
        )
    try:
        s3_client = S3StorageClient()
        result = s3_client.upload_photo(bucket_id=bucket_id, file=file)
        file_key = result.get("fileKey", "")
        return JsonResponse({
            "success": True,
            "fileKey": file_key,
            "bucketId": bucket_id,
        })
    except LambdaAPIError as e:
        logger.warning("Billing QR upload error: %s", e)
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=getattr(e, "status_code", 500),
        )
    except Exception as e:
        logger.exception("Billing QR upload error")
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


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
    client = _get_client(request)

    if request.method == "POST":
        upi_id = (request.POST.get("upi_id") or "").strip()
        phone_number = (request.POST.get("phone_number") or "").strip()
        email = (request.POST.get("email") or "").strip()
        qr_code_s3_key = (request.POST.get("qr_code_s3_key") or "").strip() or None
        qr_code_bucket_id = (request.POST.get("qr_code_bucket_id") or "").strip() or None
        try:
            payload = {
                "upiId": upi_id,
                "phoneNumber": phone_number,
                "email": email,
                "qrCodeS3Key": qr_code_s3_key,
            }
            if qr_code_bucket_id:
                payload["qrCodeBucketId"] = qr_code_bucket_id
            updated = client.update_payment_instructions(payload)
            context["settings"] = updated
            context["success"] = "Payment instructions updated."
        except GraphQLError as e:
            logger.warning("Admin billing settings GraphQL error: %s", e)
            context["error"] = str(e)
        except Exception as e:
            logger.exception("Admin billing settings error")
            context["error"] = str(e)

    if context["settings"] is None:
        try:
            context["settings"] = client.get_payment_instructions() or {}
        except Exception as e:
            logger.exception("Admin billing settings load error")
            context["error"] = str(e)

    return render(request, "admin/billing_settings.html", context)


@require_super_admin
def users_view(request):
    """User Management - SuperAdmin only."""
    page = int(request.GET.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page
    context = {"users": [], "total": 0, "error": None, "page": page, "per_page": per_page, "total_pages": 0}
    try:
        client = _get_client(request)
        result = client.list_users(limit=per_page, offset=offset)
        context["users"] = result.get("users", [])
        context["total"] = result.get("total", 0)
        context["total_pages"] = max(1, (context["total"] + per_page - 1) // per_page)
    except GraphQLError as e:
        logger.warning("Admin users GraphQL error: %s", e)
        context["error"] = str(e)
    except Exception as e:
        logger.exception("Admin users error")
        context["error"] = str(e)
    return render(request, "admin/users.html", context)


@require_super_admin
def user_history_view(request):
    """User History - SuperAdmin only."""
    page = int(request.GET.get("page", 1))
    event_type = request.GET.get("event_type", "all")
    per_page = 15
    offset = (page - 1) * per_page
    context = {
        "history": [],
        "total": 0,
        "error": None,
        "page": page,
        "per_page": per_page,
        "total_pages": 0,
        "event_type": event_type,
    }
    try:
        client = _get_client(request)
        ev = event_type if event_type not in ("all", "") else None
        result = client.get_user_history(event_type=ev, limit=per_page, offset=offset)
        context["history"] = result.get("items", [])
        context["total"] = result.get("total", 0)
        context["total_pages"] = max(1, (context["total"] + per_page - 1) // per_page)
    except GraphQLError as e:
        logger.warning("Admin user history GraphQL error: %s", e)
        context["error"] = str(e)
    except Exception as e:
        logger.exception("Admin user history error")
        context["error"] = str(e)
    return render(request, "admin/user_history.html", context)


@require_admin_or_super_admin
def statistics_view(request):
    """Statistics - Admin or SuperAdmin."""
    context = {"stats": None, "error": None}
    try:
        client = _get_client(request)
        stats = client.get_user_stats()
        plans = stats.get("users_by_plan") or {}
        stats["total_subscriptions"] = sum(plans.values())
        context["stats"] = stats
    except GraphQLError as e:
        logger.warning("Admin statistics GraphQL error: %s", e)
        context["error"] = str(e)
    except Exception as e:
        logger.exception("Admin statistics error")
        context["error"] = str(e)
    return render(request, "admin/statistics.html", context)


@require_admin_or_super_admin
def logs_view(request):
    """System Logs - Admin or SuperAdmin. Uses Lambda logs.api when configured."""
    page = max(1, int(request.GET.get("page", 1)))
    time_range = request.GET.get("time_range", "24h")
    level = request.GET.get("level", "").strip()
    logger_filter = request.GET.get("logger", "").strip()
    user_id = request.GET.get("user_id", "").strip()
    search = request.GET.get("search", "").strip()
    raw_per_page = int(request.GET.get("per_page", 50))
    per_page = raw_per_page if raw_per_page in VALID_PER_PAGE else 50
    skip = (page - 1) * per_page

    context = {
        "log_stats": None,
        "logs": [],
        "total": 0,
        "error": None,
        "page": page,
        "per_page": per_page,
        "total_pages": 0,
        "time_range": time_range,
        "level_filter": level,
        "logger_filter": logger_filter,
        "user_id_filter": user_id,
        "search": search,
        "start_index": 0,
        "end_index": 0,
        "logs_api_enabled": LOGS_API_ENABLED,
        "prev_query_params": None,
        "next_query_params": None,
        "page_urls": [],
    }

    try:
        if LOGS_API_ENABLED:
            logs_client = LogsApiClient()
            context["log_stats"] = logs_client.get_statistics(
                time_range=time_range, period="hourly"
            )
            start_time, end_time = time_range_to_iso(time_range)
            if search:
                result = logs_client.search_logs(
                    query=search,
                    level=level or None,
                    logger_filter=logger_filter or None,
                    user_id=user_id or None,
                    start_time=start_time,
                    end_time=end_time,
                    limit=per_page,
                    skip=skip,
                )
            else:
                result = logs_client.query_logs(
                    level=level or None,
                    logger_filter=logger_filter or None,
                    user_id=user_id or None,
                    start_time=start_time,
                    end_time=end_time,
                    limit=per_page,
                    skip=skip,
                )
        else:
            client = _get_client(request)
            context["log_stats"] = client.get_log_statistics(time_range=time_range)
            result = client.query_logs(
                level=level or None,
                logger_filter=logger_filter or None,
                user_id=user_id or None,
                limit=per_page,
                skip=skip,
            )

        context["logs"] = result.get("items", [])
        context["total"] = result.get("total", 0)
        context["total_pages"] = max(1, (context["total"] + per_page - 1) // per_page)
        total = context["total"]
        context["start_index"] = (page - 1) * per_page + 1 if total else 0
        context["end_index"] = min(page * per_page, total) if total else 0
        total_pages = context["total_pages"]
        base = lambda p: build_logs_query_params(
            page=p,
            per_page=per_page,
            time_range=time_range,
            level=level,
            logger_filter=logger_filter,
            user_id=user_id,
            search=search,
        )
        context["query_params"] = base(page)
        context["prev_query_params"] = base(page - 1) if page > 1 else None
        context["next_query_params"] = base(page + 1) if page < total_pages else None
        # Page links: show current ±2
        context["page_numbers"] = [
            n for n in range(1, total_pages + 1)
            if page - 2 <= n <= page + 2
        ]
        context["page_urls"] = [(n, base(n)) for n in context["page_numbers"]]
    except (GraphQLError, LambdaAPIError) as e:
        logger.warning("Admin logs error: %s", e)
        context["error"] = str(e)
    except Exception as e:
        logger.exception("Admin logs error")
        context["error"] = str(e)
    return render(request, "admin/logs.html", context)


@require_admin_or_super_admin
@require_http_methods(["POST"])
def log_update_view(request, log_id):
    """Update a single log (message/context). JSON API for Lambda logs; only when LOGS_API_ENABLED."""
    if not LOGS_API_ENABLED:
        return JsonResponse(
            {"success": False, "error": "Logs API is not enabled"},
            status=400,
        )
    try:
        body = json.loads(request.body) if request.body else {}
        message = body.get("message")
        context = body.get("context")
        if message is None and context is None:
            return JsonResponse(
                {"success": False, "error": "Provide at least message or context"},
                status=400,
            )
        client = LogsApiClient()
        log = client.update_log(log_id=log_id, message=message, context=context)
        return JsonResponse({"success": True, "data": log})
    except LambdaAPIError as e:
        logger.warning("Admin log update error: %s", e)
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=getattr(e, "status_code", 500),
        )
    except Exception as e:
        logger.exception("Admin log update error")
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


@require_admin_or_super_admin
@require_http_methods(["POST"])
def log_delete_view(request, log_id):
    """Delete a single log by ID. JSON API for Lambda logs; only when LOGS_API_ENABLED."""
    if not LOGS_API_ENABLED:
        return JsonResponse(
            {"success": False, "error": "Logs API is not enabled"},
            status=400,
        )
    try:
        client = LogsApiClient()
        client.delete_log(log_id=log_id)
        return JsonResponse({"success": True, "message": "Log deleted successfully"})
    except LambdaAPIError as e:
        logger.warning("Admin log delete error: %s", e)
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=getattr(e, "status_code", 500),
        )
    except Exception as e:
        logger.exception("Admin log delete error")
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


@require_admin_or_super_admin
@require_http_methods(["POST"])
def logs_bulk_delete_view(request):
    """Bulk delete logs matching current filters. JSON API for Lambda logs; only when LOGS_API_ENABLED."""
    if not LOGS_API_ENABLED:
        return JsonResponse(
            {"success": False, "error": "Logs API is not enabled"},
            status=400,
        )
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
        client = LogsApiClient()
        result = client.delete_logs_bulk(
            level=level,
            logger=logger_filter,
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
        )
        return JsonResponse({
            "success": True,
            "deleted_count": result.get("deleted_count"),
            "status": result.get("status"),
            "message": result.get("message"),
        })
    except LambdaAPIError as e:
        logger.warning("Admin logs bulk delete error: %s", e)
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=getattr(e, "status_code", 500),
        )
    except Exception as e:
        logger.exception("Admin logs bulk delete error")
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


@require_admin_or_super_admin
def system_status_view(request):
    """System Status - Admin or SuperAdmin."""
    context = {"metadata": None, "health": None, "error": None}
    try:
        client = _get_client(request)
        context["metadata"] = client.get_api_metadata()
        context["health"] = client.get_api_health()
    except GraphQLError as e:
        logger.warning("Admin system status GraphQL error: %s", e)
        context["error"] = str(e)
    except Exception as e:
        logger.exception("Admin system status error")
        context["error"] = str(e)
    return render(request, "admin/system_status.html", context)


# ---------------------------------------------------------------------------
# Job Scheduler (lambda/tkdjob)
# ---------------------------------------------------------------------------

@require_admin_or_super_admin
def jobs_view(request):
    """Job Scheduler - list jobs with filters and pagination."""
    config_ok = JOB_SCHEDULER_ENABLED
    page = max(1, int(request.GET.get("page", 1)))
    limit_param = int(request.GET.get("limit", 25))
    limit = limit_param if limit_param in VALID_JOBS_LIMIT else 25
    status_list = [s for s in request.GET.getlist("status") if (s or "").strip()]
    uuid_filter = (request.GET.get("uuid") or "").strip()
    offset = (page - 1) * limit

    context = {
        "jobs": [],
        "total": 0,
        "error": None,
        "config_ok": config_ok,
        "page": page,
        "limit": limit,
        "total_pages": 0,
        "status_filter": status_list,
        "uuid_filter": uuid_filter,
        "start_index": 0,
        "end_index": 0,
        "prev_query_params": None,
        "next_query_params": None,
        "page_urls": [],
        "job_stats": {"total": 0, "completed": 0, "failed": 0, "processing": 0},
    }

    if not config_ok:
        return render(request, "admin/jobs.html", context)

    try:
        client = TkdJobClient()
        result = client.list_jobs(
            status=status_list if status_list else None,
            uuid=uuid_filter or None,
            limit=limit,
            offset=offset,
        )
        jobs = result.get("jobs", [])
        total = result.get("total", len(jobs))
        if len(jobs) == limit:
            total = max(total, page * limit)
        total_pages = max(1, (total + limit - 1) // limit)
        context["jobs"] = jobs
        context["total"] = total
        context["total_pages"] = total_pages
        context["start_index"] = (page - 1) * limit + 1 if total else 0
        context["end_index"] = min(page * limit, total) if total else 0

        completed = sum(1 for j in jobs if j.get("status") == "completed")
        failed = sum(1 for j in jobs if j.get("status") == "failed")
        processing = sum(1 for j in jobs if j.get("status") == "processing")
        context["job_stats"] = {
            "total": len(jobs),
            "completed": completed,
            "failed": failed,
            "processing": processing,
        }

        def base(p):
            return build_jobs_query_params(
                page=p,
                limit=limit,
                status=status_list if status_list else None,
                uuid_filter=uuid_filter,
            )

        context["prev_query_params"] = base(page - 1) if page > 1 else None
        context["next_query_params"] = base(page + 1) if page < total_pages else None
        page_numbers = [n for n in range(1, total_pages + 1) if page - 2 <= n <= page + 2]
        context["page_urls"] = [(n, base(n)) for n in page_numbers]
    except LambdaAPIError as e:
        logger.warning("Admin jobs error: %s", e)
        context["error"] = str(e)
    except Exception as e:
        logger.exception("Admin jobs error")
        context["error"] = str(e)
    return render(request, "admin/jobs.html", context)


@require_admin_or_super_admin
def job_detail_view(request, job_uuid):
    """JSON: job + status + timeline + dag for detail modal."""
    if not JOB_SCHEDULER_ENABLED:
        return JsonResponse(
            {"success": False, "error": "Job Scheduler is not configured"},
            status=400,
        )
    try:
        client = TkdJobClient()
        job = client.get_job(job_uuid)
        status_data = client.get_job_status(job_uuid)
        timeline_data = client.get_job_timeline(job_uuid)
        dag_data = client.get_job_dag(job_uuid, include_status=True)
        return JsonResponse({
            "success": True,
            "job": job,
            "status": status_data,
            "timeline": timeline_data,
            "dag": dag_data,
        })
    except LambdaAPIError as e:
        logger.warning("Admin job detail error: %s", e)
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=getattr(e, "status_code", 500),
        )
    except Exception as e:
        logger.exception("Admin job detail error")
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


@require_admin_or_super_admin
@require_http_methods(["POST"])
def job_retry_view(request, job_uuid):
    """POST: retry a failed job. JSON body optional: data, priority, retry_count, retry_interval, run_after."""
    if not JOB_SCHEDULER_ENABLED:
        return JsonResponse(
            {"success": False, "error": "Job Scheduler is not configured"},
            status=400,
        )
    try:
        body = json.loads(request.body) if request.body else {}
        client = TkdJobClient()
        job = client.retry_job(
            job_uuid,
            data=body.get("data"),
            priority=body.get("priority"),
            retry_count=body.get("retry_count"),
            retry_interval=body.get("retry_interval"),
            run_after=body.get("run_after"),
        )
        return JsonResponse({"success": True, "data": job})
    except LambdaAPIError as e:
        logger.warning("Admin job retry error: %s", e)
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=getattr(e, "status_code", 500),
        )
    except Exception as e:
        logger.exception("Admin job retry error")
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


# ---------------------------------------------------------------------------
# Storage Files (lambda/s3storage)
# ---------------------------------------------------------------------------

@require_admin_or_super_admin
def storage_files_view(request):
    """Storage Files - list files in a bucket with optional prefix. Buckets from users API."""
    bucket_users = []
    try:
        client = _get_client(request)
        bucket_users = client.list_users_with_buckets(limit=500)
    except GraphQLError as e:
        logger.warning("Admin storage buckets GraphQL error: %s", e)
    except Exception as e:
        logger.exception("Admin storage buckets error")

    buckets = [u["bucket"] for u in bucket_users if u.get("bucket")]
    config_ok = S3STORAGE_ENABLED and len(buckets) > 0
    bucket_id = (request.GET.get("bucket_id") or "").strip()
    if not bucket_id and buckets:
        bucket_id = buckets[0]
    prefix = (request.GET.get("prefix") or "").strip()

    context = {
        "files": [],
        "bucket_id": bucket_id,
        "buckets": buckets,
        "bucket_users": bucket_users,
        "prefix": prefix,
        "error": None,
        "config_ok": config_ok,
    }

    if not config_ok or not bucket_id:
        return render(request, "admin/storage_files.html", context)

    try:
        client = S3StorageClient()
        context["files"] = client.list_objects(bucket_id=bucket_id, prefix=prefix)
    except LambdaAPIError as e:
        logger.warning("Admin storage files error: %s", e)
        context["error"] = str(e)
    except Exception as e:
        logger.exception("Admin storage files error")
        context["error"] = str(e)
    return render(request, "admin/storage_files.html", context)


@require_admin_or_super_admin
def storage_download_url_view(request):
    """GET: return presigned download URL for bucket_id + file_key (query params)."""
    if not S3STORAGE_ENABLED:
        return JsonResponse(
            {"success": False, "error": "Storage is not configured"},
            status=400,
        )
    bucket_id = (request.GET.get("bucket_id") or "").strip()
    file_key = (request.GET.get("file_key") or "").strip()
    if not bucket_id or not file_key:
        return JsonResponse(
            {"success": False, "error": "bucket_id and file_key are required"},
            status=400,
        )
    try:
        client = S3StorageClient()
        result = client.get_download_url(bucket_id=bucket_id, file_key=file_key)
        return JsonResponse({
            "success": True,
            "downloadUrl": result.get("downloadUrl", ""),
            "expiresIn": result.get("expiresIn", 0),
        })
    except LambdaAPIError as e:
        logger.warning("Admin storage download URL error: %s", e)
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=getattr(e, "status_code", 500),
        )
    except Exception as e:
        logger.exception("Admin storage download URL error")
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


@require_admin_or_super_admin
@require_http_methods(["POST"])
def storage_delete_view(request):
    """POST: delete file. Body or form: bucket_id, file_key. Returns JSON."""
    if not S3STORAGE_ENABLED:
        return JsonResponse(
            {"success": False, "error": "Storage is not configured"},
            status=400,
        )
    try:
        if request.content_type and "application/json" in request.content_type:
            body = json.loads(request.body) if request.body else {}
        else:
            body = request.POST
        bucket_id = (body.get("bucket_id") or "").strip()
        file_key = (body.get("file_key") or "").strip()
        if not bucket_id or not file_key:
            return JsonResponse(
                {"success": False, "error": "bucket_id and file_key are required"},
                status=400,
            )
        client = S3StorageClient()
        client.delete_object(bucket_id=bucket_id, file_key=file_key)
        return JsonResponse({"success": True, "message": "File deleted"})
    except LambdaAPIError as e:
        logger.warning("Admin storage delete error: %s", e)
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=getattr(e, "status_code", 500),
        )
    except Exception as e:
        logger.exception("Admin storage delete error")
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


@require_admin_or_super_admin
def settings_view(request):
    """Admin Settings - Admin or SuperAdmin. Placeholder forms."""
    is_super_admin = False
    try:
        token = request.COOKIES.get("access_token") or (
            request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        )
        if token:
            client = Appointment360Client()
            is_super_admin = client.is_super_admin(token)
    except Exception:
        pass
    context = {"is_super_admin": is_super_admin, "error": None}
    return render(request, "admin/settings.html", context)
