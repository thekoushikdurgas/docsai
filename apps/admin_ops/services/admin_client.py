"""
Admin operations service client.
Bridges to GraphQL gateway + logs.api + s3storage.server.
"""
import logging
import uuid
from typing import Any, Dict, List, Optional

import httpx
from django.conf import settings

from apps.core.services.graphql_client import graphql_query, graphql_mutation

logger = logging.getLogger(__name__)


def _graphql_data(resp: Any) -> Dict:
    if not isinstance(resp, dict):
        return {}
    data = resp.get("data")
    return data if isinstance(data, dict) else {}


def _admin(resp: Any) -> Dict:
    admin = _graphql_data(resp).get("admin")
    return admin if isinstance(admin, dict) else {}


def _s3_api_root() -> str:
    """Base URL for S3 list/download/delete paths (avoids …/api/v1/api/v1 when env already includes /api/v1)."""
    base = (settings.S3STORAGE_API_URL or "").strip().rstrip("/")
    if not base:
        return ""
    if base.endswith("/api/v1"):
        return base
    return f"{base}/api/v1"


# ===== GraphQL fragments =====

_ADMIN_USERS = """
query AdminUsers($filters: UserFilterInput, $limit: Int, $offset: Int) {
  admin {
    users(filters: $filters, limit: $limit, offset: $offset) {
      items {
        uuid email name isActive lastSignInAt createdAt
        profile { role credits subscriptionPlan expiresAt }
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
      totalUsers activeUsers newUsersToday newUsersThisWeek newUsersThisMonth
      usersBySubscription { subscriptionPlan count }
    }
  }
}
"""

_ADJUST_CREDITS = """
mutation AdminAdjustCredits($userId: ID!, $amount: Int!, $reason: String!) {
  admin {
    adjustCredits(userId: $userId, amount: $amount, reason: $reason) {
      success error
    }
  }
}
"""

_APPROVE_PAYMENT = """
mutation AdminApprovePayment($paymentId: ID!, $reason: String) {
  admin {
    approvePayment(paymentId: $paymentId, reason: $reason) {
      success error
    }
  }
}
"""

_DECLINE_PAYMENT = """
mutation AdminDeclinePayment($paymentId: ID!, $reason: String!) {
  admin {
    declinePayment(paymentId: $paymentId, reason: $reason) {
      success error
    }
  }
}
"""

_PENDING_PAYMENTS = """
query AdminPendingPayments {
  admin {
    pendingPayments {
      id userId amount planId status createdAt proofUrl
      user { email name }
    }
  }
}
"""

_JOBS_LIST = """
query AdminJobs($status: String, $limit: Int, $offset: Int) {
  admin {
    jobs(status: $status, limit: $limit, offset: $offset) {
      items {
        id type status createdAt updatedAt userId
        progress { processed total percent }
      }
      pageInfo { total limit offset hasNext hasPrevious }
    }
  }
}
"""

_JOB_DETAIL = """
query AdminJobDetail($jobId: ID!) {
  admin {
    job(id: $jobId) {
      id type status createdAt updatedAt userId requestId
      progress { processed total percent }
      logs { timestamp level message }
    }
  }
}
"""

_RETRY_JOB = """
mutation AdminRetryJob($jobId: ID!) {
  admin {
    retryJob(jobId: $jobId) {
      success error idempotent
    }
  }
}
"""


def get_users(token: str, filters: Optional[Dict] = None, limit: int = 25, offset: int = 0) -> Dict:
    resp = graphql_query(_ADMIN_USERS, {"filters": filters or {}, "limit": limit, "offset": offset}, token=token)
    users = _admin(resp).get("users")
    return users if isinstance(users, dict) else {}


def get_user_stats(token: str) -> Dict:
    resp = graphql_query(_ADMIN_USER_STATS, token=token)
    stats = _admin(resp).get("userStats")
    return stats if isinstance(stats, dict) else {}


def adjust_credits(token: str, user_id: str, amount: int, reason: str) -> Dict:
    resp = graphql_mutation(_ADJUST_CREDITS, {"userId": user_id, "amount": amount, "reason": reason}, token=token)
    out = _admin(resp).get("adjustCredits")
    return out if isinstance(out, dict) else {}


def get_pending_payments(token: str) -> List[Dict]:
    resp = graphql_query(_PENDING_PAYMENTS, token=token)
    pp = _admin(resp).get("pendingPayments")
    return pp if isinstance(pp, list) else []


def approve_payment(token: str, payment_id: str, reason: str = "") -> Dict:
    resp = graphql_mutation(_APPROVE_PAYMENT, {"paymentId": payment_id, "reason": reason}, token=token)
    out = _admin(resp).get("approvePayment")
    return out if isinstance(out, dict) else {}


