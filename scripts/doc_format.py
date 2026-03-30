"""Whitespace-safe markdown formatting for docs/ (pairs with doc_structure validation)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def format_markdown_text(text: str) -> str:
    """Normalize newlines, strip trailing whitespace on each line, ensure single trailing newline."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    lines = [line.rstrip() for line in lines]
    return "\n".join(lines) + "\n"


@dataclass(slots=True)
class FormatResult:
    path: Path
    changed: bool
    error: str | None = None


def format_file(path: Path, *, dry_run: bool = True, encoding: str = "utf-8") -> FormatResult:
    """Read markdown, apply format; write when not dry_run and content changed."""
    try:
        raw = path.read_text(encoding=encoding, errors="strict")
    except OSError as exc:
        return FormatResult(path=path, changed=False, error=str(exc))
    except UnicodeDecodeError as exc:
        return FormatResult(path=path, changed=False, error=f"not valid {encoding}: {exc}")

    new = format_markdown_text(raw)
    if new == raw:
        return FormatResult(path=path, changed=False)

    if not dry_run:
        try:
            path.write_text(new, encoding=encoding, newline="\n")
        except OSError as exc:
            return FormatResult(path=path, changed=False, error=str(exc))
    return FormatResult(path=path, changed=True)
