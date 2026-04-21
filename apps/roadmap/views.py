"""
Roadmap hub: prefers phase folders from monorepo ``docs/``; falls back to static ``ERAS``.
"""

from django.shortcuts import render

from apps.core.decorators import require_login
from apps.core.utils.repo_docs import load_phase_index_rows

from .constants import ERAS, STATUS_COLOR


def _eras_from_docs_phase_rows(rows: list) -> list[dict]:
    """Map ``index.json`` metadata to template ``era`` dicts (number, name, status, era_pct)."""
    out: list[dict] = []
    for row in rows:
        folder = row.get("folder") or ""
        num_s = ""
        for c in folder:
            if c.isdigit():
                num_s += c
            elif num_s:
                break
        try:
            number = int(num_s) if num_s else 0
        except ValueError:
            number = 0
        raw_status = (row.get("status") or "draft").lower()
        if raw_status == "draft":
            disp, pct = "planned", 15
        elif raw_status in ("populated", "active"):
            disp, pct = "in_progress", 60
        else:
            disp, pct = "planned", 30
        out.append(
            {
                "number": number,
                "name": row.get("title") or folder,
                "status": disp,
                "era_pct": pct,
            }
        )
    return out


@require_login
def dashboard_view(request):
    """
    Roadmap eras from ``docs`` phase index or static ``ERAS`` fallback.

    @role: authenticated
    """
    era_filter = request.GET.get("status", "")
    phase_rows = load_phase_index_rows()
    eras = _eras_from_docs_phase_rows(phase_rows) if phase_rows else ERAS
    if era_filter:
        eras = [e for e in eras if e["status"] == era_filter]
    return render(
        request,
        "roadmap/dashboard.html",
        {
            "eras": eras,
            "status_color": STATUS_COLOR,
            "era_filter": era_filter,
            "page_title": "Roadmap",
        },
    )
