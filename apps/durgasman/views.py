"""
Durgasman views — Postman-compatible collections/environments (Phase 8).

Local ORM + s3storage JSON; HTTP send proxy. All UI/API views use
``@require_super_admin``; docstrings end with ``@role: super_admin``.
Replaces ``postman_app``; templates/models under the ``durgasman`` namespace.
"""

from __future__ import annotations

import io
import json
import logging
import uuid

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.admin_ops.services.s3storage_client import S3StorageClient
from apps.core.decorators import require_super_admin
from apps.core.exceptions import LambdaAPIError

from .models import DurgasmanCollection, DurgasmanEnvironment
from .services.request_runner import run_request

logger = logging.getLogger(__name__)

S3STORAGE_ENABLED = bool(getattr(settings, "S3STORAGE_API_URL", ""))


def _s3_client() -> S3StorageClient:
    return S3StorageClient(request_id=str(uuid.uuid4()))


def _default_bucket() -> str:
    return getattr(settings, "PAYMENT_QR_BUCKET_ID", "") or "admin"


def _count_requests(items: list) -> int:
    """Recursively count request nodes in a Postman items array."""
    count = 0
    for item in items:
        if isinstance(item.get("request"), dict):
            count += 1
        if isinstance(item.get("item"), list):
            count += _count_requests(item["item"])
    return count


# ─── Dashboard ────────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def dashboard(request):
    """Collections and environments summary. @role: super_admin"""
    collections = list(
        DurgasmanCollection.objects.values(
            "id", "name", "description", "item_count", "request_count", "uploaded_at"
        )
    )
    environments = list(
        DurgasmanEnvironment.objects.values(
            "id", "name", "variable_count", "uploaded_at"
        )
    )
    return render(
        request,
        "durgasman/dashboard.html",
        {
            "page_title": "Durgasman",
            "collections": collections,
            "environments": environments,
            "s3_enabled": S3STORAGE_ENABLED,
        },
    )


# ─── Upload ───────────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET", "POST"])
def import_collection_page(request):
    """
    HTML import form; POST delegates to :func:`upload_collection_view`.

    @role: super_admin
    """
    if request.method == "POST":
        resp = upload_collection_view(request)
        try:
            payload = json.loads(resp.content.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            messages.error(request, "Import failed (invalid response).")
            return render(
                request,
                "durgasman/import.html",
                {"page_title": "Import collection"},
            )
        if resp.status_code >= 400 or not payload.get("success"):
            messages.error(request, payload.get("error") or "Import failed.")
        else:
            messages.success(
                request,
                f"Imported collection: {payload.get('name', 'OK')}",
            )
            return redirect("durgasman:dashboard")
    return render(
        request,
        "durgasman/import.html",
        {"page_title": "Import collection"},
    )


@require_super_admin
@require_http_methods(["GET"])
def upload_view(request):
    """Upload collection/environment shell. @role: super_admin"""
    collections = list(
        DurgasmanCollection.objects.values(
            "id", "name", "item_count", "request_count", "uploaded_at"
        )
    )
    environments = list(
        DurgasmanEnvironment.objects.values(
            "id", "name", "variable_count", "uploaded_at"
        )
    )
    return render(
        request,
        "durgasman/upload.html",
        {
            "page_title": "Upload Collection / Environment",
            "s3_enabled": S3STORAGE_ENABLED,
            "default_bucket": _default_bucket(),
            "collections": collections,
            "environments": environments,
        },
    )


@require_super_admin
@require_http_methods(["POST"])
def upload_collection_view(request):
    """
    Upload a Postman collection JSON file to S3, save metadata to DB.

    @role: super_admin
    """
    if not S3STORAGE_ENABLED:
        return JsonResponse(
            {"success": False, "error": "S3 storage not configured."}, status=400
        )

    file = request.FILES.get("file")
    if not file:
        return JsonResponse(
            {"success": False, "error": "No file provided."}, status=400
        )

    bucket_id = (request.POST.get("bucket_id") or _default_bucket()).strip()

    try:
        raw_bytes = file.read()
        parsed = json.loads(raw_bytes)
    except Exception as exc:
        return JsonResponse(
            {"success": False, "error": f"Invalid JSON: {exc}"}, status=400
        )

    info = parsed.get("info", {})
    if not isinstance(info, dict) or not info.get("name"):
        return JsonResponse(
            {
                "success": False,
                "error": "Not a valid Postman collection (missing info.name).",
            },
            status=400,
        )

    items = parsed.get("item", [])
    item_count = len(items) if isinstance(items, list) else 0
    request_count = _count_requests(items) if isinstance(items, list) else 0

    try:
        client = _s3_client()
        result = client.upload_json(
            bucket_id=bucket_id,
            file=io.BytesIO(raw_bytes),
            filename=file.name,
        )
        file_key = (result.get("fileKey") or result.get("file_key") or "").strip()
        if not file_key:
            return JsonResponse(
                {"success": False, "error": "No fileKey in S3 response."}, status=500
            )
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)

    operator = request.session.get("operator", {})
    col = DurgasmanCollection.objects.create(
        name=info.get("name", file.name),
        description=info.get("description", ""),
        postman_id=info.get("_postman_id", ""),
        schema_version="v2.1.0",
        s3_bucket_id=bucket_id,
        s3_file_key=file_key,
        item_count=item_count,
        request_count=request_count,
        size_bytes=len(raw_bytes),
        uploaded_by=operator.get("email", ""),
    )
    return JsonResponse(
        {
            "success": True,
            "id": col.pk,
            "name": col.name,
            "item_count": col.item_count,
            "request_count": col.request_count,
        }
    )


