from __future__ import annotations

from pathlib import Path


def fix_era_readme_links(era_idx: int, docs_root: Path | None = None, *, apply: bool) -> int:
    """Legacy markdown-era hook (no-op). Era execution docs are JSON-native under docs/."""
    _ = era_idx, docs_root, apply
    return 0