def decline_payment(token: str, payment_id: str, reason: str) -> Dict:
    resp = graphql_mutation(_DECLINE_PAYMENT, {"paymentId": payment_id, "reason": reason}, token=token)
    out = _admin(resp).get("declinePayment")
    return out if isinstance(out, dict) else {}


def get_jobs(token: str, status: Optional[str] = None, limit: int = 25, offset: int = 0) -> Dict:
    resp = graphql_query(_JOBS_LIST, {"status": status, "limit": limit, "offset": offset}, token=token)
    jobs = _admin(resp).get("jobs")
    return jobs if isinstance(jobs, dict) else {}


def get_job_detail(token: str, job_id: str) -> Optional[Dict]:
    resp = graphql_query(_JOB_DETAIL, {"jobId": job_id}, token=token)
    job = _admin(resp).get("job")
    return job if isinstance(job, dict) else None


def retry_job(token: str, job_id: str) -> Dict:
    resp = graphql_mutation(_RETRY_JOB, {"jobId": job_id}, token=token)
    out = _admin(resp).get("retryJob")
    return out if isinstance(out, dict) else {}


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


# ===== Logs API =====

def _logs_headers() -> Dict[str, str]:
    return {"X-API-Key": settings.LOGS_API_KEY, "X-Request-ID": str(uuid.uuid4())}


def get_logs(service: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[Dict]:
    if not settings.LOGS_API_URL:
        return []
    try:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if service:
            params["service"] = service
        with httpx.Client(timeout=10.0) as c:
            resp = c.get(f"{settings.LOGS_API_URL}/api/v1/logs", params=params, headers=_logs_headers())
            resp.raise_for_status()
            return resp.json().get("logs", [])
    except Exception as exc:
        logger.warning("get_logs failed: %s", exc)
        return []


def delete_log(log_id: str) -> bool:
    if not settings.LOGS_API_URL:
        return False
    try:
        with httpx.Client(timeout=10.0) as c:
            resp = c.delete(f"{settings.LOGS_API_URL}/api/v1/logs/{log_id}", headers=_logs_headers())
            return resp.status_code < 300
    except Exception as exc:
        logger.warning("delete_log failed: %s", exc)
        return False


# ===== S3 Storage =====

def _s3_headers() -> Dict[str, str]:
    return {"X-API-Key": settings.S3STORAGE_API_KEY, "X-Request-ID": str(uuid.uuid4())}


def get_storage_artifacts(prefix: str = "", limit: int = 50) -> List[Dict]:
    root = _s3_api_root()
    if not root:
        return []
    try:
        with httpx.Client(timeout=10.0) as c:
            resp = c.get(
                f"{root}/list",
                params={"prefix": prefix, "limit": limit},
                headers=_s3_headers(),
            )
            resp.raise_for_status()
            return resp.json().get("files", [])
    except Exception as exc:
        logger.warning("get_storage_artifacts failed: %s", exc)
        return []


def get_download_url(key: str) -> Optional[str]:
    root = _s3_api_root()
    if not root:
        return None
    try:
        with httpx.Client(timeout=10.0) as c:
            resp = c.get(
                f"{root}/download-url",
                params={"key": key},
                headers=_s3_headers(),
            )
            resp.raise_for_status()
            return resp.json().get("url")
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
                f"{root}/delete",
                params={"key": key},
                headers=_s3_headers(),
            )
            return resp.status_code < 300
    except Exception as exc:
        logger.warning("delete_storage_artifact failed: %s", exc)
        return False


# ===== System health =====

def get_system_health() -> List[Dict]:
    """Probe all known services and return health status list."""
    services = [
        {"name": "GraphQL Gateway", "key": "gateway", "url": settings.GRAPHQL_URL.replace("/graphql", "") + "/health"},
        {"name": "Logs API", "key": "logs", "url": settings.LOGS_API_URL + "/health" if settings.LOGS_API_URL else ""},
        {"name": "S3 Storage", "key": "s3storage", "url": settings.S3STORAGE_API_URL + "/health" if settings.S3STORAGE_API_URL else ""},
        {"name": "AI Server", "key": "ai", "url": settings.AI_API_URL + "/health" if settings.AI_API_URL else ""},
        {"name": "Email Campaign", "key": "emailcampaign", "url": settings.EMAILCAMPAIGN_URL + "/health" if settings.EMAILCAMPAIGN_URL else ""},
    ]
    results = []
    for svc in services:
        if not svc.get("url"):
            results.append({**svc, "status": "not_configured", "latency_ms": None})
            continue
        try:
            import time
            t0 = time.monotonic()
            with httpx.Client(timeout=5.0) as c:
                resp = c.get(svc["url"])
            latency = round((time.monotonic() - t0) * 1000)
            status = "up" if resp.status_code < 300 else "degraded"
        except Exception:
            status = "down"
            latency = None
        results.append({**svc, "status": status, "latency_ms": latency})
    return results
