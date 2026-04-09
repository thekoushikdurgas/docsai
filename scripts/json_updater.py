"""
json_updater.py — replaces updater.py
Provides field-level read/write operations on JSON doc files.
Used by cli.py commands like `update --status` and `update --field`.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.paths import JSON_ROOT, iter_doc_json_paths

VALID_STATUSES = {"completed", "in_progress", "planned", "incomplete"}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(data: dict, path: Path) -> None:
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def update_status(json_path: Path, status: str) -> bool:
    """Update the top-level `status` field of a JSON file."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status {status!r}; must be one of {VALID_STATUSES}")
    data = _load(json_path)
    old = data.get("status")
    data["status"] = status
    _save(data, json_path)
    print(f"  Updated {json_path.name}: status {old!r} → {status!r}")
    return True


def update_field(json_path: Path, field: str, value: Any) -> bool:
    """Update any top-level field in a JSON file."""
    data = _load(json_path)
    old = data.get(field)
    data[field] = value
    _save(data, json_path)
    print(f"  Updated {json_path.name}: {field} {old!r} → {value!r}")
    return True


def update_task_status(json_path: Path, track: str, task_index: int, status: str) -> bool:
    """Update the status of a specific task item in an era_task file."""
    if status not in {*VALID_STATUSES, "unknown"}:
        raise ValueError(f"Invalid task status: {status!r}")
    data = _load(json_path)
    tracks = data.get("task_tracks", {})
    task_list = tracks.get(track, [])
    if task_index >= len(task_list):
        raise IndexError(f"Task index {task_index} out of range for track {track!r} (len={len(task_list)})")
    old = task_list[task_index].get("status")
    task_list[task_index]["status"] = status
    data["task_tracks"][track] = task_list
    _save(data, json_path)
    print(f"  Updated task [{track}][{task_index}]: status {old!r} → {status!r}")
    return True


def find_json_by_source(source_path: str) -> Path | None:
    """Locate a JSON file by its source_path field."""
    for p in iter_doc_json_paths():
        try:
            data = json.loads(p.read_text(encoding="utf-8")[:500])
            if data.get("source_path") == source_path:
                return p
        except Exception:
            continue
    return None


def find_json_by_version(version: str, era: int | None = None) -> list[Path]:
    """Find era_task JSON files matching a version string."""
    results = []
    for p in iter_doc_json_paths():
        try:
            head = p.read_text(encoding="utf-8")[:300]
            if '"era_task"' not in head:
                continue
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("version") == version:
                if era is None or data.get("era") == era:
                    results.append(p)
        except Exception:
            continue
    return results


def update_index_children(index_path: Path) -> bool:
    """Refresh children[] in an index.json from sibling JSON files."""
    data = _load(index_path)
    folder = index_path.parent
    children = []
    for sibling in sorted(folder.iterdir()):
        if sibling.name == "index.json" or sibling.suffix != ".json":
            continue
        if sibling.is_dir():
            continue
        try:
            sdata = json.loads(sibling.read_text(encoding="utf-8"))
            if not isinstance(sdata.get("schema_version"), int):
                continue
            children.append({
                "title": sdata.get("title", sibling.stem),
                "path": sibling.name,
                "kind": sdata.get("kind", "document"),
                "version": sdata.get("version"),
                "status": sdata.get("status"),
            })
        except Exception:
            pass
    data["children"] = children
    _save(data, index_path)
    print(f"  Refreshed {index_path.name}: {len(children)} children")
    return True
