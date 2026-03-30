#!/usr/bin/env python3
"""Rename docs/tech/*.md from chat-derived filenames to canonical slugs."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .paths import DOCS_ROOT

# Old stem (without .md) -> new filename (with .md)
RENAME_MAP: dict[str, str] = {
    "why best extension framework , and what is the bea": "tech-extension-why-practices.md",
    "give me 100 checklist that to use full power of ex": "tech-extension-checklist-100.md",
    "why best go gin framework , and what is the beat p": "tech-go-gin-why-practices.md",
    "give me 100 checklist that to use full power of go": "tech-go-gin-checklist-100.md",
    "why best next js framework , and what is the beat": "tech-nextjs-why-practices.md",
    "give me 100 checklist that to use full power of ne": "tech-nextjs-checklist-100.md",
    "why best django python framework , and what is the": "tech-django-why-practices.md",
    "give me 100 checklist that to use full power of dj": "tech-django-checklist-100.md",
}


def tech_dir_default() -> Path:
    return DOCS_ROOT / "tech"


def plan_renames(tech_dir: Path | None = None) -> list[tuple[Path, Path]]:
    """Return list of (src, dst) for existing sources."""
    td = tech_dir or tech_dir_default()
    out: list[tuple[Path, Path]] = []
    if not td.is_dir():
        return out
    for old_stem, new_name in RENAME_MAP.items():
        src = td / f"{old_stem}.md"
        dst = td / new_name
        if src.is_file():
            out.append((src, dst))
    return out


def main(apply: bool = False, *, tech_dir: Path | None = None) -> int:
    pairs = plan_renames(tech_dir)
    if not pairs:
        print("No matching docs/tech/ files to rename (already canonical or missing).", file=sys.stderr)
        return 0

    for src, dst in pairs:
        if apply:
            if dst.exists() and dst.resolve() != src.resolve():
                print(f"Skip (target exists): {dst.name}", file=sys.stderr)
                continue
            src.rename(dst)
            print(f"Renamed: {src.name} -> {dst.name}")
        else:
            print(f"Would rename: {src.name} -> {dst.name}")

    if not apply:
        print(f"[dry-run] {len(pairs)} rename(s); pass --apply to execute.")
    return 0


if __name__ == "__main__":
    _docs = Path(__file__).resolve().parent.parent
    if str(_docs) not in sys.path:
        sys.path.insert(0, str(_docs))
    ap = argparse.ArgumentParser(description="Rename docs/tech/ files to canonical names")
    ap.add_argument("--apply", action="store_true", help="Perform renames")
    args = ap.parse_args()
    raise SystemExit(main(apply=args.apply, tech_dir=_docs / "tech"))
