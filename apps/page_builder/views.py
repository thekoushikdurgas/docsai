"""Page Builder — dashboard, upload, editor, JSON API."""

import io
import json
import logging
import re
import uuid
from copy import deepcopy

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from apps.admin_ops.services.admin_client import gateway_s3_delete_file
from apps.admin_ops.services.s3storage_client import S3StorageClient
from apps.core.decorators import require_login
from apps.core.exceptions import LambdaAPIError
from apps.json_store.models import JsonDocument

from .models import PageSpec

logger = logging.getLogger(__name__)

S3STORAGE_ENABLED = bool(getattr(settings, "S3STORAGE_API_URL", ""))


def _s3_client() -> S3StorageClient:
    return S3StorageClient(request_id=str(uuid.uuid4()))


def _default_bucket() -> str:
    return getattr(settings, "PAYMENT_QR_BUCKET_ID", "") or "admin"


def _auth_required(meta: dict) -> bool:
    if not isinstance(meta, dict):
        return False
    auth = str(meta.get("authentication") or "").lower()
    if "not required" in auth or "public" in auth or auth in ("none", ""):
        return False
    if "required" in auth and "not required" not in auth:
        return True
    return False


def _parse_page_spec_fields(data: dict) -> dict:
    """Extract PageSpec model fields from parsed page_spec JSON."""
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    sections = data.get("sections")
    if not isinstance(sections, list):
        sections = []
    ui = data.get("ui_components")
    if not isinstance(ui, list):
        ui = []
    ep = data.get("uses_endpoints")
    if not isinstance(ep, list):
        ep = []
    era = data.get("era_tags")
    if not isinstance(era, list):
        era = []
    page_id = (data.get("page_id") or "").strip()
    if not page_id:
        raise ValueError("page_id is required in page_spec JSON")
    title = (data.get("title") or page_id).strip()[:300]
    return {
        "page_id": page_id[:200],
        "title": title,
        "page_type": str(data.get("page_type") or "")[:100],
        "codebase": str(data.get("codebase") or "")[:100],
        "surface": str(data.get("surface") or "")[:200],
        "flow_id": str(data.get("flow_id") or "")[:200],
        "era_tags": era,
        "route": str(meta.get("route") or "")[:500],
        "status": str(meta.get("status") or "")[:50],
        "auth_required": _auth_required(meta),
        "purpose": str(meta.get("purpose") or "")[:10000],
        "section_count": len(sections),
        "component_count": len(ui),
        "endpoint_count": len(ep),
    }


def _json_doc_key_for_page(page_id: str) -> str:
    base = re.sub(r"[^\w\-]+", "-", page_id.lower()).strip("-")[:190] or "page-spec"
    key = f"page-spec-{base}"
    n = 1
    # ensure uniqueness only if different content - actually page_id is unique per PageSpec
    return key[:200]


@require_login
@require_http_methods(["GET"])
def dashboard_view(request):
    """List uploaded page specs (local ORM). @role: authenticated"""
    specs = list(
        PageSpec.objects.values(
            "id",
            "page_id",
            "title",
            "page_type",
            "codebase",
            "surface",
            "route",
            "status",
            "section_count",
            "component_count",
            "endpoint_count",
            "uploaded_at",
            "updated_at",
        )
    )
    codebases = sorted({s["codebase"] for s in specs if s.get("codebase")})
    page_types = sorted({s["page_type"] for s in specs if s.get("page_type")})
    statuses = sorted({s["status"] for s in specs if s.get("status")})
    return render(
        request,
        "page_builder/index.html",
        {
            "page_title": "Page Builder",
            "specs": specs,
            "codebases": codebases,
            "page_types": page_types,
            "statuses": statuses,
            "s3_enabled": S3STORAGE_ENABLED,
            "default_bucket": _default_bucket(),
            "stats": {
                "total": len(specs),
                "root": sum(1 for s in specs if s.get("codebase") == "root"),
                "app": sum(1 for s in specs if s.get("codebase") == "app"),
            },
        },
    )


@require_login
@require_http_methods(["GET"])
def upload_page_view(request):
    """
    Dedicated upload page (sidebar link).

    @role: authenticated
    """
    return render(
        request,
        "page_builder/upload.html",
        {
            "page_title": "Upload page spec",
            "s3_enabled": S3STORAGE_ENABLED,
            "default_bucket": _default_bucket(),
        },
    )


