"""
API request tracking storage: record hits and read per-endpoint statistics.

Uses Django cache (Redis or LocMem) with keys:
- api_tracking:count:{endpoint_key}
- api_tracking:last_ts:{endpoint_key}

Optional (for success rate / duration):
- api_tracking:status_2xx:{endpoint_key}, status_4xx, status_5xx
- api_tracking:duration_sum:{endpoint_key}, duration_count

User type tracking (new):
- api_tracking:count:{endpoint_key}:{user_type}
- api_tracking:last_ts:{endpoint_key}:{user_type}
- api_tracking:status_2xx:{endpoint_key}:{user_type}, etc.
- api_tracking:duration_sum:{endpoint_key}:{user_type}, duration_count
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from django.core.cache import cache

logger = logging.getLogger(__name__)

NAMESPACE = "api_tracking"
# Long TTL for count/last_ts so stats persist (e.g. 30 days); cache backends may cap
DEFAULT_TTL = 60 * 60 * 24 * 30  # 30 days

# Valid user types for tracking
VALID_USER_TYPES = frozenset(["super_admin", "admin", "pro_user", "free_user", "guest"])


def _key(suffix: str, endpoint_key: str, user_type: Optional[str] = None) -> str:
    """Build cache key with optional user_type segment."""
    if user_type:
        return f"{NAMESPACE}:{suffix}:{endpoint_key}:{user_type}"
    return f"{NAMESPACE}:{suffix}:{endpoint_key}"


def record_hit(endpoint_key: str, status_code: int, duration_ms: float) -> None:
    """
    Record one request hit for the given endpoint (global stats).
    Does not raise; logs and returns on cache errors.
    """
    if not endpoint_key:
        return
    try:
        # Count: increment (Redis) or get+set (LocMem)
        count_key = _key("count", endpoint_key)
        try:
            cache.incr(count_key)
        except (ValueError, TypeError):
            # Key missing or backend doesn't support incr
            count = cache.get(count_key, 0) or 0
            cache.set(count_key, count + 1, DEFAULT_TTL)

        # Last called timestamp
        cache.set(_key("last_ts", endpoint_key), time.time(), DEFAULT_TTL)

        # Optional: status buckets
        if 200 <= status_code < 300:
            _incr_or_set(_key("status_2xx", endpoint_key))
        elif 400 <= status_code < 500:
            _incr_or_set(_key("status_4xx", endpoint_key))
        elif status_code >= 500:
            _incr_or_set(_key("status_5xx", endpoint_key))

        # Optional: duration for average (get/set to support float)
        dur_sum_key = _key("duration_sum", endpoint_key)
        dur_count_key = _key("duration_count", endpoint_key)
        _incr_or_set(dur_count_key)
        s = cache.get(dur_sum_key, 0) or 0
        cache.set(dur_sum_key, s + duration_ms, DEFAULT_TTL)
    except Exception as e:
        logger.warning("api_tracking record_hit failed for %s: %s", endpoint_key, e)


def record_hit_with_user_type(
    endpoint_key: str, 
    user_type: str, 
    status_code: int, 
    duration_ms: float
) -> None:
    """
    Record one request hit for the given endpoint and user_type.
    This tracks per-user-type statistics in addition to global stats.
    Does not raise; logs and returns on cache errors.
    
    Args:
        endpoint_key: The endpoint identifier (e.g., "pages/list")
        user_type: The user type (super_admin, admin, pro_user, free_user, guest)
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
    """
    if not endpoint_key or not user_type:
        return
    
    # Validate user_type
    if user_type not in VALID_USER_TYPES:
        logger.warning("Invalid user_type '%s' for endpoint %s, defaulting to 'guest'", user_type, endpoint_key)
        user_type = "guest"
    
    try:
        # Count: increment with user_type
        count_key = _key("count", endpoint_key, user_type)
        try:
            cache.incr(count_key)
        except (ValueError, TypeError):
            count = cache.get(count_key, 0) or 0
            cache.set(count_key, count + 1, DEFAULT_TTL)

        # Last called timestamp with user_type
        cache.set(_key("last_ts", endpoint_key, user_type), time.time(), DEFAULT_TTL)

        # Status buckets with user_type
        if 200 <= status_code < 300:
            _incr_or_set(_key("status_2xx", endpoint_key, user_type))
        elif 400 <= status_code < 500:
            _incr_or_set(_key("status_4xx", endpoint_key, user_type))
        elif status_code >= 500:
            _incr_or_set(_key("status_5xx", endpoint_key, user_type))

        # Duration tracking with user_type
        dur_sum_key = _key("duration_sum", endpoint_key, user_type)
        dur_count_key = _key("duration_count", endpoint_key, user_type)
        _incr_or_set(dur_count_key)
        s = cache.get(dur_sum_key, 0) or 0
        cache.set(dur_sum_key, s + duration_ms, DEFAULT_TTL)
        
        logger.debug("Recorded hit for %s by %s", endpoint_key, user_type)
    except Exception as e:
        logger.warning("api_tracking record_hit_with_user_type failed for %s/%s: %s", 
                      endpoint_key, user_type, e)


def _incr_or_set(key: str) -> None:
    try:
        cache.incr(key)
    except (ValueError, TypeError):
        val = cache.get(key, 0) or 0
        cache.set(key, val + 1, DEFAULT_TTL)


def get_endpoint_stats(endpoint_keys: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Return per-endpoint stats for the given keys.
    Each value has: request_count, last_called_at (Unix float or None), and optionally
    status_2xx, status_4xx, status_5xx, avg_duration_ms.
    """
    result: Dict[str, Dict[str, Any]] = {}
    for key in endpoint_keys:
        result[key] = _get_single_stats(key)
    return result


