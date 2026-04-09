"""
convert_md_to_json.py — Phase 2 (T2-A through T2-H)
Converts docs/**/*.md to typed JSON alongside sources under docs/ using a fast heading-splitter
approach. Structured sections are primary; raw_markdown is stored only when non_parsed_raw_markdown is non-empty.

Kinds: index | hub | era_task | graphql_module | endpoint_matrix | page_spec | document

Usage (from docs/):
    python scripts/convert_md_to_json.py [--dry-run] [--era N] [--kind KIND]
                                          [--file PATH] [--skip-existing]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DOCS_ROOT = Path(__file__).resolve().parent.parent
if str(DOCS_ROOT) not in sys.path:
    sys.path.insert(0, str(DOCS_ROOT))

from scripts.paths import JSON_ROOT

ERA_FOLDER_RE = re.compile(r"^(\d{1,2})\.\s+")
ERA_VERSION_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?")

STATUS_EMOJI = {"✅": "completed", "🟡": "in_progress", "📌": "planned", "❌": "incomplete"}
TRACK_KEYS = {"contract", "service", "surface", "data", "ops"}


# ─── T2-A  KIND DETECTION ────────────────────────────────────────────────────

def detect_kind(path: Path) -> str:
    rel = path.relative_to(DOCS_ROOT)
    parts = rel.parts
    if path.name == "README.md":
        return "index"
    if len(parts) == 2 and parts[0] == "docs":
        return "hub"
    if parts and ERA_FOLDER_RE.match(parts[0]):
        return "era_task"
    if len(parts) >= 3 and parts[0] == "backend" and parts[1] == "graphql.modules":
        return "graphql_module"
    if len(parts) >= 3 and parts[0] == "backend" and parts[1] == "endpoints":
        return "endpoint_matrix"
    if len(parts) >= 3 and parts[0] == "frontend" and parts[1] == "pages":
        return "page_spec"
    return "document"


# ─── T2-B  FRONT-MATTER ──────────────────────────────────────────────────────

def parse_front_matter(lines: list[str]) -> tuple[dict | None, int]:
    """Return (front_matter_dict_or_None, first_body_line_index)."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            fm: dict = {}
            for fl in lines[1:i]:
                m = re.match(r"^([\w_-]+):\s*(.*)", fl)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
            return fm, i + 1
    return None, 0


# ─── T2-C  FAST SECTION SPLITTER ────────────────────────────────────────────

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")


def split_sections(lines: list[str], start: int = 0) -> list[dict]:
    """
    Split content into sections by heading. Each section has:
      heading, level, slug, body (raw text between this heading and next)
    """
    sections: list[dict] = []
    current: dict | None = None

    for line in lines[start:]:
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            text = re.sub(r"[*_`]{1,3}([^*_`]+)[*_`]{1,3}", r"\1", m.group(2)).strip()
            slug = re.sub(r"[^\w\s-]", "", text.lower())
            slug = re.sub(r"\s+", "-", slug.strip())
            current = {"heading": text, "level": level, "slug": slug, "body": ""}
            sections.append(current)
        elif current is not None:
            current["body"] = current["body"] + line + "\n"
        # Lines before first heading are silently captured in an intro section if non-empty
        elif line.strip():
            current = {"heading": "", "level": 0, "slug": "", "body": line + "\n"}
            sections.append(current)

    # Trim trailing whitespace from body
    for s in sections:
        s["body"] = s["body"].rstrip()

    return sections


# ─── QUICK EXTRACTORS (regex on body text) ──────────────────────────────────

def extract_tables(body: str) -> list[dict]:
    """Parse GFM tables from a body string."""
    tables: list[dict] = []
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "|" in line and i + 1 < len(lines) and re.match(r"^\|?[\s\-:|]+\|", lines[i + 1]):
            headers = [c.strip() for c in line.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i]:
                cells = [c.strip() for c in lines[i].strip("|").split("|")]
                rows.append(cells)
                i += 1
            if headers:
                tables.append({"headers": headers, "rows": rows})
            continue
        i += 1
    return tables


