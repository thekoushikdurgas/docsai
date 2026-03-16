
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
    - page_type: Filter by single page type
    - page_types: Comma-separated page types (e.g. docs,marketing); takes precedence over page_type
    - status: Filter by status
    - state: Filter by page state
    - include_drafts: Include draft pages (default: true)
    - include_deleted: Include deleted pages (default: false)
    - limit: Items per page (default: 20)          # legacy
    - offset: Offset for pagination (default: 0)   # legacy
    - page: Page number (1-based, preferred)
    - page_size: Items per page (preferred)
    - search: Search query (client-side filtering)
    - sort: Sort field
    - order: Sort order (asc|desc)
    """
    try:
        pages_service = get_pages_service()

        # Extract query parameters
        page_type = request.GET.get('page_type')
        page_types_param = request.GET.get('page_types', '').strip()
        page_types = None
        if page_types_param:
            from apps.documentation.constants import PAGE_TYPES
            raw = [p.strip().lower() for p in page_types_param.split(',') if p.strip()]
            page_types = [p for p in raw if p in PAGE_TYPES]
            if page_types:
                page_type = None  # page_types takes precedence
        status = request.GET.get('status')
        state = request.GET.get('state')
        include_drafts = request.GET.get('include_drafts', 'true').lower() == 'true'
        include_deleted = request.GET.get('include_deleted', 'false').lower() == 'true'

        # Support both limit/offset and page/page_size styles for pagination.
        page_param = request.GET.get('page')
        page_size_param = request.GET.get('page_size')
        limit_param = request.GET.get('limit')
        offset_param = request.GET.get('offset')

        try:
            if page_param is not None or page_size_param is not None:
                # Page-based pagination (used by dashboard UI + exports)
                page = max(int(page_param or 1), 1)
                page_size = min(int(page_size_param or 20), 100)
                limit = page_size
                offset = (page - 1) * page_size
            else:
                # Legacy limit/offset-based pagination (API tests, other callers)
                limit = min(int(limit_param or 20), 100)
                offset = int(offset_param or 0)
                page_size = limit
                page = (offset // max(limit, 1)) + 1
        except (TypeError, ValueError):
            page = 1
            page_size = 20
            limit = 20
            offset = 0
        
        # Get pages from service
        result = pages_service.list_pages(
            page_type=page_type,
            page_types=page_types,
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
        
        # Standard paginated response expected by dashboard JS:
        # { success, data: [...], meta: { pagination: { total, page, page_size, total_pages } } }
        return paginated_response(
            data=pages,
            total=total,
            page=page,
            page_size=page_size,
            message="Pages retrieved successfully",
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
    - limit: Items per page (default: 20)          # legacy
    - offset: Offset for pagination (default: 0)   # legacy
    - page: Page number (1-based, preferred)
    - page_size: Items per page (preferred)
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

        # Support both limit/offset and page/page_size styles for pagination.
        page_param = request.GET.get('page')
        page_size_param = request.GET.get('page_size')
        limit_param = request.GET.get('limit')
        offset_param = request.GET.get('offset')

        try:
            if page_param is not None or page_size_param is not None:
                page = max(int(page_param or 1), 1)
                page_size = min(int(page_size_param or 20), 100)
                limit = page_size
                offset = (page - 1) * page_size
            else:
                limit = min(int(limit_param or 20), 100)
                offset = int(offset_param or 0)
                page_size = limit
                page = (offset // max(limit, 1)) + 1
        except (TypeError, ValueError):
            page = 1
            page_size = 20
            limit = 20
            offset = 0
        
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
        
        return paginated_response(
            data=endpoints,
            total=total,
            page=page,
            page_size=page_size,
            message="Endpoints retrieved successfully",
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
    - limit: Items per page (default: 20)          # legacy
    - offset: Offset for pagination (default: 0)   # legacy
    - page: Page number (1-based, preferred)
    - page_size: Items per page (preferred)
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

        # Support both limit/offset and page/page_size styles for pagination.
        page_param = request.GET.get('page')
        page_size_param = request.GET.get('page_size')
        limit_param = request.GET.get('limit')
        offset_param = request.GET.get('offset')

        try:
            if page_param is not None or page_size_param is not None:
                page = max(int(page_param or 1), 1)
                page_size = min(int(page_size_param or 20), 100)
                limit = page_size
                offset = (page - 1) * page_size
            else:
                limit = min(int(limit_param or 20), 100)
                offset = int(offset_param or 0)
                page_size = limit
                page = (offset // max(limit, 1)) + 1
        except (TypeError, ValueError):
            page = 1
            page_size = 20
            limit = 20
            offset = 0
        
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
        
        return paginated_response(
            data=relationships,
            total=total,
            page=page,
            page_size=page_size,
            message="Relationships retrieved successfully",
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
    - limit: Items per page (default: 20)          # legacy
    - offset: Offset for pagination (default: 0)   # legacy
    - page: Page number (1-based, preferred)
    - page_size: Items per page (preferred)
    - search: Search query
    - sort: Sort field
    - order: Sort order (asc|desc)
    """
    try:
        postman_service = get_postman_service()
        
        # Extract query parameters
        state = request.GET.get('state')

        # Support both limit/offset and page/page_size styles for pagination.
        page_param = request.GET.get('page')
        page_size_param = request.GET.get('page_size')
        limit_param = request.GET.get('limit')
        offset_param = request.GET.get('offset')

        try:
            if page_param is not None or page_size_param is not None:
                page = max(int(page_param or 1), 1)
                page_size = min(int(page_size_param or 20), 100)
                limit = page_size
                offset = (page - 1) * page_size
            else:
                limit = min(int(limit_param or 20), 100)
                offset = int(offset_param or 0)
                page_size = limit
                page = (offset // max(limit, 1)) + 1
        except (TypeError, ValueError):
            page = 1
            page_size = 20
            limit = 20
            offset = 0
        
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
        
        return paginated_response(
            data=configurations,
            total=total,
            page=page,
            page_size=page_size,
            message="Postman configurations retrieved successfully",
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
def pages_bulk_import_check_api(request: HttpRequest) -> JsonResponse:
    """
    Check which page_ids already exist in the backend (repository).
    Used by Preview & map to show Create vs Update per page.

    Body: { "page_ids": ["about_page", "activities_page", ...] }
    Returns: { "existing": ["about_page", ...], "to_create": ["new_page", ...] }
    """
    try:
        from apps.documentation.utils.request_validation import parse_json_body as _parse_json_body  # type: ignore
    except Exception:
        import json

        def _parse_json_body(req: HttpRequest):
            try:
                body = json.loads(req.body or b"{}")
                return body, None
            except Exception as e:
                return None, str(e)

    data, err = _parse_json_body(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    page_ids = (data or {}).get("page_ids") or []
    if not isinstance(page_ids, list):
        return error_response("page_ids must be a list.", status_code=400).to_json_response()
    page_ids = [str(pid).strip() for pid in page_ids if str(pid).strip()][:500]
    try:
        service = get_pages_service()
        existing = []
        for pid in page_ids:
            try:
                if service.get_page(pid):
                    existing.append(pid)
            except Exception:
                pass
        to_create = [pid for pid in page_ids if pid not in existing]
        return success_response(
            data={"existing": existing, "to_create": to_create},
            message="Check completed",
        ).to_json_response()
    except Exception as e:
        logger.warning("pages_bulk_import_check_api failed: %s", e, exc_info=True)
        return error_response(message=str(e), status_code=500).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def pages_bulk_import_preview_api(request: HttpRequest) -> JsonResponse:
    """
    Preview bulk import: same normalization and validation as bulk-import, no write.
    Returns create/update/failed counts and per-page action for the Preview & map step.

    Body: same as pages_bulk_import_api { "pages": [ ... ] }
    Returns: { "existing": [...], "to_create": [...], "validation_errors": [{ "page_id", "error" }, ...] }
    """
    try:
        from apps.documentation.utils.request_validation import parse_json_body as _parse_json_body  # type: ignore
    except Exception:
        import json

        def _parse_json_body(req: HttpRequest):
            try:
                body = json.loads(req.body or b"{}")
                return body, None
            except Exception as e:
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
    except Exception as e:
        logger.error("pages_bulk_import_preview_api import failed: %s", e, exc_info=True)
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_pages_service()
    existing: list[str] = []
    to_create: list[str] = []
    validation_errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(pages, start=1):
        row = raw_row or {}
        page_id = str(row.get("page_id") or "").strip()
        if not page_id:
            validation_errors.append({"row": index, "page_id": "", "error": "page_id is required"})
            continue
        try:
            page_data = DataTransformer.lambda_to_django_page(row) if "_id" in row else row
            if not (page_data.get("title") or str(page_data.get("title", "")).strip()):
                metadata = page_data.get("metadata") or {}
                purpose = metadata.get("purpose", "")
                if purpose:
                    page_data["title"] = purpose
                else:
                    page_data["title"] = str(page_id).replace("_", " ").title()
            title = str(page_data.get("title") or "").strip()
            if not title:
                validation_errors.append({"row": index, "page_id": page_id, "error": "Missing required field: title"})
                continue
            try:
                exists = service.get_page(page_id)
            except Exception:
                exists = None
            if exists:
                existing.append(page_id)
            else:
                to_create.append(page_id)
        except Exception as exc:
            validation_errors.append({"row": index, "page_id": page_id, "error": str(exc)})

    return success_response(
        data={
            "existing": existing,
            "to_create": to_create,
            "validation_errors": validation_errors[:100],
            "to_create_count": len(to_create),
            "to_update_count": len(existing),
            "failed_count": len(validation_errors),
        },
        message="Preview completed",
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

            # Use unified storage (local + S3) for existence so preview and sync match; write goes to S3 via repository
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


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def pages_bulk_upload_to_s3_api(request: HttpRequest) -> JsonResponse:
    """
    Upload page JSON objects to S3 after bulk import.
    Used by Upload Pages from JSON flow: after sync result, upload the same pages to S3.

    Body: { "pages": [ { "page_id": "...", ... }, ... ] }
    Writes each page to S3 at data/pages/{page_id}.json (or S3_DATA_PREFIX + pages/ + {page_id}.json).
    Returns: { "uploaded": N, "failed": M, "errors": [ { "page_id", "error" }, ... ] }
    """
    try:
        from apps.documentation.utils.request_validation import parse_json_body as _parse_json_body  # type: ignore
    except Exception:
        import json as _json

        def _parse_json_body(req: HttpRequest):
            try:
                body = _json.loads(req.body or b"{}")
                return body, None
            except Exception as e:
                return None, str(e)

    data, err = _parse_json_body(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()

    pages = (data or {}).get("pages") or []
    if not isinstance(pages, list) or not pages:
        return error_response("Field 'pages' must be a non-empty list.", status_code=400).to_json_response()
    if len(pages) > 500:
        return error_response("Maximum 500 pages per upload.", status_code=400).to_json_response()

    # region agent log
    try:
        import json as _agent_json, time as _agent_time

        with open("debug-7e1f90.log", "a", encoding="utf-8") as _agent_f:
            _agent_f.write(
                _agent_json.dumps(
                    {
                        "sessionId": "7e1f90",
                        "runId": "initial",
                        "hypothesisId": "H3",
                        "location": "documentation_dashboard_api.pages_bulk_upload_to_s3_api",
                        "message": "Starting bulk upload to S3",
                        "data": {"pagesCount": len(pages)},
                        "timestamp": int(_agent_time.time() * 1000),
                    }
                )
                + "\n"
            )
    except Exception:
        pass
    # endregion

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    storage = S3JSONStorage()
    uploaded = 0
    errors: list[Dict[str, Any]] = []

    for row in pages:
        row = row or {}
        page_id = str(row.get("page_id") or "").strip()
        if not page_id:
            errors.append({"page_id": "", "error": "page_id is required"})
            continue
        try:
            s3_key = f"{prefix}/pages/{page_id}.json"
            storage.write_json(s3_key, row)
            uploaded += 1
        except Exception as exc:
            logger.warning("pages_bulk_upload_to_s3_api page %s failed: %s", page_id, exc)
            errors.append({"page_id": page_id, "error": str(exc)})

            # region agent log
            try:
                import json as _agent_json, time as _agent_time

                with open("debug-7e1f90.log", "a", encoding="utf-8") as _agent_f:
                    _agent_f.write(
                        _agent_json.dumps(
                            {
                                "sessionId": "7e1f90",
                                "runId": "initial",
                                "hypothesisId": "H4",
                                "location": "documentation_dashboard_api.pages_bulk_upload_to_s3_api",
                                "message": "S3 bulk upload failed for page",
                                "data": {"page_id": page_id, "error": str(exc)},
                                "timestamp": int(_agent_time.time() * 1000),
                            }
                        )
                        + "\n"
                    )
            except Exception:
                pass
            # endregion

    return success_response(
        data={
            "uploaded": uploaded,
            "failed": len(errors),
            "errors": errors[:50],
        },
        message="Pages upload to S3 completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def pages_import_one_api(request: HttpRequest) -> JsonResponse:
    """
    Import a single page (create or update). Used by Upload JSON flow with single-API pattern.
    Body: { "page": { "page_id": "...", "title": "...", ... } }
    Returns: { "created": true } or { "updated": true }, or error.
    """
    try:
        from apps.documentation.utils.request_validation import parse_json_body as _parse_json_body  # type: ignore
    except Exception:
        import json as _json

        def _parse_json_body(req: HttpRequest):
            try:
                body = _json.loads(req.body or b"{}")
                return body, None
            except Exception as e:
                return None, str(e)

    data, err = _parse_json_body(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()

    row = (data or {}).get("page")
    if not row or not isinstance(row, dict):
        return error_response("Field 'page' must be a non-empty object.", status_code=400).to_json_response()

    page_id = str(row.get("page_id") or "").strip()
    if not page_id:
        return error_response("page_id is required.", status_code=400).to_json_response()

    try:
        from apps.documentation.services import get_pages_service
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("Failed to import helpers for pages_import_one_api: %s", e, exc_info=True)
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_pages_service()
    page_data = DataTransformer.lambda_to_django_page(row) if "_id" in row else dict(row)
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

    try:
        if existing:
            try:
                service.update_page(page_id, page_data)
                return success_response(data={"updated": True, "page_id": page_id}, message="Page updated").to_json_response()
            except (ValueError, Exception) as upd_exc:
                if "Page not found" in str(upd_exc):
                    # get_page can return from S3 while update_page requires page in local/store; fallback to create (same as bulk-import)
                    service.create_page(page_data)
                    return success_response(data={"created": True, "page_id": page_id}, message="Page created").to_json_response()
                raise upd_exc
        service.create_page(page_data)
        return success_response(data={"created": True, "page_id": page_id}, message="Page created").to_json_response()
    except Exception as exc:
        logger.warning("pages_import_one_api page %s failed: %s", page_id, exc)
        return error_response(message=str(exc), status_code=400).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def pages_upload_one_to_s3_api(request: HttpRequest) -> JsonResponse:
    """
    Upload a single page JSON to S3. Used by Upload JSON flow with single-API pattern.
    Body: { "page": { "page_id": "...", ... } }
    Returns: { "uploaded": true, "page_id": "...", "s3_key": "..." } or error.
    """
    try:
        from apps.documentation.utils.request_validation import parse_json_body as _parse_json_body  # type: ignore
    except Exception:
        import json as _json

        def _parse_json_body(req: HttpRequest):
            try:
                body = _json.loads(req.body or b"{}")
                return body, None
            except Exception as e:
                return None, str(e)

    data, err = _parse_json_body(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()

    row = (data or {}).get("page")
    if not row or not isinstance(row, dict):
        return error_response("Field 'page' must be a non-empty object.", status_code=400).to_json_response()

    page_id = str(row.get("page_id") or "").strip()
    if not page_id:
        return error_response("page_id is required.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    s3_key = f"{prefix}/pages/{page_id}.json"
    try:
        storage = S3JSONStorage()
        storage.write_json(s3_key, row)

        # region agent log
        try:
            import json as _agent_json, time as _agent_time

            with open("debug-7e1f90.log", "a", encoding="utf-8") as _agent_f:
                _agent_f.write(
                    _agent_json.dumps(
                        {
                            "sessionId": "7e1f90",
                            "runId": "initial",
                            "hypothesisId": "H5",
                            "location": "documentation_dashboard_api.pages_upload_one_to_s3_api",
                            "message": "Single page uploaded to S3",
                            "data": {"page_id": page_id, "s3_key": s3_key},
                            "timestamp": int(_agent_time.time() * 1000),
                        }
                    )
                    + "\n"
                )
        except Exception:
            pass
        # endregion

        return success_response(
            data={"uploaded": True, "page_id": page_id, "s3_key": s3_key},
            message="Page uploaded to S3",
        ).to_json_response()
    except Exception as exc:
        logger.warning("pages_upload_one_to_s3_api page %s failed: %s", page_id, exc)
        # region agent log
        try:
            import json as _agent_json, time as _agent_time

            with open("debug-7e1f90.log", "a", encoding="utf-8") as _agent_f:
                _agent_f.write(
                    _agent_json.dumps(
                        {
                            "sessionId": "7e1f90",
                            "runId": "initial",
                            "hypothesisId": "H5",
                            "location": "documentation_dashboard_api.pages_upload_one_to_s3_api",
                            "message": "Single page upload to S3 failed",
                            "data": {"page_id": page_id, "error": str(exc)},
                            "timestamp": int(_agent_time.time() * 1000),
                        }
                    )
                    + "\n"
                )
        except Exception:
            pass
        # endregion
        return error_response(message=str(exc), status_code=500).to_json_response()


# ---------------------------------------------------------------------------
# Endpoints bulk import / S3 upload (mirrors pages APIs)
# ---------------------------------------------------------------------------


def _parse_json_body_endpoints(req):
    try:
        import json as _json
        body = _json.loads(req.body or b"{}")
        return body, None
    except Exception as e:
        return None, str(e)


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def endpoints_bulk_import_preview_api(request: HttpRequest) -> JsonResponse:
    """Preview bulk import for endpoints. Body: { "endpoints": [ ... ] }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    endpoints = (data or {}).get("endpoints") or []
    if not isinstance(endpoints, list) or not endpoints:
        return error_response("Field 'endpoints' must be a non-empty list.", status_code=400).to_json_response()
    if len(endpoints) > 500:
        return error_response("Maximum 500 endpoints per import.", status_code=400).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("endpoints_bulk_import_preview_api import failed: %s", e, exc_info=True)
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_endpoints_service()
    existing: list[str] = []
    to_create: list[str] = []
    validation_errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(endpoints, start=1):
        row = raw_row or {}
        endpoint_id = str(row.get("endpoint_id") or row.get("endpointId") or "").strip()
        if not endpoint_id:
            validation_errors.append({"row": index, "endpoint_id": "", "error": "endpoint_id is required"})
            continue
        path_val = str(row.get("endpoint_path") or row.get("path") or row.get("endpointPath") or "").strip()
        method_val = str(row.get("method") or "").strip().upper() or "GET"
        if not path_val:
            validation_errors.append({"row": index, "endpoint_id": endpoint_id, "error": "endpoint_path or path is required"})
            continue
        try:
            page_data = DataTransformer.lambda_to_django_endpoint(row) if "_id" in row else row
            try:
                exists = service.get_endpoint(endpoint_id)
            except Exception:
                exists = None
            if exists:
                existing.append(endpoint_id)
            else:
                to_create.append(endpoint_id)
        except Exception as exc:
            validation_errors.append({"row": index, "endpoint_id": endpoint_id, "error": str(exc)})

    return success_response(
        data={
            "existing": existing,
            "to_create": to_create,
            "validation_errors": validation_errors[:100],
            "to_create_count": len(to_create),
            "to_update_count": len(existing),
            "failed_count": len(validation_errors),
        },
        message="Preview completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def endpoints_bulk_import_api(request: HttpRequest) -> JsonResponse:
    """Bulk import endpoints. Body: { "endpoints": [ ... ] }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    endpoints = (data or {}).get("endpoints") or []
    if not isinstance(endpoints, list) or not endpoints:
        return error_response("Field 'endpoints' must be a non-empty list.", status_code=400).to_json_response()
    if len(endpoints) > 500:
        return error_response("Maximum 500 endpoints per import.", status_code=400).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("endpoints_bulk_import_api import failed: %s", e, exc_info=True)
        return error_response("Internal error preparing import.", status_code=500).to_json_response()

    service = get_endpoints_service()
    created = 0
    updated = 0
    errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(endpoints, start=1):
        row = raw_row or {}
        endpoint_id = str(row.get("endpoint_id") or row.get("endpointId") or "").strip()
        if not endpoint_id:
            errors.append({"row": index, "error": "endpoint_id is required"})
            continue
        try:
            page_data = DataTransformer.lambda_to_django_endpoint(row) if "_id" in row else dict(row)
            if not page_data.get("endpoint_path") and page_data.get("path"):
                page_data["endpoint_path"] = page_data["path"]
            if not page_data.get("endpoint_path"):
                page_data["endpoint_path"] = row.get("path") or "/"
            if not page_data.get("method"):
                page_data["method"] = row.get("method") or "GET"
            # Service requires 'path' (not just endpoint_path)
            if "path" not in page_data or not page_data["path"]:
                page_data["path"] = page_data.get("endpoint_path") or "/"
            try:
                existing = service.get_endpoint(endpoint_id)
            except Exception:
                existing = None
            if existing:
                try:
                    service.update_endpoint(endpoint_id, page_data)
                    updated += 1
                except (ValueError, Exception) as upd_exc:
                    if "not found" in str(upd_exc).lower():
                        service.create_endpoint(page_data)
                        created += 1
                    else:
                        raise upd_exc
            else:
                service.create_endpoint(page_data)
                created += 1
        except Exception as exc:
            logger.warning("endpoints_bulk_import_api row %s failed: %s", index, exc)
            errors.append({"row": index, "endpoint_id": endpoint_id, "error": str(exc)})

    return success_response(
        data={"created": created, "updated": updated, "failed": len(errors), "errors": errors[:50]},
        message="Endpoints bulk import completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def endpoints_bulk_upload_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload endpoint JSON objects to S3. Body: { "endpoints": [ ... ] }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    endpoints = (data or {}).get("endpoints") or []
    if not isinstance(endpoints, list) or not endpoints:
        return error_response("Field 'endpoints' must be a non-empty list.", status_code=400).to_json_response()
    if len(endpoints) > 500:
        return error_response("Maximum 500 endpoints per upload.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    storage = S3JSONStorage()
    uploaded = 0
    errors: list[Dict[str, Any]] = []

    for row in endpoints:
        row = row or {}
        endpoint_id = str(row.get("endpoint_id") or "").strip()
        if not endpoint_id:
            errors.append({"endpoint_id": "", "error": "endpoint_id is required"})
            continue
        try:
            s3_key = f"{prefix}/endpoints/{endpoint_id}.json"
            storage.write_json(s3_key, row)
            uploaded += 1
        except Exception as exc:
            logger.warning("endpoints_bulk_upload_to_s3_api endpoint %s failed: %s", endpoint_id, exc)
            errors.append({"endpoint_id": endpoint_id, "error": str(exc)})

    return success_response(
        data={"uploaded": uploaded, "failed": len(errors), "errors": errors[:50]},
        message="Endpoints upload to S3 completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def endpoints_import_one_api(request: HttpRequest) -> JsonResponse:
    """Import a single endpoint. Body: { "endpoint": { ... } }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    row = (data or {}).get("endpoint")
    if not row or not isinstance(row, dict):
        return error_response("Field 'endpoint' must be a non-empty object.", status_code=400).to_json_response()
    endpoint_id = str(row.get("endpoint_id") or "").strip()
    if not endpoint_id:
        return error_response("endpoint_id is required.", status_code=400).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("endpoints_import_one_api import failed: %s", e, exc_info=True)
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_endpoints_service()
    page_data = DataTransformer.lambda_to_django_endpoint(row) if "_id" in row else dict(row)
    if not page_data.get("endpoint_path"):
        page_data["endpoint_path"] = row.get("path") or "/"
    if not page_data.get("method"):
        page_data["method"] = row.get("method") or "GET"
    # Service requires 'path' (not just endpoint_path)
    if "path" not in page_data or not page_data["path"]:
        page_data["path"] = page_data.get("endpoint_path") or "/"
    try:
        existing = service.get_endpoint(endpoint_id)
    except Exception:
        existing = None
    try:
        if existing:
            service.update_endpoint(endpoint_id, page_data)
            return success_response(data={"updated": True, "endpoint_id": endpoint_id}, message="Endpoint updated").to_json_response()
        service.create_endpoint(page_data)
        return success_response(data={"created": True, "endpoint_id": endpoint_id}, message="Endpoint created").to_json_response()
    except Exception as exc:
        logger.warning("endpoints_import_one_api endpoint %s failed: %s", endpoint_id, exc)
        return error_response(message=str(exc), status_code=400).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def endpoints_upload_one_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload a single endpoint JSON to S3. Body: { "endpoint": { ... } }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    row = (data or {}).get("endpoint")
    if not row or not isinstance(row, dict):
        return error_response("Field 'endpoint' must be a non-empty object.", status_code=400).to_json_response()
    endpoint_id = str(row.get("endpoint_id") or "").strip()
    if not endpoint_id:
        return error_response("endpoint_id is required.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    s3_key = f"{prefix}/endpoints/{endpoint_id}.json"
    try:
        storage = S3JSONStorage()
        storage.write_json(s3_key, row)
        return success_response(
            data={"uploaded": True, "endpoint_id": endpoint_id, "s3_key": s3_key},
            message="Endpoint uploaded to S3",
        ).to_json_response()
    except Exception as exc:
        logger.warning("endpoints_upload_one_to_s3_api endpoint %s failed: %s", endpoint_id, exc)
        return error_response(message=str(exc), status_code=500).to_json_response()


# ---------------------------------------------------------------------------
# Relationships bulk import / S3 upload (mirrors pages/endpoints APIs)
# ---------------------------------------------------------------------------


def _parse_json_body_relationships(req):
    try:
        import json as _json
        body = _json.loads(req.body or b"{}")
        return body, None
    except Exception as e:
        return None, str(e)


def _build_relationship_id(row: dict) -> str:
    """Build relationship_id from page_path|endpoint_path|method."""
    page_path = str(row.get("page_path") or row.get("page_id") or "").strip()
    endpoint_path = str(row.get("endpoint_path") or row.get("endpoint_id") or "").strip()
    method = str(row.get("method") or "QUERY").strip().upper() or "QUERY"
    if page_path and endpoint_path:
        return f"{page_path}|{endpoint_path}|{method}"
    return row.get("relationship_id") or ""


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def relationships_bulk_import_preview_api(request: HttpRequest) -> JsonResponse:
    """Preview bulk import for relationships. Body: { "relationships": [ ... ] }."""
    data, err = _parse_json_body_relationships(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    relationships = (data or {}).get("relationships") or []
    if not isinstance(relationships, list) or not relationships:
        return error_response("Field 'relationships' must be a non-empty list.", status_code=400).to_json_response()
    if len(relationships) > 500:
        return error_response("Maximum 500 relationships per import.", status_code=400).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("relationships_bulk_import_preview_api import failed: %s", e, exc_info=True)
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_relationships_service()
    existing: list[str] = []
    to_create: list[str] = []
    validation_errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(relationships, start=1):
        row = raw_row or {}
        rel_id = _build_relationship_id(row)
        if not rel_id:
            validation_errors.append({"row": index, "error": "page_path (or page_id), endpoint_path (or endpoint_id), and method are required"})
            continue
        page_path = str(row.get("page_path") or row.get("page_id") or "").strip()
        endpoint_path = str(row.get("endpoint_path") or row.get("endpoint_id") or "").strip()
        if not page_path or not endpoint_path:
            validation_errors.append({"row": index, "relationship_id": rel_id, "error": "page_path and endpoint_path are required"})
            continue
        try:
            try:
                exists = service.get_relationship(rel_id)
            except Exception:
                exists = None
            if exists:
                existing.append(rel_id)
            else:
                to_create.append(rel_id)
        except Exception as exc:
            validation_errors.append({"row": index, "relationship_id": rel_id, "error": str(exc)})

    return success_response(
        data={
            "existing": existing,
            "to_create": to_create,
            "validation_errors": validation_errors[:100],
            "to_create_count": len(to_create),
            "to_update_count": len(existing),
            "failed_count": len(validation_errors),
        },
        message="Preview completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def relationships_bulk_import_api(request: HttpRequest) -> JsonResponse:
    """Bulk import relationships. Body: { "relationships": [ ... ] }."""
    data, err = _parse_json_body_relationships(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    relationships = (data or {}).get("relationships") or []
    if not isinstance(relationships, list) or not relationships:
        return error_response("Field 'relationships' must be a non-empty list.", status_code=400).to_json_response()
    if len(relationships) > 500:
        return error_response("Maximum 500 relationships per import.", status_code=400).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("relationships_bulk_import_api import failed: %s", e, exc_info=True)
        return error_response("Internal error preparing import.", status_code=500).to_json_response()

    service = get_relationships_service()
    created = 0
    updated = 0
    errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(relationships, start=1):
        row = raw_row or {}
        rel_id = _build_relationship_id(row)
        if not rel_id:
            errors.append({"row": index, "error": "page_path, endpoint_path, and method are required"})
            continue
        page_path = str(row.get("page_path") or row.get("page_id") or "").strip()
        endpoint_path = str(row.get("endpoint_path") or row.get("endpoint_id") or "").strip()
        method = str(row.get("method") or "QUERY").strip().upper() or "QUERY"
        if not page_path or not endpoint_path:
            errors.append({"row": index, "error": "page_path and endpoint_path are required"})
            continue
        try:
            rel_data = DataTransformer.lambda_to_django_relationship(row) if "_id" in row else dict(row)
            rel_data["relationship_id"] = rel_id
            rel_data["page_path"] = page_path
            rel_data["endpoint_path"] = endpoint_path
            rel_data["method"] = method
            if not rel_data.get("usage_type"):
                rel_data["usage_type"] = row.get("usage_type") or "primary"
            if not rel_data.get("usage_context"):
                rel_data["usage_context"] = row.get("usage_context") or "data_fetching"
            try:
                existing = service.get_relationship(rel_id)
            except Exception:
                existing = None
            if existing:
                try:
                    service.update_relationship(rel_id, rel_data)
                    updated += 1
                except (ValueError, Exception) as upd_exc:
                    if "not found" in str(upd_exc).lower():
                        service.create_relationship(rel_data)
                        created += 1
                    else:
                        raise upd_exc
            else:
                service.create_relationship(rel_data)
                created += 1
        except Exception as exc:
            logger.warning("relationships_bulk_import_api row %s failed: %s", index, exc)
            errors.append({"row": index, "relationship_id": rel_id, "error": str(exc)})

    return success_response(
        data={"created": created, "updated": updated, "failed": len(errors), "errors": errors[:50]},
        message="Relationships bulk import completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def relationships_bulk_upload_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload relationship JSON objects to S3. Body: { "relationships": [ ... ] }."""
    data, err = _parse_json_body_relationships(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    relationships = (data or {}).get("relationships") or []
    if not isinstance(relationships, list) or not relationships:
        return error_response("Field 'relationships' must be a non-empty list.", status_code=400).to_json_response()
    if len(relationships) > 500:
        return error_response("Maximum 500 relationships per upload.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    storage = S3JSONStorage()
    uploaded = 0
    errors: list[Dict[str, Any]] = []

    for row in relationships:
        row = row or {}
        rel_id = _build_relationship_id(row)
        if not rel_id:
            errors.append({"relationship_id": "", "error": "relationship_id or page_path|endpoint_path|method required"})
            continue
        try:
            s3_key = f"{prefix}/relationships/{rel_id}.json"
            storage.write_json(s3_key, row)
            uploaded += 1
        except Exception as exc:
            logger.warning("relationships_bulk_upload_to_s3_api relationship %s failed: %s", rel_id, exc)
            errors.append({"relationship_id": rel_id, "error": str(exc)})

    return success_response(
        data={"uploaded": uploaded, "failed": len(errors), "errors": errors[:50]},
        message="Relationships upload to S3 completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def relationships_import_one_api(request: HttpRequest) -> JsonResponse:
    """Import a single relationship. Body: { "relationship": { ... } }."""
    data, err = _parse_json_body_relationships(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    row = (data or {}).get("relationship")
    if not row or not isinstance(row, dict):
        return error_response("Field 'relationship' must be a non-empty object.", status_code=400).to_json_response()
    rel_id = _build_relationship_id(row)
    if not rel_id:
        return error_response("page_path (or page_id), endpoint_path (or endpoint_id), and method are required.", status_code=400).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("relationships_import_one_api import failed: %s", e, exc_info=True)
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_relationships_service()
    page_path = str(row.get("page_path") or row.get("page_id") or "").strip()
    endpoint_path = str(row.get("endpoint_path") or row.get("endpoint_id") or "").strip()
    method = str(row.get("method") or "QUERY").strip().upper() or "QUERY"
    rel_data = DataTransformer.lambda_to_django_relationship(row) if "_id" in row else dict(row)
    rel_data["relationship_id"] = rel_id
    rel_data["page_path"] = page_path
    rel_data["endpoint_path"] = endpoint_path
    rel_data["method"] = method
    if not rel_data.get("usage_type"):
        rel_data["usage_type"] = row.get("usage_type") or "primary"
    if not rel_data.get("usage_context"):
        rel_data["usage_context"] = row.get("usage_context") or "data_fetching"
    try:
        existing = service.get_relationship(rel_id)
    except Exception:
        existing = None
    try:
        if existing:
            service.update_relationship(rel_id, rel_data)
            return success_response(data={"updated": True, "relationship_id": rel_id}, message="Relationship updated").to_json_response()
        service.create_relationship(rel_data)
        return success_response(data={"created": True, "relationship_id": rel_id}, message="Relationship created").to_json_response()
    except Exception as exc:
        logger.warning("relationships_import_one_api relationship %s failed: %s", rel_id, exc)
        return error_response(message=str(exc), status_code=400).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def relationships_upload_one_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload a single relationship JSON to S3. Body: { "relationship": { ... } }."""
    data, err = _parse_json_body_relationships(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    row = (data or {}).get("relationship")
    if not row or not isinstance(row, dict):
        return error_response("Field 'relationship' must be a non-empty object.", status_code=400).to_json_response()
    rel_id = _build_relationship_id(row)
    if not rel_id:
        return error_response("page_path (or page_id), endpoint_path (or endpoint_id), and method are required.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    s3_key = f"{prefix}/relationships/{rel_id}.json"
    try:
        storage = S3JSONStorage()
        storage.write_json(s3_key, row)
        return success_response(
            data={"uploaded": True, "relationship_id": rel_id, "s3_key": s3_key},
            message="Relationship uploaded to S3",
        ).to_json_response()
    except Exception as exc:
        logger.warning("relationships_upload_one_to_s3_api relationship %s failed: %s", rel_id, exc)
        return error_response(message=str(exc), status_code=500).to_json_response()


# ---------------------------------------------------------------------------
# Postman bulk import / S3 upload (writes to postman/configurations/{config_id}.json)
# ---------------------------------------------------------------------------


def _parse_json_body_postman(req):
    try:
        import json as _json
        body = _json.loads(req.body or b"{}")
        return body, None
    except Exception as e:
        return None, str(e)


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def postman_bulk_import_preview_api(request: HttpRequest) -> JsonResponse:
    """Preview bulk import for Postman configurations. Body: { "configs": [ ... ] }."""
    data, err = _parse_json_body_postman(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    configs = (data or {}).get("configs") or (data or {}).get("configurations") or []
    if not isinstance(configs, list) or not configs:
        return error_response("Field 'configs' or 'configurations' must be a non-empty list.", status_code=400).to_json_response()
    if len(configs) > 500:
        return error_response("Maximum 500 configurations per import.", status_code=400).to_json_response()

    service = get_postman_service()
    existing: list[str] = []
    to_create: list[str] = []
    validation_errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(configs, start=1):
        row = raw_row or {}
        config_id = str(row.get("config_id") or row.get("id") or "").strip()
        if not config_id:
            validation_errors.append({"row": index, "error": "config_id (or id) is required"})
            continue
        try:
            try:
                exists = service.get_configuration(config_id)
            except Exception:
                exists = None
            if exists:
                existing.append(config_id)
            else:
                to_create.append(config_id)
        except Exception as exc:
            validation_errors.append({"row": index, "config_id": config_id, "error": str(exc)})

    return success_response(
        data={
            "existing": existing,
            "to_create": to_create,
            "validation_errors": validation_errors[:100],
            "to_create_count": len(to_create),
            "to_update_count": len(existing),
            "failed_count": len(validation_errors),
        },
        message="Preview completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def postman_bulk_import_api(request: HttpRequest) -> JsonResponse:
    """Bulk import Postman configurations (writes to S3). Body: { "configs": [ ... ] }."""
    data, err = _parse_json_body_postman(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    configs = (data or {}).get("configs") or (data or {}).get("configurations") or []
    if not isinstance(configs, list) or not configs:
        return error_response("Field 'configs' or 'configurations' must be a non-empty list.", status_code=400).to_json_response()
    if len(configs) > 500:
        return error_response("Maximum 500 configurations per import.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    storage = S3JSONStorage()
    created = 0
    updated = 0
    errors: list[Dict[str, Any]] = []
    service = get_postman_service()

    for index, row in enumerate(configs, start=1):
        row = row or {}
        config_id = str(row.get("config_id") or row.get("id") or "").strip()
        if not config_id:
            errors.append({"row": index, "error": "config_id (or id) is required"})
            continue
        try:
            try:
                existing = service.get_configuration(config_id)
            except Exception:
                existing = None
            s3_key = f"{prefix}/postman/configurations/{config_id}.json"
            if "_id" not in row:
                row["_id"] = config_id
            if "config_id" not in row:
                row["config_id"] = config_id
            storage.write_json(s3_key, row)
            if existing:
                updated += 1
            else:
                created += 1
            try:
                service.unified_storage.clear_cache("postman", config_id)
            except Exception:
                pass
        except Exception as exc:
            logger.warning("postman_bulk_import_api config %s failed: %s", config_id, exc)
            errors.append({"row": index, "config_id": config_id, "error": str(exc)})

    try:
        service.unified_storage.clear_cache("postman")
    except Exception:
        pass

    return success_response(
        data={"created": created, "updated": updated, "failed": len(errors), "errors": errors[:50]},
        message="Postman configurations bulk import completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def postman_bulk_upload_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload Postman configuration JSON objects to S3. Body: { "configs": [ ... ] }."""
    data, err = _parse_json_body_postman(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    configs = (data or {}).get("configs") or (data or {}).get("configurations") or []
    if not isinstance(configs, list) or not configs:
        return error_response("Field 'configs' or 'configurations' must be a non-empty list.", status_code=400).to_json_response()
    if len(configs) > 500:
        return error_response("Maximum 500 configurations per upload.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    storage = S3JSONStorage()
    uploaded = 0
    errors: list[Dict[str, Any]] = []

    for row in configs:
        row = row or {}
        config_id = str(row.get("config_id") or row.get("id") or "").strip()
        if not config_id:
            errors.append({"config_id": "", "error": "config_id (or id) is required"})
            continue
        try:
            s3_key = f"{prefix}/postman/configurations/{config_id}.json"
            storage.write_json(s3_key, row)
            uploaded += 1
        except Exception as exc:
            logger.warning("postman_bulk_upload_to_s3_api config %s failed: %s", config_id, exc)
            errors.append({"config_id": config_id, "error": str(exc)})

    return success_response(
        data={"uploaded": uploaded, "failed": len(errors), "errors": errors[:50]},
        message="Postman configurations upload to S3 completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def postman_import_one_api(request: HttpRequest) -> JsonResponse:
    """Import a single Postman configuration. Body: { "config": { ... } }."""
    data, err = _parse_json_body_postman(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    row = (data or {}).get("config")
    if not row or not isinstance(row, dict):
        return error_response("Field 'config' must be a non-empty object.", status_code=400).to_json_response()
    config_id = str(row.get("config_id") or row.get("id") or "").strip()
    if not config_id:
        return error_response("config_id (or id) is required.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    s3_key = f"{prefix}/postman/configurations/{config_id}.json"
    try:
        if "_id" not in row:
            row["_id"] = config_id
        if "config_id" not in row:
            row["config_id"] = config_id
        storage = S3JSONStorage()
        storage.write_json(s3_key, row)
        try:
            get_postman_service().unified_storage.clear_cache("postman", config_id)
            get_postman_service().unified_storage.clear_cache("postman")
        except Exception:
            pass
        return success_response(
            data={"uploaded": True, "config_id": config_id, "s3_key": s3_key},
            message="Postman configuration imported",
        ).to_json_response()
    except Exception as exc:
        logger.warning("postman_import_one_api config %s failed: %s", config_id, exc)
        return error_response(message=str(exc), status_code=500).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def postman_upload_one_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload a single Postman configuration JSON to S3. Body: { "config": { ... } }."""
    data, err = _parse_json_body_postman(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    row = (data or {}).get("config")
    if not row or not isinstance(row, dict):
        return error_response("Field 'config' must be a non-empty object.", status_code=400).to_json_response()
    config_id = str(row.get("config_id") or row.get("id") or "").strip()
    if not config_id:
        return error_response("config_id (or id) is required.", status_code=400).to_json_response()

    from django.conf import settings
    from apps.documentation.repositories.s3_json_storage import S3JSONStorage

    prefix = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/")
    s3_key = f"{prefix}/postman/configurations/{config_id}.json"
    try:
        storage = S3JSONStorage()
        storage.write_json(s3_key, row)
        return success_response(
            data={"uploaded": True, "config_id": config_id, "s3_key": s3_key},
            message="Postman configuration uploaded to S3",
        ).to_json_response()
    except Exception as exc:
        logger.warning("postman_upload_one_to_s3_api config %s failed: %s", config_id, exc)
        return error_response(message=str(exc), status_code=500).to_json_response()
