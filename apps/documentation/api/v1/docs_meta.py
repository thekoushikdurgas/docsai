"""
Docs/meta API v1 - Endpoint statistics and docs metadata.

GET /api/v1/docs/endpoint-stats/ returns per-endpoint request counts and last_called_at.
GET /api/v1/docs/endpoint-stats-by-user-type/ returns stats broken down by user type.
"""

from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from apps.documentation.api.v1.api_docs_registry import get_all_endpoint_keys, get_total_endpoint_count
from apps.documentation.utils.api_tracking_storage import (
    get_endpoint_stats,
    get_endpoint_stats_by_user_type,
    get_aggregated_stats_by_user_type,
)


@require_http_methods(["GET"])
def endpoint_stats(request: HttpRequest) -> JsonResponse:
    """
    GET /api/v1/docs/endpoint-stats/

    Returns JSON: { "success": true, "data": { "endpoints": {...}, "total_requests": N, "total_endpoints": N } }
    where endpoints is keyed by endpoint_key with request_count, last_called_at (Unix float or null), etc.
    """
    try:
        keys = get_all_endpoint_keys()
        stats = get_endpoint_stats(keys)
        total_requests = sum(s.get("request_count", 0) or 0 for s in stats.values())
        return JsonResponse({
            "success": True,
            "data": {
                "endpoints": stats,
                "total_requests": total_requests,
                "total_endpoints": get_total_endpoint_count(),
            },
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e),
        }, status=500)


@require_http_methods(["GET"])
def endpoint_stats_by_user_type(request: HttpRequest) -> JsonResponse:
    """
    GET /api/v1/docs/endpoint-stats-by-user-type/
    
    Returns per-endpoint statistics broken down by user type.
    
    Query parameters:
    - user_type: Filter to specific user type (optional)
    - limit: Limit number of endpoints returned (optional, default: all)
    - format: 'graph' optimizes response for graph rendering (optional)
    
    Returns JSON:
    {
        "success": true,
        "data": {
            "by_endpoint": {
                "pages/list": {
                    "super_admin": {"request_count": 45, "last_called_at": 123.45, ...},
                    "admin": {"request_count": 32, ...},
                    ...
                }
            },
            "by_user_type": {
                "super_admin": {
                    "total_requests": 150,
                    "unique_endpoints": 25,
                    "avg_duration_ms": 45.2
                },
                ...
            },
            "summary": {
                "total_requests": 500,
                "total_endpoints": 50,
                "user_types_active": 5
            }
        }
    }
    """
    try:
        keys = get_all_endpoint_keys()
        user_type_filter = request.GET.get('user_type')
        limit = request.GET.get('limit')
        response_format = request.GET.get('format', 'full')
        
        # Get stats by user type
        by_endpoint = get_endpoint_stats_by_user_type(keys)
        
        # Filter by user_type if requested
        if user_type_filter:
            filtered = {}
            for endpoint_key, user_types in by_endpoint.items():
                if user_type_filter in user_types:
                    filtered[endpoint_key] = {user_type_filter: user_types[user_type_filter]}
            by_endpoint = filtered
        
        # Sort endpoints by total requests (sum across all user types)
        if limit:
            sorted_endpoints = sorted(
                by_endpoint.items(),
                key=lambda x: sum(ut.get("request_count", 0) for ut in x[1].values()),
                reverse=True
            )
            by_endpoint = dict(sorted_endpoints[:int(limit)])
        
        # Get aggregated stats per user type
        by_user_type = get_aggregated_stats_by_user_type()
        
        # Calculate summary
        total_requests = sum(ut.get("total_requests", 0) for ut in by_user_type.values())
        user_types_active = sum(1 for ut in by_user_type.values() if ut.get("total_requests", 0) > 0)
        
        data = {
            "by_endpoint": by_endpoint,
            "by_user_type": by_user_type,
            "summary": {
                "total_requests": total_requests,
                "total_endpoints": len(keys),
                "user_types_active": user_types_active,
            }
        }
        
        # Optimize for graph format if requested
        if response_format == 'graph':
            # Transform to graph-friendly structure
            graph_data = {
                "endpoints": [],
                "user_types": list(by_user_type.keys()),
            }
            for endpoint_key, user_types in by_endpoint.items():
                endpoint_data = {"name": endpoint_key}
                for user_type in graph_data["user_types"]:
                    endpoint_data[user_type] = user_types.get(user_type, {}).get("request_count", 0)
                graph_data["endpoints"].append(endpoint_data)
            data["graph_data"] = graph_data
        
        return JsonResponse({
            "success": True,
            "data": data,
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e),
        }, status=500)