def extract_list_items(body: str) -> list[dict]:
    """Extract bullet and numbered list items from body."""
    items = []
    for line in body.splitlines():
        m = re.match(r"^\s*[-*+]\s+(.*)|^\s*\d+\.\s+(.*)", line)
        if m:
            text = (m.group(1) or m.group(2) or "").strip()
            # Task list
            tm = re.match(r"\[( |x|X)\]\s*(.*)", text)
            checked = None
            if tm:
                checked = tm.group(1).lower() == "x"
                text = tm.group(2).strip()
            items.append({"text": text, "checked": checked})
    return items


def extract_code_fences(body: str) -> list[dict]:
    """Extract fenced code blocks from body."""
    blocks = []
    pattern = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
    for m in pattern.finditer(body):
        blocks.append({"lang": m.group(1), "value": m.group(2)})
    # Also try ~~~
    pattern2 = re.compile(r"~~~(\w*)\n(.*?)~~~", re.DOTALL)
    for m in pattern2.finditer(body):
        blocks.append({"lang": m.group(1), "value": m.group(2)})
    return blocks


def extract_links(body: str) -> list[dict]:
    """Extract [text](href) links."""
    links = []
    for text, href in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body):
        links.append({"text": text, "href": href})
    return links


# ─── T2-D  ERA_TASK ──────────────────────────────────────────────────────────

def _task_item(text: str) -> dict:
    status = "unknown"
    for emoji, s in STATUS_EMOJI.items():
        if emoji in text[:5]:
            status = s
            text = text[text.index(emoji) + len(emoji):].strip()
            break
    if status == "unknown" and re.match(r"✅|Completed", text[:15], re.IGNORECASE):
        status = "completed"
    codebase = None
    m = re.search(r"\[([a-zA-Z0-9_-]+)\]", text)
    if m:
        codebase = m.group(1)
    area = None
    am = re.search(r"\barea:\s*`([^`]+)`", text)
    if am:
        area = am.group(1)
    files: list[str] = []
    fm = re.search(r"\bfiles:\s*`([^`]+)`", text)
    if fm:
        files = [f.strip() for f in fm.group(1).split(",")]
    return {"status": status, "text": text, "codebase": codebase, "area": area, "files": files}


def parse_era_task_doc(sections: list[dict], content: str, rel: Path) -> dict:
    stem = rel.stem
    vm = ERA_VERSION_RE.match(stem)
    era = minor = patch = None
    version_str = codename = None
    if vm:
        era = int(vm.group(1))
        minor = int(vm.group(2))
        patch = int(vm.group(3)) if vm.group(3) else None
        version_str = f"{era}.{minor}" + (f".{patch}" if patch is not None else "")
        after = stem[vm.end():].strip()
        for sep in [" \u2014 ", "\u2014", " -- ", " - "]:
            if sep in after:
                codename = after.split(sep, 1)[1].strip()
                break

    status = "planned"
    sm = re.search(r"\*\*Status:\*\*\s*([^\n]+)", content)
    if sm:
        raw = sm.group(1).lower()
        if "completed" in raw or "✅" in raw:
            status = "completed"
        elif "progress" in raw or "🟡" in raw:
            status = "in_progress"
        elif "incomplete" in raw or "❌" in raw:
            status = "incomplete"

    tracks: dict[str, list] = {t: [] for t in TRACK_KEYS}
    flowcharts: list[str] = []
    micro_gate = evidence_gate = scope = summary = None
    extra_sections: list[dict] = []

    current_track: str | None = None
    for sec in sections:
        hl = sec["heading"].lower()
        body = sec["body"]

        if "flowchart" in hl:
            for cb in extract_code_fences(body):
                if cb["lang"] == "mermaid":
                    flowcharts.append(cb["value"])
            continue

        if "micro" in hl and "gate" in hl:
            micro_gate = body.strip()
            continue

        if "evidence" in hl:
            evidence_gate = body.strip()
            continue

        if hl == "scope":
            scope = body.strip()
            continue

        matched_track = None
        for track in TRACK_KEYS:
            if track in hl:
                matched_track = track
                break

        if matched_track:
            current_track = matched_track
            for item in extract_list_items(body):
                tracks[current_track].append(_task_item(item["text"]))
        elif hl in ("tasks", "task tracks", "## tasks", "## task tracks"):
            current_track = None  # reset; sub-sections will pick up tracks
        else:
            if not summary:
                para = body.strip()
                if para and len(para) > 30:
                    summary = para[:500]
            extra_sections.append({"heading": sec["heading"], "level": sec["level"], "prose": body.strip()})

    return {
        "version": version_str,
        "codename": codename,
        "era": era,
        "minor": minor,
        "patch": patch,
        "status": status,
        "summary": summary,
        "scope": scope,
        "flowcharts": flowcharts,
        "micro_gate": micro_gate,
        "evidence_gate": evidence_gate,
        "task_tracks": tracks,
        "sections": extra_sections,
    }


