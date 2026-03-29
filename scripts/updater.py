from __future__ import annotations

import re
import tempfile
from pathlib import Path

from .models import Status
from .scanner import DOCS_ROOT, ERA_FOLDERS

STATUS_LINE_RE = re.compile(r"^(- \*\*Status:\*\*)\s+(.+?)\s*$", re.MULTILINE)
TASK_SECTION_HEADERS = {"## Tasks", "## Task tracks"}
TASK_PREFIX_RE = re.compile(r"^- (✅ Completed:|🟡 In Progress:|📌 Planned:|⬜ Incomplete:)\s*")

STATUS_ALIASES: dict[str, Status] = {
    "completed": Status.COMPLETED,
    "complete": Status.COMPLETED,
    "✅ completed": Status.COMPLETED,
    "in_progress": Status.IN_PROGRESS,
    "in progress": Status.IN_PROGRESS,
    "🟡 in progress": Status.IN_PROGRESS,
    "planned": Status.PLANNED,
    "📌 planned": Status.PLANNED,
    "incomplete": Status.INCOMPLETE,
    "⬜ incomplete": Status.INCOMPLETE,
}


def normalize_header_status(content: str, new_status: Status) -> str:
    def _replace(match: re.Match[str]) -> str:
        return f"{match.group(1)} {new_status.label}"

    return STATUS_LINE_RE.sub(_replace, content)


def normalize_task_bullets(content: str, new_status: Status, force: bool = True) -> str:
    lines = content.splitlines(keepends=True)
    in_tasks = False
    updated: list[str] = []

    for line in lines:
        stripped = line.strip()
        if line.startswith("## "):
            in_tasks = stripped in TASK_SECTION_HEADERS
            updated.append(line)
            continue
        if not in_tasks:
            updated.append(line)
            continue
        if not stripped.startswith("- "):
            updated.append(line)
            continue

        body = stripped[2:].strip()
        if TASK_PREFIX_RE.match(stripped):
            if not force:
                updated.append(line)
                continue
            body = TASK_PREFIX_RE.sub("", stripped[2:]).strip()
        updated.append(f"- {new_status.label}: {body}\n")

    return "".join(updated)


def _atomic_write(path: Path, content: str) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=str(path.parent))
    try:
        with open(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        Path(temp_name).replace(path)
    finally:
        temp_path = Path(temp_name)
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)


def atomic_write(path: Path, content: str) -> None:
    """Public alias for atomic file replace (used by task_filler)."""
    _atomic_write(path, content)


def update_file(
    path: Path,
    new_status: Status,
    update_tasks: bool = True,
    dry_run: bool = True,
    force: bool = True,
) -> tuple[bool, int]:
    original = path.read_text(encoding="utf-8")
    updated = normalize_header_status(original, new_status)
    if update_tasks:
        updated = normalize_task_bullets(updated, new_status, force=force)

    changed = updated != original
    if changed and not dry_run:
        _atomic_write(path, updated)

    diff_lines = 0
    if changed:
        original_lines = original.splitlines()
        updated_lines = updated.splitlines()
        diff_lines = abs(len(updated_lines) - len(original_lines))
        if diff_lines == 0:
            diff_lines = sum(1 for i, line in enumerate(updated_lines) if line != original_lines[i])
    return changed, diff_lines


def list_scope_paths(scope: str, era: int | None = None, file_path: str | None = None) -> list[Path]:
    if scope == "file":
        if not file_path:
            raise ValueError("file_path is required for scope=file")
        path = Path(file_path)
        return [path if path.is_absolute() else (DOCS_ROOT / path)]

    if scope == "era":
        if era is None or era < 0 or era >= len(ERA_FOLDERS):
            raise ValueError("era must be between 0 and 10 for scope=era")
        era_dir = DOCS_ROOT / ERA_FOLDERS[era]
        return sorted(era_dir.glob("*.md"))

    if scope == "all":
        paths: list[Path] = []
        for folder in ERA_FOLDERS:
            paths.extend(sorted((DOCS_ROOT / folder).glob("*.md")))
        return paths

    raise ValueError("scope must be one of: file, era, all")


def bulk_update(
    paths: list[Path],
    new_status: Status,
    update_tasks: bool = True,
    dry_run: bool = True,
    force: bool = True,
) -> dict[str, int]:
    summary = {"files": 0, "changed": 0, "diff_lines": 0}
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".md":
            continue
        summary["files"] += 1
        changed, diff_lines = update_file(
            path=path,
            new_status=new_status,
            update_tasks=update_tasks,
            dry_run=dry_run,
            force=force,
        )
        if changed:
            summary["changed"] += 1
            summary["diff_lines"] += diff_lines
    return summary

