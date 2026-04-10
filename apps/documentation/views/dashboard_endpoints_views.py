"""Documentation Dashboard - Endpoints resource views."""

from __future__ import annotations

import json
import logging
from collections import Counter
from typing import Any, Dict

from django.http import HttpRequest, HttpResponse, Http404
from apps.core.decorators.auth import require_super_admin

from apps.documentation.services import get_endpoints_service
from apps.documentation.views.dashboard_views_common import (
    render_resource_view as _render_resource_view,
)

logger = logging.getLogger(__name__)


@require_super_admin
def media_manager_endpoint_detail(
    request: HttpRequest, endpoint_id: str
) -> HttpResponse:
    """
    Media Manager Dashboard - Endpoint detail view.

    GET /docs/media-manager/endpoints/<endpoint_id>/
    """
    try:
        endpoints_service = get_endpoints_service()
        endpoint = endpoints_service.get_endpoint(endpoint_id)

        if not endpoint:
            raise Http404(f"Endpoint not found: {endpoint_id}")

        # Get related data
        pages_using = endpoints_service.get_endpoint_pages(endpoint_id)
        access_control = endpoints_service.get_endpoint_access_control(endpoint_id)
        lambda_services = endpoints_service.get_endpoint_lambda_services(endpoint_id)
        files = endpoints_service.get_endpoint_files(endpoint_id)
        dependencies = endpoints_service.get_endpoint_dependencies(endpoint_id)

        context: Dict[str, Any] = {
            "endpoint": endpoint,
            "pages_using": pages_using.get("pages", []),
            "access_control": access_control,
            "lambda_services": lambda_services or [],
            "files": files or [],
            "dependencies": dependencies or [],
        }

        return _render_resource_view(request, "endpoint_detail.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading endpoint detail {endpoint_id}: {e}", exc_info=True)
        raise Http404(f"Error loading endpoint: {endpoint_id}")


