"""
`non_parsed_raw_markdown` — only genuine gaps, not a second copy of `raw_markdown`.

Contains:
  1. YAML front matter (--- … ---) if present — never mirrored in section JSON.
  2. Body **fragments** (lines / fenced blocks) that are still not accounted for by
     structured string fields after **relaxed** matching (substring, markdown headings,
     token overlap with word boundaries, fenced code vs blob).

If, after matching, the “unparsed” body would still exceed ~35% of the full document,
the body remainder is cleared (only front matter is kept). That means: the structured
projection is treated as authoritative for semantics and we avoid dumping all of
`raw_markdown` again — the symptom you saw with era_task files.
"""
from __future__ import annotations

import re
from typing import Any

_EXCLUDED_KEYS = frozenset({
    "raw_markdown",
    "non_parsed_raw_markdown",
    "sha256_source",
    "generated_at",
    "schema_version",
    "source_path",
    "kind",
    "updated_at",
})

# If unparsed body is longer than this fraction of full `content`, drop body unparsed (keep FM only).
_MAX_UNPARSED_BODY_FRACTION = 0.35

_TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,}")
_HEADING_LINE_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _collapse_ws(s: str) -> str:
    return " ".join(s.split())


def _extract_front_matter_block(content: str) -> tuple[str, str]:
    if not content.startswith("---\n"):
        return "", content
    end = content.find("\n---\n", 4)
    if end == -1:
        return "", content
    cut = end + len("\n---\n")
    return content[:cut].strip(), content[cut:].lstrip("\n")


def _walk_collect_strings(obj: Any) -> list[str]:
    out: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in _EXCLUDED_KEYS or k == "entries":
                continue
            out.extend(_walk_collect_strings(v))
    elif isinstance(obj, list):
        for item in obj:
            out.extend(_walk_collect_strings(item))
    elif isinstance(obj, str):
        s = obj.strip()
        if len(s) >= 2:
            out.append(s)
    return out


def _walk_collect_headings(obj: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(obj, dict):
        h = obj.get("heading")
        if isinstance(h, str) and h.strip():
            found.add(_collapse_ws(h).lower())
        for v in obj.values():
            found |= _walk_collect_headings(v)
    elif isinstance(obj, list):
        for item in obj:
            found |= _walk_collect_headings(item)
    return found


def _coverage_blob(data: dict[str, Any]) -> str:
    work = {k: v for k, v in data.items() if k not in ("raw_markdown", "non_parsed_raw_markdown")}
    parts = _walk_collect_strings(work)
    seen: set[str] = set()
    uniq: list[str] = []
    for p in parts:
        if p in seen:
            continue
        seen.add(p)
        uniq.append(p)
    return "\n".join(uniq)


def _token_ratio_in_blob(text: str, blob_lower: str) -> float:
    toks = [t.lower() for t in _TOKEN_RE.findall(text) if len(t) >= 3]
    if not toks:
        return 1.0 if len(text.strip()) < 28 else 0.0
    hits = 0
    for t in toks:
        if re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", blob_lower, re.IGNORECASE):
            hits += 1
    return hits / len(toks)


def _fence_inner_covered(inner: str, norm_blob: str, blob_lower: str, token_threshold: float) -> bool:
    inner = inner.strip()
    if not inner:
        return True
    c = _collapse_ws(inner)
    if len(c) >= 8 and c in norm_blob:
        return True
    if _token_ratio_in_blob(inner, blob_lower) >= token_threshold:
        return True
    return False


def _line_covered(
    line: str,
    norm_blob: str,
    blob_lower: str,
    headings_norm: set[str],
    token_threshold: float,
) -> bool:
    s = line.strip()
    if not s or len(s) < 2:
        return True

    hm = _HEADING_LINE_RE.match(s)
    if hm:
        ht = _collapse_ws(hm.group(2)).lower()
        if ht in headings_norm:
            return True

    c = _collapse_ws(s)
    if len(c) >= 6 and c in norm_blob:
        return True

    if len(c) < 50 and _token_ratio_in_blob(s, blob_lower) >= token_threshold:
        return True

    if len(c) >= 50 and _token_ratio_in_blob(s, blob_lower) >= min(0.97, token_threshold + 0.08):
        return True

    return False


def _uncovered_body_lines(
    body: str,
    norm_blob: str,
    blob_lower: str,
    headings_norm: set[str],
    token_threshold: float,
) -> str:
    lines = body.splitlines()
    uncovered_chunks: list[str] = []
    buf: list[str] = []
    i = 0

    def flush_buf() -> None:
        nonlocal buf
        if buf:
            uncovered_chunks.append("\n".join(buf))
            buf = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_buf()
            fence_lines = [line]
            i += 1
            inner_parts: list[str] = []
            while i < len(lines):
                fence_lines.append(lines[i])
                if lines[i].strip() == "```" and len(fence_lines) > 1:
                    break
                if lines[i].strip() != "```":
                    inner_parts.append(lines[i])
                i += 1
            else:
                inner = "\n".join(inner_parts)
                if not _fence_inner_covered(inner, norm_blob, blob_lower, token_threshold):
                    uncovered_chunks.append("\n".join(fence_lines))
                continue
            inner = "\n".join(inner_parts)
            if not _fence_inner_covered(inner, norm_blob, blob_lower, token_threshold):
                uncovered_chunks.append("\n".join(fence_lines))
            i += 1
            continue

        if _line_covered(line, norm_blob, blob_lower, headings_norm, token_threshold):
            flush_buf()
        else:
            buf.append(line)
        i += 1

    flush_buf()
    return "\n\n".join(c for c in uncovered_chunks if c.strip()).strip()


def compute_non_parsed_raw_markdown(content: str, data: dict[str, Any]) -> str:
    fm_block, body = _extract_front_matter_block(content)
    work = {k: v for k, v in data.items() if k not in ("raw_markdown", "non_parsed_raw_markdown")}
    blob = _coverage_blob(work)
    norm_blob = _collapse_ws(blob)
    blob_lower = blob.lower()
    headings_norm = _walk_collect_headings(work)
    title = data.get("title")
    if isinstance(title, str) and title.strip():
        headings_norm.add(_collapse_ws(title).lower())

    thresholds = [0.86, 0.92, 0.97]
    uncovered_body = ""
    for th in thresholds:
        uncovered_body = _uncovered_body_lines(body, norm_blob, blob_lower, headings_norm, th)
        frac = (len(uncovered_body) / max(1, len(content)))
        if frac <= _MAX_UNPARSED_BODY_FRACTION:
            break

    if len(uncovered_body) > _MAX_UNPARSED_BODY_FRACTION * max(1, len(content)):
        uncovered_body = ""

    out_parts: list[str] = []
    if fm_block:
        out_parts.append(fm_block)
    if uncovered_body:
        out_parts.append(uncovered_body)
    return "\n\n".join(out_parts).strip()


def patch_json_object(obj: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    raw = obj.get("raw_markdown")
    if not isinstance(raw, str):
        return obj, False
    new_val = compute_non_parsed_raw_markdown(raw, obj)
    old = obj.get("non_parsed_raw_markdown")
    if old == new_val:
        return obj, False
    obj = dict(obj)
    obj["non_parsed_raw_markdown"] = new_val
    return obj, True
