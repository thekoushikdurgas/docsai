"""
archive_markdown.py — Phase 1
Copies all *.md files from docs/ (excluding _archive/) to docs/_archive/markdown/
and writes docs/_archive/manifest.json with sha256 + size per file.

Usage (from docs/):
    python scripts/archive_markdown.py [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = DOCS_ROOT / "_archive" / "markdown"
MANIFEST_PATH = DOCS_ROOT / "_archive" / "manifest.json"
TOOL_VERSION = "1.0.0"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_md_files() -> list[Path]:
    """Collect all .md files under DOCS_ROOT, skipping _archive/ subtree."""
    files: list[Path] = []
    for p in sorted(DOCS_ROOT.rglob("*.md")):
        try:
            rel = p.relative_to(DOCS_ROOT)
        except ValueError:
            continue
        parts = rel.parts
        if parts and parts[0] in ("_archive", ".git"):
            continue
        files.append(p)
    return files


def run(dry_run: bool) -> int:
    files = collect_md_files()
    print(f"Found {len(files)} markdown files under {DOCS_ROOT}")

    if dry_run:
        print("[DRY RUN] No files will be written.\n")

    entries = []
    errors = []

    for src in files:
        rel = src.relative_to(DOCS_ROOT)
        dest = ARCHIVE_ROOT / rel
        digest = sha256_file(src)
        size = src.stat().st_size

        entry = {
            "source_path": rel.as_posix(),
            "archive_path": ("_archive/markdown/" + rel.as_posix()),
            "sha256": digest,
            "size_bytes": size,
        }
        entries.append(entry)

        if dry_run:
            print(f"  COPY {rel}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

    if not dry_run:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        manifest = {
            "archived_at": datetime.now(timezone.utc).isoformat(),
            "tool_version": TOOL_VERSION,
            "total_files": len(entries),
            "entries": entries,
        }
        MANIFEST_PATH.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"\nArchived {len(entries)} files to {ARCHIVE_ROOT}")
        print(f"Manifest written to {MANIFEST_PATH}")

        if errors:
            print(f"\n{len(errors)} error(s):")
            for e in errors:
                print(f"  {e}")
            return 1
    else:
        print(f"\n[DRY RUN] Would archive {len(entries)} files.")

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive all docs/*.md files")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    args = parser.parse_args()
    sys.exit(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
