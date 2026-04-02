"""Load codebase spine, API contracts, and frontend page metadata for task generation."""
from __future__ import annotations

import json
import re
from pathlib import Path

from ..paths import DOCS_ROOT

CODEBASES_DIR = DOCS_ROOT / "codebases"
APIS_DIR = DOCS_ROOT / "backend" / "apis"
FRONTEND_PAGES_DIR = DOCS_ROOT / "frontend" / "pages"

# Era index -> primary services (from docs/version-policy.md era-to-system summary)
ERA_SERVICE_MAP: dict[int, list[str]] = {
    0: ["appointment360", "connectra", "emailapis", "logsapi", "s3storage", "jobs", "contact-ai"],
    1: [
        "appointment360",
        "app",
        "admin",
        "emailapis",
        "jobs",
        "s3storage",
        "logsapi",
        "mailvetter",
    ],
    2: ["appointment360", "emailapis", "mailvetter", "jobs", "s3storage", "app", "logsapi"],
    3: ["connectra", "appointment360", "jobs", "app", "s3storage"],
    4: ["salesnavigator", "extension", "appointment360", "app", "connectra"],
    5: ["contact-ai", "appointment360", "jobs", "app", "logsapi"],
    6: [
        "appointment360",
        "connectra",
        "emailapis",
        "jobs",
        "s3storage",
        "logsapi",
        "mailvetter",
        "app",
    ],
    7: ["appointment360", "admin", "app", "jobs", "logsapi", "s3storage"],
    8: ["appointment360", "jobs", "logsapi", "app", "connectra"],
    9: ["appointment360", "app", "admin", "jobs", "connectra", "logsapi"],
    10: ["emailcampaign", "appointment360", "jobs", "emailapis", "app", "mailvetter", "logsapi"],
}

ERA_SECTION_HEADING_RE = re.compile(
    r"^###\s+`(\d+)\.x\.x[^\n]*`\s*$",
    re.MULTILINE,
)
BACKTICK_OP_RE = re.compile(r"`([a-zA-Z_][a-zA-Z0-9_]*)`")
TABLE_ROW_OP_RE = re.compile(r"\|\s*`([a-zA-Z][a-zA-Z0-9_]*)`\s*\|")


def _parse_codebase_spine(path: Path) -> dict[int, str]:
    """Map era index 0-10 to first non-empty line of concern under ### `N.x.x` section."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    result: dict[int, str] = {}
    for m in ERA_SECTION_HEADING_RE.finditer(text):
        try:
            era_idx = int(m.group(1))
        except ValueError:
            continue
        if era_idx < 0 or era_idx > 10:
            continue
        start = m.end()
        next_h = re.search(r"^###\s|^##\s", text[start:], re.MULTILINE)
        chunk = text[start : start + next_h.start()] if next_h else text[start:]
        for line in chunk.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("```"):
                # First substantive line (often checkbox bullet)
                result[era_idx] = stripped[:500]
                break
    return result


def _load_all_codebase_spines() -> dict[str, dict[int, str]]:
    out: dict[str, dict[int, str]] = {}
    if not CODEBASES_DIR.is_dir():
        return out
    for path in sorted(CODEBASES_DIR.glob("*-codebase-analysis.md")):
        name = path.name.removesuffix(".md")
        key = name.removesuffix("-codebase-analysis") if name.endswith("-codebase-analysis") else path.stem
        spine = _parse_codebase_spine(path)
        if spine:
            out[key] = spine
    return out


def _extract_api_operations(md_text: str) -> list[str]:
    """Extract GraphQL-ish operation names from API module markdown."""
    names: set[str] = set()
    for m in TABLE_ROW_OP_RE.finditer(md_text):
        names.add(m.group(1))
    for m in BACKTICK_OP_RE.finditer(md_text):
        w = m.group(1)
        if len(w) > 2 and w[0].islower() and w not in {"true", "false", "null"}:
            names.add(w)
    return sorted(names)[:80]


def _load_api_contracts() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    if not APIS_DIR.is_dir():
        return out
    for path in sorted(APIS_DIR.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        module = path.stem
        ops = _extract_api_operations(text)
        if ops:
            out[module] = ops
    return out


def _load_frontend_pages() -> dict[str, dict[str, object]]:
    """route -> {title, file_path, page_id, hooks sample}."""
    out: dict[str, dict[str, object]] = {}
    if not FRONTEND_PAGES_DIR.is_dir():
        return out
    for path in sorted(FRONTEND_PAGES_DIR.glob("*.json")):
        if path.name in ("pages_index.json", "index.json"):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        meta = data.get("metadata") or {}
        route = meta.get("route") or ""
        if not route:
            continue
        hooks: list[str] = []
        for ep in meta.get("uses_endpoints") or []:
            h = ep.get("via_hook")
            if h and h not in hooks:
                hooks.append(h)
        out[route] = {
            "title": (meta.get("purpose") or data.get("page_id") or path.stem)[:200],
            "file_path": meta.get("file_path") or "",
            "page_id": data.get("page_id") or path.stem,
            "hooks": hooks[:8],
        }
    return out


def load_registry() -> dict[str, object]:
    """
    Return structured registry for task templates and audits.

    Keys:
      - codebase_spines: service_key -> { era_idx: concern_line }
      - api_contracts: module_stem -> [operation names]
      - frontend_pages: route -> { title, file_path, page_id, hooks }
      - era_service_map: era_idx -> [service names]
    """
    return {
        "codebase_spines": _load_all_codebase_spines(),
        "api_contracts": _load_api_contracts(),
        "frontend_pages": _load_frontend_pages(),
        "era_service_map": {k: list(v) for k, v in ERA_SERVICE_MAP.items()},
    }

