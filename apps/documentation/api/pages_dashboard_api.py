"""Pages dashboard API: list and bulk import/upload endpoints."""
from __future__ import annotations

import logging
from typing import Any, Dict

from apps.core.decorators.auth import require_super_admin, require_admin_or_super_admin
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.documentation.services import get_pages_service
from apps.documentation.utils.api_responses import success_response, error_response, paginated_response
from apps.documentation.utils.list_projectors import should_expand_full, to_page_list_item

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

        page_type = request.GET.get('page_type')
        page_types_param = request.GET.get('page_types', '').strip()
        page_types = None
        if page_types_param:
            from apps.documentation.constants import PAGE_TYPES
            raw = [p.strip().lower() for p in page_types_param.split(',') if p.strip()]
            page_types = [p for p in raw if p in PAGE_TYPES]
            if page_types:
                page_type = None
        status = request.GET.get('status')
        state = request.GET.get('state')
        include_drafts = request.GET.get('include_drafts', 'true').lower() == 'true'
        include_deleted = request.GET.get('include_deleted', 'false').lower() == 'true'

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


def _parse_json_body_pages(req):
    try:
        from apps.documentation.utils.view_helpers import parse_json_body
        return parse_json_body(req)
    except Exception:
        import json
        try:
            body = json.loads(req.body or b"{}")
            return body, None
        except Exception as e:
            return None, str(e)


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
    data, err = _parse_json_body_pages(request)
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
    data, err = _parse_json_body_pages(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()
    pages = (data or {}).get("pages") or []
    if not isinstance(pages, list) or not pages:
        return error_response("Field 'pages' must be a non-empty list.", status_code=400).to_json_response()
    if len(pages) > 500:
        return error_response("Maximum 500 pages per import.", status_code=400).to_json_response()

    try:
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

    Body: { "pages": [ { "page_id": "...", "page_type": "...", "route": "...", "title": "...", ... }, ... ] }
    """
    data, err = _parse_json_body_pages(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()

    pages = (data or {}).get("pages") or []
    if not isinstance(pages, list) or not pages:
        return error_response("Field 'pages' must be a non-empty list.", status_code=400).to_json_response()
    if len(pages) > 500:
        return error_response("Maximum 500 pages per import.", status_code=400).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
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
            page_data = DataTransformer.lambda_to_django_page(row) if "_id" in row else row
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
            errors.append({"row": index, "page_id": page_id, "error": str(exc)})

    return success_response(
        data={"created": created, "updated": updated, "failed": len(errors), "errors": errors[:50]},
        message="Pages bulk import completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def pages_bulk_upload_to_s3_api(request: HttpRequest) -> JsonResponse:
    """
    Upload page JSON objects to S3 after bulk import.
    Body: { "pages": [ { "page_id": "...", ... }, ... ] }
    """
    data, err = _parse_json_body_pages(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()

    pages = (data or {}).get("pages") or []
    if not isinstance(pages, list) or not pages:
        return error_response("Field 'pages' must be a non-empty list.", status_code=400).to_json_response()
    if len(pages) > 500:
        return error_response("Maximum 500 pages per upload.", status_code=400).to_json_response()

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

    return success_response(
        data={"uploaded": uploaded, "failed": len(errors), "errors": errors[:50]},
        message="Pages upload to S3 completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def pages_import_one_api(request: HttpRequest) -> JsonResponse:
    """
    Import a single page (create or update). Body: { "page": { "page_id": "...", "title": "...", ... } }
    """
    data, err = _parse_json_body_pages(request)
    if err:
        return error_response(f"Invalid JSON body: {err}", status_code=400).to_json_response()

    row = (data or {}).get("page")
    if not row or not isinstance(row, dict):
        return error_response("Field 'page' must be a non-empty object.", status_code=400).to_json_response()

    page_id = str(row.get("page_id") or "").strip()
    if not page_id:
        return error_response("page_id is required.", status_code=400).to_json_response()

    try:
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
    Upload a single page JSON to S3. Body: { "page": { "page_id": "...", ... } }
    """
    data, err = _parse_json_body_pages(request)
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
        return success_response(
            data={"uploaded": True, "page_id": page_id, "s3_key": s3_key},
            message="Page uploaded to S3",
        ).to_json_response()
    except Exception as exc:
        logger.warning("pages_upload_one_to_s3_api page %s failed: %s", page_id, exc)
        return error_response(message=str(exc), status_code=500).to_json_response()
