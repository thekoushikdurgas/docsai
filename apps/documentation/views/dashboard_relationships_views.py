"""Documentation Dashboard - Relationships resource views."""
from __future__ import annotations

import json
import logging
from typing import Any, Dict

from django.http import HttpRequest, HttpResponse, Http404
from apps.core.decorators.auth import require_super_admin

from apps.documentation.services import get_relationships_service
from apps.documentation.views.dashboard_views_common import render_resource_view as _render_resource_view

logger = logging.getLogger(__name__)


@require_super_admin
def media_manager_relationship_detail(request: HttpRequest, relationship_id: str) -> HttpResponse:
    """
    Media Manager Dashboard - Relationship detail view.

    GET /docs/media-manager/relationships/<relationship_id>/
    """
    try:
        relationships_service = get_relationships_service()
        relationship = relationships_service.get_relationship(relationship_id)

        if not relationship:
            raise Http404(f"Relationship not found: {relationship_id}")

        # Get related data
        access_control = relationships_service.get_relationship_access_control(relationship_id)
        data_flow = relationships_service.get_relationship_data_flow(relationship_id)
        performance = relationships_service.get_relationship_performance(relationship_id)
        dependencies = relationships_service.get_relationship_dependencies(relationship_id)
        postman_config = relationships_service.get_relationship_postman(relationship_id)

        context: Dict[str, Any] = {
            'relationship': relationship,
            'access_control': access_control,
            'data_flow': data_flow,
            'performance': performance,
            'dependencies': dependencies or [],
            'postman_config': postman_config,
        }

        return _render_resource_view(request, 'relationship_detail.html', context)

    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading relationship detail {relationship_id}: {e}", exc_info=True)
        raise Http404(f"Error loading relationship: {relationship_id}")


