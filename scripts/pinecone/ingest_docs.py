"""Ingest typed docs JSON into Pinecone (docs RAG)."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from paths import DOCS_HUB_DIR, DOCS_ROOT
from metadata.codebase_registry import CODEBASES_DIR, APIS_DIR
from core.scanner import ERA_FOLDERS
from .chunker import chunk_file
from .client import get_docs_index


TOP_LEVEL_TARGETS = [
    "architecture.json",
    "audit-compliance.json",
    "backend.json",
    "codebase.json",
    "docsai-sync.json",
    "flowchart.json",
    "frontend.json",
    "governance.json",
    "index.json",
    "roadmap.json",
    "version-policy.json",
    "versions.json",
]


def _parse_era_idx(folder_name: str) -> Optional[int]:
    m = re.match(r"^(\d+)\.", folder_name)
    return int(m.group(1)) if m else None


def _iter_files_era(era_filter: Optional[str]) -> Iterable[Tuple[int, List[Path]]]:
    for folder in ERA_FOLDERS:
        idx = _parse_era_idx(folder)
        if idx is None:
            continue
        if era_filter is not None and str(idx) != era_filter:
            continue
        era_dir = DOCS_ROOT / folder
        if not era_dir.exists():
            continue
        files = sorted(era_dir.glob("*.json"))
        if files:
            yield idx, files


def _iter_files_hub() -> List[Path]:
    files: List[Path] = []
    if DOCS_HUB_DIR.exists():
        files.extend(sorted(DOCS_HUB_DIR.glob("*.json")))
    for name in TOP_LEVEL_TARGETS:
        p = DOCS_ROOT / name
        if p.exists():
            files.append(p)
    return files


def _iter_files_codebases() -> List[Path]:
    if not CODEBASES_DIR.exists():
        return []
    return sorted(CODEBASES_DIR.glob("*.json"))


def _iter_files_backend() -> List[Path]:
    endpoints_dir = DOCS_ROOT / "backend" / "endpoints"
    files: List[Path] = []
    if APIS_DIR.exists():
        files.extend(sorted(APIS_DIR.glob("*.json")))
    if endpoints_dir.exists():
        files.extend(sorted(endpoints_dir.glob("*.json")))
    return files


def _batch(records: List[Dict], batch_size: int) -> Iterable[List[Dict]]:
    for i in range(0, len(records), batch_size):
        yield records[i : i + batch_size]


def ingest_docs(*, era: Optional[str] = None, dry_run: bool = False) -> Dict[str, object]:
    index = get_docs_index()

    namespaces: Dict[str, List[Path]] = {}
    for era_idx, files in _iter_files_era(era):
        namespaces[f"docs_era_{era_idx}"] = files

    hub_files = _iter_files_hub()
    if hub_files:
        namespaces["docs_global"] = hub_files

    codebases_files = _iter_files_codebases()
    if codebases_files:
        namespaces["docs_codebases"] = codebases_files

    backend_files = _iter_files_backend()
    if backend_files:
        namespaces["docs_backend"] = backend_files

    summary: Dict[str, object] = {
        "dry_run": dry_run,
        "era_filter": era,
        "upserts": [],
        "errors": [],
    }

    for namespace, files in namespaces.items():
        namespace_records = 0
        try:
            upsert_batches = 0
            for p in files:
                records = chunk_file(p)
                # Tolerate field_map differences: include both `content` and `text`.
                for r in records:
                    if "content" in r and "text" not in r:
                        r["text"] = r["content"]
                # Text records must be <= 96 per upsert batch.
                for batch in _batch(records, 96):
                    upsert_batches += 1
                    namespace_records += len(batch)
                    if not dry_run:
                        index.upsert_records(namespace, batch)

            summary["upserts"].append(
                {
                    "namespace": namespace,
                    "files": len(files),
                    "records_upserted": namespace_records,
                    "batches": upsert_batches,
                }
            )
        except Exception as e:
            summary["errors"].append({"namespace": namespace, "error": str(e)})
            continue

        # Mandatory: wait 10+ seconds after upserts before any subsequent search.
        # (We wait after finishing a namespace to satisfy eventual consistency.)
        if not dry_run:
            time.sleep(10)

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest typed docs JSON into Pinecone.")
    parser.add_argument("--era", default=None, help="Only ingest one era (0-10).")
    parser.add_argument("--dry-run", action="store_true", help="Do not upsert; just chunk.")
    args = parser.parse_args()

    summary = ingest_docs(era=args.era, dry_run=bool(args.dry_run))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

