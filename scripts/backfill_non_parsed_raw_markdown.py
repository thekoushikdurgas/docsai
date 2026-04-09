"""
Backfill `non_parsed_raw_markdown` on every typed doc JSON under docs/.

Usage (from docs/):
    python scripts/backfill_non_parsed_raw_markdown.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_DOCS = Path(__file__).resolve().parent.parent
if str(_DOCS) not in sys.path:
    sys.path.insert(0, str(_DOCS))

from scripts.json_scanner import VALID_DOC_KINDS  # noqa: E402
from scripts.non_parsed_markdown import patch_json_object  # noqa: E402
from scripts.paths import iter_doc_json_paths  # noqa: E402


def _is_typed_doc(data: dict) -> bool:
    return isinstance(data.get("schema_version"), int) and data.get("kind") in VALID_DOC_KINDS


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill non_parsed_raw_markdown on typed JSON docs")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    changed = skipped = errors = 0
    for p in iter_doc_json_paths():
        try:
            raw = p.read_text(encoding="utf-8")
            data = json.loads(raw)
        except Exception as e:
            print(f"  ERR {p}: {e}", file=sys.stderr)
            errors += 1
            continue
        if not _is_typed_doc(data):
            skipped += 1
            continue
        new_obj, did_change = patch_json_object(data)
        if not did_change:
            skipped += 1
            continue
        changed += 1
        if not args.dry_run:
            p.write_text(json.dumps(new_obj, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Updated: {changed}  unchanged: {skipped}  errors: {errors}  dry_run={args.dry_run}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
