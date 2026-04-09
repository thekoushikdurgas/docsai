"""
json_auditor.py — replaces task_auditor.py
Reads era_task.json files and audits task_tracks completeness.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from scripts.paths import JSON_ROOT, iter_doc_json_paths

TRACK_KEYS = ["contract", "service", "surface", "data", "ops"]


def iter_era_task_files(era: int | None = None) -> Iterator[Path]:
    for p in iter_doc_json_paths():
        try:
            # Quick check: peek at the file
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
        yield p


class AuditResult:
    def __init__(self, path: Path, data: dict):
        self.path = path
        self.data = data
        self.issues: list[str] = []

    @property
    def title(self) -> str:
        return self.data.get("title", self.path.stem)

    @property
    def version(self) -> str | None:
        return self.data.get("version")

    def check_tracks(self) -> "AuditResult":
        tracks = self.data.get("task_tracks", {})
        if not tracks:
            self.issues.append("task_tracks missing entirely")
        else:
            for key in TRACK_KEYS:
                if key not in tracks:
                    self.issues.append(f"track '{key}' missing")
                elif not isinstance(tracks[key], list):
                    self.issues.append(f"track '{key}' is not a list")
                # Note: empty list is allowed (non-standard source structure);
                # treat as warning in format_audit_report, not as error
        return self

    @property
    def ok(self) -> bool:
        return len(self.issues) == 0

    def track_counts(self) -> dict[str, int]:
        tracks = self.data.get("task_tracks", {})
        return {k: len(tracks.get(k, [])) for k in TRACK_KEYS}


def audit_era(era: int | None = None) -> list[AuditResult]:
    """Audit all era_task files, optionally for a specific era."""
    results: list[AuditResult] = []
    for path in iter_era_task_files(era=era):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            r = AuditResult(path, {})
            r.issues.append(f"JSON parse error: {e}")
            results.append(r)
            continue
        r = AuditResult(path, data)
        r.check_tracks()
        results.append(r)
    return results


def format_audit_report(results: list[AuditResult]) -> str:
    lines = []
    ok = sum(1 for r in results if r.ok)
    lines.append(f"Audited {len(results)} era_task files: {ok} ok, {len(results) - ok} with issues\n")

    for r in results:
        status = "✅" if r.ok else "❌"
        tc = r.track_counts()
        counts_str = " ".join(f"{k[:3]}={v}" for k, v in tc.items())
        lines.append(f"  {status} {r.path.relative_to(JSON_ROOT)}")
        lines.append(f"       {counts_str}")
        # Warn about empty tracks (not errors — they have the key but no items)
        empty = [k for k in TRACK_KEYS if tc.get(k, 0) == 0]
        if empty:
            lines.append(f"       ⚠ empty tracks: {', '.join(empty)}")
        for issue in r.issues:
            lines.append(f"       ❌ {issue}")

    return "\n".join(lines)
