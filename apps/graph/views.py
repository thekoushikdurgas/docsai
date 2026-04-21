"""
Documentation relationship graph: edges from gateway ``docs.relationships``;
nodes derived as the union of endpoints so the force layout has anchors.
"""

import json
import logging

from django.shortcuts import render

from apps.core.decorators import require_login
from apps.core.services.graphql_client import graphql_query

logger = logging.getLogger(__name__)

_GRAPH_DATA = """
query RelationshipGraph {
  docs { relationships { items { id pageId endpointId usageType } } }
}
"""


@require_login
def visualization_view(request):
    """
    Force-directed graph from gateway ``docs.relationships``.

    @role: authenticated
    """
    graph_nodes, graph_edges = [], []
    try:
        token = request.session.get("operator", {}).get("token", "")
        resp = graphql_query(_GRAPH_DATA, token=token)
        data = (resp.get("data") or {}) if isinstance(resp, dict) else {}
        docs = (data.get("docs") or {}) if isinstance(data, dict) else {}
        rels = (docs.get("relationships") or {}).get("items") or []
        node_ids: set[str] = set()
        for r in rels:
            graph_edges.append(
                {
                    "source": r["pageId"],
                    "target": r["endpointId"],
                    "label": r["usageType"],
                }
            )
            node_ids.add(str(r["pageId"]))
            node_ids.add(str(r["endpointId"]))
        graph_nodes = [{"id": nid, "label": nid} for nid in sorted(node_ids)]
    except Exception as exc:
        logger.warning("graph data failed: %s", exc)
    return render(
        request,
        "graph/visualization.html",
        {
            "graph_nodes_json": json.dumps(graph_nodes),
            "graph_edges_json": json.dumps(graph_edges),
            "page_title": "Relationship Graph",
        },
    )
