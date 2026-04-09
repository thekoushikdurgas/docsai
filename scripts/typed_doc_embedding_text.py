"""Flatten typed doc JSON into plain text for embeddings when `raw_markdown` is omitted."""

from __future__ import annotations

from typing import Any

_SKIP_KEYS = frozenset({"raw_markdown", "non_parsed_raw_markdown", "sha256_source"})
_MAX_CHARS = 500_000


def text_for_typed_doc_embedding(data: dict[str, Any]) -> str:
    parts: list[str] = []

    def walk(x: Any) -> None:
        if isinstance(x, str):
            t = x.strip()
            if len(t) > 2:
                parts.append(t)
        elif isinstance(x, dict):
            for k in sorted(x.keys()):
                if k in _SKIP_KEYS:
                    continue
                walk(x[k])
        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(data)
    out = "\n\n".join(parts)
    return out if len(out) <= _MAX_CHARS else out[:_MAX_CHARS]
