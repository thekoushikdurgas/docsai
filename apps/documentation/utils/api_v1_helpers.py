"""API v1 list projection helpers (Lambda-compatible shapes)."""

from __future__ import annotations

from typing import Any, Dict
from django.http import HttpRequest


def should_expand_full(query_params) -> bool:
    v = (query_params.get("expand") or "").lower()
    return v in ("1", "true", "full")


def to_page_list_item(p: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "page_id": p.get("page_id"),
        "title": (p.get("metadata") or {}).get("title") or p.get("title"),
        "page_type": (p.get("metadata") or {}).get("page_type", "docs"),
    }


def to_endpoint_list_item(ep: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "endpoint_id": ep.get("endpoint_id"),
        "endpoint_path": ep.get("endpoint_path"),
        "method": ep.get("method"),
        "api_version": ep.get("api_version"),
    }


def to_relationship_list_item(r: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "relationship_id": r.get("relationship_id") or r.get("id"),
        "page_id": r.get("page_id"),
        "endpoint_id": r.get("endpoint_id"),
        "usage_type": r.get("usage_type"),
    }


def to_postman_list_item(c: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "config_id": c.get("config_id"),
        "name": c.get("name"),
        "state": c.get("state"),
    }
