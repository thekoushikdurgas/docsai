"""
Documentation Dashboard views — facade module.

Implementation is split into:
- dashboard_views_common: Shared helpers (validate_tab, render_resource_view, etc.)
- dashboard_pages_views: Page resource views
- dashboard_endpoints_views: Endpoint resource views
- dashboard_relationships_views: Relationship resource views
- dashboard_postman_views: Postman resource views

This module re-exports all media_manager_* views for urls.py compatibility.
All exported views use ``@require_super_admin``; docstrings end with ``@role: super_admin``.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from django.shortcuts import render
from apps.core.decorators.auth import require_super_admin
from django.http import HttpRequest, HttpResponse
from django.utils.safestring import mark_safe

from apps.documentation.services import get_media_manager_dashboard_service
from apps.documentation.views.dashboard_views_common import (
    VALID_TABS,
    validate_tab as _validate_tab,
    validate_view_mode as _validate_view_mode,
    render_resource_view as _render_resource_view,
)

# Per-resource view modules - explicit imports to avoid conflicts
from .dashboard_pages_views import (
    media_manager_page_detail,
    media_manager_pages_format,
    media_manager_pages_types,
    media_manager_pages_by_type_docs,
    media_manager_pages_by_type_marketing,
    media_manager_pages_by_type_dashboard,
    media_manager_pages_by_type_product,
    media_manager_pages_by_type_title,
    media_manager_pages_by_type,
    media_manager_pages_by_type_count,
    media_manager_pages_by_type_published,
    media_manager_pages_by_type_draft,
    media_manager_pages_by_type_stats,
    media_manager_pages_by_state,
    media_manager_pages_by_state_count,
    media_manager_pages_by_user_type,
    media_manager_page_sections,
    media_manager_page_components,
    media_manager_page_endpoints,
    media_manager_page_versions,
    media_manager_page_access_control,
)
from .dashboard_endpoints_views import (
    media_manager_endpoint_detail,
    media_manager_endpoints_statistics,
    media_manager_endpoints_format,
    media_manager_endpoints_api_versions,
    media_manager_endpoints_methods,
    media_manager_endpoints_by_api_version,
    media_manager_endpoints_by_api_version_v1,
    media_manager_endpoints_by_api_version_v4,
    media_manager_endpoints_by_api_version_graphql,
    media_manager_endpoints_by_api_version_count,
    media_manager_endpoints_by_api_version_stats,
    media_manager_endpoints_by_api_version_by_method,
    media_manager_endpoints_by_method,
    media_manager_endpoints_by_method_get,
    media_manager_endpoints_by_method_post,
    media_manager_endpoints_by_method_query,
    media_manager_endpoints_by_method_mutation,
    media_manager_endpoints_by_method_count,
    media_manager_endpoints_by_method_stats,
    media_manager_endpoints_by_state,
    media_manager_endpoints_by_state_count,
    media_manager_endpoints_by_lambda,
    media_manager_endpoints_by_lambda_count,
    media_manager_endpoint_pages,
    media_manager_endpoint_access_control,
    media_manager_endpoint_lambda_services,
    media_manager_endpoint_files,
    media_manager_endpoint_methods,
    media_manager_endpoint_used_by_pages,
    media_manager_endpoint_dependencies,
)
from .dashboard_relationships_views import (
    media_manager_relationship_detail,
    media_manager_relationships_statistics,
    media_manager_relationships_format,
    media_manager_relationships_graph,
    media_manager_relationships_usage_types,
    media_manager_relationships_usage_contexts,
    media_manager_relationships_by_page,
    media_manager_relationships_by_page_count,
    media_manager_relationships_by_page_primary,
    media_manager_relationships_by_page_secondary,
    media_manager_relationships_by_page_by_usage_type,
    media_manager_relationships_by_endpoint,
    media_manager_relationships_by_endpoint_count,
    media_manager_relationships_by_endpoint_pages,
    media_manager_relationships_by_endpoint_by_usage_context,
    media_manager_relationships_by_usage_type,
    media_manager_relationships_by_usage_type_primary,
    media_manager_relationships_by_usage_type_secondary,
    media_manager_relationships_by_usage_type_conditional,
    media_manager_relationships_by_usage_type_count,
    media_manager_relationships_by_usage_type_by_usage_context,
    media_manager_relationships_by_usage_context,
    media_manager_relationships_by_usage_context_data_fetching,
    media_manager_relationships_by_usage_context_data_mutation,
    media_manager_relationships_by_usage_context_authentication,
    media_manager_relationships_by_usage_context_analytics,
    media_manager_relationships_by_usage_context_count,
    media_manager_relationships_by_state,
    media_manager_relationships_by_state_count,
    media_manager_relationships_by_lambda,
    media_manager_relationships_by_invocation_pattern,
    media_manager_relationships_by_postman_config,
    media_manager_relationships_performance_slow,
    media_manager_relationships_performance_errors,
    media_manager_relationship_access_control,
    media_manager_relationship_data_flow,
    media_manager_relationship_performance,
    media_manager_relationship_dependencies,
    media_manager_relationship_postman,
)
from .dashboard_postman_views import (
    media_manager_postman_detail,
    media_manager_postman_statistics,
    media_manager_postman_format,
    media_manager_postman_by_state,
    media_manager_postman_by_state_count,
    media_manager_postman_collection,
    media_manager_postman_environments,
    media_manager_postman_environment,
    media_manager_postman_mappings,
    media_manager_postman_mapping,
    media_manager_postman_test_suites,
    media_manager_postman_test_suite,
    media_manager_postman_access_control,
)

logger = logging.getLogger(__name__)


@require_super_admin
def media_manager_dashboard(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Main view.

    GET /docs/media-manager/
    GET /docs/media-manager/pages/
    GET /docs/media-manager/endpoints/
    GET /docs/media-manager/relationships/
    GET /docs/media-manager/postman/

    Query params:
    - tab: pages|endpoints|relationships|postman (default: pages)
    - view: list|grid|detail (default: list)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    - search: Search query
    - sort: Sort field
    - order: Sort order (asc|desc)
    - Additional filters per resource type
    """
    # Determine active tab from URL path or query param
    path_parts = request.path.strip("/").split("/")
    if (
        len(path_parts) >= 3
        and path_parts[1] == "media-manager"
        and path_parts[2] in VALID_TABS
    ):
        active_tab = path_parts[2]
    else:
        active_tab = request.GET.get("tab", "pages")

    active_tab = _validate_tab(active_tab)
    view_mode = _validate_view_mode(request.GET.get("view", "list"))

    # Initialize services
    dashboard_service = get_media_manager_dashboard_service()

    # Get overview statistics
    try:
        overview_stats = dashboard_service.get_dashboard_overview()
    except Exception as e:
        logger.error(f"Failed to get overview stats: {e}", exc_info=True)
        overview_stats = {}

    # Get health status
    try:
        health_status = dashboard_service.get_health_status()
    except Exception as e:
        logger.error(f"Failed to get health status: {e}", exc_info=True)
        health_status = {}

    # Get initial data for active tab
    initial_data: Dict[str, Any] = {}
    try:
        # Extract filters from query params
        filters = {
            "limit": int(request.GET.get("per_page", 20)),
            "offset": (int(request.GET.get("page", 1)) - 1)
            * int(request.GET.get("per_page", 20)),
        }

        # Add resource-specific filters
        if active_tab == "pages":
            if request.GET.get("page_type"):
                filters["page_type"] = request.GET.get("page_type")
            if request.GET.get("status"):
                filters["status"] = request.GET.get("status")
            if request.GET.get("state"):
                filters["state"] = request.GET.get("state")
            if request.GET.get("include_drafts"):
                filters["include_drafts"] = (
                    request.GET.get("include_drafts", "true").lower() == "true"
                )
            if request.GET.get("include_deleted"):
                filters["include_deleted"] = (
                    request.GET.get("include_deleted", "false").lower() == "true"
                )

            result = dashboard_service.get_resource_list("pages", filters)
            initial_data = {
                "pages": result.get("pages", [])[: filters["limit"]],
                "total": result.get("total", 0),
                "source": result.get("source", "local"),
            }

        elif active_tab == "endpoints":
            if request.GET.get("api_version"):
                filters["api_version"] = request.GET.get("api_version")
            if request.GET.get("method"):
                filters["method"] = request.GET.get("method")
            if request.GET.get("state"):
                filters["state"] = request.GET.get("state")
            if request.GET.get("lambda_service"):
                filters["lambda_service"] = request.GET.get("lambda_service")

            result = dashboard_service.get_resource_list("endpoints", filters)
            initial_data = {
                "endpoints": result.get("endpoints", [])[: filters["limit"]],
                "total": result.get("total", 0),
                "source": result.get("source", "local"),
            }

        elif active_tab == "relationships":
            if request.GET.get("page_id"):
                filters["page_id"] = request.GET.get("page_id")
            if request.GET.get("endpoint_id"):
                filters["endpoint_id"] = request.GET.get("endpoint_id")
            if request.GET.get("usage_type"):
                filters["usage_type"] = request.GET.get("usage_type")
            if request.GET.get("usage_context"):
                filters["usage_context"] = request.GET.get("usage_context")

            result = dashboard_service.get_resource_list("relationships", filters)
            initial_data = {
                "relationships": result.get("relationships", [])[: filters["limit"]],
                "total": result.get("total", 0),
                "source": result.get("source", "local"),
            }

        elif active_tab == "postman":
            if request.GET.get("state"):
                filters["state"] = request.GET.get("state")

            result = dashboard_service.get_resource_list("postman", filters)
            initial_data = {
                "postman": result.get("configurations", [])[: filters["limit"]],
                "total": result.get("total", 0),
                "source": result.get("source", "local"),
            }

    except Exception as e:
        logger.error(
            f"Error loading initial data for tab {active_tab}: {e}", exc_info=True
        )
        initial_data = {
            "pages": [],
            "endpoints": [],
            "relationships": [],
            "postman": [],
            "total": 0,
        }

    context: Dict[str, Any] = {
        "active_tab": active_tab,
        "view_mode": view_mode,
        "overview_stats": overview_stats,
        "health_status": health_status,
        "initial_data": mark_safe(json.dumps(initial_data)),
    }

    return render(request, "documentation/media_manager_dashboard.html", context)


