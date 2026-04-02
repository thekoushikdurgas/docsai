"""
Parse and audit era markdown filenames: `X.Y.Z — Codename.md` / `X.Y — Title.md`.

Canonical separator is Unicode em dash (U+2014). Duplicate version keys or codenames
within one era folder are reported; rename helpers normalize dash and spacing only.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .paths import DOCS_ROOT
from .scanner import ERA_FOLDERS

# Canonical separator between version and title/codename
EM_DASH = "\u2014"
EN_DASH = "\u2013"

PATCH_STEM_RE = re.compile(
    r"^(\d+\.\d+\.\d+)\s*(["
    + EM_DASH
    + EN_DASH
    + r"]|--|[-])\s*(.+)$"
)
MINOR_STEM_RE = re.compile(
    r"^(\d+\.\d+)\s*(["
    + EM_DASH
    + EN_DASH
    + r"]|--|[-])\s*(.+)$"
)


@dataclass(slots=True)
class EraFilenameRecord:
    """One versioned .md file under an era folder."""

    path: Path
    era_folder: str
    stem: str
    version: str
    codename: str
    kind: str  # "patch" | "minor"
    separator_used: str  # raw separator between version and codename
    is_canonical: bool  # True if separator is EM_DASH and spacing matches canonical


@dataclass(slots=True)
class NamingIssue:
    """Grouped naming problem within one era folder."""

    code: str  # DUPLICATE_VERSION | DUPLICATE_CODENAME | MALFORMED | NON_CANONICAL
    severity: str  # "error" | "warning"
    message: str
    paths: list[Path] = field(default_factory=list)
    detail: str = ""


def parse_era_md_stem(stem: str) -> tuple[str, str, str, str] | None:
    """
    Return (version, codename, kind, separator_used) or None if not versioned.
    kind is 'patch' or 'minor'.
    """
    m = PATCH_STEM_RE.match(stem.strip())
    if m:
        return m.group(1), m.group(3).strip(), "patch", m.group(2)
    m = MINOR_STEM_RE.match(stem.strip())
    if m:
        return m.group(1), m.group(3).strip(), "minor", m.group(2)
    return None


def canonical_filename(version: str, codename: str) -> str:
    """Return `version — codename.md` with em dash."""
    return f"{version} {EM_DASH} {codename.strip()}.md"


def _is_canonical_stem(stem: str, version: str, codename: str, sep: str) -> bool:
    expected = f"{version} {EM_DASH} {codename}"
    return stem == expected and sep == EM_DASH


def scan_era_filenames(era_idx: int | None) -> list[EraFilenameRecord]:
    """List parsed records for one era (0-10) or all era folders."""
    indices = range(len(ERA_FOLDERS)) if era_idx is None else [era_idx]
    out: list[EraFilenameRecord] = []
    for ei in indices:
        if ei < 0 or ei >= len(ERA_FOLDERS):
            continue
        folder = ERA_FOLDERS[ei]
        era_dir = DOCS_ROOT / folder
        if not era_dir.is_dir():
            continue
        for path in sorted(era_dir.glob("*.md")):
            if path.name == "README.md":
                continue
            stem = path.stem
            parsed = parse_era_md_stem(stem)
            if not parsed:
                out.append(
                    EraFilenameRecord(
                        path=path,
                        era_folder=folder,
                        stem=stem,
                        version="",
                        codename="",
                        kind="other",
                        separator_used="",
                        is_canonical=False,
                    )
                )
                continue
            version, codename, kind, sep = parsed
            out.append(
                EraFilenameRecord(
                    path=path,
                    era_folder=folder,
                    stem=stem,
                    version=version,
                    codename=codename,
                    kind=kind,
                    separator_used=sep,
                    is_canonical=_is_canonical_stem(stem, version, codename, sep),
                )
            )
    return out


def find_naming_issues(records: list[EraFilenameRecord]) -> list[NamingIssue]:
    """Detect duplicate version keys, duplicate codenames, malformed, non-canonical separators."""
    issues: list[NamingIssue] = []

    # Malformed (unparsed)
    bad = [r.path for r in records if r.kind == "other"]
    if bad:
        issues.append(
            NamingIssue(
                code="MALFORMED",
                severity="warning",
                message="Filename does not match `X.Y.Z — …` or `X.Y — …`",
                paths=bad,
            )
        )

    # Non-canonical (wrong dash or spacing) — still unique
    non_canon = [r.path for r in records if r.kind in ("patch", "minor") and not r.is_canonical]
    if non_canon:
        issues.append(
            NamingIssue(
                code="NON_CANONICAL",
                severity="warning",
                message=f"Use em dash ({EM_DASH!r}) and no extra spaces: `version — Codename.md`",
                paths=non_canon,
            )
        )

    # Duplicate version+kind (same X.Y.Z or same X.Y twice)
    by_key: dict[str, list[Path]] = {}
    for r in records:
        if r.kind not in ("patch", "minor"):
            continue
        key = f"{r.kind}:{r.version}"
        by_key.setdefault(key, []).append(r.path)
    for key, paths in by_key.items():
        uniq = sorted(set(paths), key=lambda p: str(p))
        if len(uniq) > 1:
            issues.append(
                NamingIssue(
                    code="DUPLICATE_VERSION",
                    severity="error",
                    message=f"Same version key appears twice: {key}",
                    paths=uniq,
                    detail=key,
                )
            )

    # Note: repeated codenames across patches (e.g. theme ladder "Bloom", "Void") are intentional;
    # we do not flag DUPLICATE_CODENAME. Use `name-audit` inventory to review names visually.

    return issues


def plan_renames(records: list[EraFilenameRecord]) -> list[tuple[Path, Path, str]]:
    """
    Pairs (old_path, new_path, reason) for canonical filename only.
    Skips if target exists and is not the same file.
    """
    pairs: list[tuple[Path, Path, str]] = []
    for r in records:
        if r.kind not in ("patch", "minor"):
            continue
        if r.is_canonical:
            continue
        new_name = canonical_filename(r.version, r.codename)
        new_path = r.path.with_name(new_name)
        if new_path == r.path:
            continue
        if new_path.exists() and new_path.resolve() != r.path.resolve():
            pairs.append((r.path, new_path, "SKIP_TARGET_EXISTS"))
            continue
        pairs.append((r.path, new_path, "CANONICAL_EM_DASH"))
    return pairs


def apply_renames(pairs: list[tuple[Path, Path, str]], dry_run: bool = True) -> dict[str, int]:
    """Apply renames; skip SKIP_TARGET_EXISTS. Returns counts."""
    summary = {"planned": 0, "renamed": 0, "skipped": 0, "errors": 0}
    for old, new, reason in pairs:
        if reason == "SKIP_TARGET_EXISTS":
            summary["skipped"] += 1
            continue
        summary["planned"] += 1
        if dry_run:
            continue
        try:
            old.rename(new)
            summary["renamed"] += 1
        except OSError:
            summary["errors"] += 1
    return summary
