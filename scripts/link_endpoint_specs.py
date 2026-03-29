#!/usr/bin/env python3
"""
Insert or refresh <!-- AUTO:endpoint-links:start --> ... <!-- AUTO:endpoint-links:end -->
in each *_page.md with a table linking graphql/OperationName to backend endpoint specs.

Uses docs/backend/endpoints/index.md and endpoints_index.md as canonical path → file lookup.
Run from repo root or this directory:

  python docs/frontend/pages/link_endpoint_specs.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
DOCS = DIR.parent.parent
ENDPOINTS_DIR = DOCS / "backend" / "endpoints"
INDEX_PRIMARY = ENDPOINTS_DIR / "index.md"
INDEX_AGG = ENDPOINTS_DIR / "endpoints_index.md"

MARKER_START = "<!-- AUTO:endpoint-links:start -->"
MARKER_END = "<!-- AUTO:endpoint-links:end -->"

# Match GraphQL operation names (PascalCase), not TS modules like `graphql/contactsService`.
GRAPHQL_OP = re.compile(r"graphql/([A-Z][A-Za-z0-9_]*)")
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+\.md)\)")
ERA_LINE = re.compile(r"\|\s*era\s*\|\s*([^|]+)\|", re.IGNORECASE)

# Page specs sometimes use shorthand; map to canonical `graphql/...` keys in index.md.
OPERATION_ALIASES: dict[str, str] = {
    "graphql/UserStats": "graphql/GetUserStats",
    "graphql/Activities": "graphql/GetActivities",
    "graphql/Usage": "graphql/GetUsage",
    "graphql/CompanyFilters": "graphql/GetCompanyFilters",
    "graphql/CompanyQuery": "graphql/GetCompany",
    "graphql/ContactCount": "graphql/CountContacts",
    "graphql/Exports": "graphql/ListExports",
    "graphql/PerformanceMetrics": "graphql/GetPerformanceMetrics",
    "graphql/GetPage": "graphql/GetDashboardPage",
    "graphql/S3ListFiles": "graphql/ListS3Files",
    "graphql/FindEmailsBulk": "graphql/FindEmails",
    "graphql/VerifyEmailsBulk": "graphql/VerifyBulkEmails",
    "graphql/SearchByLinkedInUrl": "graphql/SearchLinkedIn",
    "graphql/ExportByLinkedInUrls": "graphql/ExportLinkedIn",
}


def extract_md_filename(cell: str) -> str | None:
    cell = cell.strip()
    m = MD_LINK.search(cell)
    if not m:
        return None
    return m.group(2).strip()


def parse_index_table(text: str) -> dict[str, tuple[str, str]]:
    """Map graphql/OperationName -> (markdown_filename, METHOD). Later rows win (superset)."""
    out: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        parts = [p for p in parts if p]
        if len(parts) < 3:
            continue
        if parts[0].startswith("---") or parts[0] in ("endpoint_id", "Files", "markdown"):
            continue
        # Format A: | id | METHOD | graphql | graphql/GetX | [file](file) |
        if len(parts) >= 5 and parts[2] == "graphql" and parts[3].startswith("graphql/"):
            op_path = parts[3]
            method = parts[1]
            fn = extract_md_filename(parts[4])
            if fn:
                out[op_path] = (fn, method)
            continue
        # Format B: | id | METHOD | graphql/Op | graphql | state | [detail](file) |
        for i, p in enumerate(parts):
            if p.startswith("graphql/") and i + 1 < len(parts):
                op_path = p
                method = parts[1] if i >= 2 else "QUERY"
                rest = "|".join(parts[i + 1 :])
                fn = extract_md_filename(rest) or extract_md_filename(parts[-1])
                if fn:
                    out[op_path] = (fn, method)
                break
    return out


def load_catalog() -> dict[str, tuple[str, str]]:
    catalog: dict[str, tuple[str, str]] = {}
    for path in (INDEX_PRIMARY, INDEX_AGG):
        if path.is_file():
            catalog.update(parse_index_table(path.read_text(encoding="utf-8")))
    return catalog


def era_from_endpoint_file(endpoints_dir: Path, md_name: str) -> str:
    p = endpoints_dir / md_name
    if not p.is_file():
        return "—"
    text = p.read_text(encoding="utf-8")
    m = ERA_LINE.search(text)
    if m:
        return m.group(1).strip()
    return "—"


def collect_graphql_ops(md: str) -> list[str]:
    # Ignore our own generated block (avoids picking up `graphql/...` from unresolved notes).
    if MARKER_START in md and MARKER_END in md:
        pre, rest = md.split(MARKER_START, 1)
        _, post = rest.split(MARKER_END, 1)
        md = pre + post
    seen: set[str] = set()
    ordered: list[str] = []
    for m in GRAPHQL_OP.finditer(md):
        op = m.group(1)
        path = f"graphql/{op}"
        if path not in seen:
            seen.add(path)
            ordered.append(path)
    return ordered


def resolve_catalog_key(path: str) -> str:
    return OPERATION_ALIASES.get(path, path)


def build_links_block(
    ops: list[str],
    catalog: dict[str, tuple[str, str]],
    endpoints_dir: Path,
) -> str:
    lines = [
        MARKER_START,
        "",
        "## Backend endpoint specs (GraphQL)",
        "",
        "| GraphQL operation | Endpoint spec | Method | Era |",
        "| --- | --- | --- | --- |",
    ]
    unresolved: list[str] = []
    seen_resolved: set[str] = set()
    for path in ops:
        key = resolve_catalog_key(path)
        if key in catalog and key in seen_resolved:
            continue
        if key in catalog:
            seen_resolved.add(key)
        if key not in catalog:
            unresolved.append(path)
            lines.append(
                f"| `{path.split('/')[-1]}` | *unresolved — add to endpoint index* | — | — |"
            )
            continue
        fn, method = catalog[key]
        era = era_from_endpoint_file(endpoints_dir, fn)
        rel = f"../../backend/endpoints/{fn}"
        op_name = path.split("/")[-1]
        lines.append(
            f"| `{op_name}` | [{fn}]({rel}) | {method} | {era} |"
        )
    if not ops:
        lines.append("| — | *No `graphql/...` references in this page spec* | — | — |")
    lines.append("")
    if unresolved:
        lines.append("**Unresolved operations** (not found in `index.md` / `endpoints_index.md`): ")
        lines.append(", ".join(f"`{u}`" for u in unresolved))
        lines.append("")
    lines.append(
        "*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. "
        "Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*"
    )
    lines.append("")
    lines.append(MARKER_END)
    return "\n".join(lines)


def ensure_markers(text: str, block: str) -> str:
    if MARKER_START in text and MARKER_END in text:
        pre, rest = text.split(MARKER_START, 1)
        _, post = rest.split(MARKER_END, 1)
        return pre + block + post
    # Append after design-nav block if present, else at EOF
    nav_end = "<!-- AUTO:design-nav:end -->"
    if nav_end in text:
        idx = text.index(nav_end) + len(nav_end)
        return text[:idx] + "\n\n" + block + text[idx:]
    text = text.rstrip() + "\n\n"
    return text + block + "\n"


def process_file(path: Path, catalog: dict[str, tuple[str, str]]) -> tuple[bool, list[str]]:
    raw = path.read_text(encoding="utf-8")
    ops = collect_graphql_ops(raw)
    block = build_links_block(ops, catalog, ENDPOINTS_DIR)
    new_text = ensure_markers(raw, block)
    unresolved = [o for o in ops if resolve_catalog_key(o) not in catalog]
    if new_text == raw:
        return False, unresolved
    path.write_text(new_text, encoding="utf-8")
    return True, unresolved


def main() -> int:
    if not INDEX_PRIMARY.is_file() and not INDEX_AGG.is_file():
        print("No endpoint index found in docs/backend/endpoints/", file=sys.stderr)
        return 1
    catalog = load_catalog()
    updated = 0
    all_unresolved: dict[str, list[str]] = {}
    for path in sorted(DIR.glob("*_page.md")):
        changed, unr = process_file(path, catalog)
        if unr:
            all_unresolved[path.name] = unr
        if changed:
            print("updated", path.name)
            updated += 1
    print(f"done. updated {updated} files.")
    if all_unresolved:
        print("\nPages with unresolved graphql operations:", file=sys.stderr)
        for name, ops in sorted(all_unresolved.items()):
            print(f"  {name}: {', '.join(ops)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
