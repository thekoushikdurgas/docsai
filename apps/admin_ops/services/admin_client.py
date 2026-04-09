"""
Admin operations service client.
Bridges to GraphQL gateway + logs.api + s3storage.server.
"""
import json
import logging
import uuid
from typing import Any, Dict, List, Optional

import httpx
from django.conf import settings

from apps.core.services.graphql_client import graphql_query, graphql_mutation

logger = logging.getLogger(__name__)


class AdminGraphQLError(RuntimeError):
    """Raised when the gateway returns a GraphQL `errors` payload."""

    def __init__(self, message: str, *, code: Optional[str] = None):
        super().__init__(message)
        self.code = code


def _raise_if_graphql_errors(resp: Any) -> None:
    if not isinstance(resp, dict):
        return
    errs = resp.get("errors")
    if not isinstance(errs, list) or not errs:
        return
    first = errs[0]
    if not isinstance(first, dict):
        raise AdminGraphQLError(str(first))
    msg = first.get("message") or "GraphQL error"
    ext = first.get("extensions") if isinstance(first.get("extensions"), dict) else {}
    code = ext.get("code") if isinstance(ext, dict) else None
    raise AdminGraphQLError(str(msg), code=str(code) if code else None)


def _graphql_data(resp: Any) -> Dict:
    if not isinstance(resp, dict):
        return {}
    data = resp.get("data")
    return data if isinstance(data, dict) else {}


def _admin(resp: Any) -> Dict:
    admin = _graphql_data(resp).get("admin")
    return admin if isinstance(admin, dict) else {}


def _jobs_root(resp: Any) -> Dict:
    """Root ``jobs`` query/mutation namespace (scheduler jobs)."""
    jobs = _graphql_data(resp).get("jobs")
    return jobs if isinstance(jobs, dict) else {}


def _billing(resp: Any) -> Dict:
    """Root ``billing`` query/mutation namespace."""
    billing = _graphql_data(resp).get("billing")
    return billing if isinstance(billing, dict) else {}


def _s3_api_root() -> str:
    """Base URL for S3 list/download/delete paths (avoids …/api/v1/api/v1 when env already includes /api/v1)."""
    base = (settings.S3STORAGE_API_URL or "").strip().rstrip("/")
    if not base:
        return ""
    if base.endswith("/api/v1"):
        return base
    return f"{base}/api/v1"


# ===== GraphQL fragments =====

_USERS_WITH_BUCKETS = """
query AdminUsersWithBuckets($limit: Int, $offset: Int) {
  admin {
    usersWithBuckets(limit: $limit, offset: $offset) {
      items { uuid email bucket }
      pageInfo { total limit offset hasNext hasPrevious }
    }
  }
}
"""

_ADMIN_USERS = """
query AdminUsers($filters: UserFilterInput) {
  admin {
    users(filters: $filters) {
      items {
        uuid email name isActive lastSignInAt createdAt
        profile { role credits subscriptionPlan }
      }
      pageInfo { total limit offset hasNext hasPrevious }
    }
  }
}
"""

_ADMIN_USER_STATS = """
query AdminUserStats {
  admin {
    userStats {
      totalUsers
      activeUsers
      usersByRole
      usersByPlan
    }
  }
}
"""

_UPDATE_USER_CREDITS = """
mutation AdminUpdateUserCredits($input: UpdateUserCreditsInput!) {
  admin {
    updateUserCredits(input: $input) {
      uuid
      email
    }
  }
}
"""

_UPDATE_USER_ROLE = """
mutation AdminUpdateUserRole($input: UpdateUserRoleInput!) {
  admin {
    updateUserRole(input: $input) {
      uuid
      email
    }
  }
}
"""

_DELETE_USER = """
mutation AdminDeleteUser($input: DeleteUserInput!) {
  admin {
    deleteUser(input: $input)
  }
}
"""

_PROMOTE_TO_ADMIN = """
mutation AdminPromoteToAdmin($input: PromoteToAdminInput!) {
  admin {
    promoteToAdmin(input: $input) {
      uuid
      email
    }
  }
}
"""

