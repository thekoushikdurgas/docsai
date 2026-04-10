"""Documentation Dashboard - Postman resource views."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from django.http import HttpRequest, HttpResponse, Http404
from apps.core.decorators.auth import require_super_admin

from apps.documentation.services import get_postman_service
from apps.documentation.views.dashboard_views_common import (
    render_resource_view as _render_resource_view,
)

logger = logging.getLogger(__name__)


@require_super_admin
def media_manager_postman_detail(request: HttpRequest, config_id: str) -> HttpResponse:
    """
    Media Manager Dashboard - Postman configuration detail view.

    GET /docs/media-manager/postman/<config_id>/
    """
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)

        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")

        # Get related data
        collection = postman_service.get_collection(config_id)
        environments = postman_service.get_environments(config_id)
        mappings = postman_service.get_endpoint_mappings(config_id)
        test_suites = postman_service.get_test_suites(config_id)
        access_control = postman_service.get_access_control(config_id)

        context: Dict[str, Any] = {
            "configuration": configuration,
            "collection": collection,
            "environments": environments or [],
            "mappings": mappings or [],
            "test_suites": test_suites or [],
            "access_control": access_control,
        }

        return _render_resource_view(request, "postman_detail.html", context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading Postman detail {config_id}: {e}", exc_info=True)
        raise Http404(f"Error loading Postman configuration: {config_id}")


@require_super_admin
def media_manager_postman_statistics(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/postman/statistics/"""
    try:
        postman_service = get_postman_service()
        stats = postman_service.get_statistics()
        context: Dict[str, Any] = {"statistics": stats}
        return _render_resource_view(request, "postman_statistics.html", context)
    except Exception as e:
        logger.error(f"Error loading postman statistics: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "postman_statistics.html",
            {"statistics": {}, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_format(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Postman format examples view.

    GET /docs/postman/format/
    Mirrors: GET /api/v1/postman/format/
    """
    try:
        from apps.documentation.api.v1.postman_views import (
            postman_format as api_postman_format,
        )

        json_response = api_postman_format(request)
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

        return _render_resource_view(request, "postman_format.html", context)

    except Exception as e:
        logger.error(f"Error loading postman format: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "postman_format.html",
            {
                "format_data": {},
                "examples": None,
                "analyse_payload_example": None,
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_by_state(request: HttpRequest, state: str) -> HttpResponse:
    """GET /docs/media-manager/postman/by-state/<state>/"""
    try:
        postman_service = get_postman_service()
        result = postman_service.list_by_state(state)
        context: Dict[str, Any] = {
            "configurations": result.get("configurations", []),
            "total": result.get("total", 0),
            "state": state,
            "filters": {"state": state},
        }
        return _render_resource_view(request, "postman_by_state.html", context)
    except Exception as e:
        logger.error(f"Error loading postman by state {state}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            "postman_by_state.html",
            {"configurations": [], "total": 0, "state": state, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_by_state_count(
    request: HttpRequest, state: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/by-state/<state>/count/"""
    try:
        postman_service = get_postman_service()
        count = postman_service.count_by_state(state)
        context: Dict[str, Any] = {"state": state, "count": count}
        return _render_resource_view(request, "postman_count.html", context)
    except Exception as e:
        logger.error(
            f"Error loading postman by state count for {state}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "postman_count.html",
            {"state": state, "count": 0, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_collection(
    request: HttpRequest, config_id: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/<config_id>/collection/"""
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)
        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")
        collection = postman_service.get_collection(config_id)
        context: Dict[str, Any] = {
            "configuration": configuration,
            "config_id": config_id,
            "collection": collection,
        }
        return _render_resource_view(request, "postman_collection.html", context)
    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading postman collection for {config_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "postman_collection.html",
            {"config_id": config_id, "collection": None, "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_environments(
    request: HttpRequest, config_id: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/<config_id>/environments/"""
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)
        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")
        environments = postman_service.get_environments(config_id)
        context: Dict[str, Any] = {
            "configuration": configuration,
            "config_id": config_id,
            "environments": environments or [],
        }
        return _render_resource_view(request, "postman_environments.html", context)
    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading postman environments for {config_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "postman_environments.html",
            {"config_id": config_id, "environments": [], "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_environment(
    request: HttpRequest, config_id: str, env_name: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/<config_id>/environments/<env_name>/"""
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)
        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")
        environment = postman_service.get_environment(config_id, env_name)
        if not environment:
            raise Http404(f"Environment '{env_name}' not found")
        context: Dict[str, Any] = {
            "configuration": configuration,
            "config_id": config_id,
            "env_name": env_name,
            "environment": environment,
        }
        return _render_resource_view(request, "postman_environment.html", context)
    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading postman environment {env_name} for {config_id}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "postman_environment.html",
            {
                "config_id": config_id,
                "env_name": env_name,
                "environment": None,
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_mappings(
    request: HttpRequest, config_id: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/<config_id>/mappings/"""
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)
        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")
        mappings = postman_service.get_endpoint_mappings(config_id)
        context: Dict[str, Any] = {
            "configuration": configuration,
            "config_id": config_id,
            "mappings": mappings or [],
        }
        return _render_resource_view(request, "postman_mappings.html", context)
    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading postman mappings for {config_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "postman_mappings.html",
            {"config_id": config_id, "mappings": [], "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_mapping(
    request: HttpRequest, config_id: str, mapping_id: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/<config_id>/mappings/<mapping_id>/"""
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)
        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")
        mappings = postman_service.get_endpoint_mappings(config_id)
        mapping = next(
            (
                x
                for x in (mappings or [])
                if str(x.get("id")) == str(mapping_id)
                or x.get("mapping_id") == mapping_id
            ),
            None,
        )
        if not mapping:
            raise Http404(f"Mapping '{mapping_id}' not found")
        context: Dict[str, Any] = {
            "configuration": configuration,
            "config_id": config_id,
            "mapping_id": mapping_id,
            "mapping": mapping,
        }
        return _render_resource_view(request, "postman_mapping.html", context)
    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading postman mapping {mapping_id} for {config_id}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "postman_mapping.html",
            {
                "config_id": config_id,
                "mapping_id": mapping_id,
                "mapping": None,
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_test_suites(
    request: HttpRequest, config_id: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/<config_id>/test-suites/"""
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)
        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")
        test_suites = postman_service.get_test_suites(config_id)
        context: Dict[str, Any] = {
            "configuration": configuration,
            "config_id": config_id,
            "test_suites": test_suites or [],
        }
        return _render_resource_view(request, "postman_test_suites.html", context)
    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading postman test suites for {config_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "postman_test_suites.html",
            {"config_id": config_id, "test_suites": [], "error": str(e)},
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_test_suite(
    request: HttpRequest, config_id: str, suite_id: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/<config_id>/test-suites/<suite_id>/"""
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)
        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")
        suite = postman_service.get_test_suite(config_id, suite_id)
        if not suite:
            raise Http404(f"Test suite '{suite_id}' not found")
        context: Dict[str, Any] = {
            "configuration": configuration,
            "config_id": config_id,
            "suite_id": suite_id,
            "suite": suite,
        }
        return _render_resource_view(request, "postman_test_suite.html", context)
    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading postman test suite {suite_id} for {config_id}: {e}",
            exc_info=True,
        )
        return _render_resource_view(
            request,
            "postman_test_suite.html",
            {
                "config_id": config_id,
                "suite_id": suite_id,
                "suite": None,
                "error": str(e),
            },
            error_message=str(e),
        )


@require_super_admin
def media_manager_postman_access_control(
    request: HttpRequest, config_id: str
) -> HttpResponse:
    """GET /docs/media-manager/postman/<config_id>/access-control/"""
    try:
        postman_service = get_postman_service()
        configuration = postman_service.get_configuration(config_id)
        if not configuration:
            raise Http404(f"Postman configuration not found: {config_id}")
        access_control = postman_service.get_access_control(config_id)
        context: Dict[str, Any] = {
            "configuration": configuration,
            "config_id": config_id,
            "access_control": access_control,
        }
        return _render_resource_view(request, "postman_access_control.html", context)
    except Http404:
        raise
    except Exception as e:
        logger.error(
            f"Error loading postman access control for {config_id}: {e}", exc_info=True
        )
        return _render_resource_view(
            request,
            "postman_access_control.html",
            {"config_id": config_id, "access_control": None, "error": str(e)},
            error_message=str(e),
        )
