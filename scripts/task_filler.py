"""Fill missing task tracks and deduplicate bullets in era markdown."""
from __future__ import annotations

from pathlib import Path

from .codebase_registry import load_registry
from .models import TRACK_NAMES
from .scanner import ERA_FOLDERS, TASK_SECTION_HEADERS
from .task_auditor import find_duplicate_tasks, normalize_task_text
from .task_templates import generate_templates, replacement_for_duplicate
from .updater import atomic_write


def _era_index_from_path(path: Path) -> int:
    parent = path.parent.name
    for i, name in enumerate(ERA_FOLDERS):
        if name == parent:
            return i
    return 0


def _version_for_templates(doc) -> str:
    v = doc.version
    if doc.file_type == "minor":
        parts = v.split(".")
        if len(parts) == 2 and all(p.isdigit() for p in parts):
            return f"{parts[0]}.{parts[1]}.0"
    if doc.file_type not in ("patch", "minor"):
        return "0.0.0"
    return v


def _tasks_block_span(content: str) -> tuple[int, int] | None:
    """Line indices [start, end) of ## Tasks / ## Task tracks body."""
    lines = content.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if line.strip() in TASK_SECTION_HEADERS:
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        line = lines[j]
        if line.startswith("## ") and not line.startswith("###"):
            end = j
            break
    return (start, end)


def fill_missing_tracks(
    path: Path,
    era_idx: int | None,
    registry: dict | None,
    dry_run: bool = True,
) -> tuple[bool, int]:
    """
    Insert missing ### Contract|Service|Surface|Data|Ops sections with generated bullets.
    Returns (changed, diff_line_estimate).
    """
    reg = registry if registry is not None else load_registry()
    if era_idx is None:
        era_idx = _era_index_from_path(path)
    content = path.read_text(encoding="utf-8")
    from .scanner import parse_file

    doc = parse_file(path)
    version = _version_for_templates(doc)

    templates = generate_templates(era_idx, version, reg)
    present = {ts.name for ts in doc.track_sections if ts.items}
    missing = [n for n in TRACK_NAMES if n not in present]

    if not missing:
        return False, 0

    lines = content.splitlines(keepends=True)
    span = _tasks_block_span(content)

    if span is None:
        insert_at = len(lines)
        for i, line in enumerate(lines):
            if line.strip() == "## Service task slices":
                insert_at = i
                break
        block_lines: list[str] = ["## Tasks\n", "\n"]
        for name in missing:
            block_lines.append(f"### {name}\n\n")
            for bullet in templates.get(name, []):
                block_lines.append(bullet + "\n")
            block_lines.append("\n")
        new_lines = lines[:insert_at] + block_lines + lines[insert_at:]
        new_content = "".join(new_lines)
    else:
        start, end = span
        additions = ""
        for name in missing:
            additions += f"\n### {name}\n\n"
            for bullet in templates.get(name, []):
                additions += bullet + "\n"
            additions += "\n"
        inner = "".join(lines[start:end])
        new_inner = inner + additions
        new_lines = lines[:start] + [new_inner] + lines[end:]
        new_content = "".join(new_lines)

    changed = new_content != content
    diff_lines = abs(len(new_content.splitlines()) - len(content.splitlines())) if changed else 0
    if changed and not dry_run:
        atomic_write(path, new_content)
    return changed, diff_lines


def deduplicate_file_tasks(
    path: Path,
    era_idx: int | None,
    dup_map: dict[str, list[Path]] | None,
    registry: dict | None,
    dry_run: bool = True,
) -> tuple[bool, int]:
    """
    Replace duplicate task bullets (same normalized text as sibling files) with patch-specific lines.
    """
    reg = registry if registry is not None else load_registry()
    if era_idx is None:
        era_idx = _era_index_from_path(path)
    content = path.read_text(encoding="utf-8")
    from .scanner import parse_file

    doc = parse_file(path)
    version = _version_for_templates(doc)

    if dup_map is None:
        from .scanner import scan_era_only

        era_name = path.parent.name
        era_docs = [d for d in scan_era_only().files if d.era == era_name]
        dup_map = find_duplicate_tasks(era_docs)

    lines = content.splitlines(keepends=True)
    in_tasks = False
    changed = False
    new_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if line.startswith("## "):
            in_tasks = stripped in TASK_SECTION_HEADERS
            new_lines.append(line)
            continue
        if not in_tasks:
            new_lines.append(line)
            continue
        if stripped.startswith("- "):
            body = stripped[2:].strip()
            key = normalize_task_text(body)
            paths = dup_map.get(key) if key in dup_map else None
            if paths and len(paths) > 1 and path in paths and len(key) >= 8:
                rep = replacement_for_duplicate(era_idx, version, key, reg)
                new_lines.append(rep + "\n")
                changed = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    new_content = "".join(new_lines)
    diff_lines = abs(len(new_content.splitlines()) - len(content.splitlines())) if changed else 0
    if changed and not dry_run:
        atomic_write(path, new_content)
    return changed, diff_lines


def bulk_fill(
    paths: list[Path],
    registry: dict | None = None,
    dry_run: bool = True,
    dedup: bool = False,
) -> dict[str, int]:
    """Run fill_missing_tracks on each path; optionally dedup after per file."""
    reg = registry if registry is not None else load_registry()
    summary: dict[str, int] = {
        "files": 0,
        "changed": 0,
        "diff_lines": 0,
        "tracks_added": 0,
        "tasks_added": 0,
    }
    era_dup_cache: dict[str, dict[str, list[Path]]] = {}

    for path in paths:
        if not path.exists() or path.suffix.lower() != ".md":
            continue
        summary["files"] += 1
        era_idx = _era_index_from_path(path)
        ch, dl = fill_missing_tracks(path, era_idx, reg, dry_run=dry_run)
        if ch:
            summary["changed"] += 1
            summary["diff_lines"] += dl
            summary["tracks_added"] += 5
        if dedup:
            parent = path.parent.name
            if parent not in era_dup_cache:
                from .scanner import scan_era_only

                era_docs = [d for d in scan_era_only().files if d.era == parent]
                era_dup_cache[parent] = find_duplicate_tasks(era_docs)
            ch2, dl2 = deduplicate_file_tasks(
                path, era_idx, era_dup_cache[parent], reg, dry_run=dry_run
            )
            if ch2:
                summary["changed"] += 1
                summary["diff_lines"] += dl2
    return summary
