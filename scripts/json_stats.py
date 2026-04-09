"""
json_stats.py — replaces stats.py
Generates statistics reports from typed JSON under docs/.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from scripts.paths import JSON_ROOT, MANIFEST_PATH, iter_doc_json_paths

TRACK_KEYS = ["contract", "service", "surface", "data", "ops"]


def load_manifest() -> dict | None:
    mp = MANIFEST_PATH
    if not mp.exists():
        return None
    try:
        return json.loads(mp.read_text(encoding="utf-8"))
    except Exception:
        return None


def task_report(era: int | None = None) -> dict:
    """
    Compute per-track coverage stats across all era_task files.
    Returns dict with totals, by_era, and per_track counts.
    """
    by_era: dict[int | str, dict] = defaultdict(lambda: {
        "total_tasks": 0, "by_track": {t: {"total": 0, "completed": 0} for t in TRACK_KEYS}
    })
    grand: dict[str, dict] = {t: {"total": 0, "completed": 0} for t in TRACK_KEYS}

    for p in iter_doc_json_paths():
        try:
            head = p.read_text(encoding="utf-8")[:200]
            if '"era_task"' not in head:
                continue
        except Exception:
            continue

        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

        file_era = data.get("era")
        if era is not None and file_era != era:
            continue

        era_key = file_era if file_era is not None else "unknown"
        tracks = data.get("task_tracks", {})
        for track in TRACK_KEYS:
            items = tracks.get(track, [])
            n = len(items)
            c = sum(1 for i in items if i.get("status") == "completed")
            by_era[era_key]["by_track"][track]["total"] += n
            by_era[era_key]["by_track"][track]["completed"] += c
            by_era[era_key]["total_tasks"] += n
            grand[track]["total"] += n
            grand[track]["completed"] += c

    return {
        "by_era": {str(k): v for k, v in sorted(by_era.items(), key=lambda x: str(x[0]))},
        "grand_total": grand,
    }


def format_task_report(report: dict) -> str:
    lines = ["Task Coverage Report", "=" * 60]
    grand = report["grand_total"]
    for track in TRACK_KEYS:
        t = grand[track]["total"]
        c = grand[track]["completed"]
        pct = f"{100 * c / t:.0f}%" if t else "N/A"
        lines.append(f"  {track:12s}: {c:4d}/{t:4d} completed ({pct})")

    lines.append("\nBy Era:")
    for era_key, era_data in report["by_era"].items():
        lines.append(f"\n  Era {era_key} — {era_data['total_tasks']} tasks")
        for track in TRACK_KEYS:
            bt = era_data["by_track"][track]
            t = bt["total"]
            c = bt["completed"]
            pct = f"{100 * c / t:.0f}%" if t else "N/A"
            lines.append(f"    {track:12s}: {c:4d}/{t:4d} ({pct})")

    return "\n".join(lines)


def era_guide_table() -> str:
    """Print a table of all eras with their index.json titles and child counts."""
    lines = ["Era Guide", "=" * 60,
             f"{'Era':>4}  {'Title':<45}  {'Children':>8}  {'Status':<12}"]
    lines.append("-" * 75)

    for p in sorted(JSON_ROOT.rglob("index.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        ei = data.get("era_index")
        if ei is None:
            continue
        lines.append(
            f"  {ei:>2}  {data.get('title', '')[:45]:<45}  "
            f"{len(data.get('children', [])):>8}  "
            f"{(data.get('status') or ''):<12}"
        )
    return "\n".join(lines)


def overview_stats() -> str:
    """High-level stats from manifest.json."""
    manifest = load_manifest()
    if manifest is None:
        return "manifest.json not found — run build_manifest.py first"

    lines = ["Contact360 Docs Overview", "=" * 60]
    lines.append(f"Total JSON files: {manifest.get('total_files', '?')}")
    lines.append(f"Generated at:     {manifest.get('generated_at', '?')}")
    lines.append("\nBy kind:")
    for kind, count in manifest.get("by_kind", {}).items():
        lines.append(f"  {kind:<20}: {count:>4}")
    return "\n".join(lines)