_PROMOTE_TO_SUPER_ADMIN = """
mutation AdminPromoteToSuperAdmin($input: PromoteToSuperAdminInput!) {
  admin {
    promoteToSuperAdmin(input: $input) {
      uuid
      email
    }
  }
}
"""

_APPROVE_PAYMENT = """
mutation BillingApprovePayment($submissionId: String!) {
  billing {
    approvePayment(submissionId: $submissionId) {
      id status creditsToAdd
    }
  }
}
"""

_DECLINE_PAYMENT = """
mutation BillingDeclinePayment($submissionId: String!, $reason: String!) {
  billing {
    declinePayment(submissionId: $submissionId, reason: $reason) {
      id status declineReason
    }
  }
}
"""

_PENDING_PAYMENTS = """
query AdminPaymentSubmissions($status: String, $limit: Int, $offset: Int) {
  billing {
    paymentSubmissions(status: $status, limit: $limit, offset: $offset) {
      items {
        id userId userEmail amount planTier planPeriod
        screenshotDownloadUrl status creditsToAdd
        declineReason reviewedBy reviewedAt createdAt
      }
      total limit offset hasNext hasPrevious
    }
  }
}
"""

_ADMIN_LOGS = """
query AdminLogs($filters: LogQueryFilterInput) {
  admin {
    logs(filters: $filters) {
      items {
        id
        timestamp
        level
        logger
        message
        userId
        requestId
      }
      pageInfo {
        total
        limit
        offset
        hasNext
        hasPrevious
      }
    }
  }
}
"""

_ADMIN_DELETE_LOG = """
mutation AdminDeleteLog($input: DeleteLogInput!) {
  admin {
    deleteLog(input: $input)
  }
}
"""

_JOBS_LIST = """
query AdminSchedulerJobs($status: String, $sourceService: String, $limit: Int, $offset: Int) {
  admin {
    schedulerJobs(
      status: $status
      sourceService: $sourceService
      limit: $limit
      offset: $offset
    ) {
      jobs {
        id
        jobId
        userId
        jobType
        status
        sourceService
        jobFamily
        createdAt
        updatedAt
      }
      pageInfo { total limit offset hasNext hasPrevious }
    }
  }
}
"""

_JOB_DETAIL = """
query SchedulerJobDetail($jobId: ID!) {
  jobs {
    job(jobId: $jobId) {
      id
      jobId
      userId
      jobType
      status
      sourceService
      jobFamily
      jobSubtype
      requestPayload
      responsePayload
      statusPayload
      createdAt
      updatedAt
    }
  }
}
"""

_RETRY_JOB = """
mutation RetrySchedulerJob($input: RetryJobInput!) {
  jobs {
    retryJob(input: $input)
  }
}
"""


def _normalize_job_list_row(j: Dict[str, Any]) -> Dict[str, Any]:
    """Map gateway SchedulerJob JSON to Django jobs list template fields."""
    jid = j.get("jobId") or j.get("job_id")
    return {
        "id": jid,
        "jobId": jid,
        "type": j.get("jobType") or j.get("job_type"),
        "status": j.get("status"),
        "userId": j.get("userId") or j.get("user_id"),
        "sourceService": j.get("sourceService") or j.get("source_service"),
        "jobFamily": j.get("jobFamily") or j.get("job_family"),
        "createdAt": j.get("createdAt") or j.get("created_at"),
        "updatedAt": j.get("updatedAt") or j.get("updated_at"),
        "progress": None,
    }


def _normalize_job_detail(j: Dict[str, Any]) -> Dict[str, Any]:
    """Map SchedulerJob + live statusPayload for job_detail template."""
    sp = j.get("statusPayload") or j.get("status_payload")
    progress = None
    if isinstance(sp, dict):
        pct = sp.get("percent")
        proc = sp.get("processed")
        tot = sp.get("total")
        try:
            pval = int(float(pct)) if pct is not None else None
        except (TypeError, ValueError):
            pval = None
        if pval is not None or proc is not None or tot is not None:
            progress = {"percent": pval, "processed": proc, "total": tot}
    jid = j.get("jobId") or j.get("job_id")
    return {
        "id": jid,
        "jobId": jid,
        "type": j.get("jobType") or j.get("job_type"),
        "status": j.get("status"),
        "userId": j.get("userId") or j.get("user_id"),
        "sourceService": j.get("sourceService") or j.get("source_service"),
        "jobFamily": j.get("jobFamily") or j.get("job_family"),
        "requestId": None,
        "createdAt": j.get("createdAt") or j.get("created_at"),
        "updatedAt": j.get("updatedAt") or j.get("updated_at"),
        "progress": progress,
        "logs": [],
        "requestPayload": j.get("requestPayload") or j.get("request_payload"),
        "responsePayload": j.get("responsePayload") or j.get("response_payload"),
        "statusPayload": sp,
    }