# ─── T2-E  GRAPHQL_MODULE ────────────────────────────────────────────────────

def parse_gql_module_doc(sections: list[dict], path: Path) -> dict:
    stem = path.stem
    nm = re.match(r"^(\d+)_(.+)_MODULE", stem, re.IGNORECASE)
    module_number = int(nm.group(1)) if nm else None
    module_name = nm.group(2) if nm else stem

    overview = sdl_excerpt = location = None
    operations: list[dict] = []
    error_codes: list[str] = []
    code_pointers: list[str] = []
    extra: list[dict] = []

    for sec in sections:
        hl = sec["heading"].lower()
        body = sec["body"]

        if not location:
            lm = re.search(r"\*\*[Ll]ocation:\*\*\s*`([^`]+)`", body)
            if lm:
                location = lm.group(1)

        if "overview" in hl:
            overview = body.strip()
            continue

        if any(k in hl for k in ("queries", "mutations", "operation")):
            for tbl in extract_tables(body):
                headers_lower = [h.lower() for h in tbl["headers"]]
                for row in tbl["rows"]:
                    if not row:
                        continue
                    name = row[0].strip().strip("`*")
                    if not name or name in ("Queries", "Mutations", "Subscriptions", "—"):
                        continue
                    op_type = "mutation" if any("mut" in h for h in headers_lower) else "query"
                    operations.append({
                        "name": name,
                        "operation_type": op_type,
                        "parameters": [{"name": row[1].strip(), "graphql_type": row[2].strip()}] if len(row) > 2 and row[1].strip() not in ("—", "") else [],
                        "return_type": row[3].strip() if len(row) > 3 else None,
                        "description": None,
                    })
            continue

        if "sdl" in hl or "canonical" in hl:
            for cb in extract_code_fences(body):
                if cb["lang"] in ("graphql", "gql", ""):
                    sdl_excerpt = cb["value"]
                    break
            continue

        if "error" in hl:
            error_codes.extend(item["text"] for item in extract_list_items(body))
            continue

        if "pointer" in hl:
            for item in extract_list_items(body):
                refs = re.findall(r"`([^`]+\.(py|ts|tsx|go|js|md))`", item["text"])
                code_pointers.extend(r[0] for r in refs)
                path_refs = re.findall(r"contact360\.io/[^\s,)>\]]+", item["text"])
                code_pointers.extend(path_refs)
            continue

        extra.append({"heading": sec["heading"], "level": sec["level"], "prose": body.strip(),
                      "code_blocks": extract_code_fences(body)})

    return {
        "module_number": module_number,
        "module_name": module_name,
        "location": location,
        "overview": overview,
        "operations": operations,
        "sdl_excerpt": sdl_excerpt,
        "error_codes": error_codes,
        "code_pointers": list(dict.fromkeys(code_pointers)),
        "sections": extra,
    }


# ─── T2-F  PAGE_SPEC ─────────────────────────────────────────────────────────

