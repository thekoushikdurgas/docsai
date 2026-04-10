from django.shortcuts import render
from apps.core.decorators import require_login
from .constants import ERAS, STATUS_COLOR


@require_login
def dashboard_view(request):
    era_filter = request.GET.get("status", "")
    eras = ERAS
    if era_filter:
        eras = [e for e in ERAS if e["status"] == era_filter]
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
