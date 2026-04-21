"""
Architecture blueprint: static service registry plus live rows from monorepo ``docs/*/index.json``.

Phase 0: registry rows are annotated from gateway ``health.satelliteHealth`` when a static
service maps to a probe name (see ``satellite_registry.SERVICE_SATELLITE_KEY``).
"""

from django.shortcuts import render

from apps.admin_ops.services.admin_client import get_gateway_satellite_health
from apps.core.decorators import require_login
from apps.core.utils.repo_docs import load_phase_index_rows

from .constants import SERVICES, URL_MOUNTS
from .satellite_registry import merge_services_with_satellite_health


@require_login
def blueprint_view(request):
    """
    Service registry + monorepo ``docs/*/index.json`` phase rows for the blueprint page.

    Live satellite columns: ``health.satelliteHealth`` (operator JWT).

    @role: authenticated
    """
    token = request.session.get("operator", {}).get("token", "")
    satellite_health: list = []
    try:
        satellite_health = get_gateway_satellite_health(token)
    except Exception:
        satellite_health = []
    services_live = merge_services_with_satellite_health(SERVICES, satellite_health)
    phase_docs = load_phase_index_rows()
    return render(
        request,
        "architecture/blueprint.html",
        {
            "services": services_live,
            "url_mounts": URL_MOUNTS,
            "phase_docs": phase_docs,
            "page_title": "Architecture",
            "satellite_health": satellite_health,
        },
    )
