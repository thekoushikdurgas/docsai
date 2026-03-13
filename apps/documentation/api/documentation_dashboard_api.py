
"""Documentation Dashboard AJAX API endpoints - service-based implementation."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from apps.core.decorators.auth import require_super_admin, require_admin_or_super_admin
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.documentation.services import (
    get_pages_service,
    get_endpoints_service,
    get_relationships_service,
    get_postman_service,
    get_media_manager_dashboard_service,
)
from apps.documentation.utils.health_checks import get_comprehensive_health_status
from apps.documentation.utils.api_responses import (
    success_response,
    error_response,
    paginated_response,
)
from apps.documentation.utils.list_projectors import (
    should_expand_full,
    to_page_list_item,
    to_endpoint_list_item,
    to_relationship_list_item,
    to_postman_list_item,
)

logger = logging.getLogger(__name__)


@require_super_admin
@require_http_methods(["GET"])
def get_pages_list_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for pages list on the documentation dashboard.
    
    Query params:
    - page_type: Filter by page type
    - status: Filter by status
    - state: Filter by page state
    - include_drafts: Include draft pages (default: true)
    - include_deleted: Include deleted pages (default: false)
    - limit: Items per page (default: 20)
    - offset: Offset for pagination (default: 0)
    - search: Search query (client-side filtering)
    - sort: Sort field
    - order: Sort order (asc|desc)
    """
    try:
        pages_service = get_pages_service()
        
        # Extract query parameters
        page_type = request.GET.get('page_type')
        status = request.GET.get('status')
        state = request.GET.get('state')
        include_drafts = request.GET.get('include_drafts', 'true').lower() == 'true'
        include_deleted = request.GET.get('include_deleted', 'false').lower() == 'true'
        try:
            limit = min(int(request.GET.get('limit', 20)), 100)
        except (TypeError, ValueError):
            limit = 20
        offset = int(request.GET.get('offset', 0))
        
        # Get pages from service
        result = pages_service.list_pages(
            page_type=page_type,
            status=status,
            page_state=state,
            include_drafts=include_drafts,
            include_deleted=include_deleted,
            limit=limit,
            offset=offset,
        )
        
        pages = result.get('pages', [])
        total = result.get('total', 0)
        
        # Apply client-side search if provided
        search_query = request.GET.get('search', '').strip().lower()
        if search_query:
            filtered_pages = []
            for page in pages:
                page_id = page.get('page_id', '').lower()
                title = (page.get('metadata', {}).get('content_sections', {}).get('title', '') or '').lower()
                if search_query in page_id or search_query in title:
                    filtered_pages.append(page)
            pages = filtered_pages
            total = len(filtered_pages)
        
        # Apply sorting if provided
        sort_field = request.GET.get('sort')
        sort_order = request.GET.get('order', 'asc').lower()
        if sort_field:
            reverse_order = sort_order == 'desc'
            if sort_field == 'name':
                pages.sort(key=lambda p: p.get('page_id', '').lower(), reverse=reverse_order)
            elif sort_field == 'updated':
                pages.sort(key=lambda p: p.get('updated_at', ''), reverse=reverse_order)
            elif sort_field == 'created':
                pages.sort(key=lambda p: p.get('created_at', ''), reverse=reverse_order)

        if not should_expand_full(request.GET):
            pages = [to_page_list_item(p) for p in pages]
        
        return success_response(
            data={
                'pages': pages,
                'total': total,
                'limit': limit,
                'offset': offset,
            },
            message="Pages retrieved successfully"
        ).to_json_response()
    
    except Exception as e:
        logger.error(f"Error in get_pages_list_api: {e}", exc_info=True)
        return error_response(
            message=f"Failed to retrieve pages: {str(e)}",
            status_code=500
        ).to_json_response()


