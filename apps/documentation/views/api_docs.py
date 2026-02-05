"""API docs UI view: list of all GET endpoints with per-endpoint statistics."""

from __future__ import annotations

import json
import math
import time

from django.http import HttpRequest
from django.shortcuts import render

from apps.documentation.api.v1.api_docs_registry import (
    get_all_endpoint_keys,
    get_all_endpoints,
    get_total_endpoint_count,
)
from apps.documentation.utils.api_tracking_storage import (
    get_endpoint_stats,
    get_endpoint_stats_by_user_type,
    get_aggregated_stats_by_user_type,
)


def _format_last_called(ts: float | None) -> str:
    """Return human-readable last-called time (e.g. '2 min ago', 'Never')."""
    if ts is None:
        return "Never"
    now = time.time()
    delta = now - ts
    if delta < 60:
        return "Just now"
    if delta < 3600:
        m = max(1, int(math.floor(delta / 60)))
        return f"{m} min ago"
    if delta < 86400:
        h = max(1, int(math.floor(delta / 3600)))
        return f"{h} hour{'s' if h != 1 else ''} ago"
    if delta < 604800:
        d = max(1, int(math.floor(delta / 86400)))
        return f"{d} day{'s' if d != 1 else ''} ago"
    return "Long ago"


def api_docs_index(request: HttpRequest):
    """
    Render the API reference page at /api/docs/ with all registered GET endpoints
    and their usage statistics (request count, last called), plus user_type breakdown.

    The APIs table is built from the flat all_endpoints list; sorting is client-side.
    """
    keys = get_all_endpoint_keys()
    stats = get_endpoint_stats(keys)

    # Build flat list of all endpoints with stats for the single APIs table.
    # last_called_sort: numeric for client-side sort (Never = 0 so it sorts last when asc).
    all_endpoints = []
    for ep in get_all_endpoints():
        key = ep["endpoint_key"]
        s = stats.get(key, {})
        last_at = s.get("last_called_at")
        ep_copy = dict(ep)
        ep_copy["stats"] = s
        ep_copy["last_called_display"] = _format_last_called(last_at)
        ep_copy["last_called_sort"] = last_at if last_at is not None else 0
        all_endpoints.append(ep_copy)

    total = get_total_endpoint_count()
    total_requests = sum(s.get("request_count", 0) or 0 for s in stats.values())

    # Get user_type statistics for graph
    user_type_stats = get_endpoint_stats_by_user_type(keys)
    aggregated_stats = get_aggregated_stats_by_user_type()

    # Prepare data for graph (JSON serializable)
    graph_data = {
        "by_endpoint": user_type_stats,
        "by_user_type": aggregated_stats,
        "summary": {
            "total_requests": total_requests,
            "total_endpoints": total,
            "user_types_active": sum(1 for ut in aggregated_stats.values() if ut.get("total_requests", 0) > 0)
        }
    }

    context = {
        "all_endpoints": all_endpoints,
        "total_endpoints": total,
        "total_requests": total_requests,
        "user_type_stats_json": json.dumps(graph_data),
        "aggregated_stats": aggregated_stats,
    }
    return render(request, "documentation/api_docs/index.html", context)
