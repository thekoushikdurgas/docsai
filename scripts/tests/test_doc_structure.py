"""Tests for docs/scripts/doc_structure.py validators."""
from __future__ import annotations

from pathlib import Path

from scripts.doc_structure import DocKind


def test_prose_validator_warns_without_heading(tmp_path: Path) -> None:
    p = tmp_path / "api.md"
    p.write_text("no heading here\n", encoding="utf-8")
    # classify_path uses DOCS_ROOT; temp files are outside docs — call validator via validate_file
    # only works for paths under DOCS_ROOT. Instead test _prose_markdown_validator indirectly
    # by checking ValidationFinding shape from a manual path... Actually classify_path won't match.
    from scripts.doc_structure import _prose_markdown_validator

    findings = _prose_markdown_validator(p, DocKind.BACKEND_API)
    assert any("Missing top-level" in f.message for f in findings)


def test_prose_validator_ok_with_heading(tmp_path: Path) -> None:
    p = tmp_path / "api.md"
    p.write_text("# Title\n\n" + ("Body paragraph. " * 10), encoding="utf-8")
    from scripts.doc_structure import _prose_markdown_validator

    findings = _prose_markdown_validator(p, DocKind.BACKEND_API)
    assert not any("Missing top-level" in f.message for f in findings)


def test_kind_from_cli_maps_backend_kinds() -> None:
    from scripts.doc_structure import kind_from_cli

    assert kind_from_cli("backend_api") == DocKind.BACKEND_API
    assert kind_from_cli("endpoint_md") == DocKind.ENDPOINT_MD
    assert kind_from_cli("codebase_analysis") == DocKind.CODEBASE_ANALYSIS
