"""Endpoints dashboard API: list and bulk import/upload endpoints."""

from __future__ import annotations

import logging
from typing import Any, Dict

from apps.core.decorators.auth import require_super_admin, require_admin_or_super_admin
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from apps.documentation.services import get_endpoints_service
from apps.documentation.utils.api_responses import (
    success_response,
    error_response,
    paginated_response,
)
from apps.documentation.utils.list_projectors import (
    should_expand_full,
    to_endpoint_list_item,
)

logger = logging.getLogger(__name__)


def _parse_json_body_endpoints(req):
    try:
        import json as _json

        body = _json.loads(req.body or b"{}")
        return body, None
    except Exception as e:
        return None, str(e)


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
    - limit, offset (legacy) / page, page_size (preferred)
    - search, sort, order
    """
    try:
        endpoints_service = get_endpoints_service()

        api_version = request.GET.get("api_version")
        method = request.GET.get("method")
        state = request.GET.get("state")
        lambda_service = request.GET.get("lambda_service")

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

        result = endpoints_service.list_endpoints(
            api_version=api_version,
            method=method,
            endpoint_state=state,
            limit=limit,
            offset=offset,
        )

        endpoints = result.get("endpoints", [])
        total = result.get("total", 0)

        if lambda_service:
            filtered_endpoints = []
            for endpoint in endpoints:
                lambda_services = endpoint.get("lambda_services", [])
                if isinstance(lambda_services, list):
                    if any(
                        ls.get("service_name") == lambda_service
                        for ls in lambda_services
                        if isinstance(ls, dict)
                    ):
                        filtered_endpoints.append(endpoint)
                elif (
                    isinstance(lambda_services, str)
                    and lambda_services == lambda_service
                ):
                    filtered_endpoints.append(endpoint)
            endpoints = filtered_endpoints
            total = len(filtered_endpoints)

        search_query = request.GET.get("search", "").strip().lower()
        if search_query:
            filtered_endpoints = []
            for endpoint in endpoints:
                endpoint_id = endpoint.get("endpoint_id", "").lower()
                endpoint_path = endpoint.get("endpoint_path", "").lower()
                if search_query in endpoint_id or search_query in endpoint_path:
                    filtered_endpoints.append(endpoint)
            endpoints = filtered_endpoints
            total = len(filtered_endpoints)

        sort_field = request.GET.get("sort")
        sort_order = request.GET.get("order", "asc").lower()
        if sort_field:
            reverse_order = sort_order == "desc"
            if sort_field == "name":
                endpoints.sort(
                    key=lambda e: e.get("endpoint_id", "").lower(),
                    reverse=reverse_order,
                )
            elif sort_field == "updated":
                endpoints.sort(
                    key=lambda e: e.get("updated_at", ""), reverse=reverse_order
                )

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
            message=f"Failed to retrieve endpoints: {str(e)}", status_code=500
        ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def endpoints_bulk_import_preview_api(request: HttpRequest) -> JsonResponse:
    """Preview bulk import for endpoints. Body: { "endpoints": [ ... ] }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    endpoints = (data or {}).get("endpoints") or []
    if not isinstance(endpoints, list) or not endpoints:
        return error_response(
            "Field 'endpoints' must be a non-empty list.", status_code=400
        ).to_json_response()
    if len(endpoints) > 500:
        return error_response(
            "Maximum 500 endpoints per import.", status_code=400
        ).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error(
            "endpoints_bulk_import_preview_api import failed: %s", e, exc_info=True
        )
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_endpoints_service()
    existing: list[str] = []
    to_create: list[str] = []
    validation_errors: list[Dict[str, Any]] = []

    for index, raw_row in enumerate(endpoints, start=1):
        row = raw_row or {}
        endpoint_id = str(row.get("endpoint_id") or row.get("endpointId") or "").strip()
        if not endpoint_id:
            validation_errors.append(
                {"row": index, "endpoint_id": "", "error": "endpoint_id is required"}
            )
            continue
        path_val = str(
            row.get("endpoint_path") or row.get("path") or row.get("endpointPath") or ""
        ).strip()
        method_val = str(row.get("method") or "").strip().upper() or "GET"
        if not path_val:
            validation_errors.append(
                {
                    "row": index,
                    "endpoint_id": endpoint_id,
                    "error": "endpoint_path or path is required",
                }
            )
            continue
        try:
            page_data = (
                DataTransformer.lambda_to_django_endpoint(row) if "_id" in row else row
            )
            try:
                exists = service.get_endpoint(endpoint_id)
            except Exception:
                exists = None
            if exists:
                existing.append(endpoint_id)
            else:
                to_create.append(endpoint_id)
        except Exception as exc:
            validation_errors.append(
                {"row": index, "endpoint_id": endpoint_id, "error": str(exc)}
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
def endpoints_bulk_import_api(request: HttpRequest) -> JsonResponse:
    """Bulk import endpoints. Body: { "endpoints": [ ... ] }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    endpoints = (data or {}).get("endpoints") or []
    if not isinstance(endpoints, list) or not endpoints:
        return error_response(
            "Field 'endpoints' must be a non-empty list.", status_code=400
        ).to_json_response()
    if len(endpoints) > 500:
        return error_response(
            "Maximum 500 endpoints per import.", status_code=400
        ).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("endpoints_bulk_import_api import failed: %s", e, exc_info=True)
        return error_response(
            "Internal error preparing import.", status_code=500
        ).to_json_response()

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
            page_data = (
                DataTransformer.lambda_to_django_endpoint(row)
                if "_id" in row
                else dict(row)
            )
            if not page_data.get("endpoint_path") and page_data.get("path"):
                page_data["endpoint_path"] = page_data["path"]
            if not page_data.get("endpoint_path"):
                page_data["endpoint_path"] = row.get("path") or "/"
            if not page_data.get("method"):
                page_data["method"] = row.get("method") or "GET"
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
        data={
            "created": created,
            "updated": updated,
            "failed": len(errors),
            "errors": errors[:50],
        },
        message="Endpoints bulk import completed",
    ).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def endpoints_bulk_upload_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload endpoint JSON objects to S3. Body: { "endpoints": [ ... ] }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    endpoints = (data or {}).get("endpoints") or []
    if not isinstance(endpoints, list) or not endpoints:
        return error_response(
            "Field 'endpoints' must be a non-empty list.", status_code=400
        ).to_json_response()
    if len(endpoints) > 500:
        return error_response(
            "Maximum 500 endpoints per upload.", status_code=400
        ).to_json_response()

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
            logger.warning(
                "endpoints_bulk_upload_to_s3_api endpoint %s failed: %s",
                endpoint_id,
                exc,
            )
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
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    row = (data or {}).get("endpoint")
    if not row or not isinstance(row, dict):
        return error_response(
            "Field 'endpoint' must be a non-empty object.", status_code=400
        ).to_json_response()
    endpoint_id = str(row.get("endpoint_id") or "").strip()
    if not endpoint_id:
        return error_response(
            "endpoint_id is required.", status_code=400
        ).to_json_response()

    try:
        from apps.documentation.utils.data_transformers import DataTransformer
    except Exception as e:
        logger.error("endpoints_import_one_api import failed: %s", e, exc_info=True)
        return error_response("Internal error.", status_code=500).to_json_response()

    service = get_endpoints_service()
    page_data = (
        DataTransformer.lambda_to_django_endpoint(row) if "_id" in row else dict(row)
    )
    if not page_data.get("endpoint_path"):
        page_data["endpoint_path"] = row.get("path") or "/"
    if not page_data.get("method"):
        page_data["method"] = row.get("method") or "GET"
    if "path" not in page_data or not page_data["path"]:
        page_data["path"] = page_data.get("endpoint_path") or "/"
    try:
        existing = service.get_endpoint(endpoint_id)
    except Exception:
        existing = None
    try:
        if existing:
            service.update_endpoint(endpoint_id, page_data)
            return success_response(
                data={"updated": True, "endpoint_id": endpoint_id},
                message="Endpoint updated",
            ).to_json_response()
        service.create_endpoint(page_data)
        return success_response(
            data={"created": True, "endpoint_id": endpoint_id},
            message="Endpoint created",
        ).to_json_response()
    except Exception as exc:
        logger.warning(
            "endpoints_import_one_api endpoint %s failed: %s", endpoint_id, exc
        )
        return error_response(message=str(exc), status_code=400).to_json_response()


@require_admin_or_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def endpoints_upload_one_to_s3_api(request: HttpRequest) -> JsonResponse:
    """Upload a single endpoint JSON to S3. Body: { "endpoint": { ... } }."""
    data, err = _parse_json_body_endpoints(request)
    if err:
        return error_response(
            f"Invalid JSON body: {err}", status_code=400
        ).to_json_response()
    row = (data or {}).get("endpoint")
    if not row or not isinstance(row, dict):
        return error_response(
            "Field 'endpoint' must be a non-empty object.", status_code=400
        ).to_json_response()
    endpoint_id = str(row.get("endpoint_id") or "").strip()
    if not endpoint_id:
        return error_response(
            "endpoint_id is required.", status_code=400
        ).to_json_response()

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
        logger.warning(
            "endpoints_upload_one_to_s3_api endpoint %s failed: %s", endpoint_id, exc
        )
        return error_response(message=str(exc), status_code=500).to_json_response()
