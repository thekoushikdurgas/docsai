from django.shortcuts import render
from apps.core.decorators import require_login
from apps.core.services.graphql_client import graphql_query
import logging, json

logger = logging.getLogger(__name__)

_GRAPH_DATA = """
query RelationshipGraph {
  docs { relationships { items { id pageId endpointId usageType } } }
}
"""


@require_login
def visualization_view(request):
    graph_nodes, graph_edges = [], []
    try:
        token = request.session.get("operator", {}).get("token", "")
        resp = graphql_query(_GRAPH_DATA, token=token)
        data = (resp.get("data") or {}) if isinstance(resp, dict) else {}
        docs = (data.get("docs") or {}) if isinstance(data, dict) else {}
        rels = (docs.get("relationships") or {}).get("items") or []
        for r in rels:
            graph_edges.append(
                {
                    "source": r["pageId"],
                    "target": r["endpointId"],
                    "label": r["usageType"],
                }
            )
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