def parse_page_spec_doc(sections: list[dict], fm: dict | None) -> dict:
    fm = fm or {}
    metadata: dict = {}
    uses_endpoints: list[dict] = []
    ui_components: list[dict] = []
    era_tags: list[str] = []
    extra: list[dict] = []
    page_id = fm.get("page_id")
    page_type = codebase = surface = flow_id = None

    META_KEYS = {"route", "file_path", "purpose", "s3_key", "status",
                 "authentication", "authorization", "page_state", "last_updated"}

    for sec in sections:
        hl = sec["heading"].lower()
        body = sec["body"]
        items = extract_list_items(body)

        for item in items:
            text = item["text"]
            kv = re.match(r"\*\*([^*:]+):\*\*\s*(.*)", text)
            if kv:
                key = kv.group(1).strip().lower().replace(" ", "_")
                val = kv.group(2).strip()
                if key == "page_id":
                    page_id = val
                elif key == "page_type":
                    page_type = val
                elif key == "codebase":
                    codebase = val
                elif key == "surface":
                    surface = val
                elif key == "era_tags":
                    era_tags = [t.strip() for t in val.split(",") if t.strip()]
                elif key == "flow_id":
                    flow_id = val
                elif key in META_KEYS:
                    metadata[key] = val
            elif "endpoint" in hl or "uses_endpoint" in hl:
                ep = re.match(r"`([^`]+)`\s*[—\-–]\s*(.*)", text)
                if ep:
                    uses_endpoints.append({"endpoint": ep.group(1), "description": ep.group(2).strip()})
                else:
                    uses_endpoints.append({"endpoint": text.strip("`"), "description": None})
            elif "component" in hl:
                cm = re.match(r"\*\*([^*]+)\*\*\s*[—\-–]\s*`?([^`]+)`?(.*)", text)
                if cm:
                    ui_components.append({"name": cm.group(1).strip(), "file_path": cm.group(2).strip(), "description": cm.group(3).strip() or None})
                else:
                    ui_components.append({"name": text.strip("*"), "file_path": None, "description": None})

        if hl not in ("overview", "metadata") and "endpoint" not in hl and "component" not in hl:
            extra.append({"heading": sec["heading"], "level": sec["level"], "prose": body.strip()})

    return {
        "front_matter": fm,
        "page_id": page_id,
        "page_type": page_type,
        "codebase": codebase,
        "surface": surface,
        "era_tags": era_tags,
        "flow_id": flow_id,
        "metadata": metadata,
        "uses_endpoints": uses_endpoints,
        "ui_components": ui_components,
        "sections": extra,
    }


# ─── GENERIC SECTION ENRICHMENT ──────────────────────────────────────────────

def enrich_sections(sections: list[dict]) -> list[dict]:
    """Add tables, lists, code_blocks, links to each section dict."""
    result = []
    for sec in sections:
        body = sec.get("body", "")
        result.append({
            "heading": sec["heading"],
            "level": sec["level"],
            "slug": sec.get("slug", ""),
            "prose": body.strip(),
            "tables": extract_tables(body),
            "lists": [{"ordered": False, "items": extract_list_items(body)}] if extract_list_items(body) else [],
            "code_blocks": extract_code_fences(body),
            "links": extract_links(body),
        })
    return result


# ─── T2-G  ENVELOPE + WRITER ─────────────────────────────────────────────────

def extract_title(content: str) -> str:
    for line in content.splitlines():
        m = re.match(r"^#\s+(.*)", line)
        if m:
            return re.sub(r"[*_`]{1,3}([^*_`]+)[*_`]{1,3}", r"\1", m.group(1)).strip()
    return ""


