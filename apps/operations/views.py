"""Operations hub — links to admin_ops, runbooks, and cross-phase shortcuts."""

from django.shortcuts import render

from apps.core.decorators import require_login


@require_login
def index_view(request):
    """Operations landing page. @role: authenticated"""
    return render(request, "operations/index.html", {"page_title": "Operations"})