@require_super_admin
@require_http_methods(["POST"])
def upload_environment_view(request):
    """
    Upload a Postman environment JSON file.

    @role: super_admin
    """
    if not S3STORAGE_ENABLED:
        return JsonResponse(
            {"success": False, "error": "S3 storage not configured."}, status=400
        )

    file = request.FILES.get("file")
    if not file:
        return JsonResponse(
            {"success": False, "error": "No file provided."}, status=400
        )

    bucket_id = (request.POST.get("bucket_id") or _default_bucket()).strip()

    try:
        raw_bytes = file.read()
        parsed = json.loads(raw_bytes)
    except Exception as exc:
        return JsonResponse(
            {"success": False, "error": f"Invalid JSON: {exc}"}, status=400
        )

    if not isinstance(parsed.get("values"), list) and not isinstance(
        parsed.get("name"), str
    ):
        return JsonResponse(
            {
                "success": False,
                "error": "Not a valid Postman environment (missing name or values).",
            },
            status=400,
        )

    values = parsed.get("values", [])
    variable_count = len([v for v in values if isinstance(v, dict)])

    try:
        client = _s3_client()
        result = client.upload_json(
            bucket_id=bucket_id,
            file=io.BytesIO(raw_bytes),
            filename=file.name,
        )
        file_key = (result.get("fileKey") or result.get("file_key") or "").strip()
        if not file_key:
            return JsonResponse(
                {"success": False, "error": "No fileKey in S3 response."}, status=500
            )
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)

    operator = request.session.get("operator", {})
    env = DurgasmanEnvironment.objects.create(
        name=parsed.get("name", file.name),
        postman_id=str(parsed.get("id", "")),
        s3_bucket_id=bucket_id,
        s3_file_key=file_key,
        variable_count=variable_count,
        size_bytes=len(raw_bytes),
        uploaded_by=operator.get("email", ""),
    )
    return JsonResponse(
        {
            "success": True,
            "id": env.pk,
            "name": env.name,
            "variable_count": env.variable_count,
        }
    )


# ─── Collections API ─────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def collections_list_view(request):
    """JSON list of collections. @role: super_admin"""
    cols = list(
        DurgasmanCollection.objects.values(
            "id",
            "name",
            "description",
            "item_count",
            "request_count",
            "uploaded_at",
            "uploaded_by",
        )
    )
    for c in cols:
        c["uploaded_at"] = (
            c["uploaded_at"].strftime("%Y-%m-%d %H:%M") if c["uploaded_at"] else ""
        )
    return JsonResponse({"collections": cols})


@require_super_admin
@require_http_methods(["GET"])
def collection_json_view(request, col_id: int):
    """
    Return full collection JSON fetched from S3.

    @role: super_admin
    """
    col = get_object_or_404(DurgasmanCollection, pk=col_id)
    try:
        client = _s3_client()
        raw = client.get_object(col.full_s3_key)
        data = json.loads(raw)
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)
    except Exception as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)
    return JsonResponse(
        {
            "success": True,
            "collection": data,
            "meta": {
                "id": col.pk,
                "name": col.name,
                "request_count": col.request_count,
            },
        }
    )