@require_login
@require_http_methods(["POST"])
def upload_view(request):
    """
    Upload ``page_spec`` JSON to S3 and upsert ``PageSpec`` + ``JsonDocument``.

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

    bucket_id = (request.POST.get("bucket_id") or _default_bucket()).strip()
    if not bucket_id:
        return JsonResponse(
            {"success": False, "error": "No bucket configured."}, status=400
        )

    try:
        raw_bytes = file.read()
        data = json.loads(raw_bytes.decode("utf-8"))
    except Exception as exc:
        return JsonResponse(
            {"success": False, "error": f"Invalid JSON: {exc}"}, status=400
        )

    if data.get("kind") != "page_spec":
        return JsonResponse(
            {"success": False, "error": 'JSON must have kind "page_spec".'},
            status=400,
        )

    try:
        fields = _parse_page_spec_fields(data)
    except ValueError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=400)

    try:
        client = _s3_client()
        result = client.upload_json(
            bucket_id=bucket_id, file=io.BytesIO(raw_bytes), filename=file.name
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

    operator = request.session.get("operator", {})
    email = operator.get("email", "")

    existing = PageSpec.objects.filter(page_id=fields["page_id"]).first()
    if existing:
        PageSpec.objects.filter(pk=existing.pk).update(
            title=fields["title"],
            page_type=fields["page_type"],
            codebase=fields["codebase"],
            surface=fields["surface"],
            flow_id=fields["flow_id"],
            era_tags=fields["era_tags"],
            route=fields["route"],
            status=fields["status"],
            auth_required=fields["auth_required"],
            purpose=fields["purpose"],
            section_count=fields["section_count"],
            component_count=fields["component_count"],
            endpoint_count=fields["endpoint_count"],
            s3_bucket_id=bucket_id,
            s3_file_key=file_key,
            size_bytes=len(raw_bytes),
            sections_override=[],
            uploaded_by=email,
            updated_at=timezone.now(),
        )
        spec = PageSpec.objects.get(pk=existing.pk)
    else:
        spec = PageSpec.objects.create(
            **fields,
            s3_bucket_id=bucket_id,
            s3_file_key=file_key,
            size_bytes=len(raw_bytes),
            sections_override=[],
            uploaded_by=email,
        )

    jd_key = _json_doc_key_for_page(fields["page_id"])
    JsonDocument.objects.update_or_create(
        key=jd_key,
        defaults={
            "label": f"{fields['title']} (page_spec)",
            "s3_bucket_id": bucket_id,
            "s3_file_key": file_key,
            "size_bytes": len(raw_bytes),
            "content_type": "application/json",
            "tags": "page_spec",
            "uploaded_by": email,
        },
    )

    return JsonResponse(
        {
            "success": True,
            "id": spec.pk,
            "page_id": spec.page_id,
            "title": spec.title,
            "codebase": spec.codebase,
        }
    )


@require_login
@require_http_methods(["GET"])
def editor_view(request, spec_id: int):
    """Section editor shell for one spec. @role: authenticated"""
    spec = get_object_or_404(PageSpec, pk=spec_id)
    return render(
        request,
        "page_builder/editor.html",
        {
            "page_title": f"Edit: {spec.title}",
            "spec": spec,
            "spec_id": spec.pk,
            "s3_enabled": S3STORAGE_ENABLED,
        },
    )


@require_login
@require_http_methods(["GET"])
def page_spec_json_view(request, spec_id: int):
    """JSON API: full page_spec from S3 with optional section overrides. @role: authenticated"""
    spec = get_object_or_404(PageSpec, pk=spec_id)
    try:
        client = _s3_client()
        raw = client.get_object(spec.full_s3_key)
        data = json.loads(raw.decode("utf-8"))
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)
    except Exception as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)

    out = deepcopy(data)
    if (
        spec.sections_override
        and isinstance(spec.sections_override, list)
        and len(spec.sections_override) > 0
    ):
        out["sections"] = spec.sections_override
    return JsonResponse(
        {
            "success": True,
            "spec": out,
            "meta": {
                "id": spec.pk,
                "page_id": spec.page_id,
                "has_override": bool(spec.sections_override),
            },
        }
    )


@require_login
@require_http_methods(["POST"])
def save_sections_view(request, spec_id: int):
    """Persist ``sections_override`` for a spec. @role: authenticated"""
    spec = get_object_or_404(PageSpec, pk=spec_id)
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON body."}, status=400
        )
    sections = payload.get("sections")
    if not isinstance(sections, list):
        return JsonResponse(
            {"success": False, "error": "sections must be a list."}, status=400
        )
    spec.sections_override = sections
    spec.section_count = len(sections)
    spec.save(update_fields=["sections_override", "section_count", "updated_at"])
    return JsonResponse({"success": True, "section_count": spec.section_count})


@require_login
@require_http_methods(["POST"])
def delete_view(request, spec_id: int):
    """
    Delete spec + linked ``JsonDocument``; S3 via gateway or direct API.

    @role: authenticated
    """
    spec = get_object_or_404(PageSpec, pk=spec_id)
    jd_key = _json_doc_key_for_page(spec.page_id)
    gateway_ok = False
    if getattr(settings, "ADMIN_STORAGE_VIA_GATEWAY", False):
        tok = (request.session.get("operator") or {}).get("token")
        if tok:
            try:
                gateway_s3_delete_file(tok, spec.s3_file_key)
                gateway_ok = True
            except Exception as exc:
                logger.warning(
                    "page_builder gateway s3.deleteFile failed, trying direct API: %s",
                    exc,
                )
    if not gateway_ok:
        try:
            client = _s3_client()
            client._request(
                "DELETE", "/api/v1/objects", params={"key": spec.full_s3_key}
            )
        except Exception as exc:
            logger.warning("page_builder delete S3: %s", exc)
    JsonDocument.objects.filter(key=jd_key).delete()
    spec.delete()
    return JsonResponse({"success": True})


@require_login
@require_http_methods(["GET"])
def api_list_view(request):
    """JSON list of page specs (summary fields). @role: authenticated"""
    specs = list(
        PageSpec.objects.values(
            "id",
            "page_id",
            "title",
            "page_type",
            "codebase",
            "surface",
            "route",
            "status",
            "section_count",
            "component_count",
            "endpoint_count",
        )
    )
    return JsonResponse({"success": True, "pages": specs})
