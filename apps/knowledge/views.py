"""Knowledge base CRUD (GraphQL wiring optional)."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.core.decorators import require_super_admin


@require_super_admin
def knowledge_list(request):
    return render(
        request,
        "knowledge/list.html",
        {"page_title": "Knowledge", "items": [], "q": request.GET.get("q", "")},
    )


@require_super_admin
def knowledge_create(request):
    if request.method == "POST":
        messages.info(request, "Create (stub) — wire GraphQL knowledge mutations.")
        return redirect("knowledge:list")
    return render(request, "knowledge/create.html", {"page_title": "New knowledge"})


@require_super_admin
def knowledge_detail(request, knowledge_id):
    return render(
        request,
        "knowledge/detail.html",
        {"page_title": "Knowledge", "knowledge_id": knowledge_id, "item": None},
    )


@require_super_admin
def knowledge_edit(request, knowledge_id):
    if request.method == "POST":
        messages.success(request, "Saved (stub).")
        return redirect("knowledge:detail", knowledge_id=knowledge_id)
    return render(
        request,
        "knowledge/edit.html",
        {"page_title": "Edit", "knowledge_id": knowledge_id, "item": None},
    )


@require_super_admin
@require_http_methods(["POST"])
def knowledge_delete(request, knowledge_id):
    messages.info(request, "Deleted (stub).")
    return redirect("knowledge:list")


@require_super_admin
def knowledge_search(request):
    q = request.GET.get("q", "")
    return render(
        request,
        "knowledge/list.html",
        {"page_title": "Search", "items": [], "q": q, "search_mode": True},
    )
