"""
generate_indexes.py — Phase 3
Enriches every docs/**/index.json with:
  - children[] list built from sibling typed JSON files
  - updated_at timestamp
  - folder + era_index derived from path

Run after adding or renaming JSON docs (optional; safe to re-run).

Usage (from docs/):
    python scripts/generate_indexes.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_DOCS = Path(__file__).resolve().parent.parent
if str(_DOCS) not in sys.path:
    sys.path.insert(0, str(_DOCS))

from scripts.paths import DOCS_ROOT, JSON_ROOT
ERA_FOLDER_RE = re.compile(r"^(\d{1,2})\.\s+")


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  WARN: could not read {path}: {e}", file=sys.stderr)
        return None


def save_json(obj: dict, path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"  [DRY] would update {path.relative_to(DOCS_ROOT)}")
        return
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def find_all_index_jsons() -> list[Path]:
    """Find every index.json under JSON_ROOT."""
    return sorted(JSON_ROOT.rglob("index.json"))


def build_children(index_path: Path) -> list[dict]:
    """Scan sibling JSON files and build children[] list."""
    folder = index_path.parent
    children: list[dict] = []

    for sibling in sorted(folder.iterdir()):
        if sibling.name == "index.json" or sibling.suffix != ".json":
            continue
        if sibling.is_dir():
            continue
        data = load_json(sibling)
        if data is None:
            continue
        child = {
            "title": data.get("title", sibling.stem),
            "path": sibling.name,
            "kind": data.get("kind", "document"),
            "version": data.get("version"),
            "status": data.get("status"),
        }
        children.append(child)

    return children


def enrich_index(index_path: Path, dry_run: bool) -> bool:
    data = load_json(index_path)
    if data is None:
        return False

    # Build children from sibling JSON files
    data["children"] = build_children(index_path)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()

    # Derive folder-level info from JSON root path
    rel_folder = index_path.parent.relative_to(JSON_ROOT)
    folder_str = rel_folder.as_posix() if str(rel_folder) != "." else "."

    # era_index from folder name
    if rel_folder.parts:
        em = ERA_FOLDER_RE.match(rel_folder.parts[0])
        if em:
            data["era_index"] = int(em.group(1))

    data["folder"] = folder_str

    save_json(data, index_path, dry_run)
    return True


def run(dry_run: bool) -> int:
    indexes = find_all_index_jsons()
    print(f"Found {len(indexes)} index.json files to enrich")

    ok = fail = 0
    for idx_path in indexes:
        if enrich_index(idx_path, dry_run):
            ok += 1
            print(f"  ✓ {idx_path.relative_to(JSON_ROOT)}: {len(build_children(idx_path))} children")
        else:
            fail += 1

    print(f"\nDone: {ok} enriched, {fail} errors")
    return 0 if fail == 0 else 1


def main() -> None:
    ap = argparse.ArgumentParser(description="Enrich index.json files with children[] and metadata")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.exit(run(args.dry_run))


if __name__ == "__main__":
    main()
