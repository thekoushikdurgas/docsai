"""Shared dashboard API: statistics and health endpoints."""

from __future__ import annotations

import logging

from apps.core.decorators.auth import require_super_admin
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from apps.documentation.services import get_media_manager_dashboard_service
from apps.documentation.utils.health_checks import get_comprehensive_health_status
from apps.documentation.utils.api_responses import success_response, error_response

logger = logging.getLogger(__name__)


@require_super_admin
@require_http_methods(["GET"])
def get_statistics_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for aggregated documentation statistics.

    Returns aggregated statistics from all services.
    """
    try:
        dashboard_service = get_media_manager_dashboard_service()

        pages_stats = dashboard_service.pages_service.get_pages_statistics()
        endpoints_stats = (
            dashboard_service.endpoints_service.get_api_version_statistics()
        )
        relationships_stats = dashboard_service.relationships_service.get_statistics()
        postman_stats = dashboard_service.postman_service.get_statistics()

        return success_response(
            data={
                "pages": pages_stats,
                "endpoints": endpoints_stats,
                "relationships": relationships_stats,
                "postman": postman_stats,
            },
            message="Statistics retrieved successfully",
        ).to_json_response()

    except Exception as e:
        logger.error(f"Error in get_statistics_api: {e}", exc_info=True)
        return error_response(
            message=f"Failed to retrieve statistics: {str(e)}", status_code=500
        ).to_json_response()


@require_super_admin
@require_http_methods(["GET"])
def get_health_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for aggregated health status for the documentation system.

    Returns comprehensive health status.
    """
    try:
        health_status = get_comprehensive_health_status()

        return success_response(
            data=health_status, message="Health status retrieved successfully"
        ).to_json_response()

    except Exception as e:
        logger.error(f"Error in get_health_api: {e}", exc_info=True)
        return error_response(
            message=f"Failed to retrieve health status: {str(e)}", status_code=500
        ).to_json_response()
