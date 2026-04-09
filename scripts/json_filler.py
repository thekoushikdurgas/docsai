"""
json_filler.py — replaces task_filler.py
Injects missing task_track keys into era_task JSON files.
If a track key is absent or empty, an empty list [] is inserted.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from scripts.paths import JSON_ROOT, iter_doc_json_paths

TRACK_KEYS = ["contract", "service", "surface", "data", "ops"]


def fill_file(path: Path, dry_run: bool = False) -> dict[str, bool]:
    """
    Ensure all five track keys exist in task_tracks.
    Returns dict of {track_key: was_added}.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ERROR reading {path}: {e}")
        return {}

    if data.get("kind") != "era_task":
        return {}

    tracks = data.setdefault("task_tracks", {})
    added: dict[str, bool] = {}
    for key in TRACK_KEYS:
        if key not in tracks:
            tracks[key] = []
            added[key] = True
        else:
            added[key] = False

    if any(added.values()):
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        if not dry_run:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    return added


def fill_era(era: int | None = None, dry_run: bool = False) -> int:
    """Fill all era_task files, optionally for a specific era. Returns count of files modified."""
    modified = 0
    for p in iter_doc_json_paths():
        rel = p.relative_to(JSON_ROOT)
        try:
            head = p.read_text(encoding="utf-8")[:200]
            if '"era_task"' not in head:
                continue
        except Exception:
            continue

        if era is not None:
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if data.get("era") != era and data.get("era_index") != era:
                    continue
            except Exception:
                continue

        added = fill_file(p, dry_run=dry_run)
        if any(added.values()):
            keys = [k for k, v in added.items() if v]
            action = "[DRY]" if dry_run else "✓"
            print(f"  {action} {rel} → added tracks: {', '.join(keys)}")
            modified += 1

    return modified
