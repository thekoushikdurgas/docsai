"""Tests for docs/scripts/doc_format.py."""
from __future__ import annotations

from pathlib import Path

from scripts.doc_format import format_file, format_markdown_text


def test_format_markdown_text_normalizes_crlf_and_trailing_space() -> None:
    assert format_markdown_text("a  \r\nb\t ") == "a\nb\n"


def test_format_markdown_text_ensures_trailing_newline() -> None:
    assert format_markdown_text("# x") == "# x\n"


def test_format_file_dry_run_reports_change_without_write(tmp_path: Path) -> None:
    p = tmp_path / "x.md"
    p.write_text("hi  \n", encoding="utf-8")
    r = format_file(p, dry_run=True)
    assert r.changed is True
    assert p.read_text(encoding="utf-8") == "hi  \n"


def test_format_file_apply_writes(tmp_path: Path) -> None:
    p = tmp_path / "x.md"
    p.write_text("hi  \n", encoding="utf-8")
    r = format_file(p, dry_run=False)
    assert r.changed is True
    assert p.read_text(encoding="utf-8") == "hi\n"
