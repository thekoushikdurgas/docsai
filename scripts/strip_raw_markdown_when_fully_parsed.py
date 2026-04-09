"""
Remove `raw_markdown` from typed doc JSON when `non_parsed_raw_markdown` is empty.

Convention: empty gaps ⇒ structured fields are authoritative; full markdown is omitted.

Usage (from docs/):
    python scripts/strip_raw_markdown_when_fully_parsed.py [--dry-run]
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
from scripts.paths import iter_doc_json_paths  # noqa: E402


def _is_typed_doc(data: dict) -> bool:
    return isinstance(data.get("schema_version"), int) and data.get("kind") in VALID_DOC_KINDS


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Drop raw_markdown when non_parsed_raw_markdown is empty"
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    stripped = unchanged = errors = 0
    for p in iter_doc_json_paths():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ERR {p}: {e}", file=sys.stderr)
            errors += 1
            continue
        if not _is_typed_doc(data):
            unchanged += 1
            continue
        np = (data.get("non_parsed_raw_markdown") or "").strip()
        if np or "raw_markdown" not in data:
            unchanged += 1
            continue
        obj = dict(data)
        del obj["raw_markdown"]
        stripped += 1
        if not args.dry_run:
            p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"stripped raw_markdown: {stripped}  skipped: {unchanged}  errors: {errors}  dry_run={args.dry_run}"
    )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
