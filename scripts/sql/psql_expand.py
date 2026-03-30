"""Expand psql \\i include directives into a single SQL script (no other psql commands)."""

from __future__ import annotations

import re
from pathlib import Path

_I_LINE = re.compile(r"^\s*\\i\s+(\S+)\s*$")


def expand_psql_includes(path: Path, _stack: list[Path] | None = None) -> str:
    """Read a .sql file and inline nested \\i paths relative to each file's directory."""
    path = path.resolve()
    if _stack is None:
        _stack = []
    if path in _stack:
        raise ValueError(f"Include cycle involving {path}")
    _stack.append(path)
    try:
        text = path.read_text(encoding="utf-8")
        base = path.parent
        parts: list[str] = []
        for line in text.splitlines(keepends=True):
            m = _I_LINE.match(line)
            if not m:
                parts.append(line)
                continue
            raw = m.group(1).strip().strip('"').strip("'")
            inc = (base / raw).resolve()
            if not inc.is_file():
                raise FileNotFoundError(f"\\i target not found: {inc} (from {path})")
            parts.append(f"\n-- >> included from {path.name}: \\i {raw}\n")
            parts.append(expand_psql_includes(inc, _stack))
            parts.append("\n")
        return "".join(parts)
    finally:
        _stack.pop()
