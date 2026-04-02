"""Search helper enforcing namespace + reranking constraints."""

from __future__ import annotations

import time
from typing import Any, List, Optional


def search(
    index: Any,
    *,
    namespace: str,
    query_text: str,
    top_k: int = 5,
    wait_seconds: float = 0,
) -> List[Any]:
    """
    Semantic search over integrated-embedding text field (`field_map text=content`).

    Mandatory behaviors (from `.agents/PINECONE-*.md`):
    - Always specify `namespace`
    - Always apply reranking with `bge-reranker-v2-m3`
    - Request 2x candidates for reranking (top_k * 2)
    """

    if not namespace:
        raise ValueError("namespace is required (Pinecone namespace isolation).")
    if not query_text.strip():
        return []
    if top_k <= 0:
        return []

    if wait_seconds > 0:
        time.sleep(wait_seconds)

    results = index.search(
        namespace=namespace,
        query={
            "top_k": top_k * 2,
            "inputs": {"text": query_text},
        },
        rerank={
            "model": "bge-reranker-v2-m3",
            "top_n": top_k,
            "rank_fields": ["content"],
        },
    )

    # SDK result objects differ slightly by version; handle both.
    if getattr(results, "result", None) is not None and getattr(results.result, "hits", None) is not None:
        return list(results.result.hits)
    if isinstance(results, dict):
        try:
            return list(results["result"]["hits"])
        except Exception:
            pass
    return []

