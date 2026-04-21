"""Templates hub (Phase 0 stub — see ``TODO.md``)."""

from django.shortcuts import render

from apps.core.decorators import require_login


@require_login
def index_view(request):
    """Render templates index. @role: authenticated"""
    return render(request, "templates_app/index.html", {"page_title": "Templates"})
