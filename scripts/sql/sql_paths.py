"""Resolve SQL and CSV paths relative to docs/, scripts/, or cwd."""

from __future__ import annotations

from pathlib import Path


def resolve_under_bases(name: str, bases: list[Path]) -> Path:
    """Return first existing file path for `name` as given or under each base."""
    raw = name.strip()
    p = Path(raw).expanduser()
    if p.is_file():
        return p.resolve()
    for base in bases:
        cand = (base / raw).resolve()
        if cand.is_file():
            return cand
    raise FileNotFoundError(raw)