@require_super_admin
@require_http_methods(["GET"])
def get_endpoints_list_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for endpoints list on the documentation dashboard.
    
    Query params:
    - api_version: Filter by API version
    - method: Filter by HTTP/GraphQL method
    - state: Filter by endpoint state
    - lambda_service: Filter by Lambda service
    - limit: Items per page (default: 20)
    - offset: Offset for pagination (default: 0)
    - search: Search query
    - sort: Sort field
    - order: Sort order (asc|desc)
    """
    try:
        endpoints_service = get_endpoints_service()
        
        # Extract query parameters
        api_version = request.GET.get('api_version')
        method = request.GET.get('method')
        state = request.GET.get('state')
        lambda_service = request.GET.get('lambda_service')
        try:
            limit = min(int(request.GET.get('limit', 20)), 100)
        except (TypeError, ValueError):
            limit = 20
        offset = int(request.GET.get('offset', 0))
        
        # Get endpoints from service
        result = endpoints_service.list_endpoints(
            api_version=api_version,
            method=method,
            endpoint_state=state,
            limit=limit,
            offset=offset,
        )
        
        endpoints = result.get('endpoints', [])
        total = result.get('total', 0)
        
        # Filter by Lambda service if provided
        if lambda_service:
            filtered_endpoints = []
            for endpoint in endpoints:
                lambda_services = endpoint.get('lambda_services', [])
                if isinstance(lambda_services, list):
                    if any(ls.get('service_name') == lambda_service for ls in lambda_services if isinstance(ls, dict)):
                        filtered_endpoints.append(endpoint)
                elif isinstance(lambda_services, str) and lambda_services == lambda_service:
                    filtered_endpoints.append(endpoint)
            endpoints = filtered_endpoints
            total = len(filtered_endpoints)
        
        # Apply client-side search if provided
        search_query = request.GET.get('search', '').strip().lower()
        if search_query:
            filtered_endpoints = []
            for endpoint in endpoints:
                endpoint_id = endpoint.get('endpoint_id', '').lower()
                endpoint_path = endpoint.get('endpoint_path', '').lower()
                if search_query in endpoint_id or search_query in endpoint_path:
                    filtered_endpoints.append(endpoint)
            endpoints = filtered_endpoints
            total = len(filtered_endpoints)
        
        # Apply sorting if provided
        sort_field = request.GET.get('sort')
        sort_order = request.GET.get('order', 'asc').lower()
        if sort_field:
            reverse_order = sort_order == 'desc'
            if sort_field == 'name':
                endpoints.sort(key=lambda e: e.get('endpoint_id', '').lower(), reverse=reverse_order)
            elif sort_field == 'updated':
                endpoints.sort(key=lambda e: e.get('updated_at', ''), reverse=reverse_order)

        if not should_expand_full(request.GET):
            endpoints = [to_endpoint_list_item(ep) for ep in endpoints]
        
        return success_response(
            data={
                'endpoints': endpoints,
                'total': total,
                'limit': limit,
                'offset': offset,
            },
            message="Endpoints retrieved successfully"
        ).to_json_response()
    
    except Exception as e:
        logger.error(f"Error in get_endpoints_list_api: {e}", exc_info=True)
        return error_response(
            message=f"Failed to retrieve endpoints: {str(e)}",
            status_code=500
        ).to_json_response()


@require_super_admin
@require_http_methods(["GET"])
def get_relationships_list_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for relationships list on the documentation dashboard.
    
    Query params:
    - page_id: Filter by page
    - endpoint_id: Filter by endpoint
    - usage_type: Filter by usage type
    - usage_context: Filter by usage context
    - limit: Items per page (default: 20)
    - offset: Offset for pagination (default: 0)
    - search: Search query
    - sort: Sort field
    - order: Sort order (asc|desc)
    """
    try:
        relationships_service = get_relationships_service()
        
        # Extract query parameters
        page_id = request.GET.get('page_id')
        endpoint_id = request.GET.get('endpoint_id')
        usage_type = request.GET.get('usage_type')
        usage_context = request.GET.get('usage_context')
        try:
            limit = min(int(request.GET.get('limit', 20)), 100)
        except (TypeError, ValueError):
            limit = 20
        offset = int(request.GET.get('offset', 0))
        
        # Get relationships from service
        result = relationships_service.list_relationships(
            page_id=page_id,
            endpoint_id=endpoint_id,
            usage_type=usage_type,
            usage_context=usage_context,
            limit=limit,
            offset=offset,
        )
        
        relationships = result.get('relationships', [])
        total = result.get('total', 0)
        
        # Apply client-side search if provided
        search_query = request.GET.get('search', '').strip().lower()
        if search_query:
            filtered_relationships = []
            for rel in relationships:
                page_path = (rel.get('page_path') or '').lower()
                endpoint_path = (rel.get('endpoint_path') or '').lower()
                if search_query in page_path or search_query in endpoint_path:
                    filtered_relationships.append(rel)
            relationships = filtered_relationships
            total = len(filtered_relationships)
        
        # Apply sorting if provided
        sort_field = request.GET.get('sort')
        sort_order = request.GET.get('order', 'asc').lower()
        if sort_field:
            reverse_order = sort_order == 'desc'
            if sort_field == 'name':
                relationships.sort(key=lambda r: (r.get('page_path') or '').lower(), reverse=reverse_order)
            elif sort_field == 'updated':
                relationships.sort(key=lambda r: r.get('updated_at', ''), reverse=reverse_order)

        if not should_expand_full(request.GET):
            relationships = [to_relationship_list_item(r) for r in relationships]
        
        return success_response(
            data={
                'relationships': relationships,
                'total': total,
                'limit': limit,
                'offset': offset,
            },
            message="Relationships retrieved successfully"
        ).to_json_response()
    
    except Exception as e:
        logger.error(f"Error in get_relationships_list_api: {e}", exc_info=True)
        return error_response(
            message=f"Failed to retrieve relationships: {str(e)}",
            status_code=500
        ).to_json_response()


