from __future__ import annotations

import re
from pathlib import Path

from .models import DocFile, ScanResult, Status, TrackSection

DOCS_ROOT = Path(__file__).resolve().parent.parent
ERA_FOLDERS = [
    "0. Foundation and pre-product stabilization and codebase setup",
    "1. Contact360 user and billing and credit system",
    "2. Contact360 email system",
    "3. Contact360 contact and company data system",
    "4. Contact360 Extension and Sales Navigator maturity",
    "5. Contact360 AI workflows",
    "6. Contact360 Reliability and Scaling",
    "7. Contact360 deployment",
    "8. Contact360 public and private apis and endpoints",
    "9. Contact360 Ecosystem integrations and Platform productization",
    "10. Contact360 email campaign",
]

STATUS_RE = re.compile(r"^- \*\*Status:\*\*\s+(.+?)\s*$", re.MULTILINE)
PATCH_RE = re.compile(r"^(\d+\.\d+\.\d+)")
MINOR_RE = re.compile(r"^(\d+\.\d+)\s+")
TASK_SECTION_HEADERS = {"## Tasks", "## Task tracks"}
TASK_STATUS_PREFIX_RE = re.compile(r"^- (✅|🟡|📌|⬜) ")
TRACK_HEADER_RE = re.compile(r"^### (Contract|Service|Surface|Data|Ops)\s*$")


def _infer_file_type(filename: str) -> tuple[str, str]:
    if filename == "README.md":
        return "readme", "README"
    stem = filename.removesuffix(".md")
    patch_match = PATCH_RE.match(stem)
    if patch_match:
        return "patch", patch_match.group(1)
    minor_match = MINOR_RE.match(stem)
    if minor_match:
        return "minor", minor_match.group(1)
    return "other", stem


def _extract_tasks_block_lines(content: str) -> list[str] | None:
    """Return lines inside the first ## Tasks or ## Task tracks section until next ## heading."""
    lines = content.splitlines()
    start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in TASK_SECTION_HEADERS:
            start = i + 1
            break
    if start is None:
        return None
    block: list[str] = []
    for j in range(start, len(lines)):
        line = lines[j]
        if line.startswith("## ") and not line.startswith("###"):
            break
        block.append(line)
    return block


def extract_track_sections(content: str) -> list[TrackSection]:
    """Parse ### Contract|Service|Surface|Data|Ops subsections under ## Tasks / ## Task tracks."""
    block_lines = _extract_tasks_block_lines(content)
    if not block_lines:
        return []

    sections: list[TrackSection] = []
    current_name: str | None = None
    current_items: list[str] = []

    def flush() -> None:
        nonlocal current_name, current_items
        if current_name is not None:
            sections.append(TrackSection(name=current_name, items=list(current_items)))
        current_name = None
        current_items = []

    for line in block_lines:
        stripped = line.strip()
        m = TRACK_HEADER_RE.match(stripped)
        if m:
            flush()
            current_name = m.group(1)
            current_items = []
            continue
        if current_name is None:
            continue
        if stripped.startswith("- "):
            body = stripped[2:].strip()
            if body:
                current_items.append(body)
    flush()
    return sections


def extract_service_task_slices(content: str) -> dict[str, list[str]]:
    """
    Parse '## Service task slices' and following ### Subsection headings until next ## at level 2.
    Returns {subsection_title: [bullet lines without '- ']}.
    """
    lines = content.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Service task slices":
            start = i + 1
            break
    if start is None:
        return {}

    result: dict[str, list[str]] = {}
    current_heading: str | None = None
    current_bullets: list[str] = []

    def flush_slice() -> None:
        nonlocal current_heading, current_bullets
        if current_heading is not None:
            result[current_heading] = list(current_bullets)
        current_heading = None
        current_bullets = []

    for j in range(start, len(lines)):
        line = lines[j]
        if line.startswith("## ") and not line.startswith("###"):
            break
        if line.startswith("### "):
            flush_slice()
            current_heading = line[4:].strip()
            continue
        if current_heading is None:
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            body = stripped[2:].strip()
            if body:
                current_bullets.append(body)
        elif stripped.startswith(">") or not stripped:
            continue
    flush_slice()
    return result


def _extract_task_stats(content: str) -> tuple[int, int]:
    """Count task bullets under ## Tasks / ## Task tracks (legacy line-based scan)."""
    task_count = 0
    tasks_without_prefix = 0
    in_tasks = False
    for line in content.splitlines():
        if line.startswith("## "):
            in_tasks = line.strip() in TASK_SECTION_HEADERS
            continue
        if not in_tasks:
            continue
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        task_count += 1
        if not TASK_STATUS_PREFIX_RE.match(stripped):
            tasks_without_prefix += 1
    return task_count, tasks_without_prefix


def parse_file(path: Path) -> DocFile:
    content = path.read_text(encoding="utf-8")
    status_match = STATUS_RE.search(content)
    status = Status.from_raw(status_match.group(1) if status_match else None)
    file_type, version = _infer_file_type(path.name)
    track_sections = extract_track_sections(content)

    if track_sections:
        task_count = sum(len(ts.items) for ts in track_sections)
        tasks_without_prefix = 0
        for ts in track_sections:
            for item in ts.items:
                line = f"- {item}"
                if not TASK_STATUS_PREFIX_RE.match(line):
                    tasks_without_prefix += 1
    else:
        task_count, tasks_without_prefix = _extract_task_stats(content)

    era = path.parent.name if path.parent != DOCS_ROOT else "top-level"
    return DocFile(
        path=path,
        era=era,
        file_type=file_type,
        version=version,
        status=status,
        task_count=task_count,
        tasks_without_prefix=tasks_without_prefix,
        track_sections=track_sections,
    )


def _iter_era_docs() -> list[Path]:
    paths: list[Path] = []
    for folder in ERA_FOLDERS:
        era_dir = DOCS_ROOT / folder
        if not era_dir.exists():
            continue
        paths.extend(sorted(era_dir.glob("*.md")))
    return paths


def _iter_top_level_docs() -> list[Path]:
    targets = [
        "architecture.md",
        "audit-compliance.md",
        "backend.md",
        "codebase.md",
        "docsai-sync.md",
        "flowchart.md",
        "frontend.md",
        "governance.md",
        "README.md",
        "roadmap.md",
        "version-policy.md",
        "versions.md",
    ]
    files: list[Path] = []
    for name in targets:
        path = DOCS_ROOT / name
        if path.exists():
            files.append(path)
    return files


def scan_all(include_top_level: bool = True) -> ScanResult:
    files = _iter_era_docs()
    if include_top_level:
        files.extend(_iter_top_level_docs())
    parsed = [parse_file(path) for path in files]
    return ScanResult(files=parsed)


def scan_era_only() -> ScanResult:
    """Scan only era-folder markdown (no docs root top-level files)."""
    parsed = [parse_file(path) for path in _iter_era_docs()]
    return ScanResult(files=parsed)
