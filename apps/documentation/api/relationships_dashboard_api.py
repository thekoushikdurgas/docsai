"""Relationships dashboard API: list and bulk import/upload endpoints."""

from __future__ import annotations

import logging
from typing import Any, Dict

from apps.core.decorators.auth import require_super_admin, require_admin_or_super_admin
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.documentation.services import get_relationships_service
from apps.documentation.utils.api_responses import (
    success_response,
    error_response,
    paginated_response,
)
from apps.documentation.utils.list_projectors import (
    should_expand_full,
    to_relationship_list_item,
)

logger = logging.getLogger(__name__)


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
    endpoint_path = str(
        row.get("endpoint_path") or row.get("endpoint_id") or ""
    ).strip()
    method = str(row.get("method") or "QUERY").strip().upper() or "QUERY"
    if page_path and endpoint_path:
        return f"{page_path}|{endpoint_path}|{method}"
    return row.get("relationship_id") or ""


@require_super_admin
@require_http_methods(["GET"])
def get_relationships_list_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for relationships list on the documentation dashboard.

    Query params:
    - page_id, endpoint_id, usage_type, usage_context
    - limit, offset (legacy) / page, page_size (preferred)
    - search, sort, order
    """
    try:
        relationships_service = get_relationships_service()

        page_id = request.GET.get("page_id")
        endpoint_id = request.GET.get("endpoint_id")
        usage_type = request.GET.get("usage_type")
        usage_context = request.GET.get("usage_context")

        page_param = request.GET.get("page")
        page_size_param = request.GET.get("page_size")
        limit_param = request.GET.get("limit")
        offset_param = request.GET.get("offset")

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

        result = relationships_service.list_relationships(
            page_id=page_id,
            endpoint_id=endpoint_id,
            usage_type=usage_type,
            usage_context=usage_context,
            limit=limit,
            offset=offset,
        )

        relationships = result.get("relationships", [])
        total = result.get("total", 0)

        search_query = request.GET.get("search", "").strip().lower()
        if search_query:
            filtered_relationships = []
            for rel in relationships:
                page_path = (rel.get("page_path") or "").lower()
                endpoint_path = (rel.get("endpoint_path") or "").lower()
                if search_query in page_path or search_query in endpoint_path:
                    filtered_relationships.append(rel)
            relationships = filtered_relationships
            total = len(filtered_relationships)

        sort_field = request.GET.get("sort")
        sort_order = request.GET.get("order", "asc").lower()
        if sort_field:
            reverse_order = sort_order == "desc"
            if sort_field == "name":
                relationships.sort(
                    key=lambda r: (r.get("page_path") or "").lower(),
                    reverse=reverse_order,
                )
            elif sort_field == "updated":
                relationships.sort(
                    key=lambda r: r.get("updated_at", ""), reverse=reverse_order
                )

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
            message=f"Failed to retrieve relationships: {str(e)}", status_code=500
        ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def relationships_bulk_import_preview_api(request: HttpRequest) -> JsonResponse:
    """Preview bulk import for relationships. Body: { "relationships": [ ... ] }."""
    data, err = _parse_json_body_relationships(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    relationships = (data or {}).get("relationships") or []
    if not isinstance(relationships, list) or not relationships:
        return error_response(
            "Field 'relationships' must be a non-empty list.", status_code=400
        ).to_json_response()
    if len(relationships) > 500:
        return error_response(
            "Maximum 500 relationships per import.", status_code=400
        ).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error(
            "relationships_bulk_import_preview_api import failed: %s", e, exc_info=True
        )
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_relationships_service()
    existing: list[str] = []
    to_create: list[str] = []
    validation_errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(relationships, start=1):
        row = raw_row or {}
        rel_id = _build_relationship_id(row)
        if not rel_id:
            validation_errors.append(
                {
                    "row": index,
                    "error": "page_path (or page_id), endpoint_path (or endpoint_id), and method are required",
                }
            )
            continue
        page_path = str(row.get("page_path") or row.get("page_id") or "").strip()
        endpoint_path = str(
            row.get("endpoint_path") or row.get("endpoint_id") or ""
        ).strip()
        if not page_path or not endpoint_path:
            validation_errors.append(
                {
                    "row": index,
                    "relationship_id": rel_id,
                    "error": "page_path and endpoint_path are required",
                }
            )
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
            validation_errors.append(
                {"row": index, "relationship_id": rel_id, "error": str(exc)}
            )

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
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    relationships = (data or {}).get("relationships") or []
    if not isinstance(relationships, list) or not relationships:
        return error_response(
            "Field 'relationships' must be a non-empty list.", status_code=400
        ).to_json_response()
    if len(relationships) > 500:
        return error_response(
            "Maximum 500 relationships per import.", status_code=400
        ).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error(
            "relationships_bulk_import_api import failed: %s", e, exc_info=True
        )
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_relationships_service()
    created = 0
    updated = 0
    errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(relationships, start=1):
        row = raw_row or {}
        rel_id = _build_relationship_id(row)
        if not rel_id:
            errors.append(
                {
                    "row": index,
                    "error": "page_path, endpoint_path, and method are required",
                }
            )
            continue
        page_path = str(row.get("page_path") or row.get("page_id") or "").strip()
        endpoint_path = str(
            row.get("endpoint_path") or row.get("endpoint_id") or ""
        ).strip()
        method = str(row.get("method") or "QUERY").strip().upper() or "QUERY"
        if not page_path or not endpoint_path:
            errors.append(
                {"row": index, "error": "page_path and endpoint_path are required"}
            )
            continue
        try:
            rel_data = (
                DataTransformer.lambda_to_django_relationship(row)
                if "_id" in row
                else dict(row)
            )
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
            logger.warning(
                "relationships_bulk_import_api row %s failed: %s", index, exc
            )
            errors.append({"row": index, "relationship_id": rel_id, "error": str(exc)})

    return success_response(
        data={
            "created": created,
            "updated": updated,
            "failed": len(errors),
            "errors": errors[:50],
        },
        message="Relationships bulk import completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def relationships_bulk_upload_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload relationship JSON objects to S3. Body: { "relationships": [ ... ] }."""
    data, err = _parse_json_body_relationships(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    relationships = (data or {}).get("relationships") or []
    if not isinstance(relationships, list) or not relationships:
        return error_response(
            "Field 'relationships' must be a non-empty list.", status_code=400
        ).to_json_response()
    if len(relationships) > 500:
        return error_response(
            "Maximum 500 relationships per upload.", status_code=400
        ).to_json_response()

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
            errors.append(
                {
                    "relationship_id": "",
                    "error": "relationship_id or page_path|endpoint_path|method required",
                }
            )
            continue
        try:
            s3_key = f"{prefix}/relationships/{rel_id}.json"
            storage.write_json(s3_key, row)
            uploaded += 1
        except Exception as exc:
            logger.warning(
                "relationships_bulk_upload_to_s3_api relationship %s failed: %s",
                rel_id,
                exc,
            )
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
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    row = (data or {}).get("relationship")
    if not row or not isinstance(row, dict):
        return error_response(
            "Field 'relationship' must be a non-empty object.", status_code=400
        ).to_json_response()
    rel_id = _build_relationship_id(row)
    if not rel_id:
        return error_response(
            "page_path (or page_id), endpoint_path (or endpoint_id), and method are required.",
            status_code=400,
        ).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("relationships_import_one_api import failed: %s", e, exc_info=True)
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_relationships_service()
    page_path = str(row.get("page_path") or row.get("page_id") or "").strip()
    endpoint_path = str(
        row.get("endpoint_path") or row.get("endpoint_id") or ""
    ).strip()
    method = str(row.get("method") or "QUERY").strip().upper() or "QUERY"
    rel_data = (
        DataTransformer.lambda_to_django_relationship(row)
        if "_id" in row
        else dict(row)
    )
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
            return success_response(
                data={"updated": True, "relationship_id": rel_id},
                message="Relationship updated",
            ).to_json_response()
        service.create_relationship(rel_data)
        return success_response(
            data={"created": True, "relationship_id": rel_id},
            message="Relationship created",
        ).to_json_response()
    except Exception as exc:
        logger.warning(
            "relationships_import_one_api relationship %s failed: %s", rel_id, exc
        )
        return error_response(message=str(exc), status_code=400).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def relationships_upload_one_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload a single relationship JSON to S3. Body: { "relationship": { ... } }."""
    data, err = _parse_json_body_relationships(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    row = (data or {}).get("relationship")
    if not row or not isinstance(row, dict):
        return error_response(
            "Field 'relationship' must be a non-empty object.", status_code=400
        ).to_json_response()
    rel_id = _build_relationship_id(row)
    if not rel_id:
        return error_response(
            "page_path (or page_id), endpoint_path (or endpoint_id), and method are required.",
            status_code=400,
        ).to_json_response()

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
        logger.warning(
            "relationships_upload_one_to_s3_api relationship %s failed: %s", rel_id, exc
        )
        return error_response(message=str(exc), status_code=500).to_json_response()
