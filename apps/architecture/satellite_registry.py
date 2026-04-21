"""
Map static architecture registry rows to ``health.satelliteHealth`` probe names (Phase 0).

Gateway returns satellite keys: ``connectra``, ``campaign``, ``phone``, ``email``,
``ai_server``, ``s3storage``, ``logs``, ``sales_navigator``.
"""

from __future__ import annotations

from typing import Any

# Human-readable service name (from SERVICES ``name``) -> satelliteHealth ``name``
SERVICE_SATELLITE_KEY: dict[str, str] = {
    "Go/Gin Sync Service": "connectra",
    "Email Campaign": "campaign",
    "Go Email Server": "email",
    "Go S3 Storage": "s3storage",
    "Go Logs API": "logs",
    "Contact AI": "ai_server",
    "Extension Server": "sales_navigator",
}


def merge_services_with_satellite_health(
    services: list[dict[str, Any]],
    satellite_health: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    """
    Annotate each static service row with live gateway probe data when names align.

    Rows without a mapped satellite get ``live_status`` of ``not_probed``.
    """
    by_name: dict[str, dict[str, Any]] = {}
    for row in satellite_health or []:
        n = row.get("name")
        if isinstance(n, str) and n:
            by_name[n] = row

    out: list[dict[str, Any]] = []
    for svc in services:
        name = svc.get("name", "")
        key = SERVICE_SATELLITE_KEY.get(str(name))
        live = by_name.get(key) if key else None
        if live:
            merged = {
                **svc,
                "live_status": live.get("status"),
                "live_configured": live.get("configured"),
                "live_detail": live.get("detail"),
                "satellite_key": key,
            }
        else:
            merged = {
                **svc,
                "live_status": "not_probed",
                "live_configured": None,
                "live_detail": None,
                "satellite_key": None,
            }
        out.append(merged)
    return out
