"""Documentation Dashboard - Pages resource views."""
from __future__ import annotations

import json
import logging
from typing import Any, Dict

from django.http import HttpRequest, HttpResponse, Http404
from apps.core.decorators.auth import require_super_admin

from apps.documentation.constants import PAGE_TYPES
from apps.documentation.services import get_pages_service
from apps.documentation.views.dashboard_views_common import render_resource_view as _render_resource_view

logger = logging.getLogger(__name__)


@require_super_admin
def media_manager_page_detail(request: HttpRequest, page_id: str) -> HttpResponse:
    """
    Media Manager Dashboard - Page detail view.

    GET /docs/media-manager/pages/<page_id>/
    """
    try:
        pages_service = get_pages_service()
        page = pages_service.get_page(page_id)

        if not page:
            raise Http404(f"Page not found: {page_id}")

        # Get related data
        page_sections = pages_service.get_page_sections(page_id)
        page_components = pages_service.get_page_components(page_id)
        page_endpoints = pages_service.get_page_endpoints(page_id)
        page_versions = pages_service.get_page_versions(page_id)
        access_control = pages_service.get_page_access_control(page_id)

        context: Dict[str, Any] = {
            'page': page,
            'page_sections': page_sections,
            'page_components': page_components,
            'page_endpoints': page_endpoints,
            'page_versions': page_versions,
            'access_control': access_control,
        }

        return _render_resource_view(request, 'page_detail.html', context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading page detail {page_id}: {e}", exc_info=True)
        raise Http404(f"Error loading page: {page_id}")


@require_super_admin
def media_manager_pages_format(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Pages format examples view.

    GET /docs/pages/format/
    Mirrors: GET /api/v1/pages/format/
    """
    try:
        from apps.documentation.api.v1.pages_views import pages_format as api_pages_format

        # Call the API function to get format data
        json_response = api_pages_format(request)
        format_data = json.loads(json_response.content)

        # Format examples for display
        examples = None
        if 'examples' in format_data:
            examples = json.dumps(format_data['examples'], indent=2)

        analyse_payload_example = None
        if 'analyse_payload_example' in format_data:
            analyse_payload_example = json.dumps(format_data['analyse_payload_example'], indent=2)

        context: Dict[str, Any] = {
            'format_data': format_data,
            'examples': examples,
            'analyse_payload_example': analyse_payload_example,
        }

        return _render_resource_view(request, 'pages_format.html', context)

    except Exception as e:
        logger.error(f"Error loading pages format: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_format.html',
            {'format_data': {}, 'examples': None, 'analyse_payload_example': None, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_types(request: HttpRequest) -> HttpResponse:
    """
    Media Manager Dashboard - Pages types view.

    GET /docs/media-manager/pages/types/
    Mirrors: GET /api/v1/pages/types/
    """
    try:
        pages_service = get_pages_service()
        types_data = []
        for pt in PAGE_TYPES:
            count = pages_service.count_pages_by_type(pt)
            types_data.append({"type": pt, "count": count})
        total = sum(t["count"] for t in types_data)

        context: Dict[str, Any] = {
            'types': types_data,
            'total': total,
        }

        return _render_resource_view(request, 'pages_types.html', context)

    except Exception as e:
        logger.error(f"Error loading pages types: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_types.html',
            {'types': [], 'total': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_docs(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/docs/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(page_type="docs", limit=None, offset=0)

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'page_type': 'docs',
            'filters': {'page_type': 'docs'},
        }

        return _render_resource_view(request, 'pages_by_type.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type docs: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_type.html',
            {'pages': [], 'total': 0, 'page_type': 'docs', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_marketing(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/marketing/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(page_type="marketing", limit=None, offset=0)

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'page_type': 'marketing',
            'filters': {'page_type': 'marketing'},
        }

        return _render_resource_view(request, 'pages_by_type.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type marketing: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_type.html',
            {'pages': [], 'total': 0, 'page_type': 'marketing', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_dashboard(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/dashboard/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(page_type="dashboard", limit=None, offset=0)

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'page_type': 'dashboard',
            'filters': {'page_type': 'dashboard'},
        }

        return _render_resource_view(request, 'pages_by_type.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type dashboard: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_type.html',
            {'pages': [], 'total': 0, 'page_type': 'dashboard', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_product(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/product/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(page_type="product", limit=None, offset=0)

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'page_type': 'product',
            'filters': {'page_type': 'product'},
        }

        return _render_resource_view(request, 'pages_by_type.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type product: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_type.html',
            {'pages': [], 'total': 0, 'page_type': 'product', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_title(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/title/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(page_type="title", limit=None, offset=0)

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'page_type': 'title',
            'filters': {'page_type': 'title'},
        }

        return _render_resource_view(request, 'pages_by_type.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type title: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_type.html',
            {'pages': [], 'total': 0, 'page_type': 'title', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type(request: HttpRequest, page_type: str) -> HttpResponse:
    """GET /docs/pages/by-type/<page_type>/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(page_type=page_type, limit=None, offset=0)

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'page_type': page_type,
            'filters': {'page_type': page_type},
        }

        return _render_resource_view(request, 'pages_by_type.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type {page_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_type.html',
            {'pages': [], 'total': 0, 'page_type': page_type, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_count(request: HttpRequest, page_type: str) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/<page_type>/count/"""
    try:
        pages_service = get_pages_service()
        count = pages_service.count_pages_by_type(page_type)

        context: Dict[str, Any] = {
            'page_type': page_type,
            'count': count,
        }

        return _render_resource_view(request, 'pages_count.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type count for {page_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_count.html',
            {'page_type': page_type, 'count': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_published(request: HttpRequest, page_type: str) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/<page_type>/published/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(
            page_type=page_type,
            include_drafts=False,
            include_deleted=False,
            page_state="published",
            limit=None,
            offset=0
        )

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'page_type': page_type,
            'state': 'published',
            'filters': {'page_type': page_type, 'state': 'published'},
        }

        return _render_resource_view(request, 'pages_by_type.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type published for {page_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_type.html',
            {'pages': [], 'total': 0, 'page_type': page_type, 'state': 'published', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_draft(request: HttpRequest, page_type: str) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/<page_type>/draft/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(
            page_type=page_type,
            include_drafts=True,
            include_deleted=False,
            page_state="draft",
            limit=None,
            offset=0
        )

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'page_type': page_type,
            'state': 'draft',
            'filters': {'page_type': page_type, 'state': 'draft'},
        }

        return _render_resource_view(request, 'pages_by_type.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type draft for {page_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_type.html',
            {'pages': [], 'total': 0, 'page_type': page_type, 'state': 'draft', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_type_stats(request: HttpRequest, page_type: str) -> HttpResponse:
    """GET /docs/media-manager/pages/by-type/<page_type>/stats/"""
    try:
        pages_service = get_pages_service()
        stats = pages_service.get_type_statistics()
        statistics = stats.get("statistics", [])
        type_stats = next((s for s in statistics if s.get("type") == page_type), {})

        from apps.documentation.services import get_shared_s3_index_manager
        index_manager = get_shared_s3_index_manager()
        index_data = index_manager.read_index("pages")

        context: Dict[str, Any] = {
            'page_type': page_type,
            'total': type_stats.get("count", 0),
            'published': type_stats.get("published", 0),
            'draft': type_stats.get("draft", 0),
            'deleted': type_stats.get("deleted", 0),
            'last_updated': index_data.get("last_updated"),
        }

        return _render_resource_view(request, 'pages_stats.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by type stats for {page_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_stats.html',
            {'page_type': page_type, 'total': 0, 'published': 0, 'draft': 0, 'deleted': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_state(request: HttpRequest, state: str) -> HttpResponse:
    """GET /docs/media-manager/pages/by-state/<state>/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(page_state=state, limit=None, offset=0)

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'state': state,
            'filters': {'state': state},
        }

        return _render_resource_view(request, 'pages_by_state.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by state {state}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_state.html',
            {'pages': [], 'total': 0, 'state': state, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_state_count(request: HttpRequest, state: str) -> HttpResponse:
    """GET /docs/media-manager/pages/by-state/<state>/count/"""
    try:
        pages_service = get_pages_service()
        result = pages_service.list_pages(page_state=state, limit=None, offset=0)
        count = result.get("total", 0)

        context: Dict[str, Any] = {
            'state': state,
            'count': count,
        }

        return _render_resource_view(request, 'pages_count.html', context)

    except Exception as e:
        logger.error(f"Error loading pages by state count for {state}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_count.html',
            {'state': state, 'count': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_pages_by_user_type(request: HttpRequest, user_type: str) -> HttpResponse:
    """GET /docs/media-manager/pages/by-user-type/<user_type>/"""
    try:
        pages_service = get_pages_service()
        page_type = request.GET.get("page_type")
        include_drafts = request.GET.get("include_drafts", "true").lower() == "true"
        include_deleted = request.GET.get("include_deleted", "false").lower() == "true"
        status_filter = request.GET.get("status")

        result = pages_service.list_pages_by_user_type(
            user_type=user_type,
            page_type=page_type,
            include_drafts=include_drafts,
            include_deleted=include_deleted,
            status=status_filter,
        )

        context: Dict[str, Any] = {
            'pages': result.get("pages", []),
            'total': result.get("total", 0),
            'user_type': user_type,
            'filters': {'user_type': user_type},
        }

        return _render_resource_view(request, 'pages_by_user_type.html', context)

    except ValueError as e:
        logger.error(f"Invalid user type {user_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_user_type.html',
            {'pages': [], 'total': 0, 'user_type': user_type, 'error': str(e)},
            error_message=str(e)
        )
    except Exception as e:
        logger.error(f"Error loading pages by user type {user_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'pages_by_user_type.html',
            {'pages': [], 'total': 0, 'user_type': user_type, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_page_sections(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/pages/<page_id>/sections/"""
    try:
        pages_service = get_pages_service()
        page = pages_service.get_page(page_id)

        if not page:
            raise Http404(f"Page not found: {page_id}")

        sections = pages_service.get_page_sections(page_id)

        context: Dict[str, Any] = {
            'page': page,
            'page_id': page_id,
            'sections': sections,
        }

        return _render_resource_view(request, 'page_sections.html', context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading page sections for {page_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'page_sections.html',
            {'page_id': page_id, 'sections': None, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_page_components(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/pages/<page_id>/components/"""
    try:
        pages_service = get_pages_service()
        page = pages_service.get_page(page_id)

        if not page:
            raise Http404(f"Page not found: {page_id}")

        components = pages_service.get_page_components(page_id)
        # Also get components from sections
        sections = page.get("sections", {})
        section_components = sections.get("components", []) if sections else []

        context: Dict[str, Any] = {
            'page': page,
            'page_id': page_id,
            'components': section_components,
            'ui_components': components or [],
            'total': len(section_components) + len(components or []),
        }

        return _render_resource_view(request, 'page_components.html', context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading page components for {page_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'page_components.html',
            {'page_id': page_id, 'components': [], 'ui_components': [], 'total': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_page_endpoints(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/pages/<page_id>/endpoints/"""
    try:
        pages_service = get_pages_service()
        page = pages_service.get_page(page_id)

        if not page:
            raise Http404(f"Page not found: {page_id}")

        endpoints = pages_service.get_page_endpoints(page_id)

        context: Dict[str, Any] = {
            'page': page,
            'page_id': page_id,
            'section_endpoints': [],
            'metadata_endpoints': endpoints or [],
            'total': len(endpoints or []),
        }

        return _render_resource_view(request, 'page_endpoints.html', context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading page endpoints for {page_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'page_endpoints.html',
            {'page_id': page_id, 'section_endpoints': [], 'metadata_endpoints': [], 'total': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_page_versions(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/pages/<page_id>/versions/"""
    try:
        pages_service = get_pages_service()
        page = pages_service.get_page(page_id)

        if not page:
            raise Http404(f"Page not found: {page_id}")

        versions = pages_service.get_page_versions(page_id)

        context: Dict[str, Any] = {
            'page': page,
            'page_id': page_id,
            'versions': versions or [],
            'count': len(versions or []),
        }

        return _render_resource_view(request, 'page_versions.html', context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading page versions for {page_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'page_versions.html',
            {'page_id': page_id, 'versions': [], 'count': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_page_access_control(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/pages/<page_id>/access-control/"""
    try:
        pages_service = get_pages_service()
        page = pages_service.get_page(page_id)

        if not page:
            raise Http404(f"Page not found: {page_id}")

        access_control = pages_service.get_page_access_control(page_id)

        context: Dict[str, Any] = {
            'page': page,
            'page_id': page_id,
            'access_control': access_control,
        }

        return _render_resource_view(request, 'page_access_control.html', context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading page access control for {page_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'page_access_control.html',
            {'page_id': page_id, 'access_control': None, 'error': str(e)},
            error_message=str(e)
        )
