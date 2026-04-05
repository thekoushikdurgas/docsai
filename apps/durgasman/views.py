"""Durgasman — Postman-style collections (shell views + JSON API stubs)."""
import json
import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.core.decorators import require_super_admin

logger = logging.getLogger(__name__)


@require_super_admin
def dashboard(request):
    return render(
        request,
        "durgasman/dashboard.html",
        {"page_title": "Durgasman", "collections": []},
    )


@require_super_admin
def collection_detail(request, collection_id):
    return render(
        request,
        "durgasman/collection_detail.html",
        {"page_title": "Collection", "collection_id": collection_id, "requests": []},
    )


@require_super_admin
def import_view(request):
    if request.method == "POST":
        messages.info(request, "Import handler not wired yet — file ignored.")
        return redirect("durgasman:import_view")
    return render(request, "durgasman/import.html", {"page_title": "Import collection"})


def _json_ok(data=None, status=200):
    return JsonResponse({"success": True, "data": data or {}, "stub": True}, status=status)


@require_super_admin
def api_collections(request):
    if request.method == "GET":
        return _json_ok({"items": [], "total": 0})
    return JsonResponse({"success": False, "error": "Use GET"}, status=405)


@require_super_admin
def api_collection_requests(request, collection_id):
    return _json_ok({"collection_id": collection_id, "items": []})


@require_super_admin
def api_request_detail(request, request_id):
    return _json_ok({"id": request_id})


@require_super_admin
def api_environments(request):
    return _json_ok({"items": []})


@require_super_admin
def api_history(request):
    return _json_ok({"items": []})


@require_super_admin
def api_mocks(request):
    return _json_ok({"items": []})


@require_super_admin
@require_http_methods(["POST"])
def api_analyze_response(request):
    try:
        json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    return _json_ok({"analysis": "stub"})
