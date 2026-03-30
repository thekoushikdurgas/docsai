"""Audit era markdown for missing task tracks and duplicate bullets."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from .models import DocFile, TaskAuditResult, TRACK_NAMES
from .scanner import ERA_FOLDERS, scan_era_only

NORMALIZE_TASK_RE = re.compile(
    r"^- (✅ Completed:|🟡 In Progress:|📌 Planned:|⬜ Incomplete:)\s*",
)


def normalize_task_text(text: str) -> str:
    """Strip status prefix and lowercase for duplicate detection."""
    t = text.strip()
    t = NORMALIZE_TASK_RE.sub("", t)
    return t.lower()


def _missing_tracks(doc: DocFile) -> list[str]:
    if not doc.track_sections:
        # No parsed ### tracks — treat all five as missing if file is patch/minor with tasks expected
        return list(TRACK_NAMES)
    present: dict[str, bool] = {}
    for ts in doc.track_sections:
        present[ts.name] = bool(ts.items)
    missing: list[str] = []
    for name in TRACK_NAMES:
        if not present.get(name):
            missing.append(name)
    return missing


def _empty_task_section(doc: DocFile, content: str) -> bool:
    """True when there is no ## Tasks / ## Task tracks section at all."""
    return "## Tasks" not in content and "## Task tracks" not in content


def audit_file(doc: DocFile, content: str, dup_hashes: dict[str, list[Path]]) -> TaskAuditResult:
    """Audit one DocFile; dup_hashes maps normalized text -> paths (len>1 means duplicate)."""
    missing = _missing_tracks(doc)
    empty_sec = _empty_task_section(doc, content)

    dup_items: list[str] = []
    sections = doc.track_sections
    if not sections:
        from .scanner import extract_track_sections

        sections = extract_track_sections(content)
    for ts in sections:
        for item in ts.items:
            key = normalize_task_text(item)
            if len(key) < 8:
                continue
            paths = dup_hashes.get(key) or []
            if len(paths) > 1 and doc.path in paths:
                dup_items.append(item[:200])

    # Coverage: tracks that exist with at least one item
    filled = sum(1 for n in TRACK_NAMES if any(ts.name == n and ts.items for ts in sections))
    coverage = (filled / len(TRACK_NAMES)) * 100.0

    return TaskAuditResult(
        path=doc.path,
        era=doc.era,
        version=doc.version,
        missing_tracks=missing,
        empty_task_section=empty_sec,
        duplicate_items=dup_items,
        coverage_pct=coverage,
    )


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_duplicate_tasks(era_docs: Iterable[DocFile]) -> dict[str, list[Path]]:
    """Map normalized bullet text -> file paths where it appears (multi-file = duplicate)."""
    bucket: dict[str, list[Path]] = {}
    for doc in era_docs:
        if doc.file_type not in ("patch", "minor"):
            continue
        try:
            content = _read(doc.path)
        except OSError:
            continue
        doc_file = doc.path
        # Prefer parsed tracks
        if doc.track_sections:
            sections = doc.track_sections
        else:
            from .scanner import extract_track_sections

            sections = extract_track_sections(content)
        for ts in sections:
            for item in ts.items:
                key = normalize_task_text(item)
                if len(key) < 8:
                    continue
                bucket.setdefault(key, []).append(doc_file)
    # Dedupe paths per key
    result: dict[str, list[Path]] = {}
    for k, paths in bucket.items():
        uniq = sorted(set(paths), key=lambda p: str(p))
        if len(uniq) > 1:
            result[k] = uniq
    return result


def audit_era(era_idx: int) -> list[TaskAuditResult]:
    if era_idx < 0 or era_idx >= len(ERA_FOLDERS):
        raise ValueError("era must be 0-10")
    era_name = ERA_FOLDERS[era_idx]
    scan = scan_era_only()
    era_docs = [d for d in scan.files if d.era == era_name]
    dup_map = find_duplicate_tasks(era_docs)
    # Flatten to normalized -> paths for audit_file
    dup_hashes: dict[str, list[Path]] = dup_map

    results: list[TaskAuditResult] = []
    for doc in era_docs:
        if doc.file_type not in ("patch", "minor"):
            continue
        try:
            content = _read(doc.path)
        except OSError:
            continue
        results.append(audit_file(doc, content, dup_hashes))
    return results


def audit_all() -> dict[str, list[TaskAuditResult]]:
    """All eras -> list of TaskAuditResult for patch/minor files."""
    out: dict[str, list[TaskAuditResult]] = {}
    for idx in range(len(ERA_FOLDERS)):
        name = ERA_FOLDERS[idx]
        out[name] = audit_era(idx)
    return out
