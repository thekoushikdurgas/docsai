"""
Load phase metadata from the monorepo ``docs/`` tree (sibling of ``contact360.io/``).

Used by architecture and roadmap admin views so the console stays aligned with
``docs/PHASE-DOCS-INDEX.md`` without duplicating tables by hand.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)


def repo_docs_root() -> Path | None:
    """``contact360/docs`` when running from the monorepo; else ``None``."""
    base = Path(getattr(settings, "BASE_DIR", ".")).resolve()
    # BASE_DIR = .../contact360.io/admin
    candidate = base.parent.parent / "docs"
    if candidate.is_dir() and (candidate / "PHASE-DOCS-INDEX.md").is_file():
        return candidate
    logger.debug("repo docs not found at %s", candidate)
    return None


def load_phase_index_rows() -> list[dict[str, Any]]:
    """
    One row per phase folder under ``docs/`` with numeric prefix (0–11).
    Reads ``index.json`` when present for ``title`` and ``status``.
    """
    root = repo_docs_root()
    if not root:
        return []
    rows: list[dict[str, Any]] = []
    for d in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not d.is_dir() or not d.name or not d.name[0].isdigit():
            continue
        row: dict[str, Any] = {
            "folder": d.name,
            "title": d.name,
            "status": "",
            "sections_count": 0,
        }
        idx = d / "index.json"
        if idx.is_file():
            try:
                data = json.loads(idx.read_text(encoding="utf-8"))
                row["title"] = data.get("title") or row["title"]
                row["status"] = data.get("status") or ""
                sections = data.get("sections") or []
                if isinstance(sections, list):
                    row["sections_count"] = len(sections)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("phase index %s: %s", idx, exc)
        rows.append(row)
    return rows
