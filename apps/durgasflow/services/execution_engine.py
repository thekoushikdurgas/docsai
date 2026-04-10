"""
Simplified Durgasflow Execution Engine.

Runs an n8n-exported workflow synchronously (suitable for admin/test use):
  - topological-sort of nodes from connections graph
  - executes HTTP-request nodes via httpx
  - logs each node result to N8nExecutionLog
  - saves final status to N8nExecution (PostgreSQL)
  - returns execution_id

Unsupported node types are skipped with a warning log entry.
"""

from __future__ import annotations

import logging
import time
from typing import Any
from urllib.parse import urlencode

from django.utils import timezone

from apps.durgasflow.models import N8nExecution, N8nExecutionLog, N8nWorkflow

logger = logging.getLogger(__name__)

# --- Node handlers -----------------------------------------------------------

try:
    import httpx as _httpx

    _HTTPX_AVAILABLE = True
except ImportError:
    _HTTPX_AVAILABLE = False


def _handle_manual_trigger(node: dict, context: dict) -> dict:
    return {"triggered": True, "trigger_data": context.get("trigger_data", {})}


def _handle_set(node: dict, context: dict) -> dict:
    """Return values defined in the Set node parameters."""
    params = node.get("parameters", {})
    values = {}
    for field in params.get("values", {}).get("string", []):
        values[field.get("name", "")] = field.get("value", "")
    return {"set_values": values}


def _handle_http_request(node: dict, context: dict) -> dict:
    if not _HTTPX_AVAILABLE:
        return {"skipped": True, "reason": "httpx not installed"}

    params = node.get("parameters", {})
    url = params.get("url", "")
    method = (params.get("method") or "GET").upper()
    headers = {}
    body = None
    timeout = min(int(params.get("timeout", 10000)) / 1000, 30)

    # Build query string
    qs_params = params.get("queryParameters", {}).get("parameters", [])
    if qs_params:
        url = (
            url
            + "?"
            + urlencode({p["name"]: p["value"] for p in qs_params if p.get("name")})
        )

    # Body
    if method not in ("GET", "HEAD") and params.get("body"):
        body = params["body"]

    try:
        resp = _httpx.request(
            method, url, headers=headers, content=body, timeout=timeout
        )
        try:
            result_body = resp.json()
        except Exception:
            result_body = resp.text[:2000]
        return {
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "body": result_body,
        }
    except Exception as exc:
        return {"error": str(exc)}


def _handle_code(node: dict, context: dict) -> dict:
    """Safely evaluate simple JavaScript-style code (Python eval only)."""
    return {
        "skipped": True,
        "reason": "Code node execution not supported in admin engine",
    }


# Map of n8n node type → handler function
_NODE_HANDLERS: dict[str, Any] = {
    "n8n-nodes-base.manualTrigger": _handle_manual_trigger,
    "n8n-nodes-base.set": _handle_set,
    "n8n-nodes-base.httpRequest": _handle_http_request,
    "n8n-nodes-base.code": _handle_code,
    "n8n-nodes-base.noOp": lambda n, c: {"noop": True},
    "n8n-nodes-base.wait": lambda n, c: {"waited": True},
}


def _topological_sort(nodes: list[dict], connections: dict) -> list[dict]:
    """
    Return nodes in execution order using Kahn's algorithm.
    Falls back to original order on cycle detection.
    """
    name_to_node = {n["name"]: n for n in nodes}
    in_degree: dict[str, int] = {n["name"]: 0 for n in nodes}

    # Build adjacency list: source → list of targets
    adj: dict[str, list[str]] = {n["name"]: [] for n in nodes}
    for src_name, outputs in connections.items():
        for _output_type, links_list in outputs.items():
            for links in links_list:
                for link in links:
                    tgt = link.get("node", "")
                    if tgt in in_degree:
                        in_degree[tgt] += 1
                        adj[src_name].append(tgt)

    queue = [name for name, deg in in_degree.items() if deg == 0]
    sorted_names: list[str] = []

    while queue:
        current = queue.pop(0)
        sorted_names.append(current)
        for neighbour in adj.get(current, []):
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    if len(sorted_names) != len(nodes):
        # Cycle or disconnected — fall back to original order
        return nodes

    return [name_to_node[name] for name in sorted_names if name in name_to_node]


# --- Public API --------------------------------------------------------------


def run_workflow(
    workflow: N8nWorkflow,
    workflow_json: dict,
    trigger_data: dict | None = None,
    triggered_by: str = "",
) -> str:
    """
    Execute a workflow and persist results.

    Args:
        workflow: N8nWorkflow DB record
        workflow_json: full n8n JSON dict (from S3 / graph_data)
        trigger_data: optional dict with external trigger payload
        triggered_by: username / identifier string

    Returns:
        str — the execution UUID
    """
    trigger_data = trigger_data or {}

    # Create execution record
    execution = N8nExecution.objects.create(
        workflow=workflow,
        status="running",
        trigger_type=workflow.trigger_type,
        trigger_data=trigger_data,
        triggered_by=triggered_by,
        started_at=timezone.now(),
    )

    nodes: list[dict] = workflow_json.get("nodes", [])
    connections: dict = workflow_json.get("connections", {})

    sorted_nodes = _topological_sort(nodes, connections)
    context = {"trigger_data": trigger_data, "node_outputs": {}}

    node_results: dict = {}
    final_error: str | None = None

    for node in sorted_nodes:
        node_name = node.get("name", "unnamed")
        node_type = node.get("type", "unknown")
        node_id = node.get("id", "")

        log_entry = N8nExecutionLog(
            execution=execution,
            node_id=node_id,
            node_name=node_name,
            node_type=node_type,
            level="info",
            message=f"Starting node: {node_name}",
            started_at=timezone.now(),
        )

        try:
            handler = _NODE_HANDLERS.get(node_type)
            if handler is None:
                result = {
                    "skipped": True,
                    "reason": f"Node type '{node_type}' not supported",
                }
                log_entry.level = "warning"
                log_entry.message = f"Skipped unsupported node: {node_type}"
            else:
                result = handler(node, context)
                log_entry.message = f"Completed node: {node_name}"

            context["node_outputs"][node_name] = result
            node_results[node_name] = result

            log_entry.data = result
            log_entry.finished_at = timezone.now()
            log_entry.save()

        except Exception as exc:
            err_msg = str(exc)
            logger.exception("Node %s raised an error: %s", node_name, err_msg)
            node_results[node_name] = {"error": err_msg}
            log_entry.level = "error"
            log_entry.message = f"Error in node {node_name}: {err_msg}"
            log_entry.data = {"error": err_msg}
            log_entry.finished_at = timezone.now()
            log_entry.save()
            final_error = err_msg
            # Continue executing remaining nodes (n8n behaviour: continue on error by default)

    if final_error:
        execution.fail(
            error_message=final_error,
            error_stack="",
        )
        # node_results already set on the record by fail() parent
        execution.node_results = node_results
        execution.save(update_fields=["node_results"])
    else:
        execution.complete(
            result_data={
                "message": "Workflow completed",
                "node_count": len(sorted_nodes),
            },
            node_results=node_results,
        )

    return str(execution.id)