@require_super_admin
@require_http_methods(["GET"])
def get_postman_list_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for Postman configurations list on the documentation dashboard.
    
    Query params:
    - state: Filter by state
    - limit: Items per page (default: 20)
    - offset: Offset for pagination (default: 0)
    - search: Search query
    - sort: Sort field
    - order: Sort order (asc|desc)
    """
    try:
        postman_service = get_postman_service()
        
        # Extract query parameters
        state = request.GET.get('state')
        try:
            limit = min(int(request.GET.get('limit', 20)), 100)
        except (TypeError, ValueError):
            limit = 20
        offset = int(request.GET.get('offset', 0))
        
        # Get configurations from service
        result = postman_service.list_configurations(
            state=state,
            limit=limit,
            offset=offset,
        )
        
        configurations = result.get('configurations', [])
        total = result.get('total', 0)
        
        # Apply client-side search if provided
        search_query = request.GET.get('search', '').strip().lower()
        if search_query:
            filtered_configs = []
            for config in configurations:
                config_id = (config.get('config_id') or '').lower()
                name = (config.get('name') or '').lower()
                if search_query in config_id or search_query in name:
                    filtered_configs.append(config)
            configurations = filtered_configs
            total = len(filtered_configs)
        
        # Apply sorting if provided
        sort_field = request.GET.get('sort')
        sort_order = request.GET.get('order', 'asc').lower()
        if sort_field:
            reverse_order = sort_order == 'desc'
            if sort_field == 'name':
                configurations.sort(key=lambda c: (c.get('config_id') or '').lower(), reverse=reverse_order)
            elif sort_field == 'updated':
                configurations.sort(key=lambda c: c.get('updated_at', ''), reverse=reverse_order)

        if not should_expand_full(request.GET):
            configurations = [to_postman_list_item(c) for c in configurations]
        
        return success_response(
            data={
                'configurations': configurations,
                'total': total,
                'limit': limit,
                'offset': offset,
            },
            message="Postman configurations retrieved successfully"
        ).to_json_response()
    
    except Exception as e:
        logger.error(f"Error in get_postman_list_api: {e}", exc_info=True)
        return error_response(
            message=f"Failed to retrieve Postman configurations: {str(e)}",
            status_code=500
        ).to_json_response()


@require_super_admin
@require_http_methods(["GET"])
def get_statistics_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for aggregated documentation statistics.
    
    Returns aggregated statistics from all services.
    """
    try:
        dashboard_service = get_media_manager_dashboard_service()
        
        # Get statistics from all services
        pages_stats = dashboard_service.pages_service.get_pages_statistics()
        endpoints_stats = dashboard_service.endpoints_service.get_api_version_statistics()
        relationships_stats = dashboard_service.relationships_service.get_statistics()
        postman_stats = dashboard_service.postman_service.get_statistics()
        
        return success_response(
            data={
                'pages': pages_stats,
                'endpoints': endpoints_stats,
                'relationships': relationships_stats,
                'postman': postman_stats,
            },
            message="Statistics retrieved successfully"
        ).to_json_response()
    
    except Exception as e:
        logger.error(f"Error in get_statistics_api: {e}", exc_info=True)
        return error_response(
            message=f"Failed to retrieve statistics: {str(e)}",
            status_code=500
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
            data=health_status,
            message="Health status retrieved successfully"
        ).to_json_response()
    
    except Exception as e:
        logger.error(f"Error in get_health_api: {e}", exc_info=True)
        return error_response(
            message=f"Failed to retrieve health status: {str(e)}",
            status_code=500
        ).to_json_response()