@require_super_admin
def media_manager_endpoints_statistics(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/statistics/"""
    try:
        endpoints_service = get_endpoints_service()
        api_version_stats = endpoints_service.get_api_version_statistics()
        method_stats = endpoints_service.get_method_statistics()

        context: Dict[str, Any] = {
            "api_version_statistics": api_version_stats,
            "method_statistics": method_stats,
        }

        return _render_resource_view(request, "statistics_endpoints.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints statistics: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "statistics_endpoints.html",
            {"api_version_statistics": {}, "method_statistics": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_format(request: HttpRequest) -> HttpResponse:
    """GET /docs/endpoints/format/"""
    try:
        from apps.documentation.api.v1.endpoints_views import (
            endpoints_format as api_endpoints_format,
        )

        json_response = api_endpoints_format(request)
        format_data = json.loads(json_response.content)

        examples = None
        if "examples" in format_data:
            examples = json.dumps(format_data["examples"], indent=2)

        analyse_payload_example = None
        if "analyse_payload_example" in format_data:
            analyse_payload_example = json.dumps(
                format_data["analyse_payload_example"], indent=2
            )

        context: Dict[str, Any] = {
            "format_data": format_data,
            "examples": examples,
            "analyse_payload_example": analyse_payload_example,
        }

        return _render_resource_view(request, "endpoints_format.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints format: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_format.html",
            {
                "format_data": {},
                "examples": None,
                "analyse_payload_example": None,
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_api_versions(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/api-versions/"""
    try:
        endpoints_service = get_endpoints_service()
        stats = endpoints_service.get_api_version_statistics()

        context: Dict[str, Any] = {
            "api_versions": stats.get("versions", []),
            "total": stats.get("total", 0),
        }

        return _render_resource_view(request, "endpoints_api_versions.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints api versions: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_api_versions.html",
            {"api_versions": [], "total": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_methods(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/methods/"""
    try:
        endpoints_service = get_endpoints_service()
        stats = endpoints_service.get_method_statistics()

        context: Dict[str, Any] = {
            "methods": stats.get("methods", []),
            "total": stats.get("total", 0),
        }

        return _render_resource_view(request, "endpoints_methods.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints methods: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_methods.html",
            {"methods": [], "total": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_api_version(
    request: HttpRequest, api_version: str
) -> HttpResponse:
    """GET /docs/endpoints/by-api-version/<api_version>/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_api_version(api_version)

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "api_version": api_version,
            "filters": {"api_version": api_version},
        }

        return _render_resource_view(request, "endpoints_by_api_version.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by api version {api_version}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoints_by_api_version.html",
            {"endpoints": [], "total": 0, "api_version": api_version, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_api_version_v1(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-api-version/v1/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_api_version("v1")

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "api_version": "v1",
            "filters": {"api_version": "v1"},
        }

        return _render_resource_view(request, "endpoints_by_api_version.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints by api version v1: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_by_api_version.html",
            {"endpoints": [], "total": 0, "api_version": "v1", "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_api_version_v4(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-api-version/v4/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_api_version("v4")

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "api_version": "v4",
            "filters": {"api_version": "v4"},
        }

        return _render_resource_view(request, "endpoints_by_api_version.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints by api version v4: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_by_api_version.html",
            {"endpoints": [], "total": 0, "api_version": "v4", "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_api_version_graphql(
    request: HttpRequest,
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-api-version/graphql/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_api_version("graphql")

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "api_version": "graphql",
            "filters": {"api_version": "graphql"},
        }

        return _render_resource_view(request, "endpoints_by_api_version.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by api version graphql: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoints_by_api_version.html",
            {"endpoints": [], "total": 0, "api_version": "graphql", "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_api_version_count(
    request: HttpRequest, api_version: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-api-version/<api_version>/count/"""
    try:
        endpoints_service = get_endpoints_service()
        count = endpoints_service.count_endpoints_by_api_version(api_version)

        context: Dict[str, Any] = {
            "api_version": api_version,
            "count": count,
        }

        return _render_resource_view(request, "endpoints_count.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by api version count for {api_version}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "endpoints_count.html",
            {"api_version": api_version, "count": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_api_version_stats(
    request: HttpRequest, api_version: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-api-version/<api_version>/stats/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_api_version(api_version)
        by_method = Counter(ep.get("method", "GET") for ep in endpoints)

        context: Dict[str, Any] = {
            "api_version": api_version,
            "total": len(endpoints),
            "by_method": dict(by_method),
        }

        return _render_resource_view(request, "endpoints_stats.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by api version stats for {api_version}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "endpoints_stats.html",
            {"api_version": api_version, "total": 0, "by_method": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_api_version_by_method(
    request: HttpRequest, api_version: str, method: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-api-version/<api_version>/by-method/<method>/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_version_and_method(
            api_version, method
        )

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "api_version": api_version,
            "method": method,
            "filters": {"api_version": api_version, "method": method},
        }

        return _render_resource_view(request, "endpoints_by_api_version.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by api version {api_version} and method {method}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "endpoints_by_api_version.html",
            {
                "endpoints": [],
                "total": 0,
                "api_version": api_version,
                "method": method,
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_method(
    request: HttpRequest, method: str
) -> HttpResponse:
    """GET /docs/endpoints/by-method/<method>/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_method(method)

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "method": method,
            "filters": {"method": method},
        }

        return _render_resource_view(request, "endpoints_by_method.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints by method {method}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_by_method.html",
            {"endpoints": [], "total": 0, "method": method, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_method_get(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-method/GET/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_method("GET")

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "method": "GET",
            "filters": {"method": "GET"},
        }

        return _render_resource_view(request, "endpoints_by_method.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints by method GET: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_by_method.html",
            {"endpoints": [], "total": 0, "method": "GET", "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_method_post(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-method/POST/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_method("POST")

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "method": "POST",
            "filters": {"method": "POST"},
        }

        return _render_resource_view(request, "endpoints_by_method.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints by method POST: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_by_method.html",
            {"endpoints": [], "total": 0, "method": "POST", "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_method_query(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-method/QUERY/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_method("QUERY")

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "method": "QUERY",
            "filters": {"method": "QUERY"},
        }

        return _render_resource_view(request, "endpoints_by_method.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints by method QUERY: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_by_method.html",
            {"endpoints": [], "total": 0, "method": "QUERY", "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_method_mutation(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-method/MUTATION/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_method("MUTATION")

        context: Dict[str, Any] = {
            "endpoints": endpoints,
            "total": len(endpoints),
            "method": "MUTATION",
            "filters": {"method": "MUTATION"},
        }

        return _render_resource_view(request, "endpoints_by_method.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints by method MUTATION: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_by_method.html",
            {"endpoints": [], "total": 0, "method": "MUTATION", "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_method_count(
    request: HttpRequest, method: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-method/<method>/count/"""
    try:
        endpoints_service = get_endpoints_service()
        count = endpoints_service.count_endpoints_by_method(method)

        context: Dict[str, Any] = {
            "method": method,
            "count": count,
        }

        return _render_resource_view(request, "endpoints_count.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by method count for {method}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoints_count.html",
            {"method": method, "count": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_method_stats(
    request: HttpRequest, method: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-method/<method>/stats/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoints = endpoints_service.get_endpoints_by_method(method)
        by_version = Counter(ep.get("api_version", "v1") for ep in endpoints)

        context: Dict[str, Any] = {
            "method": method,
            "total": len(endpoints),
            "by_api_version": dict(by_version),
        }

        return _render_resource_view(request, "endpoints_stats.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by method stats for {method}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoints_stats.html",
            {"method": method, "total": 0, "by_api_version": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_state(request: HttpRequest, state: str) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-state/<state>/"""
    try:
        endpoints_service = get_endpoints_service()
        result = endpoints_service.list_endpoints(
            endpoint_state=state, limit=None, offset=0
        )

        context: Dict[str, Any] = {
            "endpoints": result.get("endpoints", []),
            "total": result.get("total", 0),
            "state": state,
            "filters": {"state": state},
        }

        return _render_resource_view(request, "endpoints_by_state.html", context)

    except Exception as e:
        logger.error(f"Error loading endpoints by state {state}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "endpoints_by_state.html",
            {"endpoints": [], "total": 0, "state": state, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_state_count(
    request: HttpRequest, state: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-state/<state>/count/"""
    try:
        endpoints_service = get_endpoints_service()
        result = endpoints_service.list_endpoints(
            endpoint_state=state, limit=None, offset=0
        )
        count = result.get("total", 0)

        context: Dict[str, Any] = {
            "state": state,
            "count": count,
        }

        return _render_resource_view(request, "endpoints_count.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by state count for {state}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoints_count.html",
            {"state": state, "count": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_lambda(
    request: HttpRequest, service_name: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-lambda/<service_name>/"""
    try:
        endpoints_service = get_endpoints_service()
        result = endpoints_service.list_endpoints(limit=None, offset=0)
        endpoints = result.get("endpoints", [])
        filtered = []
        for ep in endpoints:
            ls = ep.get("lambda_services") or {}
            primary = ls.get("primary") or {}
            if primary.get("service_name") == service_name:
                filtered.append(ep)
                continue
            for dep in ls.get("dependencies") or []:
                if dep.get("service_name") == service_name:
                    filtered.append(ep)
                    break

        context: Dict[str, Any] = {
            "endpoints": filtered,
            "total": len(filtered),
            "service_name": service_name,
            "filters": {"lambda_service": service_name},
        }

        return _render_resource_view(request, "endpoints_by_lambda.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by lambda service {service_name}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "endpoints_by_lambda.html",
            {
                "endpoints": [],
                "total": 0,
                "service_name": service_name,
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoints_by_lambda_count(
    request: HttpRequest, service_name: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/by-lambda/<service_name>/count/"""
    try:
        endpoints_service = get_endpoints_service()
        result = endpoints_service.list_endpoints(limit=None, offset=0)
        endpoints = result.get("endpoints", [])
        count = 0
        for ep in endpoints:
            ls = ep.get("lambda_services") or {}
            primary = ls.get("primary") or {}
            if primary.get("service_name") == service_name:
                count += 1
                continue
            for dep in ls.get("dependencies") or []:
                if dep.get("service_name") == service_name:
                    count += 1
                    break

        context: Dict[str, Any] = {
            "service_name": service_name,
            "count": count,
        }

        return _render_resource_view(request, "endpoints_count.html", context)

    except Exception as e:
        logger.error(
            f"Error loading endpoints by lambda service count for {service_name}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "endpoints_count.html",
            {"service_name": service_name, "count": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoint_pages(
    request: HttpRequest, endpoint_id: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/<endpoint_id>/pages/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoint = endpoints_service.get_endpoint(endpoint_id)

        if not endpoint:
            raise Http404(f"Endpoint not found: {endpoint_id}")

        pages_result = endpoints_service.get_endpoint_pages(endpoint_id)
        pages = (
            pages_result.get("pages", [])
            if isinstance(pages_result, dict)
            else pages_result or []
        )

        context: Dict[str, Any] = {
            "endpoint": endpoint,
            "endpoint_id": endpoint_id,
            "pages": pages,
            "count": len(pages),
        }

        return _render_resource_view(request, "endpoint_pages.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading endpoint pages for {endpoint_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoint_pages.html",
            {"endpoint_id": endpoint_id, "pages": [], "count": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoint_access_control(
    request: HttpRequest, endpoint_id: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/<endpoint_id>/access-control/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoint = endpoints_service.get_endpoint(endpoint_id)

        if not endpoint:
            raise Http404(f"Endpoint not found: {endpoint_id}")

        access_control = endpoints_service.get_endpoint_access_control(endpoint_id)

        context: Dict[str, Any] = {
            "endpoint": endpoint,
            "endpoint_id": endpoint_id,
            "access_control": access_control,
        }

        return _render_resource_view(request, "endpoint_access_control.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading endpoint access control for {endpoint_id}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "endpoint_access_control.html",
            {"endpoint_id": endpoint_id, "access_control": None, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoint_lambda_services(
    request: HttpRequest, endpoint_id: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/<endpoint_id>/lambda-services/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoint = endpoints_service.get_endpoint(endpoint_id)

        if not endpoint:
            raise Http404(f"Endpoint not found: {endpoint_id}")

        lambda_services = endpoints_service.get_endpoint_lambda_services(endpoint_id)

        context: Dict[str, Any] = {
            "endpoint": endpoint,
            "endpoint_id": endpoint_id,
            "lambda_services": lambda_services or {},
        }

        return _render_resource_view(request, "endpoint_lambda_services.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading endpoint lambda services for {endpoint_id}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "endpoint_lambda_services.html",
            {"endpoint_id": endpoint_id, "lambda_services": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoint_files(
    request: HttpRequest, endpoint_id: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/<endpoint_id>/files/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoint = endpoints_service.get_endpoint(endpoint_id)

        if not endpoint:
            raise Http404(f"Endpoint not found: {endpoint_id}")

        files = endpoints_service.get_endpoint_files(endpoint_id)

        context: Dict[str, Any] = {
            "endpoint": endpoint,
            "endpoint_id": endpoint_id,
            "service_file": endpoint.get("service_file"),
            "router_file": endpoint.get("router_file"),
            "files": files or [],
        }

        return _render_resource_view(request, "endpoint_files.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading endpoint files for {endpoint_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoint_files.html",
            {
                "endpoint_id": endpoint_id,
                "service_file": None,
                "router_file": None,
                "files": [],
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoint_methods(
    request: HttpRequest, endpoint_id: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/<endpoint_id>/methods/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoint = endpoints_service.get_endpoint(endpoint_id)

        if not endpoint:
            raise Http404(f"Endpoint not found: {endpoint_id}")

        methods = endpoint.get("service_methods") or []

        context: Dict[str, Any] = {
            "endpoint": endpoint,
            "endpoint_id": endpoint_id,
            "methods": methods,
            "count": len(methods),
        }

        return _render_resource_view(request, "endpoint_methods.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading endpoint methods for {endpoint_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoint_methods.html",
            {"endpoint_id": endpoint_id, "methods": [], "count": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoint_used_by_pages(
    request: HttpRequest, endpoint_id: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/<endpoint_id>/used-by-pages/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoint = endpoints_service.get_endpoint(endpoint_id)

        if not endpoint:
            raise Http404(f"Endpoint not found: {endpoint_id}")

        pages = endpoint.get("used_by_pages") or []

        context: Dict[str, Any] = {
            "endpoint": endpoint,
            "endpoint_id": endpoint_id,
            "used_by_pages": pages,
            "count": len(pages),
        }

        return _render_resource_view(request, "endpoint_used_by_pages.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading endpoint used by pages for {endpoint_id}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "endpoint_used_by_pages.html",
            {
                "endpoint_id": endpoint_id,
                "used_by_pages": [],
                "count": 0,
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_endpoint_dependencies(
    request: HttpRequest, endpoint_id: str
) -> HttpResponse:
    """GET /docs/media-manager/endpoints/<endpoint_id>/dependencies/"""
    try:
        endpoints_service = get_endpoints_service()
        endpoint = endpoints_service.get_endpoint(endpoint_id)

        if not endpoint:
            raise Http404(f"Endpoint not found: {endpoint_id}")

        dependencies = endpoints_service.get_endpoint_dependencies(endpoint_id)
        deps = (
            dependencies
            if isinstance(dependencies, list)
            else (endpoint.get("lambda_services") or {}).get("dependencies") or []
        )

        context: Dict[str, Any] = {
            "endpoint": endpoint,
            "endpoint_id": endpoint_id,
            "dependencies": deps,
            "count": len(deps),
        }

        return _render_resource_view(request, "endpoint_dependencies.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading endpoint dependencies for {endpoint_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "endpoint_dependencies.html",
            {
                "endpoint_id": endpoint_id,
                "dependencies": [],
                "count": 0,
                "error": str(e),
            },
            error_message=str(e),
        )
