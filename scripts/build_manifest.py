"""
build_manifest.py — Phase 4
Scans all typed doc JSON under docs/ (see scripts/paths.iter_doc_json_paths) and writes
docs/manifest.json with by_kind counts, totals, and an entries[] list.

Run AFTER generate_indexes.py (optional).

Usage (from docs/):
    python scripts/build_manifest.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_DOCS = Path(__file__).resolve().parent.parent
if str(_DOCS) not in sys.path:
    sys.path.insert(0, str(_DOCS))

from scripts.paths import JSON_ROOT, MANIFEST_PATH, iter_doc_json_paths

VALID_KINDS = {"index", "hub", "era_task", "graphql_module", "endpoint_matrix", "page_spec", "document"}


def load_light(path: Path) -> dict | None:
    """Load only metadata for typed doc envelopes (skip Postman and other JSON)."""
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception as e:
        print(f"  WARN: {path}: {e}", file=sys.stderr)
        return None
    if not isinstance(data.get("schema_version"), int):
        return None
    kind = data.get("kind")
    if kind not in VALID_KINDS:
        return None
    return {
        "source_path": data.get("source_path", ""),
        "kind": kind,
        "title": data.get("title", ""),
        "sha256_source": data.get("sha256_source", ""),
        "generated_at": data.get("generated_at", ""),
        "schema_version": data.get("schema_version", 1),
        "status": data.get("status"),
        "version": data.get("version"),
        "era_index": data.get("era_index"),
    }


def collect_json_files() -> list[Path]:
    return list(iter_doc_json_paths())


def run(dry_run: bool) -> int:
    files = collect_json_files()
    print(f"Scanning {len(files)} JSON file candidates under {JSON_ROOT}")

    by_kind: dict[str, int] = defaultdict(int)
    entries: list[dict] = []
    errors = 0

    for p in files:
        data = load_light(p)
        if data is None:
            continue

        kind = data.get("kind", "document")
        by_kind[kind] += 1

        rel_json = p.relative_to(JSON_ROOT)
        entries.append({
            "json_path": rel_json.as_posix(),
            "source_path": data.get("source_path", ""),
            "kind": kind,
            "title": data.get("title", ""),
            "sha256_source": data.get("sha256_source", ""),
            "status": data.get("status"),
            "version": data.get("version"),
            "era_index": data.get("era_index"),
        })

    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "docs_root": "docs/",
        "json_root": "docs/",
        "total_files": len(entries),
        "by_kind": dict(sorted(by_kind.items())),
        "errors": errors,
        "entries": entries,
    }

    print(f"\nBy kind: {dict(by_kind)}")
    print(f"Total: {len(entries)} typed doc entries")

    if dry_run:
        print(f"[DRY RUN] Would write {MANIFEST_PATH}")
    else:
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Manifest written to {MANIFEST_PATH}")

    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Build docs/manifest.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.exit(run(args.dry_run))


if __name__ == "__main__":
    main()