@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def pages_bulk_import_api(request: HttpRequest) -> JsonResponse:
    """
    Bulk import pages from JSON payload (used by Excel upload flow).

    Body:
        {
          "pages": [
            {
              "page_id": "...",
              "page_type": "...",
              "route": "...",
              "title": "...",
              "status": "...",
              "content": "...",
              "metadata": { ... }
            },
            ...
          ]
        }
    """
    try:
        from apps.documentation.utils.request_validation import parse_json_body as _parse_json_body  # type: ignore
    except Exception:
        import json

        def _parse_json_body(req: HttpRequest):
            try:
                body = json.loads(req.body or b"{}")
                return body, None
            except Exception as e:  # pragma: no cover - defensive fallback
                return None, str(e)

    data, err = _parse_json_body(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()

    pages = (data or {}).get("pages") or []
    if not isinstance(pages, list) or not pages:
        return error_response("Field 'pages' must be a non-empty list.", status_code=400).to_json_response()
    if len(pages) > 500:
        return error_response("Maximum 500 pages per import.", status_code=400).to_json_response()

    try:
        from apps.documentation.services import get_pages_service
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:  # pragma: no cover - import defensive
        logger.error("Failed to import helpers for pages_bulk_import_api: %s", e, exc_info=True)
        return error_response("Internal error preparing import.", status_code=500).to_json_response()

    service = get_pages_service()
    created = 0
    updated = 0
    errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(pages, start=1):
        row = raw_row or {}
        page_id = str(row.get("page_id") or "").strip()
        if not page_id:
            errors.append({"row": index, "error": "page_id is required"})
            continue
        try:
            # Normalize to Django format (includes top-level title from metadata.purpose)
            page_data = DataTransformer.lambda_to_django_page(row) if "_id" in row else row
            # Ensure title exists for create_page/update_page validation
            if not (page_data.get("title") or str(page_data.get("title", "")).strip()):
                metadata = page_data.get("metadata") or {}
                purpose = metadata.get("purpose", "")
                if purpose:
                    page_data["title"] = purpose
                else:
                    page_data["title"] = str(page_id).replace("_", " ").title()

            try:
                existing = service.get_page(page_id)
            except Exception:
                existing = None

            if existing:
                try:
                    service.update_page(page_id, page_data)
                    updated += 1
                except (ValueError, Exception) as upd_exc:
                    if "Page not found" in str(upd_exc):
                        service.create_page(page_data)
                        created += 1
                    else:
                        raise upd_exc
            else:
                service.create_page(page_data)
                created += 1
        except Exception as exc:
            logger.warning("pages_bulk_import_api row %s failed: %s", index, exc)
            errors.append(
                {
                    "row": index,
                    "page_id": page_id,
                    "error": str(exc),
                }
            )

    return success_response(
        data={
            "created": created,
            "updated": updated,
            "failed": len(errors),
            "errors": errors[:50],
        },
        message="Pages bulk import completed",
    ).to_json_response()
