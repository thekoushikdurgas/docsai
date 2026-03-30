"""
Create patch documents `X.Y.Z — <Codename>.md` across Contact360 docs.

This script is intentionally dependency-free (stdlib only) and follows existing
filename/title sanitization rules from `docs_versions_utils.py`.

Supported inputs:
  - Minor docs `X.Y — <Title>.md` inside era folders `X. <Era Name>/`.
  - Patch ladder tables inside minor docs: `## Patch ladder (...)` with markdown table rows.
  - Patch subsections for eras that define `### X.Y.Z — ...` headings (e.g. era 1).
  - Synthesized patches when no patch ladder exists: derived from the minor's `## Task tracks`
    and the era's `*-task-pack.md` files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from docs_versions_utils import DASH, sanitize_title_for_filename


PATCH_FILE_RE = re.compile(r"^(?P<era>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\s*[—-]\s*(?P<codename>.+)\.md$")
MINOR_FILE_RE = re.compile(r"^(?P<era>\d+)\.(?P<minor>\d+)\s*[—-]\s*(?P<title>.+)\.md$")
ERA_DIR_RE = re.compile(r"^(?P<era>\d+)\.")


@dataclass(frozen=True)
class PatchRow:
    patch_ref: str  # e.g. "1.0.0"
    patch_index: int  # 0..9
    codename: str
    focus: str
    evidence_gate: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text_if_changed(path: Path, new_text: str, *, apply: bool) -> bool:
    old_text = read_text(path) if path.exists() else ""
    if old_text == new_text:
        return False
    if apply:
        path.write_text(new_text, encoding="utf-8")
    return True


def iter_markdown_files(root: Path) -> Iterable[Path]:
    yield from (p for p in root.rglob("*.md") if p.is_file())


def discover_era_dirs(docs_root: Path, eras: Optional[set[int]]) -> list[Path]:
    out: list[Path] = []
    for p in sorted(docs_root.iterdir()):
        if not p.is_dir():
            continue
        m = ERA_DIR_RE.match(p.name)
        if not m:
            continue
        era = int(m.group("era"))
        if eras is not None and era not in eras:
            continue
        out.append(p)
    return out


def discover_minor_docs(era_dir: Path, era: int) -> list[Path]:
    out: list[Path] = []
    for p in sorted(era_dir.glob("*.md")):
        m = MINOR_FILE_RE.match(p.name)
        if not m:
            continue
        e = int(m.group("era"))
        minor = int(m.group("minor"))
        if e != era:
            continue
        # Exclude non-minor docs that still match the numeric prefix pattern.
        if p.name.endswith("-task-pack.md"):
            continue
        if p.name.endswith("x-master-checklist.md"):
            continue
        if p.name.lower() == "readme.md":
            continue
        out.append(p)
    return out


def extract_task_tracks_from_minor(minor_doc_text: str) -> Dict[str, str]:
    """
    Returns blocks keyed by: Contract, Service, Surface, Data, Ops.
    Each value is the raw markdown block after the `### TrackName` heading.
    """
    tracks = {"Contract": "", "Service": "", "Surface": "", "Data": "", "Ops": ""}
    lines = minor_doc_text.splitlines()

    in_tracks = False
    current_track: Optional[str] = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, current_track
        if current_track is None:
            return
        if current_track in tracks:
            # Preserve content exactly as markdown; trimming trailing whitespace is safe.
            tracks[current_track] = "\n".join(buffer).rstrip() + "\n" if buffer else tracks[current_track]
        buffer = []

    for line in lines:
        if not in_tracks:
            if line.strip() == "## Task tracks":
                in_tracks = True
            continue

        # Stop condition: next top-level section.
        if in_tracks and line.startswith("## ") and line.strip() != "## Task tracks":
            flush()
            break

        m = re.match(r"^###\s+(Contract|Service|Surface|Data|Ops)\s*$", line.strip(), flags=re.IGNORECASE)
        if m:
            flush()
            current_track = m.group(1).capitalize()
            continue

        if current_track is not None:
            buffer.append(line)

    flush()
    return tracks


def parse_patch_ladder_table(minor_doc_text: str, *, expected_era: int, expected_minor: int) -> list[PatchRow]:
    """
    Parse markdown table rows under `## Patch ladder (...)`.

    Supported shapes:
      - `| Patch | Codename | Focus | Evidence gate |`
      - `| Patch | Codename | Focus |` (era 1 style; evidence gate optional)
    """
    # Regex matches both with and without backticks around patch ref.
    row_re = re.compile(
        r"^\|\s*`?(?P<patch>\d+\.\d+\.\d+)\s*`?\s*\|\s*(?P<codename>[^|]+?)\s*\|\s*(?P<focus>[^|]+?)"
        r"(?:\s*\|\s*(?P<evidence>[^|]+?)\s*)?\|\s*$"
    )

    lines = minor_doc_text.splitlines()
    in_ladder = False
    rows: list[PatchRow] = []

    for line in lines:
        if not in_ladder:
            if line.strip().startswith("## Patch ladder"):
                in_ladder = True
            continue

        # Stop when we reach a patch subsection (era 1) or the next top-level section.
        if in_ladder and (line.startswith("### ") or line.startswith("## ") and not line.startswith("## Patch ladder")):
            break

        line_stripped = line.strip()
        if not line_stripped.startswith("|"):
            continue

        m = row_re.match(line_stripped)
        if not m:
            continue

        patch_ref = m.group("patch").strip()
        patch_m = re.match(r"^(?P<era>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$", patch_ref)
        if not patch_m:
            continue

        era = int(patch_m.group("era"))
        minor = int(patch_m.group("minor"))
        if era != expected_era or minor != expected_minor:
            continue

        patch_index = int(patch_m.group("patch"))
        codename = m.group("codename").strip()
        focus = m.group("focus").strip()
        evidence = (m.group("evidence").strip() if m.group("evidence") is not None else "").strip()

        rows.append(
            PatchRow(
                patch_ref=patch_ref,
                patch_index=patch_index,
                codename=codename,
                focus=focus,
                evidence_gate=evidence or "",
            )
        )

    # Ensure consistent ordering.
    rows.sort(key=lambda r: r.patch_index)
    return rows


def parse_patch_subsection_bodies(minor_doc_text: str, *, expected_era: int, expected_minor: int) -> Dict[int, str]:
    """
    Extracts bodies keyed by patch index for headings:
      ### X.Y.Z — ...
    Returns the raw body text (excluding the heading line).
    """
    # Capture until next `###` heading at same level.
    heading_re = re.compile(rf"^###\s+{expected_era}\.{expected_minor}\.(?P<patch>\d+)\s*[—-]\s+.+?\s*$")
    lines = minor_doc_text.splitlines()

    out: Dict[int, List[str]] = {}
    current_patch: Optional[int] = None
    body: list[str] = []

    def flush() -> None:
        nonlocal current_patch, body
        if current_patch is None:
            return
        out[current_patch] = body[:]
        body = []

    for i, line in enumerate(lines):
        m = heading_re.match(line.strip())
        if m:
            flush()
            current_patch = int(m.group("patch"))
            continue

        if current_patch is not None:
            # Stop when we hit the next `###` heading for any patch.
            if line.startswith("### ") and not heading_re.match(line.strip()):
                # If a different subsection appears, stop collecting.
                flush()
                current_patch = None
                continue
            body.append(line)

    flush()
    return {k: "\n".join(v).strip("\n") for k, v in out.items()}


def parse_bold_tracks_from_patch_body(body_text: str) -> Dict[str, str]:
    """
    Convert bodies like:
      **Contract**
      - ...
      **Service**
      - ...
    into:
      { "Contract": "...raw block...", ... }
    """
    track_names = ["Contract", "Service", "Surface", "Data", "Ops"]
    # Accept optional whitespace: **Contract** or **Contract** (with no colon)
    track_heading_re = re.compile(r"^\*\*\s*(Contract|Service|Surface|Data|Ops)\s*\*\*\s*$", re.IGNORECASE)

    out: Dict[str, List[str]] = {t: [] for t in track_names}
    current: Optional[str] = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal current, buffer
        if current is None:
            return
        out[current] = buffer[:]
        buffer = []

    for line in body_text.splitlines():
        m = track_heading_re.match(line.strip())
        if m:
            flush()
            current = m.group(1).capitalize()
            continue
        if current is not None:
            buffer.append(line)

    flush()
    return {k: "\n".join(v).strip("\n") + "\n" if v else "" for k, v in out.items()}


def get_patch_codename_ladder_from_era0(docs_root: Path) -> Dict[int, str]:
    """
    Uses the existing era-0 `0.0 — Pre-repo baseline.md` patch ladder table
    as the canonical fallback codename mapping for patch indices 0..9.
    """
    era0_dir = None
    for d in docs_root.iterdir():
        if not d.is_dir():
            continue
        m = ERA_DIR_RE.match(d.name)
        if m and int(m.group("era")) == 0:
            era0_dir = d
            break
    if era0_dir is None:
        return {i: f"Patch{i}" for i in range(10)}

    minor0 = era0_dir / "0.0 — Pre-repo baseline.md"
    if not minor0.exists():
        # Fallback: find the first minor doc that starts with "0.0 —"
        candidates = list(era0_dir.glob("0.0*—*.md")) + list(era0_dir.glob('0.0*-*.md'))
        if candidates:
            minor0 = candidates[0]

    if not minor0.exists():
        return {i: f"Patch{i}" for i in range(10)}

    rows = parse_patch_ladder_table(read_text(minor0), expected_era=0, expected_minor=0)
    if not rows:
        return {i: f"Patch{i}" for i in range(10)}

    return {r.patch_index: sanitize_title_for_filename(r.codename) for r in rows}


def sanitize_patch_codename(codename: str) -> str:
    # Ensure we never end up with empty filenames.
    cleaned = sanitize_title_for_filename(codename).strip()
    return cleaned or "Untitled"


def patch_filename(era: int, minor: int, patch_index: int, codename: str) -> str:
    codename_s = sanitize_patch_codename(codename)
    return f"{era}.{minor}.{patch_index} {DASH} {codename_s}.md"


def assemble_table_based_patch_tasks(minor_doc_text: str) -> Dict[str, str]:
    """
    Returns track blocks for patch docs in table-based eras: copies the minor's `## Task tracks`.
    """
    return extract_task_tracks_from_minor(minor_doc_text)


def build_patch_doc_text(
    *,
    era: int,
    minor: int,
    patch_index: int,
    codename: str,
    focus: str,
    evidence_gate: str,
    era_name: str,
    minor_doc_name: str,
    track_blocks: Dict[str, str],
) -> str:
    title_codename = codename
    # Keep front-matter consistent with planned schema (minus any non-existent file links).
    era_link = "./README.md"
    minor_link = f"./{minor_doc_name}"

    # Normalize focus/evidence.
    focus_line = focus.strip() if focus.strip() else "TBD"
    evidence_line = evidence_gate.strip() if evidence_gate.strip() else "TBD — evidence gate TBD"

    parts: list[str] = []
    parts.append(f"# {era}.{minor}.{patch_index} {DASH} {title_codename}\n")
    parts.append(f"- **Era:** [{era}.{0 if era == 0 else era} — {era_name}]({era_link})")
    parts.append(f"- **Minor:** [{era}.{minor} — {minor_doc_name.rsplit('—', 1)[-1].strip().replace('.md','').strip()}]({minor_link})")
    parts.append(f"- **Codename:** {title_codename}")
    parts.append(f"- **Status:** planned\n")

    parts.append("## Focus")
    parts.append(f"{focus_line}\n")

    parts.append("## Tasks")
    for t in ["Contract", "Service", "Surface", "Data", "Ops"]:
        block = track_blocks.get(t, "").rstrip("\n")
        if not block.strip():
            continue
        parts.append(f"### {t}")
        parts.append(block)
        if not block.endswith("\n"):
            parts.append("")

    parts.append("## Evidence gate")
    parts.append(f"{evidence_line}\n")

    return "\n".join(parts).rstrip() + "\n"


def build_patch_doc_text_from_patch_body(
    *,
    era: int,
    minor: int,
    patch_index: int,
    codename: str,
    focus: str,
    evidence_gate: str,
    era_name: str,
    minor_doc_name: str,
    patch_body_text: str,
) -> str:
    tracks = parse_bold_tracks_from_patch_body(patch_body_text)
    return build_patch_doc_text(
        era=era,
        minor=minor,
        patch_index=patch_index,
        codename=codename,
        focus=focus,
        evidence_gate=evidence_gate,
        era_name=era_name,
        minor_doc_name=minor_doc_name,
        track_blocks=tracks,
    )


def extract_minor_task_track_bullets(minor_doc_text: str) -> Dict[str, List[str]]:
    """
    Returns track bullets as individual lines for slicing across patches.
    """
    blocks = extract_task_tracks_from_minor(minor_doc_text)
    out: Dict[str, List[str]] = {"Contract": [], "Service": [], "Surface": [], "Data": [], "Ops": []}
    for track, block in blocks.items():
        bullets: list[str] = []
        for line in block.splitlines():
            if line.lstrip().startswith("- "):
                bullets.append(line.strip())
        out[track] = bullets
    return out


def parse_task_pack_bullets(task_pack_text: str) -> Dict[str, List[str]]:
    """
    Extracts bullet lists from a `*-task-pack.md` file.

    Expected headings like:
      ## Contract track
      ## Service track
      ## Database / data track
      ## Surface track
      ## Ops track
    """
    # Map heading variants -> our standard keys.
    heading_map = {
        "contract track": "Contract",
        "service track": "Service",
        "database / data track": "Data",
        "database/data track": "Data",
        "database track": "Data",
        "data track": "Data",
        "surface track": "Surface",
        "ops track": "Ops",
    }

    lines = task_pack_text.splitlines()
    current: Optional[str] = None
    out: Dict[str, List[str]] = {"Contract": [], "Service": [], "Surface": [], "Data": [], "Ops": []}
    buffer: list[str] = []

    def flush() -> None:
        nonlocal current, buffer
        if current is None:
            buffer = []
            return
        # Keep only bullet lines; other text is ignored.
        for line in buffer:
            if line.lstrip().startswith("- "):
                out[current].append(line.strip())
        buffer = []

    for line in lines:
        m = re.match(r"^##\s+(.*?)\s*$", line.strip())
        if m:
            flush()
            key = m.group(1).strip().lower()
            current = heading_map.get(key)
            buffer = []
            continue
        if current is not None:
            buffer.append(line)

    flush()
    return out


def discover_task_packs(era_dir: Path) -> list[Path]:
    return sorted([p for p in era_dir.glob("*-task-pack.md") if p.is_file()])


def build_synthesized_tracks_for_patch(
    patch_index: int,
    minor_bullets: Dict[str, List[str]],
    era_task_packs: list[Path],
    task_pack_bullets: Dict[str, List[str]],
) -> Dict[str, str]:
    """
    Build track blocks for synthesized patch docs by slicing bullets.

    Patch slot mapping (per plan):
      - 0..3: Contract + Service
      - 4..6: Surface + Data
      - 7..8: Ops
      - 9: exit gate/evidence -> Ops (plus any remaining)
    """
    tracks_out: Dict[str, List[str]] = {"Contract": [], "Service": [], "Surface": [], "Data": [], "Ops": []}

    def pick_slice(items: List[str], stride: int, residue: int, *, limit: int = 4) -> List[str]:
        if stride <= 0:
            stride = 1
        chosen = [items[i] for i in range(len(items)) if (i % stride) == residue]
        return chosen[:limit]

    # Include minor bullets + task-pack bullets.
    for track in tracks_out.keys():
        tracks_out[track] = []

    # Contract + Service for patches 0..3 (map each patch to residue in its track list).
    if patch_index in (0, 1, 2, 3):
        residue = patch_index
        tracks_out["Contract"] = pick_slice(minor_bullets.get("Contract", []) + task_pack_bullets.get("Contract", []), stride=4, residue=residue)
        tracks_out["Service"] = pick_slice(minor_bullets.get("Service", []) + task_pack_bullets.get("Service", []), stride=4, residue=residue)
    # Surface + Data for patches 4..6.
    elif patch_index in (4, 5, 6):
        residue = patch_index - 4
        tracks_out["Surface"] = pick_slice(minor_bullets.get("Surface", []) + task_pack_bullets.get("Surface", []), stride=3, residue=residue)
        tracks_out["Data"] = pick_slice(minor_bullets.get("Data", []) + task_pack_bullets.get("Data", []), stride=3, residue=residue)
    # Ops for patches 7..8.
    elif patch_index in (7, 8):
        residue = patch_index - 7
        tracks_out["Ops"] = pick_slice(minor_bullets.get("Ops", []) + task_pack_bullets.get("Ops", []), stride=2, residue=residue)
    # Patch 9: include last items; prefer Ops.
    else:
        # Exit gate: include some ops bullets plus fallback.
        ops_items = minor_bullets.get("Ops", []) + task_pack_bullets.get("Ops", [])
        # Take last 6 bullets to represent the "exit gate" hardening.
        tracks_out["Ops"] = ops_items[-6:]

    # Ensure each included section has at least one line for readability.
    for track, items in list(tracks_out.items()):
        if not items:
            if track in ("Contract", "Service", "Surface", "Data", "Ops"):
                # Only add TBD for tracks expected in this patch.
                if (
                    (patch_index in (0, 1, 2, 3) and track in ("Contract", "Service"))
                    or (patch_index in (4, 5, 6) and track in ("Surface", "Data"))
                    or (patch_index in (7, 8) and track == "Ops")
                    or (patch_index == 9 and track == "Ops")
                ):
                    tracks_out[track] = [f"- TBD for {era_dir_name_hint()}"]

    # Convert to markdown blocks.
    return {k: "\n".join(v) + ("\n" if v else "") for k, v in tracks_out.items()}


def era_dir_name_hint() -> str:
    # We don't always have the era name at this layer; keep placeholder short.
    return "exit gate"


def synthesize_focus_and_evidence_for_slot(patch_index: int, minor_title: str) -> Tuple[str, str]:
    """
    Focus/evidence fallback used when patch ladder data is missing.
    """
    if patch_index in (0, 1, 2, 3):
        focus = f"{minor_title} — contract/service micro-slice (patch {patch_index})"
        evidence = f"Derived evidence: align with `### Contract/Service` bullets in minor doc for {minor_title}"
    elif patch_index in (4, 5, 6):
        focus = f"{minor_title} — surface/data micro-slice (patch {patch_index})"
        evidence = f"Derived evidence: align with `### Surface/Data` bullets in minor doc for {minor_title}"
    elif patch_index in (7, 8):
        focus = f"{minor_title} — ops hardening micro-slice (patch {patch_index})"
        evidence = f"Derived evidence: align with `### Ops` bullets in minor doc for {minor_title}"
    else:
        focus = f"{minor_title} — exit gate / release evidence (patch 9)"
        evidence = f"Derived evidence: cover end-to-end validation steps and rollback readiness for {minor_title}"
    return focus, evidence


def update_minor_doc_with_patch_links(
    minor_doc_path: Path,
    patch_docs: list[Tuple[str, str]],
    *,
    apply: bool,
    dry_run: bool,
) -> bool:
    """
    patch_docs: list of (patch_ref, patch_filename)
    """
    text = read_text(minor_doc_path)
    new_section_lines: list[str] = []
    new_section_lines.append("## Patches")
    new_section_lines.append("")
    new_section_lines.append("| Patch | Codename | Doc |")
    new_section_lines.append("| --- | --- | --- |")
    for patch_ref, patch_file in patch_docs:
        m = PATCH_FILE_RE.match(patch_file)
        codename = m.group("codename") if m else patch_file
        # Ensure visible codename is readable.
        doc_link = f"[`{patch_ref}` — {codename}]({patch_file})"
        new_section_lines.append(f"| `{patch_ref}` | {codename} | {doc_link} |")
    new_section = "\n".join(new_section_lines).rstrip() + "\n"

    # Replace existing `## Patches` block if present.
    replaced = False
    if "## Patches" in text:
        # Find start of patches section and replace until next `## ` heading at same level.
        lines = text.splitlines()
        start_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "## Patches":
                start_idx = i
                break
        if start_idx is not None:
            end_idx = len(lines)
            for j in range(start_idx + 1, len(lines)):
                if lines[j].startswith("## ") and lines[j].strip() != "## Patches":
                    end_idx = j
                    break
            lines = lines[:start_idx] + [new_section.rstrip("\n")] + lines[end_idx:]
            new_text = "\n".join(lines).rstrip() + "\n"
            replaced = True
        else:
            new_text = text + "\n" + new_section
    else:
        new_text = text.rstrip() + "\n\n" + new_section

    if new_text == text:
        return False

    if apply and not dry_run:
        minor_doc_path.write_text(new_text, encoding="utf-8")
        return True
    return True  # planned change


def discover_era_name(era_dir: Path) -> str:
    # Era dir names are like "0. Foundation ..." or "5. Contact360 AI workflows".
    # Extract trailing title after "X.".
    m = ERA_DIR_RE.match(era_dir.name)
    if not m:
        return era_dir.name
    era_prefix = f"{m.group('era')}."
    return era_dir.name[len(era_prefix) :].strip()


def synthesize_patch_row_from_slot(
    patch_index: int,
    codename_ladder: Dict[int, str],
    minor_doc_text: str,
    minor_title: str,
) -> PatchRow:
    codename = codename_ladder.get(patch_index, f"Patch{patch_index}")
    focus, evidence = synthesize_focus_and_evidence_for_slot(patch_index, minor_title=minor_title)
    return PatchRow(
        patch_ref="",
        patch_index=patch_index,
        codename=codename,
        focus=focus,
        evidence_gate=evidence,
    )


def run_creation(
    docs_root: Path,
    eras: Optional[set[int]],
    apply: bool,
    dry_run: bool,
    report_json: Optional[Path],
    on_conflict: str,
) -> int:
    codename_ladder = get_patch_codename_ladder_from_era0(docs_root)

    # Gather a patch summary report.
    report: list[dict] = []

    era_dirs = discover_era_dirs(docs_root, eras=eras)
    if not era_dirs:
        print("No era dirs discovered.")
        return 0

    for era_dir in era_dirs:
        m = ERA_DIR_RE.match(era_dir.name)
        if not m:
            continue
        era = int(m.group("era"))
        era_name = discover_era_name(era_dir)

        minor_docs = discover_minor_docs(era_dir, era=era)
        if not minor_docs:
            continue

        # For synthesized patches we need all task packs in this era.
        task_packs = discover_task_packs(era_dir)
        task_pack_bullets_all: Dict[str, List[str]] = {"Contract": [], "Service": [], "Surface": [], "Data": [], "Ops": []}
        task_pack_texts_by_path: Dict[Path, str] = {}
        for tp in task_packs:
            if dry_run and not apply:
                pass
            txt = read_text(tp)
            task_pack_texts_by_path[tp] = txt
            bullets = parse_task_pack_bullets(txt)
            for k, v in bullets.items():
                task_pack_bullets_all[k].extend(v)

        for minor_doc in minor_docs:
            minor_m = MINOR_FILE_RE.match(minor_doc.name)
            if not minor_m:
                continue
            minor = int(minor_m.group("minor"))
            minor_doc_text = read_text(minor_doc)
            minor_title_raw = minor_m.group("title").strip()
            minor_title = minor_title_raw.replace(".md", "").strip()

            # Extract patch data if a ladder exists.
            ladder_rows = parse_patch_ladder_table(minor_doc_text, expected_era=era, expected_minor=minor)
            patch_rows_by_index: Dict[int, PatchRow] = {}

            patch_subsections = parse_patch_subsection_bodies(minor_doc_text, expected_era=era, expected_minor=minor)

            if ladder_rows:
                for r in ladder_rows:
                    patch_rows_by_index[r.patch_index] = r
            else:
                # No ladder: synthesize rows, but patch names use fallback codename ladder.
                for pi in range(10):
                    row = synthesize_patch_row_from_slot(pi, codename_ladder, minor_doc_text, minor_title=minor_title)
                    row = PatchRow(
                        patch_ref=f"{era}.{minor}.{pi}",
                        patch_index=pi,
                        codename=row.codename,
                        focus=row.focus,
                        evidence_gate=row.evidence_gate,
                    )
                    patch_rows_by_index[pi] = row

            # Create patch docs for patch indices 0..9.
            patch_docs_for_minor: list[Tuple[str, str]] = []
            minor_task_tracks = extract_task_tracks_from_minor(minor_doc_text)  # used by table-based eras
            minor_bullets = extract_minor_task_track_bullets(minor_doc_text)  # used by synthesized eras

            for pi in range(10):
                row = patch_rows_by_index.get(pi)
                if not row:
                    continue
                p_ref = f"{era}.{minor}.{pi}"
                codename = row.codename
                out_name = patch_filename(era, minor, pi, codename)
                out_path = era_dir / out_name

                if out_path.exists():
                    if on_conflict == "skip":
                        patch_docs_for_minor.append((p_ref, out_name))
                        continue
                    if on_conflict == "error":
                        raise FileExistsError(f"Patch doc exists: {out_path}")

                if ladder_rows:
                    # If patch subsections exist, we can prefer them (era 1 style).
                    if pi in patch_subsections and patch_subsections[pi].strip():
                        patch_body = patch_subsections[pi]
                        track_blocks: Dict[str, str] = parse_bold_tracks_from_patch_body(patch_body)
                        patch_text = build_patch_doc_text(
                            era=era,
                            minor=minor,
                            patch_index=pi,
                            codename=codename,
                            focus=row.focus,
                            evidence_gate=row.evidence_gate,
                            era_name=era_name,
                            minor_doc_name=minor_doc.name,
                            track_blocks=track_blocks,
                        )
                    else:
                        track_blocks = assemble_table_based_patch_tasks(minor_doc_text)
                        patch_text = build_patch_doc_text(
                            era=era,
                            minor=minor,
                            patch_index=pi,
                            codename=codename,
                            focus=row.focus,
                            evidence_gate=row.evidence_gate,
                            era_name=era_name,
                            minor_doc_name=minor_doc.name,
                            track_blocks=track_blocks,
                        )
                else:
                    # Synthesized patches (eras 5,6,8,9,10 and some of era 7).
                    tracks = build_synthesized_tracks_for_patch(
                        patch_index=pi,
                        minor_bullets=minor_bullets,
                        era_task_packs=task_packs,
                        task_pack_bullets=task_pack_bullets_all,
                    )
                    focus, evidence = row.focus, row.evidence_gate
                    patch_text = build_patch_doc_text(
                        era=era,
                        minor=minor,
                        patch_index=pi,
                        codename=codename,
                        focus=focus,
                        evidence_gate=evidence,
                        era_name=era_name,
                        minor_doc_name=minor_doc.name,
                        track_blocks=tracks,
                    )

                if apply and not dry_run:
                    changed = write_text_if_changed(out_path, patch_text, apply=True)
                    if changed:
                        print(f"[apply] wrote patch doc: {out_path.name}")
                else:
                    print(f"[dry-run] would write patch doc: {out_path.relative_to(docs_root)}")

                report.append(
                    {
                        "era": era,
                        "minor": minor,
                        "patch": pi,
                        "patch_ref": p_ref,
                        "codename": codename,
                        "out_path": str(out_path),
                        "created_or_updated": bool(apply and (not dry_run)),
                    }
                )
                patch_docs_for_minor.append((p_ref, out_name))

            # Update minor doc with links to patch docs.
            patch_docs_for_minor.sort(key=lambda t: int(t[0].split(".")[-1]))
            if apply and not dry_run:
                update_minor_doc_with_patch_links(minor_doc, patch_docs_for_minor, apply=True, dry_run=False)
            else:
                # In dry-run, we still report intent.
                pass

    if report_json:
        if apply and not dry_run:
            report_json.parent.mkdir(parents=True, exist_ok=True)
            report_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        else:
            report_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    return 0


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs-root", type=str, default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--eras", type=str, default="", help="Comma-separated era numbers to include, e.g. 0,1,2. Empty = all.")
    ap.add_argument("--dry-run", action="store_true", help="Print planned work without writing.")
    ap.add_argument("--apply", action="store_true", help="Write changes (implies not dry-run).")
    ap.add_argument("--report-json", type=str, default="", help="Optional report JSON path.")
    ap.add_argument("--on-conflict", type=str, default="skip", choices=["skip", "error"], help="Behavior when patch doc already exists.")
    args = ap.parse_args(argv)

    docs_root = Path(args.docs_root)
    if not docs_root.exists():
        raise FileNotFoundError(f"docs-root does not exist: {docs_root}")

    eras: Optional[set[int]] = None
    if args.eras.strip():
        eras = {int(x.strip()) for x in args.eras.split(",") if x.strip()}

    dry_run = bool(args.dry_run) or (not bool(args.apply))
    apply = bool(args.apply) and not dry_run

    report_path = Path(args.report_json) if args.report_json.strip() else None

    return run_creation(
        docs_root=docs_root,
        eras=eras,
        apply=apply,
        dry_run=dry_run,
        report_json=report_path,
        on_conflict=args.on_conflict,
    )


if __name__ == "__main__":
    raise SystemExit(main())