@require_super_admin
@require_http_methods(["POST"])
def collection_delete_view(request, col_id: int):
    """Delete collection row + S3 object. @role: super_admin"""
    col = get_object_or_404(DurgasmanCollection, pk=col_id)
    try:
        _s3_client()._request(
            "DELETE", "/api/v1/objects", params={"key": col.full_s3_key}
        )
    except Exception as exc:
        logger.warning("delete collection S3: %s", exc)
    col.delete()
    return JsonResponse({"success": True})


# ─── Environments API ─────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def environments_list_view(request):
    """JSON list of environments. @role: super_admin"""
    envs = list(
        DurgasmanEnvironment.objects.values(
            "id", "name", "variable_count", "uploaded_at"
        )
    )
    for e in envs:
        e["uploaded_at"] = (
            e["uploaded_at"].strftime("%Y-%m-%d %H:%M") if e["uploaded_at"] else ""
        )
    return JsonResponse({"environments": envs})


@require_super_admin
@require_http_methods(["GET"])
def environment_json_view(request, env_id: int):
    """
    Return full environment JSON fetched from S3.

    @role: super_admin
    """
    env = get_object_or_404(DurgasmanEnvironment, pk=env_id)
    try:
        client = _s3_client()
        raw = client.get_object(env.full_s3_key)
        data = json.loads(raw)
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)
    except Exception as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)
    return JsonResponse(
        {
            "success": True,
            "environment": data,
            "meta": {
                "id": env.pk,
                "name": env.name,
                "variable_count": env.variable_count,
            },
        }
    )


@require_super_admin
@require_http_methods(["POST"])
def environment_delete_view(request, env_id: int):
    """Delete environment row + S3 object. @role: super_admin"""
    env = get_object_or_404(DurgasmanEnvironment, pk=env_id)
    try:
        _s3_client()._request(
            "DELETE", "/api/v1/objects", params={"key": env.full_s3_key}
        )
    except Exception as exc:
        logger.warning("delete environment S3: %s", exc)
    env.delete()
    return JsonResponse({"success": True})


# ─── Request proxy ────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["POST"])
def send_request_view(request):
    """
    Proxy an HTTP request from the browser through the admin backend.

    @role: super_admin
    """
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, Exception):
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    method = (payload.get("method") or "GET").upper()
    url = (payload.get("url") or "").strip()
    if not url:
        return JsonResponse({"error": "URL is required."}, status=400)

    result = run_request(
        method=method,
        url=url,
        headers=payload.get("headers") or {},
        body=payload.get("body") or "",
        body_type=payload.get("body_type") or "raw",
        form_data=payload.get("form_data") or {},
        query_params=payload.get("query_params") or {},
        timeout=min(int(payload.get("timeout") or 30), 120),
        variables=payload.get("variables") or {},
    )
    return JsonResponse(result)


# ─── DEPRECATED: legacy JSON endpoints (kept for old JS clients) ──────────────


@require_super_admin
def api_collections(request):
    """
    JSON list — delegates to collections_list_view for GET.

    @role: super_admin
    """
    if request.method == "GET":
        return collections_list_view(request)
    return JsonResponse({"success": False, "error": "Use GET"}, status=405)


@require_super_admin
def api_environments(request):
    """Legacy JSON — delegates to environments list. @role: super_admin"""
    if request.method == "GET":
        return environments_list_view(request)
    return JsonResponse({"success": False, "error": "Use GET"}, status=405)


@require_super_admin
def api_history(request):
    """Stub history for old clients. @role: super_admin"""
    return JsonResponse({"success": True, "items": []})


@require_super_admin
def api_analyze_response(request):
    """
    Deprecated analyze hook; use ``/durgasman/send/`` or execute API.

    @role: super_admin
    """
    try:
        json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    resp = JsonResponse(
        {
            "success": True,
            "analysis": None,
            "deprecated": True,
            "successor": "/durgasman/send/",
        }
    )
    resp["Deprecation"] = "true"
    return resp
