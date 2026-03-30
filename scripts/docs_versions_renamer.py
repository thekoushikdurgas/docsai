"""
Rename Contact360 "version_X.Y.md" files to "X.Y — <Title>.md" and rewrite markdown links.

Usage examples (PowerShell):
  python scripts\\docs_versions_renamer.py --docs-root .\\docs --mode all --dry-run
  python scripts\\docs_versions_renamer.py --docs-root .\\docs --mode all --apply

Defaults:
  - docs-root: <repo_root>/docs (inferred from this file)
  - mode: all (rename + link rewrite + verify)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

from docs_versions_utils import (
    DASH,
    VersionRef,
    compute_new_filename,
    extract_title_from_version_file,
    iter_markdown_files,
    parse_old_version_filename,
)


@dataclass(frozen=True)
class RenameAction:
    old_path: str
    new_path: str
    era: int
    minor: int
    old_base: str
    new_base: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text_if_changed(path: Path, new_text: str) -> bool:
    old_text = read_text(path)
    if old_text == new_text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def discover_old_version_files(docs_root: Path, eras: Optional[set[int]]) -> list[Path]:
    old_files: list[Path] = []
    for p in docs_root.rglob("version_*.md"):
        if not p.is_file():
            continue
        ref = parse_old_version_filename(p.name)
        if not ref:
            continue
        if eras is not None and ref.era not in eras:
            continue
        old_files.append(p)
    return sorted(old_files)


def build_rename_actions(old_files: Iterable[Path]) -> list[RenameAction]:
    actions: list[RenameAction] = []
    for p in old_files:
        ref = parse_old_version_filename(p.name)
        if not ref:
            continue
        text = read_text(p)
        raw_title = extract_title_from_version_file(text, ref.era, ref.minor)
        if raw_title is None:
            raw_title = ""
        new_base = compute_new_filename(ref.era, ref.minor, raw_title)
        new_path = p.with_name(new_base)
        actions.append(
            RenameAction(
                old_path=str(p),
                new_path=str(new_path),
                era=ref.era,
                minor=ref.minor,
                old_base=ref.old_base,
                new_base=new_path.name,
            )
        )
    return actions


def maybe_rename(actions: list[RenameAction], apply: bool, on_conflict: str) -> None:
    # on_conflict: "error" | "skip"
    for a in actions:
        old_path = Path(a.old_path)
        new_path = Path(a.new_path)

        if old_path.resolve() == new_path.resolve():
            continue
        if new_path.exists():
            if on_conflict == "skip":
                continue
            raise FileExistsError(f"Target already exists: {new_path}")
        if not apply:
            print(f"[dry-run] rename: {a.old_base} -> {a.new_base}")
            continue

        # Use rename/move so that filesystem metadata is preserved as much as possible.
        new_path.parent.mkdir(parents=True, exist_ok=True)
        old_path.rename(new_path)
        print(f"[apply] rename: {a.old_base} -> {a.new_base}")


def rewrite_markdown_links(docs_root: Path, mapping: Dict[str, str], apply: bool) -> int:
    """
    Replace occurrences of old filename base (e.g., version_2.0.md) with new base.
    This updates:
      - link targets: (../path/version_2.0.md)
      - link labels: [`version_2.0.md`](...)
      - inline text/code spans
    """
    md_files = iter_markdown_files(docs_root)
    changed = 0
    for f in md_files:
        text = read_text(f)
        new_text = text
        for old_base, new_base in mapping.items():
            if old_base in new_text:
                new_text = new_text.replace(old_base, new_base)
        if new_text != text:
            if apply:
                f.write_text(new_text, encoding="utf-8")
            changed += 1
            print(("[apply]" if apply else "[dry-run]") + f" rewrite: {f.relative_to(docs_root)}")
    return changed


def verify_no_old_patterns(docs_root: Path, eras: Optional[set[int]], mapping: Dict[str, str]) -> Dict[str, int]:
    """
    Verify by counting remaining occurrences of old bases.
    """
    counts: Dict[str, int] = {}
    old_bases = list(mapping.keys())
    if not old_bases:
        return counts

    all_md = iter_markdown_files(docs_root)
    for old_base in old_bases:
        pattern = old_base  # literal
        total = 0
        for f in all_md:
            txt = read_text(f)
            total += txt.count(pattern)
        counts[old_base] = total
    return counts


def parse_eras_csv(s: str) -> set[int]:
    out: set[int] = set()
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        out.add(int(part))
    return out


def main(argv: Optional[list[str]] = None) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    default_docs_root = repo_root / "docs"

    ap = argparse.ArgumentParser()
    ap.add_argument("--docs-root", type=str, default=str(default_docs_root))
    ap.add_argument("--mode", type=str, default="all", choices=["rename", "links", "all", "verify"])
    ap.add_argument("--apply", action="store_true", help="Actually write changes (no effect without --apply).")
    ap.add_argument("--dry-run", action="store_true", help="Alias for not applying changes.")
    ap.add_argument("--eras", type=str, default="", help="Comma-separated era numbers to rename (e.g. 2,3,4). Empty = all discovered.")
    ap.add_argument("--on-conflict", type=str, default="error", choices=["error", "skip"])
    ap.add_argument("--report-json", type=str, default="", help="Optional path to write rename mapping report JSON.")
    args = ap.parse_args(argv)

    docs_root = Path(args.docs_root)
    if not docs_root.exists():
        raise FileNotFoundError(f"docs-root does not exist: {docs_root}")

    apply = bool(args.apply) and not bool(args.dry_run)
    eras: Optional[set[int]] = None
    if args.eras.strip():
        eras = parse_eras_csv(args.eras)

    # 1) Discover old files
    old_files = discover_old_version_files(docs_root, eras)
    if not old_files:
        print("No old version_X.Y.md files discovered. Nothing to rename/link.")
        return 0

    # 2) Build actions
    actions = build_rename_actions(old_files)

    # mapping: old_base -> new_base
    mapping: Dict[str, str] = {a.old_base: a.new_base for a in actions}

    report = {
        "docs_root": str(docs_root),
        "mode": args.mode,
        "apply": apply,
        "eras_filter": sorted(list(eras)) if eras is not None else None,
        "actions": [
            {
                "old_path": a.old_path,
                "new_path": a.new_path,
                "era": a.era,
                "minor": a.minor,
                "old_base": a.old_base,
                "new_base": a.new_base,
            }
            for a in actions
        ],
        "mapping": mapping,
    }

    if args.report_json:
        out_path = Path(args.report_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote report: {out_path}")

    # 3) Rename
    if args.mode in ("rename", "all"):
        maybe_rename(actions, apply=apply, on_conflict=args.on_conflict)

    # 4) Links update
    if args.mode in ("links", "all"):
        changed = rewrite_markdown_links(docs_root, mapping=mapping, apply=apply)
        print(f"Markdown files with changes: {changed}")

    # 5) Verify
    if args.mode in ("verify", "all"):
        counts = verify_no_old_patterns(docs_root, eras=eras, mapping=mapping)
        remaining = {k: v for k, v in counts.items() if v != 0}
        if remaining:
            print("Verification: remaining old filenames detected:")
            for k, v in sorted(remaining.items()):
                print(f"  {k}: {v}")
            # For dry-run, remaining old filenames are expected.
            if apply:
                return 2
            print("(Dry-run mode: verification failures are not treated as errors.)")
            return 0
        print("Verification: no remaining old version_X.Y.md filenames found.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

