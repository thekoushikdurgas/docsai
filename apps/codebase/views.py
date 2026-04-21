"""
Codebase scanner UI (Phase 0). Parity routes; live scanner microservice TBD.

Gateway: none from this app today.
"""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.core.decorators import require_super_admin


@require_super_admin
def codebase_dashboard(request):
    """Scanner dashboard (empty analyses until service wired). @role: super_admin"""
    return render(
        request,
        "codebase/dashboard.html",
        {"page_title": "Codebase", "analyses": []},
    )


@require_super_admin
def scan_view(request):
    """Start scan form (POST warns if scanner unavailable). @role: super_admin"""
    if request.method == "POST":
        messages.warning(
            request,
            "Codebase scanner microservice is not configured — see "
            "contact360.io/admin/TODO.md (Phase 0 — Foundation).",
        )
        return redirect("codebase:dashboard")
    return render(request, "codebase/scan.html", {"page_title": "New scan"})


@require_super_admin
def analysis_detail_view(request, analysis_id):
    """Single analysis placeholder. @role: super_admin"""
    return render(
        request,
        "codebase/analysis_detail.html",
        {"page_title": "Analysis", "analysis_id": analysis_id, "analysis": None},
    )


@require_super_admin
def file_list_view(request, analysis_id):
    """File list placeholder. @role: super_admin"""
    return render(
        request,
        "codebase/file_list.html",
        {"page_title": "Files", "analysis_id": analysis_id, "files": []},
    )


@require_super_admin
def file_detail_view(request, analysis_id, file_path):
    """File content placeholder. @role: super_admin"""
    return render(
        request,
        "codebase/file_detail.html",
        {
            "page_title": "File",
            "analysis_id": analysis_id,
            "file_path": file_path,
            "content": None,
        },
    )


@require_super_admin
def dependencies_view(request, analysis_id):
    """Dependencies placeholder. @role: super_admin"""
    return render(
        request,
        "codebase/dependencies.html",
        {"page_title": "Dependencies", "analysis_id": analysis_id, "dependencies": []},
    )


@require_super_admin
def patterns_view(request, analysis_id):
    """Patterns placeholder. @role: super_admin"""
    return render(
        request,
        "codebase/patterns.html",
        {"page_title": "Patterns", "analysis_id": analysis_id, "patterns": []},
    )