def _get_single_stats(endpoint_key: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "request_count": 0,
        "last_called_at": None,
    }
    try:
        count = cache.get(_key("count", endpoint_key))
        if count is not None:
            out["request_count"] = int(count)
        ts = cache.get(_key("last_ts", endpoint_key))
        if ts is not None:
            out["last_called_at"] = float(ts)
        s2 = cache.get(_key("status_2xx", endpoint_key))
        s4 = cache.get(_key("status_4xx", endpoint_key))
        s5 = cache.get(_key("status_5xx", endpoint_key))
        if s2 is not None or s4 is not None or s5 is not None:
            out["status_2xx"] = int(s2 or 0)
            out["status_4xx"] = int(s4 or 0)
            out["status_5xx"] = int(s5 or 0)
        dur_sum = cache.get(_key("duration_sum", endpoint_key))
        dur_count = cache.get(_key("duration_count", endpoint_key))
        if dur_count and int(dur_count) > 0 and dur_sum is not None:
            out["avg_duration_ms"] = round(float(dur_sum) / int(dur_count), 2)
    except Exception as e:
        logger.warning("api_tracking get_endpoint_stats failed for %s: %s", endpoint_key, e)
    return out


def _get_single_stats_with_user_type(endpoint_key: str, user_type: str) -> Dict[str, Any]:
    """Get stats for a specific endpoint and user_type."""
    out: Dict[str, Any] = {
        "request_count": 0,
        "last_called_at": None,
    }
    try:
        count = cache.get(_key("count", endpoint_key, user_type))
        if count is not None:
            out["request_count"] = int(count)
        ts = cache.get(_key("last_ts", endpoint_key, user_type))
        if ts is not None:
            out["last_called_at"] = float(ts)
        s2 = cache.get(_key("status_2xx", endpoint_key, user_type))
        s4 = cache.get(_key("status_4xx", endpoint_key, user_type))
        s5 = cache.get(_key("status_5xx", endpoint_key, user_type))
        if s2 is not None or s4 is not None or s5 is not None:
            out["status_2xx"] = int(s2 or 0)
            out["status_4xx"] = int(s4 or 0)
            out["status_5xx"] = int(s5 or 0)
        dur_sum = cache.get(_key("duration_sum", endpoint_key, user_type))
        dur_count = cache.get(_key("duration_count", endpoint_key, user_type))
        if dur_count and int(dur_count) > 0 and dur_sum is not None:
            out["avg_duration_ms"] = round(float(dur_sum) / int(dur_count), 2)
    except Exception as e:
        logger.warning("api_tracking get_endpoint_stats failed for %s/%s: %s", 
                      endpoint_key, user_type, e)
    return out


def get_endpoint_stats_by_user_type(endpoint_keys: List[str]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Return per-endpoint stats broken down by user_type.
    
    Args:
        endpoint_keys: List of endpoint identifiers
        
    Returns:
        Dict with structure:
        {
            "endpoint_key": {
                "super_admin": {"request_count": 10, "last_called_at": 123.45, ...},
                "admin": {"request_count": 5, ...},
                ...
            }
        }
    """
    result: Dict[str, Dict[str, Dict[str, Any]]] = {}
    
    for endpoint_key in endpoint_keys:
        result[endpoint_key] = {}
        for user_type in VALID_USER_TYPES:
            stats = _get_single_stats_with_user_type(endpoint_key, user_type)
            # Only include user_type if it has data
            if stats.get("request_count", 0) > 0:
                result[endpoint_key][user_type] = stats
    
    return result


def get_aggregated_stats_by_user_type() -> Dict[str, Dict[str, Any]]:
    """
    Get aggregated statistics per user_type across all endpoints.
    
    Returns:
        Dict with structure:
        {
            "super_admin": {
                "total_requests": 100,
                "unique_endpoints": 25,
                "avg_duration_ms": 45.2
            },
            ...
        }
    """
    from apps.documentation.api.v1.api_docs_registry import get_all_endpoint_keys
    
    endpoint_keys = get_all_endpoint_keys()
    result: Dict[str, Dict[str, Any]] = {}
    
    for user_type in VALID_USER_TYPES:
        total_requests = 0
        unique_endpoints = 0
        total_duration = 0.0
        total_duration_count = 0
        
        for endpoint_key in endpoint_keys:
            stats = _get_single_stats_with_user_type(endpoint_key, user_type)
            req_count = stats.get("request_count", 0)
            if req_count > 0:
                total_requests += req_count
                unique_endpoints += 1
                
                # Accumulate duration for overall average
                dur_sum = cache.get(_key("duration_sum", endpoint_key, user_type))
                dur_count = cache.get(_key("duration_count", endpoint_key, user_type))
                if dur_sum and dur_count:
                    total_duration += float(dur_sum)
                    total_duration_count += int(dur_count)
        
        avg_duration = None
        if total_duration_count > 0:
            avg_duration = round(total_duration / total_duration_count, 2)
        
        result[user_type] = {
            "total_requests": total_requests,
            "unique_endpoints": unique_endpoints,
            "avg_duration_ms": avg_duration,
        }
    
    return result
