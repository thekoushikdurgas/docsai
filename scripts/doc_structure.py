"""Document kind classification and lightweight structure validation for docs/."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .paths import DOCS_ROOT
from .scanner import ERA_FOLDERS, extract_track_sections

class DocKind(Enum):
    ERA_TASK = "era_task"
    HUB = "hub"
    BACKEND_API = "backend_api"
    ENDPOINT_JSON = "endpoint_json"
    ENDPOINT_MD = "endpoint_md"
    CODEBASE_ANALYSIS = "codebase_analysis"
    FRONTEND_PAGE = "frontend_page"
    TOOLING_SCRIPT = "tooling_script"
    OTHER = "other"


@dataclass(slots=True)
class StructureSpec:
    kind: DocKind
    required_sections: list[str]
    required_frontmatter_keys: list[str]
    name_pattern: str | None


@dataclass(slots=True)
class ValidationFinding:
    path: Path
    kind: DocKind
    severity: str  # "error" | "warning"
    message: str
    line: int | None = None


def resolve_docs_subpath(prefix: str) -> Path:
    """Path under DOCS_ROOT; if missing, strip one leading `docs/` (repo-style vs docs-root-relative)."""
    p = prefix.replace("\\", "/").strip("/")
    base = DOCS_ROOT / p
    if not base.exists() and p.startswith("docs/"):
        base = DOCS_ROOT / p[5:].lstrip("/")
    return base


def _rel_posix(path: Path) -> str:
    try:
        return path.resolve().relative_to(DOCS_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def classify_path(path: Path) -> DocKind:
    """Assign DocKind from path under DOCS_ROOT."""
    if not path.is_file():
        return DocKind.OTHER
    rel = _rel_posix(path)
    # Policy hubs: docs/docs/*.md → relative path starts with "docs/"
    if rel.startswith("docs/") and path.suffix.lower() == ".md":
        return DocKind.HUB
    if path.suffix.lower() == ".py" and "scripts" in rel:
        return DocKind.TOOLING_SCRIPT
    parent = path.parent.name
    if parent in ERA_FOLDERS and path.suffix.lower() == ".md":
        return DocKind.ERA_TASK
    if "backend/apis" in rel and path.suffix.lower() == ".md":
        return DocKind.BACKEND_API
    if "backend/endpoints" in rel:
        if path.suffix.lower() == ".json":
            return DocKind.ENDPOINT_JSON
        if path.suffix.lower() == ".md":
            return DocKind.ENDPOINT_MD
    if "codebases" in rel and path.suffix.lower() == ".md":
        return DocKind.CODEBASE_ANALYSIS
    if "frontend/pages" in rel and path.name.endswith("_page.md"):
        return DocKind.FRONTEND_PAGE
    return DocKind.OTHER


def _hub_validator(path: Path) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.lstrip().startswith("#"):
        findings.append(
            ValidationFinding(path, DocKind.HUB, "warning", "Missing top-level # heading", None)
        )
    if len(text.strip()) < 50:
        findings.append(
            ValidationFinding(path, DocKind.HUB, "warning", "Very short hub file", None)
        )
    return findings


def _era_task_validator(path: Path) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    if path.name == "README.md":
        return findings
    text = path.read_text(encoding="utf-8", errors="replace")
    tracks = extract_track_sections(text)
    if path.name[0].isdigit() and "." in path.name:
        if "## Tasks" not in text and "## Task tracks" not in text:
            findings.append(
                ValidationFinding(
                    path,
                    DocKind.ERA_TASK,
                    "error",
                    "Versioned era file missing ## Tasks or ## Task tracks",
                    None,
                )
            )
        elif not tracks:
            findings.append(
                ValidationFinding(
                    path,
                    DocKind.ERA_TASK,
                    "warning",
                    "No ### Contract/Service/Surface/Data/Ops subsections under Tasks",
                    None,
                )
            )
    return findings


def _frontend_page_validator(path: Path) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.lstrip().startswith("---"):
        end = text.find("\n---", 3)
        if end == -1:
            findings.append(
                ValidationFinding(
                    path,
                    DocKind.FRONTEND_PAGE,
                    "error",
                    "YAML front matter started but not closed with ---",
                    None,
                )
            )
        else:
            fm = text[3:end]
            for key in ("title", "page_id"):
                if f"{key}:" not in fm:
                    findings.append(
                        ValidationFinding(
                            path,
                            DocKind.FRONTEND_PAGE,
                            "error",
                            f"Front matter missing required key: {key}",
                            None,
                        )
                    )
    else:
        findings.append(
            ValidationFinding(
                path,
                DocKind.FRONTEND_PAGE,
                "warning",
                "Expected YAML front matter starting with ---",
                None,
            )
        )
    if "## Overview" not in text:
        findings.append(
            ValidationFinding(
                path,
                DocKind.FRONTEND_PAGE,
                "warning",
                "Missing ## Overview section",
                None,
            )
        )
    return findings


def _prose_markdown_validator(path: Path, kind: DocKind) -> list[ValidationFinding]:
    """Light checks for backend/apis, backend/endpoints *.md, and codebases/*.md."""
    findings: list[ValidationFinding] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    stripped = text.lstrip()
    if not stripped.startswith("#"):
        findings.append(
            ValidationFinding(
                path,
                kind,
                "warning",
                "Missing top-level # heading",
                None,
            )
        )
    if len(text.strip()) < 40:
        findings.append(
            ValidationFinding(
                path,
                kind,
                "warning",
                "Very short markdown file",
                None,
            )
        )
    return findings


def validate_file(path: Path) -> list[ValidationFinding]:
    """Run validators for the file's DocKind."""
    kind = classify_path(path)
    if kind == DocKind.HUB:
        return _hub_validator(path)
    if kind == DocKind.ERA_TASK:
        return _era_task_validator(path)
    if kind == DocKind.FRONTEND_PAGE:
        return _frontend_page_validator(path)
    if kind == DocKind.BACKEND_API:
        return _prose_markdown_validator(path, DocKind.BACKEND_API)
    if kind == DocKind.ENDPOINT_MD:
        return _prose_markdown_validator(path, DocKind.ENDPOINT_MD)
    if kind == DocKind.CODEBASE_ANALYSIS:
        return _prose_markdown_validator(path, DocKind.CODEBASE_ANALYSIS)
    return []


def iter_paths_for_validation(
    *,
    prefix: str | None = None,
    kind_filter: DocKind | None = None,
    era_index: int | None = None,
) -> list[Path]:
    """Collect paths under DOCS_ROOT matching filters."""
    paths: list[Path] = []
    if era_index is not None:
        if era_index < 0 or era_index >= len(ERA_FOLDERS):
            return []
        era_dir = DOCS_ROOT / ERA_FOLDERS[era_index]
        if era_dir.is_dir():
            paths.extend(sorted(era_dir.glob("*.md")))
    elif prefix:
        base = resolve_docs_subpath(prefix)
        if base.is_file():
            paths = [base]
        elif base.is_dir():
            paths.extend(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() == ".md")
    else:
        # default: hub only (docs/docs/*.md)
        hub = DOCS_ROOT / "docs"
        if hub.is_dir():
            paths.extend(sorted(hub.glob("*.md")))
    if kind_filter is not None:
        paths = [p for p in paths if classify_path(p) == kind_filter]
    return paths


def kind_from_cli(value: str) -> DocKind | None:
    if not value:
        return None
    return {
        "hub": DocKind.HUB,
        "era_task": DocKind.ERA_TASK,
        "frontend_page": DocKind.FRONTEND_PAGE,
        "backend_api": DocKind.BACKEND_API,
        "endpoint_md": DocKind.ENDPOINT_MD,
        "codebase_analysis": DocKind.CODEBASE_ANALYSIS,
    }.get(value)


def collect_structure_paths(
    *,
    prefix: str,
    era_index: int | None,
    kind: DocKind | None,
) -> list[Path]:
    """Path set for `validate-structure` / `format-structure` (same filters)."""
    if era_index is not None:
        return iter_paths_for_validation(era_index=era_index, kind_filter=kind)
    if prefix:
        return iter_paths_for_validation(prefix=prefix, kind_filter=kind)
    if kind == DocKind.ERA_TASK:
        paths: list[Path] = []
        for i in range(len(ERA_FOLDERS)):
            paths.extend(iter_paths_for_validation(era_index=i, kind_filter=DocKind.ERA_TASK))
        return paths
    if kind == DocKind.FRONTEND_PAGE:
        return iter_paths_for_validation(prefix="frontend/pages", kind_filter=DocKind.FRONTEND_PAGE)
    if kind == DocKind.BACKEND_API:
        return iter_paths_for_validation(prefix="backend/apis", kind_filter=DocKind.BACKEND_API)
    if kind == DocKind.ENDPOINT_MD:
        return iter_paths_for_validation(prefix="backend/endpoints", kind_filter=DocKind.ENDPOINT_MD)
    if kind == DocKind.CODEBASE_ANALYSIS:
        return iter_paths_for_validation(prefix="codebases", kind_filter=DocKind.CODEBASE_ANALYSIS)
    return iter_paths_for_validation(kind_filter=DocKind.HUB)


def collect_validate_all_structure_paths(*, include_prose: bool = False) -> list[Path]:
    """Paths whose structure is checked by `validate-all` (hubs + era tasks + frontend pages)."""
    seen: set[str] = set()
    out: list[Path] = []

    def add(paths: list[Path]) -> None:
        for p in paths:
            key = str(p.resolve())
            if key not in seen:
                seen.add(key)
                out.append(p)

    add(iter_paths_for_validation(kind_filter=DocKind.HUB))
    for ei in range(len(ERA_FOLDERS)):
        add(iter_paths_for_validation(era_index=ei, kind_filter=DocKind.ERA_TASK))
    add(iter_paths_for_validation(prefix="frontend/pages", kind_filter=DocKind.FRONTEND_PAGE))
    if include_prose:
        add(iter_paths_for_validation(prefix="backend/apis", kind_filter=DocKind.BACKEND_API))
        add(iter_paths_for_validation(prefix="backend/endpoints", kind_filter=DocKind.ENDPOINT_MD))
        add(iter_paths_for_validation(prefix="codebases", kind_filter=DocKind.CODEBASE_ANALYSIS))
    return out
