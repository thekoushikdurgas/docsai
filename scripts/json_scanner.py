"""
json_scanner.py — replaces scanner.py
Walk docs/**/*.json (typed doc envelopes), group results by era/kind.
Returns structured scan results used by cli.py commands like `scan` and `stats`.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterator

from scripts.paths import JSON_ROOT, iter_doc_json_paths

VALID_DOC_KINDS = frozenset({
    "index", "hub", "era_task", "graphql_module", "endpoint_matrix", "page_spec", "document",
})


def iter_json_files() -> Iterator[Path]:
    yield from iter_doc_json_paths()


def load_envelope(path: Path) -> dict | None:
    """Load a typed doc JSON and return envelope fields (no raw_markdown)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data.get("schema_version"), int):
        return None
    if data.get("kind") not in VALID_DOC_KINDS:
        return None
    skip = ("raw_markdown", "non_parsed_raw_markdown")
    return {k: v for k, v in data.items() if k not in skip}


def scan_all(era: int | None = None) -> list[dict]:
    """Return a list of all doc envelope dicts, optionally filtered by era."""
    results = []
    for p in iter_json_files():
        data = load_envelope(p)
        if data is None:
            continue
        if era is not None and data.get("era_index") != era and data.get("era") != era:
            continue
        data["_json_path"] = p.relative_to(JSON_ROOT).as_posix()
        results.append(data)
    return results


def group_by_kind(docs: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for d in docs:
        groups[d.get("kind", "document")].append(d)
    return dict(groups)


def group_by_era(docs: list[dict]) -> dict[int | str, list[dict]]:
    groups: dict[int | str, list[dict]] = defaultdict(list)
    for d in docs:
        era = d.get("era_index") if d.get("era_index") is not None else d.get("era")
        groups[era if era is not None else "none"].append(d)
    return dict(groups)


def count_by_status(docs: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for d in docs:
        s = d.get("status") or "unknown"
        counts[s] += 1
    return dict(counts)


def era_summary(era: int) -> dict:
    """Return a summary dict for a specific era."""
    docs = scan_all(era=era)
    idx = next((d for d in docs if d.get("kind") == "index"), None)
    return {
        "era": era,
        "total_docs": len(docs),
        "by_kind": {k: len(v) for k, v in group_by_kind(docs).items()},
        "status_counts": count_by_status(docs),
        "index_title": idx.get("title") if idx else None,
    }