def sha256_content(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def dest_path(source: Path) -> Path:
    rel = source.relative_to(DOCS_ROOT)
    stem = "index" if rel.name == "README.md" else rel.stem
    return JSON_ROOT / rel.parent / (stem + ".json")


def build_envelope(kind: str, payload: dict, source_path: Path, content: str) -> dict:
    rel = source_path.relative_to(DOCS_ROOT)
    obj: dict[str, Any] = {
        "schema_version": 1,
        "kind": kind,
        "source_path": rel.as_posix(),
        "sha256_source": sha256_content(content),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": extract_title(content),
        "raw_markdown": content,
    }
    obj.update(payload)
    return obj


def write_json(obj: dict, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


# ─── T2-H  PER-FILE CONVERTER ────────────────────────────────────────────────

def convert_file(path: Path, dry_run: bool) -> bool:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR {path}: {e}", file=sys.stderr)
        return False

    kind = detect_kind(path)
    lines = content.splitlines()
    fm, body_start = parse_front_matter(lines)
    sections = split_sections(lines, body_start)

    rel = path.relative_to(DOCS_ROOT)

    if kind == "index":
        payload = {
            "folder": rel.parent.as_posix(),
            "era_index": None,
            "summary": None,
            "status": "planned",
            "children": [],
            "navigation_tables": [t for sec in sections for t in extract_tables(sec["body"])],
            "links": [lk for sec in sections for lk in extract_links(sec["body"])],
            "sections": enrich_sections(sections),
        }
        # Set era_index for era folders
        if rel.parts:
            em = ERA_FOLDER_RE.match(rel.parts[0])
            if em:
                payload["era_index"] = int(em.group(1))
        # Status from content
        sm = re.search(r"\*\*Status:\*\*\s*([^\n]+)", content)
        if sm:
            raw = sm.group(1).lower()
            if "completed" in raw:
                payload["status"] = "completed"
            elif "progress" in raw:
                payload["status"] = "in_progress"

    elif kind == "hub":
        payload = {"sections": enrich_sections(sections)}

    elif kind == "era_task":
        payload = parse_era_task_doc(sections, content, rel)

    elif kind == "graphql_module":
        payload = parse_gql_module_doc(sections, path)

    elif kind == "endpoint_matrix":
        all_tables = [t for sec in sections for t in extract_tables(sec["body"])]
        payload = {
            "overview": sections[0]["body"].strip() if sections and not sections[0]["heading"] else None,
            "tables": [{"section_heading": sec["heading"],
                        "headers": t["headers"],
                        "rows": t["rows"]} for sec in sections for t in extract_tables(sec["body"])],
            "sections": [{"heading": s["heading"], "level": s["level"], "prose": s["body"].strip()}
                         for s in sections if s["heading"]],
        }

    elif kind == "page_spec":
        payload = parse_page_spec_doc(sections, fm)

    else:  # document
        payload = {
            "front_matter": fm,
            "sections": enrich_sections(sections),
        }

    obj = build_envelope(kind, payload, path, content)
    from scripts.non_parsed_markdown import compute_non_parsed_raw_markdown

    obj["non_parsed_raw_markdown"] = compute_non_parsed_raw_markdown(content, obj)
    if not (obj.get("non_parsed_raw_markdown") or "").strip():
        obj.pop("raw_markdown", None)
    out = dest_path(path)

    if not dry_run:
        write_json(obj, out)

    return True


# ─── MAIN ────────────────────────────────────────────────────────────────────

def collect_files(era: int | None, kind_filter: str | None, file_path: str | None,
                  skip_existing: bool) -> list[Path]:
    if file_path:
        p = Path(file_path)
        return [p if p.is_absolute() else DOCS_ROOT / p]

    files: list[Path] = []
    for p in sorted(DOCS_ROOT.rglob("*.md")):
        parts = p.relative_to(DOCS_ROOT).parts
        if parts and parts[0] in ("_archive", ".git", "json"):
            continue
        if era is not None:
            em = ERA_FOLDER_RE.match(parts[0]) if parts else None
            if not em or int(em.group(1)) != era:
                continue
        if kind_filter and detect_kind(p) != kind_filter:
            continue
        if skip_existing and dest_path(p).exists():
            continue
        files.append(p)
    return files


def run(dry_run: bool, era: int | None, kind_filter: str | None,
        file_path: str | None, skip_existing: bool) -> int:
    files = collect_files(era, kind_filter, file_path, skip_existing)
    total = len(files)
    print(f"Converting {total} files (dry={dry_run}, skip_existing={skip_existing})", flush=True)

    ok = fail = 0
    for idx, p in enumerate(files, 1):
        if idx % 50 == 0 or idx == total:
            print(f"  [{idx}/{total}]", flush=True)
        if convert_file(p, dry_run):
            ok += 1
        else:
            fail += 1

    print(f"Done: {ok} ok, {fail} errors", flush=True)
    return 0 if fail == 0 else 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--era", type=int)
    ap.add_argument("--kind", type=str)
    ap.add_argument("--file", type=str)
    ap.add_argument("--skip-existing", action="store_true")
    args = ap.parse_args()
    sys.exit(run(args.dry_run, args.era, args.kind, args.file, args.skip_existing))


if __name__ == "__main__":
    main()