@require_super_admin
def media_manager_index_pages(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/index/pages/"""
    try:
        from apps.documentation.services import get_shared_s3_index_manager

        index_manager = get_shared_s3_index_manager()
        index_data = index_manager.read_index("pages")
        context: Dict[str, Any] = {"index_type": "pages", "index_data": index_data}
        return _render_resource_view(request, "index_detail.html", context)
    except Exception as e:
        logger.error(f"Error loading pages index: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "index_detail.html",
            {"index_type": "pages", "index_data": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_index_endpoints(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/index/endpoints/"""
    try:
        from apps.documentation.services import get_shared_s3_index_manager

        index_manager = get_shared_s3_index_manager()
        index_data = index_manager.read_index("endpoints")
        context: Dict[str, Any] = {"index_type": "endpoints", "index_data": index_data}
        return _render_resource_view(request, "index_detail.html", context)
    except Exception as e:
        logger.error(f"Error loading endpoints index: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "index_detail.html",
            {"index_type": "endpoints", "index_data": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_index_relationships(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/index/relationships/"""
    try:
        from apps.documentation.services import get_shared_s3_index_manager

        index_manager = get_shared_s3_index_manager()
        index_data = index_manager.read_index("relationships")
        context: Dict[str, Any] = {
            "index_type": "relationships",
            "index_data": index_data,
        }
        return _render_resource_view(request, "index_detail.html", context)
    except Exception as e:
        logger.error(f"Error loading relationships index: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "index_detail.html",
            {"index_type": "relationships", "index_data": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_index_postman(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/index/postman/"""
    try:
        from apps.documentation.services import get_shared_s3_index_manager

        index_manager = get_shared_s3_index_manager()
        index_data = index_manager.read_index("postman")
        context: Dict[str, Any] = {"index_type": "postman", "index_data": index_data}
        return _render_resource_view(request, "index_detail.html", context)
    except Exception as e:
        logger.error(f"Error loading postman index: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "index_detail.html",
            {"index_type": "postman", "index_data": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_index_pages_validate(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/index/pages/validate/"""
    try:
        from apps.documentation.services import get_shared_s3_index_manager

        index_manager = get_shared_s3_index_manager()
        result = index_manager.validate_index("pages")
        context: Dict[str, Any] = {"index_type": "pages", "validation_result": result}
        return _render_resource_view(request, "index_validate.html", context)
    except Exception as e:
        logger.error(f"Error validating pages index: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "index_validate.html",
            {
                "index_type": "pages",
                "validation_result": {"valid": False, "error": str(e)},
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_index_endpoints_validate(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/index/endpoints/validate/"""
    try:
        from apps.documentation.services import get_shared_s3_index_manager

        index_manager = get_shared_s3_index_manager()
        result = index_manager.validate_index("endpoints")
        context: Dict[str, Any] = {
            "index_type": "endpoints",
            "validation_result": result,
        }
        return _render_resource_view(request, "index_validate.html", context)
    except Exception as e:
        logger.error(f"Error validating endpoints index: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "index_validate.html",
            {
                "index_type": "endpoints",
                "validation_result": {"valid": False, "error": str(e)},
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_index_relationships_validate(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/index/relationships/validate/"""
    try:
        from apps.documentation.services import get_shared_s3_index_manager

        index_manager = get_shared_s3_index_manager()
        result = index_manager.validate_index("relationships")
        context: Dict[str, Any] = {
            "index_type": "relationships",
            "validation_result": result,
        }
        return _render_resource_view(request, "index_validate.html", context)
    except Exception as e:
        logger.error(f"Error validating relationships index: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "index_validate.html",
            {
                "index_type": "relationships",
                "validation_result": {"valid": False, "error": str(e)},
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_index_postman_validate(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/index/postman/validate/"""
    try:
        from apps.documentation.services import get_shared_s3_index_manager

        index_manager = get_shared_s3_index_manager()
        result = index_manager.validate_index("postman")
        context: Dict[str, Any] = {"index_type": "postman", "validation_result": result}
        return _render_resource_view(request, "index_validate.html", context)
    except Exception as e:
        logger.error(f"Error validating postman index: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "index_validate.html",
            {
                "index_type": "postman",
                "validation_result": {"valid": False, "error": str(e)},
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_service_info(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Service info view.

    GET /docs/media-manager/service-info/
    Mirrors: GET /api/v1/
    """
    try:
        from apps.documentation.api.v1.health import service_info

        json_response = service_info(request)
        data = json.loads(json_response.content)

        context: Dict[str, Any] = {
            "service_info": data.get("data", {}),
            "success": data.get("success", True),
        }

        return _render_resource_view(request, "service_info.html", context)

    except Exception as e:
        logger.error(f"Error loading service info: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "service_info.html",
            {"service_info": {}, "success": False, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_docs_endpoint_stats(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Docs endpoint stats view.

    GET /docs/media-manager/docs/endpoint-stats/
    Mirrors: GET /api/v1/docs/endpoint-stats/
    """
    try:
        from apps.documentation.api.v1.docs_meta import endpoint_stats

        json_response = endpoint_stats(request)
        data = json.loads(json_response.content)

        context: Dict[str, Any] = {
            "endpoint_stats": data.get("data", {}),
            "success": data.get("success", True),
        }

        return _render_resource_view(request, "docs_endpoint_stats.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoint stats: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "docs_endpoint_stats.html",
            {"endpoint_stats": {}, "success": False, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_dashboard_pages(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Dashboard pages API view.

    GET /docs/media-manager/dashboard/pages/
    Mirrors: GET /api/v1/dashboard/pages/
    """
    try:
        from apps.documentation.api.v1.core import dashboard_pages

        json_response = dashboard_pages(request)
        data = json.loads(json_response.content)

        context: Dict[str, Any] = {
            "resource": "pages",
            "dashboard_data": data,
            "items": data.get("items", []),
            "pagination": data.get("pagination", {}),
        }

        return _render_resource_view(request, "dashboard_pages.html", context)

    except Exception as e:
        logger.error(f"Error loading dashboard pages: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "dashboard_pages.html",
            {"resource": "pages", "dashboard_data": {}, "items": [], "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_dashboard_endpoints(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Dashboard endpoints API view.

    GET /docs/media-manager/dashboard/endpoints/
    Mirrors: GET /api/v1/dashboard/endpoints/
    """
    try:
        from apps.documentation.api.v1.core import dashboard_endpoints

        json_response = dashboard_endpoints(request)
        data = json.loads(json_response.content)

        context: Dict[str, Any] = {
            "resource": "endpoints",
            "dashboard_data": data,
            "items": data.get("items", []),
            "pagination": data.get("pagination", {}),
        }

        return _render_resource_view(request, "dashboard_endpoints.html", context)

    except Exception as e:
        logger.error(f"Error loading dashboard endpoints: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "dashboard_endpoints.html",
            {
                "resource": "endpoints",
                "dashboard_data": {},
                "items": [],
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_dashboard_relationships(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Dashboard relationships API view.

    GET /docs/media-manager/dashboard/relationships/
    Mirrors: GET /api/v1/dashboard/relationships/
    """
    try:
        from apps.documentation.api.v1.core import dashboard_relationships

        json_response = dashboard_relationships(request)
        data = json.loads(json_response.content)

        context: Dict[str, Any] = {
            "resource": "relationships",
            "dashboard_data": data,
            "items": data.get("items", []),
            "pagination": data.get("pagination", {}),
        }

        return _render_resource_view(request, "dashboard_relationships.html", context)

    except Exception as e:
        logger.error(f"Error loading dashboard relationships: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "dashboard_relationships.html",
            {
                "resource": "relationships",
                "dashboard_data": {},
                "items": [],
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_dashboard_postman(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Dashboard postman API view.

    GET /docs/media-manager/dashboard/postman/
    Mirrors: GET /api/v1/dashboard/postman/
    """
    try:
        from apps.documentation.api.v1.core import dashboard_postman

        json_response = dashboard_postman(request)
        data = json.loads(json_response.content)

        context: Dict[str, Any] = {
            "resource": "postman",
            "dashboard_data": data,
            "items": data.get("items", []),
            "pagination": data.get("pagination", {}),
        }

        return _render_resource_view(request, "dashboard_postman.html", context)

    except Exception as e:
        logger.error(f"Error loading dashboard postman: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "dashboard_postman.html",
            {"resource": "postman", "dashboard_data": {}, "items": [], "error": str(e)},
            error_message=str(e),
        )