@require_super_admin
def media_manager_relationships_statistics(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/statistics/"""
    try:
        relationships_service = get_relationships_service()
        stats = relationships_service.get_statistics()

        context: Dict[str, Any] = {
            'statistics': stats,
        }

        return _render_resource_view(request, 'relationships_statistics.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships statistics: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_statistics.html',
            {'statistics': {}, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_format(request: HttpRequest) -> HttpResponse:
    """GET /docs/relationships/format/"""
    try:
        from apps.documentation.api.v1.relationships_views import relationships_format as api_relationships_format

        json_response = api_relationships_format(request)
        format_data = json.loads(json_response.content)

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

        return _render_resource_view(request, 'relationships_format.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships format: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_format.html',
            {'format_data': {}, 'examples': None, 'analyse_payload_example': None, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_graph(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/graph/"""
    try:
        relationships_service = get_relationships_service()
        graph = relationships_service.get_graph()

        context: Dict[str, Any] = {
            'graph': graph,
            'nodes': graph.get("nodes", []),
            'edges': graph.get("edges", []),
        }

        return _render_resource_view(request, 'relationships_graph.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships graph: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_graph.html',
            {'graph': {}, 'nodes': [], 'edges': [], 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_usage_types(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/usage-types/"""
    try:
        relationships_service = get_relationships_service()
        stats = relationships_service.get_statistics()
        by_ut = stats.get("by_usage_type", {})
        types_data = [{"usage_type": k, "count": v} for k, v in by_ut.items()]

        context: Dict[str, Any] = {
            'usage_types': types_data,
            'total': sum(v for v in by_ut.values()),
        }

        return _render_resource_view(request, 'relationships_usage_types.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships usage types: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_usage_types.html',
            {'usage_types': [], 'total': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_usage_contexts(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/usage-contexts/"""
    try:
        relationships_service = get_relationships_service()
        stats = relationships_service.get_statistics()
        by_uc = stats.get("by_usage_context", {})
        ctx_data = [{"usage_context": k, "count": v} for k, v in by_uc.items()]

        context: Dict[str, Any] = {
            'usage_contexts': ctx_data,
            'total': sum(v for v in by_uc.values()),
        }

        return _render_resource_view(request, 'relationships_usage_contexts.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships usage contexts: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_usage_contexts.html',
            {'usage_contexts': [], 'total': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_page(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-page/<page_id>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(page_id=page_id, limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'page_id': page_id,
            'filters': {'page_id': page_id},
        }

        return _render_resource_view(request, 'relationships_by_page.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by page {page_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_page.html',
            {'relationships': [], 'total': 0, 'page_id': page_id, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_page_count(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-page/<page_id>/count/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(page_id=page_id, limit=None, offset=0)
        count = result.get("total", 0)

        context: Dict[str, Any] = {
            'page_id': page_id,
            'count': count,
        }

        return _render_resource_view(request, 'relationships_count.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by page count for {page_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_count.html',
            {'page_id': page_id, 'count': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_page_primary(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-page/<page_id>/primary/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(page_id=page_id, usage_type="primary", limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'page_id': page_id,
            'usage_type': 'primary',
            'filters': {'page_id': page_id, 'usage_type': 'primary'},
        }

        return _render_resource_view(request, 'relationships_by_page.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by page {page_id} primary: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_page.html',
            {'relationships': [], 'total': 0, 'page_id': page_id, 'usage_type': 'primary', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_page_secondary(request: HttpRequest, page_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-page/<page_id>/secondary/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(page_id=page_id, usage_type="secondary", limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'page_id': page_id,
            'usage_type': 'secondary',
            'filters': {'page_id': page_id, 'usage_type': 'secondary'},
        }

        return _render_resource_view(request, 'relationships_by_page.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by page {page_id} secondary: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_page.html',
            {'relationships': [], 'total': 0, 'page_id': page_id, 'usage_type': 'secondary', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_page_by_usage_type(
    request: HttpRequest, page_id: str, usage_type: str
) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-page/<page_id>/by-usage-type/<usage_type>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(page_id=page_id, usage_type=usage_type, limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'page_id': page_id,
            'usage_type': usage_type,
            'filters': {'page_id': page_id, 'usage_type': usage_type},
        }

        return _render_resource_view(request, 'relationships_by_page.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by page {page_id} and usage type {usage_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_page.html',
            {'relationships': [], 'total': 0, 'page_id': page_id, 'usage_type': usage_type, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_endpoint(request: HttpRequest, endpoint_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-endpoint/<endpoint_id>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(endpoint_id=endpoint_id, limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'endpoint_id': endpoint_id,
            'filters': {'endpoint_id': endpoint_id},
        }

        return _render_resource_view(request, 'relationships_by_endpoint.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by endpoint {endpoint_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_endpoint.html',
            {'relationships': [], 'total': 0, 'endpoint_id': endpoint_id, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_endpoint_count(request: HttpRequest, endpoint_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-endpoint/<endpoint_id>/count/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(endpoint_id=endpoint_id, limit=None, offset=0)
        count = result.get("total", 0)

        context: Dict[str, Any] = {
            'endpoint_id': endpoint_id,
            'count': count,
        }

        return _render_resource_view(request, 'relationships_count.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by endpoint count for {endpoint_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_count.html',
            {'endpoint_id': endpoint_id, 'count': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_endpoint_pages(request: HttpRequest, endpoint_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-endpoint/<endpoint_id>/pages/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(endpoint_id=endpoint_id, limit=None, offset=0)
        rels = result.get("relationships", [])
        pages = []
        for rel in rels:
            if rel.get("page_path"):
                pages.append({"page_path": rel.get("page_path"), "page_title": rel.get("page_title", "")})

        context: Dict[str, Any] = {
            'endpoint_id': endpoint_id,
            'pages': pages,
            'count': len(pages),
        }

        return _render_resource_view(request, 'relationships_by_endpoint_pages.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by endpoint pages for {endpoint_id}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_endpoint_pages.html',
            {'endpoint_id': endpoint_id, 'pages': [], 'count': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_endpoint_by_usage_context(
    request: HttpRequest, endpoint_id: str, usage_context: str
) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-endpoint/<endpoint_id>/by-usage-context/<usage_context>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(endpoint_id=endpoint_id, usage_context=usage_context, limit=None, offset=0)
        rels = result.get("relationships", [])

        context: Dict[str, Any] = {
            'endpoint_id': endpoint_id,
            'usage_context': usage_context,
            'relationships': rels,
            'count': len(rels),
            'filters': {'endpoint_id': endpoint_id, 'usage_context': usage_context},
        }

        return _render_resource_view(request, 'relationships_by_endpoint.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by endpoint {endpoint_id} and usage context {usage_context}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_endpoint.html',
            {'relationships': [], 'count': 0, 'endpoint_id': endpoint_id, 'usage_context': usage_context, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_usage_type(request: HttpRequest, usage_type: str) -> HttpResponse:
    """GET /docs/relationships/by-usage-type/<usage_type>/"""
    try:
        relationships_service = get_relationships_service()
        relationships = relationships_service.get_relationships_by_usage_type(usage_type)

        context: Dict[str, Any] = {
            'relationships': relationships,
            'total': len(relationships) if isinstance(relationships, list) else relationships.get("total", 0),
            'usage_type': usage_type,
            'filters': {'usage_type': usage_type},
        }

        return _render_resource_view(request, 'relationships_by_usage_type.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by usage type {usage_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_usage_type.html',
            {'relationships': [], 'total': 0, 'usage_type': usage_type, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_usage_type_primary(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-type/primary/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_type="primary", limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_type': 'primary',
            'filters': {'usage_type': 'primary'},
        }

        return _render_resource_view(request, 'relationships_by_usage_type.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by usage type primary: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_usage_type.html',
            {'relationships': [], 'total': 0, 'usage_type': 'primary', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_usage_type_secondary(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-type/secondary/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_type="secondary", limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_type': 'secondary',
            'filters': {'usage_type': 'secondary'},
        }

        return _render_resource_view(request, 'relationships_by_usage_type.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by usage type secondary: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_usage_type.html',
            {'relationships': [], 'total': 0, 'usage_type': 'secondary', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_usage_type_conditional(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-type/conditional/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_type="conditional", limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_type': 'conditional',
            'filters': {'usage_type': 'conditional'},
        }

        return _render_resource_view(request, 'relationships_by_usage_type.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by usage type conditional: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_usage_type.html',
            {'relationships': [], 'total': 0, 'usage_type': 'conditional', 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_usage_type_count(request: HttpRequest, usage_type: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-type/<usage_type>/count/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_type=usage_type, limit=None, offset=0)
        count = result.get("total", 0)

        context: Dict[str, Any] = {
            'usage_type': usage_type,
            'count': count,
        }

        return _render_resource_view(request, 'relationships_count.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by usage type count for {usage_type}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_count.html',
            {'usage_type': usage_type, 'count': 0, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_usage_type_by_usage_context(
    request: HttpRequest, usage_type: str, usage_context: str
) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-type/<usage_type>/by-usage-context/<usage_context>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_type=usage_type, usage_context=usage_context, limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_type': usage_type,
            'usage_context': usage_context,
            'filters': {'usage_type': usage_type, 'usage_context': usage_context},
        }

        return _render_resource_view(request, 'relationships_by_usage_type.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by usage type {usage_type} and usage context {usage_context}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_usage_type.html',
            {'relationships': [], 'total': 0, 'usage_type': usage_type, 'usage_context': usage_context, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_usage_context(request: HttpRequest, usage_context: str) -> HttpResponse:
    """GET /docs/relationships/by-usage-context/<usage_context>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_context=usage_context, limit=None, offset=0)

        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_context': usage_context,
            'filters': {'usage_context': usage_context},
        }

        return _render_resource_view(request, 'relationships_by_usage_context.html', context)

    except Exception as e:
        logger.error(f"Error loading relationships by usage context {usage_context}: {e}", exc_info=True)
        return _render_resource_view(
            request,
            'relationships_by_usage_context.html',
            {'relationships': [], 'total': 0, 'usage_context': usage_context, 'error': str(e)},
            error_message=str(e)
        )


@require_super_admin
def media_manager_relationships_by_usage_context_data_fetching(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-context/data_fetching/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_context="data_fetching", limit=None, offset=0)
        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_context': 'data_fetching',
            'filters': {'usage_context': 'data_fetching'},
        }
        return _render_resource_view(request, 'relationships_by_usage_context.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by usage context data_fetching: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_by_usage_context.html', {'relationships': [], 'total': 0, 'usage_context': 'data_fetching', 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_usage_context_data_mutation(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-context/data_mutation/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_context="data_mutation", limit=None, offset=0)
        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_context': 'data_mutation',
            'filters': {'usage_context': 'data_mutation'},
        }
        return _render_resource_view(request, 'relationships_by_usage_context.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by usage context data_mutation: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_by_usage_context.html', {'relationships': [], 'total': 0, 'usage_context': 'data_mutation', 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_usage_context_authentication(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-context/authentication/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_context="authentication", limit=None, offset=0)
        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_context': 'authentication',
            'filters': {'usage_context': 'authentication'},
        }
        return _render_resource_view(request, 'relationships_by_usage_context.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by usage context authentication: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_by_usage_context.html', {'relationships': [], 'total': 0, 'usage_context': 'authentication', 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_usage_context_analytics(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-context/analytics/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_context="analytics", limit=None, offset=0)
        context: Dict[str, Any] = {
            'relationships': result.get("relationships", []),
            'total': result.get("total", 0),
            'usage_context': 'analytics',
            'filters': {'usage_context': 'analytics'},
        }
        return _render_resource_view(request, 'relationships_by_usage_context.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by usage context analytics: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_by_usage_context.html', {'relationships': [], 'total': 0, 'usage_context': 'analytics', 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_usage_context_count(request: HttpRequest, usage_context: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-usage-context/<usage_context>/count/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(usage_context=usage_context, limit=None, offset=0)
        context: Dict[str, Any] = {'usage_context': usage_context, 'count': result.get("total", 0)}
        return _render_resource_view(request, 'relationships_count.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by usage context count for {usage_context}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_count.html', {'usage_context': usage_context, 'count': 0, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_state(request: HttpRequest, state: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-state/<state>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(limit=None, offset=0)
        rels = [x for x in (result.get("relationships") or []) if (x.get("state") or x.get("relationship_state")) == state]
        context: Dict[str, Any] = {'relationships': rels, 'total': len(rels), 'state': state, 'filters': {'state': state}}
        return _render_resource_view(request, 'relationships_by_state.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by state {state}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_by_state.html', {'relationships': [], 'total': 0, 'state': state, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_state_count(request: HttpRequest, state: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-state/<state>/count/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(limit=None, offset=0)
        rels = [x for x in (result.get("relationships") or []) if (x.get("state") or x.get("relationship_state")) == state]
        context: Dict[str, Any] = {'state': state, 'count': len(rels)}
        return _render_resource_view(request, 'relationships_count.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by state count for {state}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_count.html', {'state': state, 'count': 0, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_lambda(request: HttpRequest, service_name: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-lambda/<service_name>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(limit=None, offset=0)
        rels = [x for x in (result.get("relationships") or []) if (x.get("lambda_service") or x.get("via_service")) == service_name]
        context: Dict[str, Any] = {'relationships': rels, 'total': len(rels), 'service_name': service_name, 'filters': {'lambda_service': service_name}}
        return _render_resource_view(request, 'relationships_by_lambda.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by lambda {service_name}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_by_lambda.html', {'relationships': [], 'total': 0, 'service_name': service_name, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_invocation_pattern(request: HttpRequest, pattern: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-invocation-pattern/<pattern>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(limit=None, offset=0)
        rels = [x for x in (result.get("relationships") or []) if pattern in str(x.get("via_hook", "")) or pattern in str(x.get("via_service", ""))]
        context: Dict[str, Any] = {'relationships': rels, 'total': len(rels), 'pattern': pattern, 'filters': {'pattern': pattern}}
        return _render_resource_view(request, 'relationships_by_invocation_pattern.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by invocation pattern {pattern}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_by_invocation_pattern.html', {'relationships': [], 'total': 0, 'pattern': pattern, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_by_postman_config(request: HttpRequest, config_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/by-postman-config/<config_id>/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(limit=None, offset=0)
        rels = [x for x in (result.get("relationships") or []) if x.get("postman_config_id") == config_id]
        context: Dict[str, Any] = {'relationships': rels, 'total': len(rels), 'config_id': config_id, 'filters': {'postman_config_id': config_id}}
        return _render_resource_view(request, 'relationships_by_postman_config.html', context)
    except Exception as e:
        logger.error(f"Error loading relationships by postman config {config_id}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_by_postman_config.html', {'relationships': [], 'total': 0, 'config_id': config_id, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_performance_slow(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/performance/slow/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(limit=None, offset=0)
        rels = [x for x in (result.get("relationships") or []) if (x.get("performance") or {}).get("slow")]
        context: Dict[str, Any] = {'relationships': rels, 'total': len(rels), 'performance_type': 'slow'}
        return _render_resource_view(request, 'relationships_performance.html', context)
    except Exception as e:
        logger.error(f"Error loading slow performance relationships: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_performance.html', {'relationships': [], 'total': 0, 'performance_type': 'slow', 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationships_performance_errors(request: HttpRequest) -> HttpResponse:
    """GET /docs/media-manager/relationships/performance/errors/"""
    try:
        relationships_service = get_relationships_service()
        result = relationships_service.list_relationships(limit=None, offset=0)
        rels = [x for x in (result.get("relationships") or []) if (x.get("performance") or {}).get("errors")]
        context: Dict[str, Any] = {'relationships': rels, 'total': len(rels), 'performance_type': 'errors'}
        return _render_resource_view(request, 'relationships_performance.html', context)
    except Exception as e:
        logger.error(f"Error loading error performance relationships: {e}", exc_info=True)
        return _render_resource_view(request, 'relationships_performance.html', {'relationships': [], 'total': 0, 'performance_type': 'errors', 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationship_access_control(request: HttpRequest, relationship_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/<relationship_id>/access-control/"""
    try:
        relationships_service = get_relationships_service()
        relationship = relationships_service.get_relationship(relationship_id)
        if not relationship:
            raise Http404(f"Relationship not found: {relationship_id}")
        context: Dict[str, Any] = {'relationship': relationship, 'relationship_id': relationship_id, 'access_control': relationship.get("access_control")}
        return _render_resource_view(request, 'relationship_access_control.html', context)
    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading relationship access control for {relationship_id}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationship_access_control.html', {'relationship_id': relationship_id, 'access_control': None, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationship_data_flow(request: HttpRequest, relationship_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/<relationship_id>/data-flow/"""
    try:
        relationships_service = get_relationships_service()
        relationship = relationships_service.get_relationship(relationship_id)
        if not relationship:
            raise Http404(f"Relationship not found: {relationship_id}")
        context: Dict[str, Any] = {'relationship': relationship, 'relationship_id': relationship_id, 'data_flow': relationship.get("data_flow")}
        return _render_resource_view(request, 'relationship_data_flow.html', context)
    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading relationship data flow for {relationship_id}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationship_data_flow.html', {'relationship_id': relationship_id, 'data_flow': None, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationship_performance(request: HttpRequest, relationship_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/<relationship_id>/performance/"""
    try:
        relationships_service = get_relationships_service()
        relationship = relationships_service.get_relationship(relationship_id)
        if not relationship:
            raise Http404(f"Relationship not found: {relationship_id}")
        context: Dict[str, Any] = {'relationship': relationship, 'relationship_id': relationship_id, 'performance': relationship.get("performance")}
        return _render_resource_view(request, 'relationship_performance.html', context)
    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading relationship performance for {relationship_id}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationship_performance.html', {'relationship_id': relationship_id, 'performance': None, 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationship_dependencies(request: HttpRequest, relationship_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/<relationship_id>/dependencies/"""
    try:
        relationships_service = get_relationships_service()
        relationship = relationships_service.get_relationship(relationship_id)
        if not relationship:
            raise Http404(f"Relationship not found: {relationship_id}")
        context: Dict[str, Any] = {'relationship': relationship, 'relationship_id': relationship_id, 'dependencies': relationship.get("dependencies", [])}
        return _render_resource_view(request, 'relationship_dependencies.html', context)
    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading relationship dependencies for {relationship_id}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationship_dependencies.html', {'relationship_id': relationship_id, 'dependencies': [], 'error': str(e)}, error_message=str(e))


@require_super_admin
def media_manager_relationship_postman(request: HttpRequest, relationship_id: str) -> HttpResponse:
    """GET /docs/media-manager/relationships/<relationship_id>/postman/"""
    try:
        relationships_service = get_relationships_service()
        relationship = relationships_service.get_relationship(relationship_id)
        if not relationship:
            raise Http404(f"Relationship not found: {relationship_id}")
        context: Dict[str, Any] = {'relationship': relationship, 'relationship_id': relationship_id, 'postman': relationship.get("postman")}
        return _render_resource_view(request, 'relationship_postman.html', context)
    except Http404:
        raise
    except Exception as e:
        logger.error(f"Error loading relationship postman for {relationship_id}: {e}", exc_info=True)
        return _render_resource_view(request, 'relationship_postman.html', {'relationship_id': relationship_id, 'postman': None, 'error': str(e)}, error_message=str(e))
