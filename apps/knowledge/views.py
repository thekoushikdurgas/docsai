"""
Knowledge base UI (Phase 5 — AI).

Gateway: ``knowledge.articles``, ``knowledge.createArticle``, ``knowledge.updateArticle``,
``knowledge.deleteArticle`` (SuperAdmin). See ``apps.admin_ops.services.admin_client``.
"""

from __future__ import annotations

from typing import Any, Dict, List

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.admin_ops.services.admin_client import (
    AdminGraphQLError,
    create_knowledge_article,
    delete_knowledge_article,
    list_knowledge_articles,
    update_knowledge_article,
)
from apps.core.decorators import require_super_admin


def _token(request) -> str:
    return request.session.get("operator", {}).get("token", "")


def _normalize_rows(raw: List[Any], q: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    qlow = (q or "").strip().lower()
    for row in raw:
        if not isinstance(row, dict):
            continue
        title = str(row.get("title") or "")
        body = str(row.get("body") or "")
        if qlow and qlow not in title.lower() and qlow not in body.lower():
            continue
        out.append(
            {
                "id": row.get("id"),
                "title": title,
                "updated": row.get("updatedAt") or row.get("createdAt") or "—",
                "body": body,
                "tags": row.get("tags") or [],
            }
        )
    return out


def _find_item(items: List[Dict[str, Any]], knowledge_id: str) -> Dict[str, Any] | None:
    for it in items:
        if str(it.get("id")) == str(knowledge_id):
            return it
    return None


@require_super_admin
def knowledge_list(request):
    """List ``knowledge.articles``. @role: super_admin"""
    raw: list = []
    try:
        raw = list_knowledge_articles(_token(request), limit=100, offset=0)
    except (AdminGraphQLError, Exception) as exc:
        messages.error(request, f"Knowledge list failed: {exc}")
        raw = []
    items = _normalize_rows(raw, "")
    return render(
        request,
        "knowledge/list.html",
        {"page_title": "Knowledge", "items": items, "q": ""},
    )


@require_super_admin
def knowledge_create(request):
    """Create via ``knowledge.createArticle``. @role: super_admin"""
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        body = (request.POST.get("body") or "").strip()
        tags_raw = (request.POST.get("tags") or "").strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
        if not title:
            messages.error(request, "Title is required.")
            return render(
                request, "knowledge/create.html", {"page_title": "New knowledge"}
            )
        try:
            row = create_knowledge_article(
                _token(request), title=title, body=body, tags=tags or None
            )
            rid = row.get("id") if isinstance(row, dict) else None
            messages.success(request, "Knowledge article created.")
            if rid:
                return redirect("knowledge:detail", knowledge_id=rid)
            return redirect("knowledge:list")
        except (AdminGraphQLError, Exception) as exc:
            messages.error(request, str(exc))
    return render(request, "knowledge/create.html", {"page_title": "New knowledge"})


@require_super_admin
def knowledge_detail(request, knowledge_id):
    """Detail for one article (from list). @role: super_admin"""
    raw: list = []
    try:
        raw = list_knowledge_articles(_token(request), limit=200, offset=0)
    except (AdminGraphQLError, Exception) as exc:
        messages.error(request, str(exc))
    items = _normalize_rows(raw, "")
    item = _find_item(items, str(knowledge_id))
    if not item:
        messages.warning(request, "Article not found.")
        return redirect("knowledge:list")
    return render(
        request,
        "knowledge/detail.html",
        {
            "page_title": item.get("title", "Knowledge"),
            "knowledge_id": knowledge_id,
            "item": item,
        },
    )


@require_super_admin
def knowledge_edit(request, knowledge_id):
    """Edit via ``knowledge.updateArticle``. @role: super_admin"""
    raw: list = []
    try:
        raw = list_knowledge_articles(_token(request), limit=200, offset=0)
    except (AdminGraphQLError, Exception) as exc:
        messages.error(request, str(exc))
    items = _normalize_rows(raw, "")
    item = _find_item(items, str(knowledge_id))
    if not item:
        messages.warning(request, "Article not found.")
        return redirect("knowledge:list")

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        body = (request.POST.get("body") or "").strip()
        tags_raw = (request.POST.get("tags") or "").strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
        if not title:
            messages.error(request, "Title is required.")
        else:
            try:
                update_knowledge_article(
                    _token(request),
                    article_id=str(knowledge_id),
                    title=title,
                    body=body,
                    tags=tags,
                )
                messages.success(request, "Saved.")
                return redirect("knowledge:detail", knowledge_id=knowledge_id)
            except (AdminGraphQLError, Exception) as exc:
                messages.error(request, str(exc))
    return render(
        request,
        "knowledge/edit.html",
        {
            "page_title": "Edit",
            "knowledge_id": knowledge_id,
            "item": item,
        },
    )


@require_super_admin
@require_http_methods(["POST"])
def knowledge_delete(request, knowledge_id):
    """``knowledge.deleteArticle``. @role: super_admin"""
    try:
        delete_knowledge_article(_token(request), article_id=str(knowledge_id))
        messages.success(request, "Deleted.")
    except (AdminGraphQLError, Exception) as exc:
        messages.error(request, str(exc))
    return redirect("knowledge:list")


@require_super_admin
def knowledge_search(request):
    """Filter loaded articles by ``q`` (client-side on list payload). @role: super_admin"""
    q = request.GET.get("q", "")
    raw: list = []
    try:
        raw = list_knowledge_articles(_token(request), limit=200, offset=0)
    except (AdminGraphQLError, Exception) as exc:
        messages.error(request, str(exc))
    items = _normalize_rows(raw, q)
    return render(
        request,
        "knowledge/list.html",
        {"page_title": "Search", "items": items, "q": q, "search_mode": True},
    )
