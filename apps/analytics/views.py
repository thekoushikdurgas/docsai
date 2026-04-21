"""
Observability-oriented dashboard: gateway ``admin.logStatistics``,
``health.satelliteHealth``, and ``admin.userStats``.

Time-series charts: pending gateway metrics — see ``contact360.io/admin/TODO.md``
(Phase 6 — Reliability).
"""

from django.shortcuts import render

from apps.admin_ops.services.admin_client import (
    AdminGraphQLError,
    get_gateway_satellite_health,
    get_health_performance_stats,
    get_log_statistics,
    get_user_stats,
)
from apps.core.decorators import require_login


@require_login
def dashboard_view(request):
    """
    Analytics dashboard: gateway ``admin.logStatistics``, ``admin.userStats``, ``health.satelliteHealth``.

    @role: authenticated
    """
    token = request.session.get("operator", {}).get("token", "")
    satellite_health: list = []
    log_stats: dict = {}
    user_stats: dict = {}
    perf_stats: dict = {}
    observability_error = None
    try:
        satellite_health = get_gateway_satellite_health(token)
    except Exception as exc:
        observability_error = str(exc)
    try:
        log_stats = get_log_statistics(token, "24h")
    except AdminGraphQLError as exc:
        if not observability_error:
            observability_error = str(exc)
    except Exception as exc:
        if not observability_error:
            observability_error = str(exc)
    try:
        user_stats = get_user_stats(token)
    except Exception:
        pass
    try:
        perf_stats = get_health_performance_stats(token)
    except Exception:
        perf_stats = {}
    perf_trends = []
    if isinstance(log_stats, dict):
        pt = log_stats.get("performanceTrends") or log_stats.get(
            "performance_trends"
        )
        if isinstance(pt, list):
            perf_trends = pt
    return render(
        request,
        "analytics/dashboard.html",
        {
            "page_title": "Analytics",
            "satellite_health": satellite_health,
            "log_stats": log_stats,
            "user_stats": user_stats,
            "perf_stats": perf_stats,
            "perf_trends": perf_trends,
            "observability_error": observability_error,
        },
    )
