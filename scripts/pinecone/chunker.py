"""Markdown chunker for Pinecone ingestion.

Splits markdown at `##` / `###` headings and returns records compatible with
`field_map text=content` (integrated embeddings), with flat metadata only.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from paths import DOCS_HUB_DIR, DOCS_ROOT


HEADING_RE = re.compile(r"^(##|###)\s+(.+?)\s*$")
VERSION_RE = re.compile(r"^(\d+\.\d+(?:\.\d+)?)")


def _truncate(s: str, limit: int) -> str:
    s = s.strip()
    return s if len(s) <= limit else s[:limit]


def _infer_version_from_filename(path: Path) -> str:
    stem = path.stem
    m = VERSION_RE.match(stem)
    return m.group(1) if m else ""


def _infer_service_from_path(path: Path) -> str:
    parts = list(path.parts)
    # Best-effort: service folder is usually the segment just before `apis` / `endpoints`.
    for marker in ("apis", "endpoints"):
        if marker in parts:
            idx = parts.index(marker)
            if idx > 0:
                return str(parts[idx - 1])

    # Fallback: infer from filename prefix.
    stem = path.stem
    if not stem:
        return ""

    # Remove leading version-like prefix.
    stem = VERSION_RE.sub("", stem, count=1)
    return stem.split()[0].strip("-_ ") if stem else ""


def _infer_era_and_kind(doc_path_rel: str, abs_path: Path) -> Tuple[str, str]:
    """
    Map file location to:
    - era: "0"-"10", "global", "codebases", "backend"
    - doc_kind: era_task, codebase_analysis, backend_api, hub, endpoint_md
    """

    # backend*
    if doc_path_rel.startswith("backend/"):
        if doc_path_rel.startswith("backend/apis/"):
            return "backend", "backend_api"
        if doc_path_rel.startswith("backend/endpoints/"):
            return "backend", "endpoint_md"
        return "backend", "backend_api"

    # codebases analysis
    if doc_path_rel.startswith("codebases/"):
        return "codebases", "codebase_analysis"

    # hub/top-level docs
    try:
        if abs_path.is_relative_to(DOCS_HUB_DIR):
            return "global", "hub"
    except Exception:
        # Python < 3.9 doesn't have is_relative_to; keep compatibility.
        if str(DOCS_HUB_DIR) in str(abs_path):
            return "global", "hub"

    # If the file sits directly in docs/ (top-level hub docs like roadmap.md), treat as global.
    if abs_path.parent == DOCS_ROOT:
        return "global", "hub"

    # era folder: "0. Foundation ...", "10. ..." -> leading number.
    parent_name = abs_path.parent.name
    m = re.match(r"^(\d+)\.", parent_name)
    if m:
        return m.group(1), "era_task"

    return "global", "hub"


def _iter_heading_chunks(
    content: str,
) -> Iterable[Tuple[str, List[str]]]:
    """
    Yield (heading_text, lines_in_chunk) where each chunk begins with `##` or `###`.
    """

    current_heading: str | None = None
    current_lines: List[str] = []

    for line in content.splitlines():
        m = HEADING_RE.match(line.strip())
        if m:
            # Flush previous chunk.
            if current_heading is not None and current_lines:
                yield current_heading, current_lines
            current_heading = m.group(2).strip()
            current_lines = [line]
        else:
            if current_heading is not None:
                current_lines.append(line)

    if current_heading is not None and current_lines:
        yield current_heading, current_lines


def _split_text_by_max_chars(text: str, max_chars: int) -> List[str]:
    if len(text) <= max_chars:
        return [text]

    segments: List[str] = []
    buf: List[str] = []
    buf_len = 0

    for line in text.splitlines(keepends=True):
        next_len = len(line)
        if buf and (buf_len + next_len) > max_chars:
            segments.append("".join(buf).strip())
            buf = [line]
            buf_len = next_len
        else:
            buf.append(line)
            buf_len += next_len

    if buf:
        segments.append("".join(buf).strip())

    # Avoid empty segments.
    return [s for s in segments if s]


def chunk_file(path: Path, *, max_chunk_chars: int = 2000) -> List[Dict]:
    """
    Chunk a markdown file into Pinecone records.

    Record schema:
    - `_id`: deterministic sha256
    - `content`: chunk text (integrated embeddings uses field_map text=content)
    - flat metadata: doc_path, era, doc_kind, heading, service, version
    """

    raw = path.read_text(encoding="utf-8")
    doc_path_rel = str(path.relative_to(DOCS_ROOT)).replace("\\", "/")

    era, doc_kind = _infer_era_and_kind(doc_path_rel, path)
    service = _infer_service_from_path(path)
    version = _infer_version_from_filename(path)

    records: List[Dict] = []

    # If the doc has no headings at level 2/3, index it as a single chunk.
    heading_chunks = list(_iter_heading_chunks(raw))
    if not heading_chunks:
        content = raw.strip()
        for i, seg in enumerate(_split_text_by_max_chars(content, max_chunk_chars)):
            payload = {
                "_id": hashlib.sha256(
                    f"{doc_path_rel}::(no-heading)::seg{i}::{seg}".encode("utf-8")
                ).hexdigest(),
                "content": seg,
                "doc_path": doc_path_rel,
                "era": era,
                "doc_kind": doc_kind,
                "heading": "",
                "service": service,
                "version": version,
            }
            records.append(payload)
        return records

    for heading_text, lines in heading_chunks:
        heading_line = heading_text.strip()
        full_chunk_text = "\n".join(lines).strip()
        if not full_chunk_text:
            continue

        segments = _split_text_by_max_chars(full_chunk_text, max_chunk_chars)
        for i, seg in enumerate(segments):
            _id_seed = f"{doc_path_rel}::{heading_line}::seg{i}::{seg}"
            record_id = hashlib.sha256(_id_seed.encode("utf-8")).hexdigest()
            records.append(
                {
                    "_id": record_id,
                    "content": seg,
                    "doc_path": doc_path_rel,
                    "era": era,
                    "doc_kind": doc_kind,
                    "heading": _truncate(heading_line, 200),
                    "service": service,
                    "version": version,
                }
            )

    return records


def iter_records(paths: Iterable[Path]) -> Iterable[Dict]:
    for p in paths:
        yield from chunk_file(p)