def get_users(token: str, filters: Optional[Dict] = None, limit: int = 25, offset: int = 0) -> Dict:
    # Gateway expects limit/offset inside UserFilterInput, not as separate users(...) arguments.
    merged = dict(filters or {})
    merged["limit"] = limit
    merged["offset"] = offset
    resp = graphql_query(_ADMIN_USERS, {"filters": merged}, token=token)
    _raise_if_graphql_errors(resp)
    users = _admin(resp).get("users")
    return users if isinstance(users, dict) else {}


def find_admin_user(token: str, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Resolve a user by UUID via paginated admin.users (SuperAdmin-only query on gateway).
    Scans up to max_scan rows when the user is not on the first pages.
    """
    limit = 100
    offset = 0
    max_scan = 8000
    scanned = 0
    uid = str(user_id).strip()
    while scanned < max_scan:
        data = get_users(token, filters={}, limit=limit, offset=offset)
        items = data.get("items") or []
        for u in items:
            if str(u.get("uuid")) == uid:
                return u if isinstance(u, dict) else None
        page_info = data.get("pageInfo") or {}
        if not page_info.get("hasNext"):
            break
        offset += limit
        scanned += len(items)
    return None


def get_user_stats(token: str) -> Dict:
    resp = graphql_query(_ADMIN_USER_STATS, token=token)
    stats = _admin(resp).get("userStats")
    return stats if isinstance(stats, dict) else {}


def adjust_credits(token: str, user_id: str, amount: int, reason: str) -> Dict:
    """
    Apply a delta to credits using admin.updateUserCredits (absolute balance on gateway).
    """
    _ = reason  # audit note reserved for future gateway field
    row = find_admin_user(token, user_id)
    if not row:
        return {"success": False, "error": "User not found in admin directory (scan limit reached)."}
    profile = row.get("profile") if isinstance(row.get("profile"), dict) else {}
    try:
        current = int(profile.get("credits") or 0)
    except (TypeError, ValueError):
        current = 0
    new_credits = max(0, current + int(amount))
    try:
        resp = graphql_mutation(
            _UPDATE_USER_CREDITS,
            {"input": {"userId": user_id, "credits": new_credits}},
            token=token,
        )
    except Exception as exc:
        logger.warning("adjust_credits mutation failed: %s", exc)
        return {"success": False, "error": str(exc)}
    if isinstance(resp, dict) and resp.get("errors"):
        return {"success": False, "error": str(resp.get("errors"))}
    adm = _admin(resp)
    updated = adm.get("updateUserCredits") if isinstance(adm, dict) else None
    if isinstance(updated, dict) and updated.get("uuid"):
        return {"success": True, "credits": new_credits}
    return {"success": False, "error": "Gateway did not return updated user."}


def update_user_role(token: str, user_id: str, role: str) -> Dict[str, Any]:
    try:
        resp = graphql_mutation(
            _UPDATE_USER_ROLE,
            {"input": {"userId": user_id, "role": role}},
            token=token,
        )
    except Exception as exc:
        return {"success": False, "error": str(exc)}
    if isinstance(resp, dict) and resp.get("errors"):
        return {"success": False, "error": str(resp.get("errors"))}
    u = _admin(resp).get("updateUserRole")
    return {"success": bool(isinstance(u, dict) and u.get("uuid"))}


def delete_user_account(token: str, user_id: str) -> Dict[str, Any]:
    try:
        resp = graphql_mutation(_DELETE_USER, {"input": {"userId": user_id}}, token=token)
    except Exception as exc:
        return {"success": False, "error": str(exc)}
    if isinstance(resp, dict) and resp.get("errors"):
        return {"success": False, "error": str(resp.get("errors"))}
    ok = _admin(resp).get("deleteUser")
    return {"success": bool(ok)}


def promote_to_admin(token: str, user_id: str) -> Dict[str, Any]:
    try:
        resp = graphql_mutation(_PROMOTE_TO_ADMIN, {"input": {"userId": user_id}}, token=token)
    except Exception as exc:
        return {"success": False, "error": str(exc)}
    if isinstance(resp, dict) and resp.get("errors"):
        return {"success": False, "error": str(resp.get("errors"))}
    u = _admin(resp).get("promoteToAdmin")
    return {"success": bool(isinstance(u, dict) and u.get("uuid"))}


def promote_to_super_admin(token: str, user_id: str) -> Dict[str, Any]:
    try:
        resp = graphql_mutation(
            _PROMOTE_TO_SUPER_ADMIN,
            {"input": {"userId": user_id}},
            token=token,
        )
    except Exception as exc:
        return {"success": False, "error": str(exc)}
    if isinstance(resp, dict) and resp.get("errors"):
        return {"success": False, "error": str(resp.get("errors"))}
    u = _admin(resp).get("promoteToSuperAdmin")
    return {"success": bool(isinstance(u, dict) and u.get("uuid"))}


def get_pending_payments(
    token: str,
    status: Optional[str] = "pending",
    limit: int = 50,
    offset: int = 0,
) -> Dict:
    """Return ``{"items": [...], "total": int, "hasNext": bool, "hasPrevious": bool}``."""
    resp = graphql_query(
        _PENDING_PAYMENTS,
        {"status": status, "limit": limit, "offset": offset},
        token=token,
    )
    _raise_if_graphql_errors(resp)
    conn = _billing(resp).get("paymentSubmissions") or {}
    return {
        "items": conn.get("items") if isinstance(conn.get("items"), list) else [],
        "total": conn.get("total", 0),
        "limit": conn.get("limit", limit),
        "offset": conn.get("offset", offset),
        "hasNext": conn.get("hasNext", False),
        "hasPrevious": conn.get("hasPrevious", False),
    }


def approve_payment(token: str, submission_id: str) -> Dict:
    resp = graphql_mutation(_APPROVE_PAYMENT, {"submissionId": submission_id}, token=token)
    _raise_if_graphql_errors(resp)
    out = _billing(resp).get("approvePayment")
    return out if isinstance(out, dict) else {}


def decline_payment(token: str, submission_id: str, reason: str) -> Dict:
    resp = graphql_mutation(_DECLINE_PAYMENT, {"submissionId": submission_id, "reason": reason}, token=token)
    _raise_if_graphql_errors(resp)
    out = _billing(resp).get("declinePayment")
    return out if isinstance(out, dict) else {}


def get_jobs(
    token: str,
    status: Optional[str] = None,
    limit: int = 25,
    offset: int = 0,
    source_service: Optional[str] = None,
) -> Dict:
    """
    List scheduler jobs from gateway DB (``admin.schedulerJobs``).

    Covers jobs executed on email.server and sync.server (Connectra); live satellite
    status is resolved on the detail query via ``jobs.job`` → ``statusPayload``.
    """
    variables: Dict[str, Any] = {
        "limit": limit,
        "offset": offset,
        "status": status,
        "sourceService": source_service,
    }
    resp = graphql_query(_JOBS_LIST, variables, token=token)
    _raise_if_graphql_errors(resp)
    raw = _admin(resp).get("schedulerJobs")
    if not isinstance(raw, dict):
        return {}
    rows = raw.get("jobs") if isinstance(raw.get("jobs"), list) else []
    items = [_normalize_job_list_row(j) for j in rows if isinstance(j, dict)]
    return {
        "items": items,
        "pageInfo": raw.get("pageInfo") if isinstance(raw.get("pageInfo"), dict) else {},
    }


def get_job_detail(token: str, job_id: str) -> Optional[Dict]:
    resp = graphql_query(_JOB_DETAIL, {"jobId": job_id}, token=token)
    _raise_if_graphql_errors(resp)
    job = _jobs_root(resp).get("job")
    if not isinstance(job, dict):
        return None
    return _normalize_job_detail(job)


def retry_job(token: str, job_id: str) -> Dict:
    resp = graphql_mutation(_RETRY_JOB, {"input": {"jobId": job_id}}, token=token)
    _raise_if_graphql_errors(resp)
    out = _jobs_root(resp).get("retryJob")
    if isinstance(out, dict):
        return out
    if isinstance(out, str):
        try:
            parsed = json.loads(out)
            return parsed if isinstance(parsed, dict) else {"success": False, "error": out}
        except json.JSONDecodeError:
            return {"success": False, "error": out}
    return {"success": bool(out), "detail": out}


_USER_HISTORY_FOR_USER = """
query UserHistoryForUser($filters: UserHistoryFilterInput!) {
  admin {
    userHistory(filters: $filters) {
      items {
        id userId userEmail userName eventType ip country city createdAt
      }
      pageInfo { total limit offset }
    }
  }
}
"""

_PAYMENT_INSTRUCTIONS_Q = """
query GetPaymentInstructions {
  billing {
    paymentInstructions {
      upiId phoneNumber email qrCodeS3Key qrCodeBucketId
    }
  }
}
"""

_UPDATE_PAYMENT_INSTRUCTIONS_M = """
mutation UpdatePaymentInstructions($input: UpdatePaymentInstructionsInput!) {
  billing {
    updatePaymentInstructions(input: $input) {
      upiId phoneNumber email qrCodeS3Key qrCodeBucketId
    }
  }
}
"""


def _billing_root(resp: Any) -> Dict:
    b = _graphql_data(resp).get("billing")
    return b if isinstance(b, dict) else {}


def get_user_activity_for_user(
    token: str,
    user_id: str,
    limit: int = 25,
    offset: int = 0,
    event_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Per-user audit trail via admin.userHistory (userId filter when supported by gateway)."""
    filters: Dict[str, Any] = {"limit": limit, "offset": offset, "userId": user_id}
    if event_type and event_type not in ("all", ""):
        filters["eventType"] = event_type
    try:
        resp = graphql_query(_USER_HISTORY_FOR_USER, {"filters": filters}, token=token)
    except Exception as exc:
        logger.warning("get_user_activity_for_user failed: %s", exc)
        return {"items": [], "total": 0, "error": str(exc)}
    if isinstance(resp, dict) and resp.get("errors"):
        logger.warning("get_user_activity_for_user GraphQL errors: %s", resp.get("errors"))
        return {"items": [], "total": 0, "error": "GraphQL error"}
    conn = _admin(resp).get("userHistory")
    if not isinstance(conn, dict):
        return {"items": [], "total": 0}
    items = []
    for h in conn.get("items") or []:
        items.append(
            {
                "id": h.get("id", ""),
                "user_id": h.get("userId"),
                "user_email": h.get("userEmail"),
                "user_name": h.get("userName"),
                "event_type": h.get("eventType", ""),
                "ip": h.get("ip"),
                "country": h.get("country"),
                "city": h.get("city"),
                "created_at": h.get("createdAt"),
            }
        )
    total = (conn.get("pageInfo") or {}).get("total", 0)
    return {"items": items, "total": total}


def get_payment_instructions(token: str) -> Optional[Dict]:
    try:
        resp = graphql_query(_PAYMENT_INSTRUCTIONS_Q, token=token)
    except Exception as exc:
        logger.warning("get_payment_instructions failed: %s", exc)
        return None
    if isinstance(resp, dict) and resp.get("errors"):
        return None
    return _billing_root(resp).get("paymentInstructions")


def update_payment_instructions(token: str, input_data: Dict[str, Any]) -> Dict:
    try:
        resp = graphql_mutation(_UPDATE_PAYMENT_INSTRUCTIONS_M, {"input": input_data}, token=token)
    except Exception as exc:
        logger.warning("update_payment_instructions failed: %s", exc)
        return {}
    if isinstance(resp, dict) and resp.get("errors"):
        return {}
    return _billing_root(resp).get("updatePaymentInstructions") or {}


# ===== Logs (gateway → log.server via LogsServerClient) =====


def get_logs(
    token: str,
    *,
    logger: Optional[str] = None,
    level: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    List logs through GraphQL ``admin.logs`` (SuperAdmin), which calls the same
    log.server HTTP API as ``contact360.io/api/app/clients/logs_client.py`` (GET /logs).
    """
    filters: Dict[str, Any] = {"limit": limit, "offset": offset}
    if logger:
        filters["logger"] = logger
    if level:
        filters["level"] = level
    try:
        resp = graphql_query(_ADMIN_LOGS, {"filters": filters}, token=token)
        _raise_if_graphql_errors(resp)
        raw = _admin(resp).get("logs")
        if not isinstance(raw, dict):
            return {"items": [], "pageInfo": {}}
        items = raw.get("items") if isinstance(raw.get("items"), list) else []
        out_rows: List[Dict[str, Any]] = []
        for row in items:
            if not isinstance(row, dict):
                continue
            lg = row.get("logger") or ""
            out_rows.append(
                {
                    "id": row.get("id", ""),
                    "timestamp": row.get("timestamp"),
                    "level": row.get("level", ""),
                    "logger": lg,
                    "message": row.get("message", ""),
                    "userId": row.get("userId") or row.get("user_id"),
                    "requestId": row.get("requestId") or row.get("request_id"),
                    "service": lg,
                }
            )
        return {
            "items": out_rows,
            "pageInfo": raw.get("pageInfo") if isinstance(raw.get("pageInfo"), dict) else {},
        }
    except Exception as exc:
        logger.warning("get_logs failed: %s", exc)
        raise


def delete_log(token: str, log_id: str) -> bool:
    """Delete one log via GraphQL ``admin.deleteLog`` (SuperAdmin → log.server DELETE)."""
    try:
        resp = graphql_mutation(_ADMIN_DELETE_LOG, {"input": {"logId": log_id}}, token=token)
        _raise_if_graphql_errors(resp)
        return bool(_admin(resp).get("deleteLog"))
    except Exception as exc:
        logger.warning("delete_log failed: %s", exc)
        return False


# ===== S3 Storage =====

def _s3_headers() -> Dict[str, str]:
    return {"X-API-Key": settings.S3STORAGE_API_KEY, "X-Request-ID": str(uuid.uuid4())}


def _normalize_artifact(obj: Any) -> Dict[str, Any]:
    """Coerce a single S3 list row to a stable shape regardless of PascalCase/snake_case from the server."""
    key = obj.get("key") or obj.get("Key") or ""
    size = obj.get("size") or obj.get("Size") or obj.get("ContentLength") or 0
    last_modified = (
        obj.get("last_modified")
        or obj.get("lastModified")
        or obj.get("LastModified")
        or ""
    )
    content_type = (
        obj.get("content_type")
        or obj.get("contentType")
        or obj.get("ContentType")
        or ""
    )
    filename = obj.get("filename") or obj.get("Filename") or key.split("/")[-1]
    return {
        "key": key,
        "filename": filename,
        "size": int(size) if size else 0,
        "last_modified": last_modified,
        "content_type": content_type,
    }


def get_storage_artifacts(prefix: str = "", limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """Return ``{"items": [...], "total": int}`` from ``GET /api/v1/files``."""
    root = _s3_api_root()
    if not root:
        raise RuntimeError("S3STORAGE_API_URL is not configured.")
    with httpx.Client(timeout=15.0) as c:
        resp = c.get(
            f"{root}/files",
            params={"prefix": prefix, "limit": limit, "offset": offset},
            headers=_s3_headers(),
        )
        resp.raise_for_status()
        body = resp.json()
        raw = body.get("objects") or body.get("files") or []
        return {
            "items": [_normalize_artifact(obj) for obj in raw],
            "total": body.get("total", len(raw)),
        }


def get_download_url(key: str) -> Optional[str]:
    root = _s3_api_root()
    if not root:
        return None
    try:
        with httpx.Client(timeout=10.0) as c:
            resp = c.get(
                f"{root}/objects/presign-download",
                params={"key": key},
                headers=_s3_headers(),
            )
            resp.raise_for_status()
            body = resp.json()
            return body.get("downloadUrl") or body.get("download_url") or body.get("url")
    except Exception as exc:
        logger.warning("get_download_url failed: %s", exc)
        return None


def delete_storage_artifact(key: str) -> bool:
    root = _s3_api_root()
    if not root:
        return False
    try:
        with httpx.Client(timeout=10.0) as c:
            resp = c.delete(
                f"{root}/objects",
                params={"key": key},
                headers=_s3_headers(),
            )
            return resp.status_code < 300
    except Exception as exc:
        logger.warning("delete_storage_artifact failed: %s", exc)
        return False


def get_users_with_buckets(token: str, limit: int = 200, offset: int = 0) -> List[Dict]:
    """Return list of users that have a bucket configured (for the storage picker)."""
    try:
        resp = graphql_query(
            _USERS_WITH_BUCKETS,
            {"limit": limit, "offset": offset},
            token=token,
        )
        _raise_if_graphql_errors(resp)
        items = _admin(resp).get("usersWithBuckets", {})
        if isinstance(items, dict):
            return items.get("items") or []
        return []
    except Exception as exc:
        logger.warning("get_users_with_buckets failed: %s", exc)
        return []


# ===== System health =====

def _graphql_health_url() -> str:
    """GET /health on the GraphQL gateway host (strip /graphql suffix if present)."""
    url = (settings.GRAPHQL_URL or "").strip()
    if not url:
        return ""
    base = url.replace("/graphql", "").rstrip("/")
    return f"{base}/health"


def _health_url(base: str, path: str = "/health") -> str:
    root = (base or "").strip().rstrip("/")
    if not root:
        return ""
    p = path if path.startswith("/") else f"/{path}"
    return f"{root}{p}"


def _optional_full_or_base_health(raw: str) -> str:
    """Empty, full http(s) URL as-is, or service base URL with /health appended."""
    s = (raw or "").strip()
    if not s:
        return ""
    if s.lower().startswith("http"):
        return s
    return _health_url(s)


def _probe_http_health(name: str, key: str, url: str) -> Dict:
    """Return one service row: probe url or mark not_configured."""
    row = {"name": name, "key": key, "url": url}
    if not url:
        return {**row, "status": "not_configured", "latency_ms": None}
    try:
        import time

        t0 = time.monotonic()
        with httpx.Client(timeout=5.0) as c:
            resp = c.get(url)
        latency = round((time.monotonic() - t0) * 1000)
        status = "up" if resp.status_code < 300 else "degraded"
    except Exception:
        status = "down"
        latency = None
    return {**row, "status": status, "latency_ms": latency}


def get_system_health() -> List[Dict]:
    """
    Probe configured services. Order matches the admin dashboard Service Health widget.
    Optional settings (defaults empty): CONNECTRA_URL, EMAIL_SERVER_HEALTH_URL,
    EXTENSION_SERVER_URL, MAILVETTER_URL.
    """
    connectra = getattr(settings, "CONNECTRA_URL", "") or ""
    email_srv = getattr(settings, "EMAIL_SERVER_HEALTH_URL", "") or ""
    extension = getattr(settings, "EXTENSION_SERVER_URL", "") or ""
    mailvetter = getattr(settings, "MAILVETTER_URL", "") or ""

    jobs_root = (settings.SCHEDULER_URL or "").strip()

    specs = [
        ("GraphQL Gateway", "gateway", _graphql_health_url()),
        ("Connectra (Sync)", "sync", _health_url(connectra)),
        ("Email Server", "email", _optional_full_or_base_health(email_srv)),
        ("Jobs", "jobs", _health_url(jobs_root)),
        ("S3 Storage", "s3storage", _health_url(settings.S3STORAGE_API_URL or "")),
        ("Logs API", "logs", _health_url(settings.LOGS_API_URL or "")),
        ("Contact AI", "ai", _health_url(settings.AI_API_URL or "")),
        ("Extension Server", "extension", _health_url(extension)),
        ("Email Campaign", "emailcampaign", _health_url(settings.EMAILCAMPAIGN_URL or "")),
        ("Mailvetter", "mailvetter", _health_url(mailvetter)),
    ]
    return [_probe_http_health(name, key, url) for name, key, url in specs]
