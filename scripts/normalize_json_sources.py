"""
Set each typed doc's source_path to its path relative to docs/ and refresh sha256_source.

sha256_source = SHA-256 of canonical JSON (sorted keys, compact) of the document with
sha256_source omitted — stable logical fingerprint, not the on-disk pretty-print bytes.

Usage (from docs/):
    python scripts/normalize_json_sources.py [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

_DOCS = Path(__file__).resolve().parent.parent
if str(_DOCS) not in sys.path:
    sys.path.insert(0, str(_DOCS))

from scripts.json_scanner import VALID_DOC_KINDS  # noqa: E402
from scripts.paths import JSON_ROOT, iter_doc_json_paths  # noqa: E402


def _canonical_hash(obj: dict) -> str:
    sans = {k: v for k, v in obj.items() if k != "sha256_source"}
    blob = json.dumps(sans, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _is_typed(data: dict) -> bool:
    return isinstance(data.get("schema_version"), int) and data.get("kind") in VALID_DOC_KINDS


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize envelope source_path and sha256_source")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    updated = skipped = errors = 0
    for p in iter_doc_json_paths():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ERR {p}: {e}", file=sys.stderr)
            errors += 1
            continue
        if not _is_typed(data):
            skipped += 1
            continue

        rel = p.relative_to(JSON_ROOT).as_posix()
        new_obj = dict(data)
        new_obj["source_path"] = rel
        new_hash = _canonical_hash(new_obj)
        new_obj["sha256_source"] = new_hash

        if data.get("source_path") == rel and data.get("sha256_source") == new_hash:
            skipped += 1
            continue

        updated += 1
        if not args.dry_run:
            p.write_text(json.dumps(new_obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        f"updated: {updated}  unchanged: {skipped}  errors: {errors}  dry_run={args.dry_run}"
    )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
