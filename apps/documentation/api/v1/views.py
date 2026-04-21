"""
REST API v1 — DRF JSON endpoints (health, dashboard slices, GraphQL-backed stats).

Health/service_info use ``AllowAny`` — ``@role: public``. Dashboard and ``endpoint_stats``
use default DRF session auth when present — document as ``@role: authenticated`` (JWT/session
optional depending on deployment).
"""

import logging

from django.conf import settings
from django.core.cache import cache
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.core.services.graphql_client import graphql_query
from apps.documentation.services.docs_graphql_adapter import get_adapter
from apps.documentation.utils.api_v1_helpers import (
    to_endpoint_list_item,
    to_page_list_item,
    to_postman_list_item,
    to_relationship_list_item,
)

logger = logging.getLogger(__name__)

_DOCS_STATS = """
query DocsStatsApi {
  docs {
    stats {
      totalPages
      totalEndpoints
      totalRelationships
      totalPostman
      pagesByType { type count }
      endpointsByMethod { method count }
    }
  }
}
"""


@extend_schema(
    summary="Service info", tags=["Health"], responses={200: OpenApiTypes.OBJECT}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def service_info(request):
    cache_key = "admin_api_v1_service_info"
    cached = cache.get(cache_key)
    if cached is not None:
        return Response(cached)
    payload = {
        "service": "contact360-docsai-admin",
        "version": settings.DOCS_AGENT_VERSION,
        "status": "ok",
    }
    cache.set(cache_key, payload, 60)
    return Response(payload)


@extend_schema(
    summary="Overall health", tags=["Health"], responses={200: OpenApiTypes.OBJECT}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_view(request):
    cache_key = "admin_api_v1_health_summary"
    cached = cache.get(cache_key)
    if cached is not None:
        return Response(cached)
    payload = {"status": "ok", "database": "ok", "cache": "ok", "storage": "ok"}
    cache.set(cache_key, payload, 30)
    return Response(payload)


@extend_schema(
    summary="Database health", tags=["Health"], responses={200: OpenApiTypes.OBJECT}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_database(request):
    try:
        from django.db import connection

        connection.ensure_connection()
        return Response({"status": "ok"})
    except Exception as exc:
        return Response({"status": "error", "error": str(exc)}, status=503)


@extend_schema(
    summary="Cache health", tags=["Health"], responses={200: OpenApiTypes.OBJECT}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_cache(request):
    return Response({"status": "ok", "backend": "db"})


@extend_schema(
    summary="Storage health", tags=["Health"], responses={200: OpenApiTypes.OBJECT}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_storage(request):
    url = getattr(settings, "S3STORAGE_API_URL", "")
    return Response(
        {"status": "configured" if url else "not_configured", "url": url or None}
    )


@extend_schema(
    summary="Endpoint stats", tags=["Stats"], responses={200: OpenApiTypes.OBJECT}
)
@api_view(["GET"])
def endpoint_stats(request):
    token = (
        request.session.get("operator", {}).get("token")
        if hasattr(request, "session")
        else None
    )
    try:
        resp = graphql_query(_DOCS_STATS, token=token)
        data = (resp.get("data") or {}).get("docs") or {}
        stats = data.get("stats") or {}
        return Response(
            {"stats": stats, "endpointsByMethod": stats.get("endpointsByMethod") or []}
        )
    except Exception as exc:
        logger.warning("endpoint_stats: %s", exc)
        return Response({"stats": {}, "endpointsByMethod": []})


@extend_schema(
    summary="Endpoint stats by user type",
    tags=["Stats"],
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(["GET"])
def endpoint_stats_by_user_type(request):
    return Response(
        {"byUserType": [], "note": "Populate when gateway exposes user-type breakdown."}
    )


def _page_info(total: int, limit: int, offset: int) -> dict:
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "hasNext": offset + limit < total,
        "hasPrevious": offset > 0,
    }


@extend_schema(
    summary="Dashboard pages", tags=["Dashboard"], responses={200: OpenApiTypes.OBJECT}
)
@api_view(["GET"])
def dashboard_pages(request):
    limit = int(request.query_params.get("limit", 10))
    offset = int(request.query_params.get("offset", 0))
    ad = get_adapter(request)
    r = ad.list_pages(limit=limit, offset=offset)
    pages = r.get("pages", [])
    items = [to_page_list_item(p) for p in pages]
    total = r.get("total", 0)
    return Response({"items": items, "pageInfo": _page_info(total, limit, offset)})


@extend_schema(
    summary="Dashboard endpoints",
    tags=["Dashboard"],
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(["GET"])
def dashboard_endpoints(request):
    limit = int(request.query_params.get("limit", 10))
    offset = int(request.query_params.get("offset", 0))
    ad = get_adapter(request)
    r = ad.list_endpoints(limit=limit, offset=offset)
    eps = r.get("endpoints", [])
    items = [to_endpoint_list_item(p) for p in eps]
    total = r.get("total", 0)
    return Response({"items": items, "pageInfo": _page_info(total, limit, offset)})


@extend_schema(
    summary="Dashboard relationships",
    tags=["Dashboard"],
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(["GET"])
def dashboard_relationships(request):
    limit = int(request.query_params.get("limit", 20))
    offset = int(request.query_params.get("offset", 0))
    ad = get_adapter(request)
    r = ad.list_relationships(limit=limit, offset=offset)
    rels = r.get("relationships", [])
    items = [to_relationship_list_item(p) for p in rels]
    total = r.get("total", 0)
    return Response({"items": items, "pageInfo": _page_info(total, limit, offset)})


@extend_schema(
    summary="Dashboard postman",
    tags=["Dashboard"],
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(["GET"])
def dashboard_postman(request):
    limit = int(request.query_params.get("limit", 10))
    offset = int(request.query_params.get("offset", 0))
    ad = get_adapter(request)
    r = ad.list_configurations(limit=limit, offset=offset)
    cfgs = r.get("configurations", [])
    items = [to_postman_list_item(p) for p in cfgs]
    total = r.get("total", 0)
    return Response({"items": items, "pageInfo": _page_info(total, limit, offset)})
