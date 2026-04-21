"""
Pages API v1 — GraphQL-backed (Lambda-parity JSON shapes).

GET handlers are unauthenticated at the Django layer (optional ``get_adapter`` session token).
Convention: ``@role: public`` for these read-only JSON routes.
"""

from __future__ import annotations

import logging

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from apps.documentation.constants import PAGE_TYPES, VALID_USER_TYPES
from apps.documentation.services.docs_graphql_adapter import get_adapter
from apps.documentation.utils.api_v1_helpers import (
    should_expand_full,
    to_page_list_item,
)

logger = logging.getLogger(__name__)


def _svc(request: HttpRequest):
    return get_adapter(request)


@require_http_methods(["GET"])
def pages_list(request: HttpRequest) -> JsonResponse:
    try:
        service = _svc(request)
        page_type = request.GET.get("page_type")
        include_drafts = request.GET.get("include_drafts", "true").lower() == "true"
        include_deleted = request.GET.get("include_deleted", "false").lower() == "true"
        status_filter = request.GET.get("status")
        limit = request.GET.get("limit")
        offset = int(request.GET.get("offset", 0))
        if limit is not None:
            limit = int(limit)
        result = service.list_pages(
            page_type=page_type,
            include_drafts=include_drafts,
            include_deleted=include_deleted,
            status=status_filter,
            limit=limit,
            offset=offset,
        )
        pages = result.get("pages", [])
        if not should_expand_full(request.GET):
            pages = [to_page_list_item(p) for p in pages]
        return JsonResponse({"pages": pages, "total": result.get("total", 0)})
    except Exception as e:
        logger.exception("pages list failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_docs(request: HttpRequest) -> JsonResponse:
    try:
        result = _svc(request).list_pages(page_type="docs", limit=None, offset=0)
        return JsonResponse(
            {"pages": result.get("pages", []), "total": result.get("total", 0)}
        )
    except Exception as e:
        logger.exception("pages by-type docs failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_marketing(request: HttpRequest) -> JsonResponse:
    try:
        result = _svc(request).list_pages(page_type="marketing", limit=None, offset=0)
        return JsonResponse(
            {"pages": result.get("pages", []), "total": result.get("total", 0)}
        )
    except Exception as e:
        logger.exception("pages by-type marketing failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_dashboard(request: HttpRequest) -> JsonResponse:
    try:
        result = _svc(request).list_pages(page_type="dashboard", limit=None, offset=0)
        return JsonResponse(
            {"pages": result.get("pages", []), "total": result.get("total", 0)}
        )
    except Exception as e:
        logger.exception("pages by-type dashboard failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_product(request: HttpRequest) -> JsonResponse:
    try:
        result = _svc(request).list_pages(page_type="product", limit=None, offset=0)
        return JsonResponse(
            {"pages": result.get("pages", []), "total": result.get("total", 0)}
        )
    except Exception as e:
        logger.exception("pages by-type product failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_title(request: HttpRequest) -> JsonResponse:
    try:
        result = _svc(request).list_pages(page_type="title", limit=None, offset=0)
        return JsonResponse(
            {"pages": result.get("pages", []), "total": result.get("total", 0)}
        )
    except Exception as e:
        logger.exception("pages by-type title failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_count(request: HttpRequest, page_type: str) -> JsonResponse:
    try:
        count = _svc(request).count_pages_by_type(page_type)
        return JsonResponse({"page_type": page_type, "count": count})
    except Exception as e:
        logger.exception("pages by-type count failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_published(request: HttpRequest, page_type: str) -> JsonResponse:
    try:
        result = _svc(request).list_pages(
            page_type=page_type,
            include_drafts=False,
            include_deleted=False,
            page_state="published",
            limit=None,
            offset=0,
        )
        return JsonResponse(
            {"pages": result.get("pages", []), "total": result.get("total", 0)}
        )
    except Exception as e:
        logger.exception("pages by-type published failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_draft(request: HttpRequest, page_type: str) -> JsonResponse:
    try:
        result = _svc(request).list_pages(
            page_type=page_type,
            include_drafts=True,
            include_deleted=False,
            page_state="draft",
            limit=None,
            offset=0,
        )
        return JsonResponse(
            {"pages": result.get("pages", []), "total": result.get("total", 0)}
        )
    except Exception as e:
        logger.exception("pages by-type draft failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_type_stats(request: HttpRequest, page_type: str) -> JsonResponse:
    try:
        count = _svc(request).count_pages_by_type(page_type)
        return JsonResponse(
            {
                "page_type": page_type,
                "total": count,
                "published": 0,
                "draft": 0,
                "deleted": 0,
                "last_updated": None,
            }
        )
    except Exception as e:
        logger.exception("pages by-type stats failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_state_list(request: HttpRequest, state: str) -> JsonResponse:
    try:
        result = _svc(request).list_pages(page_state=state, limit=None, offset=0)
        return JsonResponse(
            {"pages": result.get("pages", []), "total": result.get("total", 0)}
        )
    except Exception as e:
        logger.exception("pages by-state list failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_state_count(request: HttpRequest, state: str) -> JsonResponse:
    try:
        result = _svc(request).list_pages(page_state=state, limit=None, offset=0)
        return JsonResponse({"state": state, "count": result.get("total", 0)})
    except Exception as e:
        logger.exception("pages by-state count failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_by_user_type_or_page_detail(
    request: HttpRequest, segment: str
) -> JsonResponse:
    if segment in VALID_USER_TYPES:
        try:
            service = _svc(request)
            page_type = request.GET.get("page_type")
            include_drafts = request.GET.get("include_drafts", "true").lower() == "true"
            include_deleted = (
                request.GET.get("include_deleted", "false").lower() == "true"
            )
            status_filter = request.GET.get("status")
            result = service.list_pages_by_user_type(
                user_type=segment,
                page_type=page_type,
                include_drafts=include_drafts,
                include_deleted=include_deleted,
                status=status_filter,
            )
            return JsonResponse(
                {"pages": result.get("pages", []), "total": result.get("total", 0)}
            )
        except ValueError as e:
            return JsonResponse({"detail": str(e)}, status=400)
        except Exception as e:
            logger.exception("pages by user_type failed")
            return JsonResponse({"detail": str(e)}, status=500)
    try:
        service = _svc(request)
        page_type = request.GET.get("page_type")
        page = service.get_page(segment, page_type=page_type)
        if not page:
            return JsonResponse(
                {"detail": f"Documentation page '{segment}' not found"}, status=404
            )
        return JsonResponse(page)
    except Exception as e:
        logger.exception("pages detail failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_detail_access_control(request: HttpRequest, page_id: str) -> JsonResponse:
    try:
        page = _svc(request).get_page(page_id)
        if not page:
            return JsonResponse({"detail": f"Page '{page_id}' not found"}, status=404)
        ac = page.get("access_control")
        return JsonResponse({"page_id": page_id, "access_control": ac})
    except Exception as e:
        logger.exception("pages detail access control failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_detail_sections(request: HttpRequest, page_id: str) -> JsonResponse:
    try:
        page = _svc(request).get_page(page_id)
        if not page:
            return JsonResponse({"detail": f"Page '{page_id}' not found"}, status=404)
        sections = page.get("sections") or (page.get("metadata") or {}).get(
            "content_sections"
        )
        return JsonResponse({"page_id": page_id, "sections": sections})
    except Exception as e:
        logger.exception("pages detail sections failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_detail_components(request: HttpRequest, page_id: str) -> JsonResponse:
    try:
        page = _svc(request).get_page(page_id)
        if not page:
            return JsonResponse({"detail": f"Page '{page_id}' not found"}, status=404)
        sections = page.get("sections") or {}
        components = (
            sections.get("components", []) if isinstance(sections, dict) else []
        )
        ui_components = (page.get("metadata") or {}).get("ui_components", [])
        return JsonResponse(
            {
                "page_id": page_id,
                "components": components,
                "ui_components": ui_components,
                "total": len(components) + len(ui_components),
            }
        )
    except Exception as e:
        logger.exception("pages detail components failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_detail_endpoints(request: HttpRequest, page_id: str) -> JsonResponse:
    try:
        page = _svc(request).get_page(page_id)
        if not page:
            return JsonResponse({"detail": f"Page '{page_id}' not found"}, status=404)
        metadata_endpoints = (page.get("metadata") or {}).get("uses_endpoints", [])
        return JsonResponse(
            {
                "page_id": page_id,
                "section_endpoints": [],
                "metadata_endpoints": metadata_endpoints,
                "total": len(metadata_endpoints),
            }
        )
    except Exception as e:
        logger.exception("pages detail endpoints failed")
        return JsonResponse({"detail": str(e)}, status=500)


@require_http_methods(["GET"])
def pages_detail_versions(request: HttpRequest, page_id: str) -> JsonResponse:
    try:
        page = _svc(request).get_page(page_id)
        if not page:
            return JsonResponse({"detail": f"Page '{page_id}' not found"}, status=404)
        versions = (page.get("metadata") or {}).get("versions")
        v = versions or []
        return JsonResponse({"page_id": page_id, "versions": v, "count": len(v)})
    except Exception as e:
        logger.exception("pages detail versions failed")
        return JsonResponse({"detail": str(e)}, status=500)
