"""Postman dashboard API: list and bulk import/upload endpoints."""

from __future__ import annotations

import logging
from typing import Any, Dict

from apps.core.decorators.auth import require_super_admin, require_admin_or_super_admin
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.documentation.services import get_postman_service
from apps.documentation.utils.api_responses import (
    success_response,
    error_response,
    paginated_response,
)
from apps.documentation.utils.list_projectors import (
    should_expand_full,
    to_postman_list_item,
)

logger = logging.getLogger(__name__)


def _parse_json_body_postman(req):
    try:
        import json as _json

        body = _json.loads(req.body or b"{}")
        return body, None
    except Exception as e:
        return None, str(e)


@require_super_admin
@require_http_methods(["GET"])
def get_postman_list_api(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for Postman configurations list on the documentation dashboard.

    Query params:
    - state: Filter by state
    - limit, offset (legacy) / page, page_size (preferred)
    - search, sort, order
    """
    try:
        postman_service = get_postman_service()

        state = request.GET.get("state")

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

        result = postman_service.list_configurations(
            state=state,
            limit=limit,
            offset=offset,
        )

        configurations = result.get("configurations", [])
        total = result.get("total", 0)

        search_query = request.GET.get("search", "").strip().lower()
        if search_query:
            filtered_configs = []
            for config in configurations:
                config_id = (config.get("config_id") or "").lower()
                name = (config.get("name") or "").lower()
                if search_query in config_id or search_query in name:
                    filtered_configs.append(config)
            configurations = filtered_configs
            total = len(filtered_configs)

        sort_field = request.GET.get("sort")
        sort_order = request.GET.get("order", "asc").lower()
        if sort_field:
            reverse_order = sort_order == "desc"
            if sort_field == "name":
                configurations.sort(
                    key=lambda c: (c.get("config_id") or "").lower(),
                    reverse=reverse_order,
                )
            elif sort_field == "updated":
                configurations.sort(
                    key=lambda c: c.get("updated_at", ""), reverse=reverse_order
                )

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
            status_code=500,
        ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def postman_bulk_import_preview_api(request: HttpRequest) -> JsonResponse:
    """Preview bulk import for Postman configurations. Body: { "configs": [ ... ] }."""
    data, err = _parse_json_body_postman(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    configs = (data or {}).get("configs") or (data or {}).get("configurations") or []
    if not isinstance(configs, list) or not configs:
        return error_response(
            "Field 'configs' or 'configurations' must be a non-empty list.",
            status_code=400,
        ).to_json_response()
    if len(configs) > 500:
        return error_response(
            "Maximum 500 configurations per import.", status_code=400
        ).to_json_response()

    service = get_postman_service()
    existing: list[str] = []
    to_create: list[str] = []
    validation_errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(configs, start=1):
        row = raw_row or {}
        config_id = str(row.get("config_id") or row.get("id") or "").strip()
        if not config_id:
            validation_errors.append(
                {"row": index, "error": "config_id (or id) is required"}
            )
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
            validation_errors.append(
                {"row": index, "config_id": config_id, "error": str(exc)}
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
def postman_bulk_import_api(request: HttpRequest) -> JsonResponse:
    """Bulk import Postman configurations (writes to S3). Body: { "configs": [ ... ] }."""
    data, err = _parse_json_body_postman(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    configs = (data or {}).get("configs") or (data or {}).get("configurations") or []
    if not isinstance(configs, list) or not configs:
        return error_response(
            "Field 'configs' or 'configurations' must be a non-empty list.",
            status_code=400,
        ).to_json_response()
    if len(configs) > 500:
        return error_response(
            "Maximum 500 configurations per import.", status_code=400
        ).to_json_response()

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
            logger.warning(
                "postman_bulk_import_api config %s failed: %s", config_id, exc
            )
            errors.append({"row": index, "config_id": config_id, "error": str(exc)})

    try:
        service.unified_storage.clear_cache("postman")
    except Exception:
        pass

    return success_response(
        data={
            "created": created,
            "updated": updated,
            "failed": len(errors),
            "errors": errors[:50],
        },
        message="Postman configurations bulk import completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def postman_bulk_upload_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload Postman configuration JSON objects to S3. Body: { "configs": [ ... ] }."""
    data, err = _parse_json_body_postman(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    configs = (data or {}).get("configs") or (data or {}).get("configurations") or []
    if not isinstance(configs, list) or not configs:
        return error_response(
            "Field 'configs' or 'configurations' must be a non-empty list.",
            status_code=400,
        ).to_json_response()
    if len(configs) > 500:
        return error_response(
            "Maximum 500 configurations per upload.", status_code=400
        ).to_json_response()

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
            logger.warning(
                "postman_bulk_upload_to_s3_api config %s failed: %s", config_id, exc
            )
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
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    row = (data or {}).get("config")
    if not row or not isinstance(row, dict):
        return error_response(
            "Field 'config' must be a non-empty object.", status_code=400
        ).to_json_response()
    config_id = str(row.get("config_id") or row.get("id") or "").strip()
    if not config_id:
        return error_response(
            "config_id (or id) is required.", status_code=400
        ).to_json_response()

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
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    row = (data or {}).get("config")
    if not row or not isinstance(row, dict):
        return error_response(
            "Field 'config' must be a non-empty object.", status_code=400
        ).to_json_response()
    config_id = str(row.get("config_id") or row.get("id") or "").strip()
    if not config_id:
        return error_response(
            "config_id (or id) is required.", status_code=400
        ).to_json_response()

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
        logger.warning(
            "postman_upload_one_to_s3_api config %s failed: %s", config_id, exc
        )
        return error_response(message=str(exc), status_code=500).to_json_response()
