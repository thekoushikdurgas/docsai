"""Shared helpers and constants for documentation dashboard views."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

VALID_TABS = frozenset({"pages", "endpoints", "relationships", "postman"})
VALID_VIEW_MODES = frozenset({"list", "grid", "detail"})


def validate_tab(tab: Optional[str]) -> str:
    """Validate and normalize tab query parameter."""
    if not tab or tab not in VALID_TABS:
        return "pages"
    return tab


def validate_view_mode(view_mode: Optional[str]) -> str:
    """Validate and normalize view mode query parameter."""
    if not view_mode or view_mode not in VALID_VIEW_MODES:
        return "list"
    return view_mode


def render_resource_view(
    request: HttpRequest,
    template_name: str,
    context: Dict[str, Any],
    error_message: Optional[str] = None,
) -> HttpResponse:
    """Reusable helper to render resource views with standardized error handling."""
    if error_message:
        context['error'] = error_message
        logger.warning(f"View error: {error_message}")
    full_template_path = f'documentation/media_manager/{template_name}'
    return render(request, full_template_path, context)


def handle_service_call(
    service_call: callable,
    resource_name: str,
    resource_id: Optional[str] = None,
) -> tuple:
    """Reusable helper to handle service calls with standardized error handling."""
    try:
        result = service_call()
        return result, None
    except Http404:
        raise
    except Exception as e:
        error_msg = f"Error loading {resource_name}"
        if resource_id:
            error_msg += f" {resource_id}"
        error_msg += f": {e}"
        logger.error(error_msg, exc_info=True)
        return None, error_msg
