"""
n8n Workflow JSON Parser for Durgasflow admin.

Validates and normalises exported n8n workflow JSON files, maps node types to
internal categories, and extracts metadata for DB storage.
"""

from __future__ import annotations

import re
from typing import Any

# Maps n8n node type prefixes / full names to internal categories
NODE_TYPE_CATEGORY_MAP: dict[str, str] = {
    # Triggers
    "n8n-nodes-base.manualTrigger": "trigger",
    "n8n-nodes-base.webhookTrigger": "trigger",
    "n8n-nodes-base.webhook": "trigger",
    "n8n-nodes-base.scheduleTrigger": "trigger",
    "n8n-nodes-base.cron": "trigger",
    "n8n-nodes-base.sseTrigger": "trigger",
    "n8n-nodes-base.errorTrigger": "trigger",
    "n8n-nodes-base.emailReadImap": "trigger",
    # AI / LLM
    "@n8n/n8n-nodes-langchain.agent": "ai_agent",
    "@n8n/n8n-nodes-langchain.openAi": "ai_agent",
    "@n8n/n8n-nodes-langchain.lmChatOpenAi": "ai_agent",
    "@n8n/n8n-nodes-langchain.chainLlm": "ai_agent",
    "n8n-nodes-base.openAi": "ai_agent",
    # Logic / flow control
    "n8n-nodes-base.if": "logic",
    "n8n-nodes-base.switch": "logic",
    "n8n-nodes-base.merge": "logic",
    "n8n-nodes-base.splitOut": "logic",
    "n8n-nodes-base.aggregate": "logic",
    "n8n-nodes-base.code": "logic",
    "n8n-nodes-base.set": "logic",
    "n8n-nodes-base.noOp": "logic",
    "n8n-nodes-base.wait": "logic",
    "n8n-nodes-base.splitInBatches": "logic",
}

# Prefix-based fallbacks
_TRIGGER_PREFIXES = ("trigger", "webhook", "cron", "schedule", "sse", "email", "error")
_AI_PREFIXES = (
    "langchain",
    "openai",
    "anthropic",
    "gemini",
    "llm",
    "chain",
    "agent",
    "vector",
)
_LOGIC_PREFIXES = (
    "if",
    "switch",
    "merge",
    "split",
    "aggregate",
    "code",
    "set",
    "filter",
    "sort",
)


def _guess_category(node_type: str) -> str:
    """Infer category from node type string when not in the explicit map."""
    t = node_type.lower()
    for p in _TRIGGER_PREFIXES:
        if p in t:
            return "trigger"
    for p in _AI_PREFIXES:
        if p in t:
            return "ai_agent"
    for p in _LOGIC_PREFIXES:
        if p in t:
            return "logic"
    return "action"


def _categorise_node(node_type: str) -> str:
    return NODE_TYPE_CATEGORY_MAP.get(node_type) or _guess_category(node_type)


def _detect_trigger_type(nodes: list[dict]) -> str:
    """Return the primary trigger category for the workflow."""
    for node in nodes:
        t = node.get("type", "").lower()
        if "webhook" in t:
            return "webhook"
        if "cron" in t or "schedule" in t:
            return "schedule"
        if "trigger" in t:
            return "manual"
    return "manual"


def parse_workflow(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate and enrich a raw n8n workflow JSON dict.

    Raises ValueError with a descriptive message when the JSON is invalid.
    Returns an enriched result dict with:
      - workflow_json  : normalised workflow dict (ready to store)
      - name           : workflow name
      - n8n_id         : original n8n id / workflow_id field
      - n8n_version_id : versionId field
      - node_count     : int
      - trigger_type   : "manual" | "webhook" | "schedule" | "event"
      - has_trigger    : bool
      - node_types     : list of distinct node type strings
      - node_categories: dict mapping node name → category string
      - tags           : list of tag name strings
      - settings       : settings dict
      - is_active      : bool
    """
    if not isinstance(data, dict):
        raise ValueError("Workflow JSON must be a JSON object.")

    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("Workflow JSON must have a 'nodes' list.")

    if len(nodes) == 0:
        raise ValueError("Workflow must contain at least one node.")

    # Normalise connections
    connections = data.get("connections")
    if not isinstance(connections, dict):
        connections = {}

    node_types: list[str] = []
    node_categories: dict[str, str] = {}
    has_trigger = False

    for node in nodes:
        if not isinstance(node, dict):
            continue
        ntype = node.get("type", "unknown")
        nname = node.get("name", node.get("id", "unnamed"))
        cat = _categorise_node(ntype)
        if cat == "trigger":
            has_trigger = True
        node_types.append(ntype)
        node_categories[nname] = cat

    # Extract tags as simple name strings
    raw_tags = data.get("tags", [])
    tag_names: list[str] = []
    for t in raw_tags:
        if isinstance(t, dict):
            tag_names.append(t.get("name", ""))
        elif isinstance(t, str):
            tag_names.append(t)

    # Workflow identity
    n8n_id = (str(data.get("id", "")) or str(data.get("workflow_id", ""))).strip()
    n8n_version_id = str(data.get("versionId", "")).strip()
    name = (data.get("name") or "Untitled Workflow").strip() or "Untitled Workflow"
    settings = data.get("settings") or {}
    is_active = bool(data.get("active", False))

    trigger_type = _detect_trigger_type(nodes)

    # Build the normalised workflow JSON to store / return
    workflow_json = {
        **data,
        "connections": connections,
        "tags": raw_tags,
        "settings": settings,
    }

    return {
        "workflow_json": workflow_json,
        "name": name,
        "n8n_id": n8n_id,
        "n8n_version_id": n8n_version_id,
        "node_count": len(nodes),
        "trigger_type": trigger_type,
        "has_trigger": has_trigger,
        "node_types": list(set(node_types)),
        "node_categories": node_categories,
        "tags": tag_names,
        "settings": settings,
        "is_active": is_active,
    }


def parse_index(data: dict[str, Any]) -> dict[str, Any]:
    """Validate a docs/n8n/index.json catalog dict."""
    if not isinstance(data, dict):
        raise ValueError("Index JSON must be an object.")
    if "workflows" not in data:
        raise ValueError("Index JSON must have a 'workflows' list.")
    return {
        "version": data.get("version", ""),
        "last_updated": data.get("last_updated", ""),
        "total": data.get("total", 0),
        "workflows": data.get("workflows", []),
    }
