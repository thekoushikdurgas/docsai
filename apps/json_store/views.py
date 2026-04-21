"""JSON Store views — upload, list, view, delete, download JSON documents via S3."""

import json
import logging
import re
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from apps.admin_ops.services.admin_client import gateway_s3_delete_file
from apps.admin_ops.services.s3storage_client import S3StorageClient
from apps.core.decorators import require_login
from apps.core.exceptions import LambdaAPIError

from .models import JsonDocument

logger = logging.getLogger(__name__)

S3STORAGE_ENABLED = bool(getattr(settings, "S3STORAGE_API_URL", ""))


def _s3_client(request_id: str = "") -> S3StorageClient:
    return S3StorageClient(request_id=request_id or str(uuid.uuid4()))


def _default_bucket() -> str:
    return getattr(settings, "PAYMENT_QR_BUCKET_ID", "") or "admin"


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:190]


def _unique_slug(label: str) -> str:
    base = _slugify(label) or "document"
    slug = base
    n = 1
    while JsonDocument.objects.filter(key=slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


# ─── Views ────────────────────────────────────────────────────────────────────


@require_login
@require_http_methods(["GET"])
def index_view(request):
    """List JSON documents (local DB + S3 keys). @role: authenticated"""
    docs = JsonDocument.objects.all()
    return render(
        request,
        "json_store/index.html",
        {
            "page_title": "JSON Store",
            "docs": docs,
            "s3_enabled": S3STORAGE_ENABLED,
            "default_bucket": _default_bucket(),
        },
    )


@require_login
@require_http_methods(["POST"])
def upload_view(request):
    """
    Accept multipart/form-data: file (JSON), label (optional), bucket_id (optional).

    @role: authenticated
    """
    if not S3STORAGE_ENABLED:
        return JsonResponse(
            {"success": False, "error": "S3 storage is not configured."}, status=400
        )

    file = request.FILES.get("file")
    if not file:
        return JsonResponse(
            {"success": False, "error": "No file provided."}, status=400
        )

    label = (request.POST.get("label") or file.name or "document").strip()
    bucket_id = (request.POST.get("bucket_id") or _default_bucket()).strip()
    if not bucket_id:
        return JsonResponse(
            {
                "success": False,
                "error": "No bucket configured (set PAYMENT_QR_BUCKET_ID).",
            },
            status=400,
        )

    # Read and validate JSON
    try:
        raw_bytes = file.read()
        json.loads(raw_bytes)  # syntax validation
    except (ValueError, Exception) as exc:
        return JsonResponse(
            {"success": False, "error": f"Invalid JSON: {exc}"}, status=400
        )

    # Re-seek for upload
    import io

    file_like = io.BytesIO(raw_bytes)

    try:
        client = _s3_client()
        result = client.upload_json(
            bucket_id=bucket_id, file=file_like, filename=file.name
        )
        file_key = (result.get("fileKey") or result.get("file_key") or "").strip()
        if not file_key:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Upload succeeded but no fileKey returned.",
                },
                status=500,
            )
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)

    slug = _unique_slug(label)
    operator = request.session.get("operator", {})
    doc = JsonDocument.objects.create(
        key=slug,
        label=label,
        s3_bucket_id=bucket_id,
        s3_file_key=file_key,
        size_bytes=len(raw_bytes),
        content_type="application/json",
        uploaded_by=operator.get("email", ""),
    )
    return JsonResponse(
        {
            "success": True,
            "id": doc.pk,
            "key": doc.key,
            "label": doc.label,
            "size": doc.size_display,
        }
    )


@require_login
@require_http_methods(["GET"])
def view_json_view(request, doc_id: int):
    """
    Return parsed JSON content for a document (for modal viewer).

    @role: authenticated
    """
    doc = get_object_or_404(JsonDocument, pk=doc_id)
    try:
        client = _s3_client()
        raw = client.get_object(doc.full_s3_key)
        data = json.loads(raw)
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)
    except Exception as exc:
        return JsonResponse(
            {"success": False, "error": f"Failed to load: {exc}"}, status=500
        )
    return JsonResponse({"success": True, "data": data, "label": doc.label})


@require_login
@require_http_methods(["POST"])
def delete_view(request, doc_id: int):
    """
    Delete a JSON document (DB record + S3 object; optional ``s3.deleteFile``).

    @role: authenticated
    """
    doc = get_object_or_404(JsonDocument, pk=doc_id)
    gateway_ok = False
    if getattr(settings, "ADMIN_STORAGE_VIA_GATEWAY", False):
        tok = (request.session.get("operator") or {}).get("token")
        if tok:
            try:
                gateway_s3_delete_file(tok, doc.s3_file_key)
                gateway_ok = True
            except Exception as exc:
                logger.warning(
                    "json_store gateway s3.deleteFile failed, trying direct API: %s",
                    exc,
                )
    if not gateway_ok:
        try:
            client = _s3_client()
            client._request(
                "DELETE", "/api/v1/objects", params={"key": doc.full_s3_key}
            )
        except Exception as exc:
            logger.warning("json_store delete S3 object failed: %s", exc)
    doc.delete()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True})
    return redirect("json_store:index")


@require_login
@require_http_methods(["GET"])
def download_view(request, doc_id: int):
    """
    Redirect to presigned download URL for the document.

    @role: authenticated
    """
    doc = get_object_or_404(JsonDocument, pk=doc_id)
    try:
        client = _s3_client()
        result = client._request(
            "GET",
            "/api/v1/objects/presign-download",
            params={"key": doc.full_s3_key, "expires_in": 3600},
        )
        url = result.get("downloadUrl") or result.get("download_url")
        if not url:
            return JsonResponse(
                {"success": False, "error": "No download URL."}, status=500
            )
        return redirect(url)
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)
