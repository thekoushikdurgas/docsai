#!/usr/bin/env python3
"""
Enrich docs/4. Contact360 Extension.../4.N.P — *.md with Micro-gate + Service task slices
from era `4.x` *extension-sn* / *extension-salesnav* task packs (P0→.0–.2, P1→.3–.6, Ops→.7–.9).
No-ops when task packs are absent.
"""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "4. Contact360 Extension and Sales Navigator maturity"

PACK_KEY_TO_FILE = {
    "appointment360": "appointment360-extension-sn-task-pack.md",
    "connectra": "connectra-extension-sn-task-pack.md",
    "contact-ai": "contact-ai-extension-sn-task-pack.md",
    "emailapis": "emailapis-extension-salesnav-task-pack.md",
    "emailcampaign": "emailcampaign-extension-sn-task-pack.md",
    "jobs": "jobs-extension-sn-task-pack.md",
    "logsapi": "logsapi-extension-salesnav-task-pack.md",
    "mailvetter": "mailvetter-extension-sn-task-pack.md",
    "s3storage": "s3storage-extension-sn-task-pack.md",
    "salesnavigator": "salesnavigator-extension-sn-task-pack.md",
}

MINOR_PRIMARY_PACKS: dict[str, list[str]] = {
    "4.0": ["connectra", "salesnavigator", "appointment360", "logsapi", "s3storage", "jobs"],
    "4.1": ["appointment360", "logsapi", "emailapis"],
    "4.2": ["salesnavigator", "connectra", "jobs", "appointment360"],
    "4.3": ["connectra", "jobs", "logsapi", "salesnavigator"],
    "4.4": ["logsapi", "salesnavigator", "jobs"],
    "4.5": ["salesnavigator", "appointment360", "logsapi"],
    "4.6": ["appointment360", "connectra", "salesnavigator"],
    "4.7": ["emailcampaign", "jobs", "appointment360", "mailvetter", "connectra"],
    "4.8": ["contact-ai", "appointment360", "emailapis", "salesnavigator"],
    "4.9": ["jobs", "salesnavigator", "connectra", "logsapi", "s3storage"],
    "4.10": list(PACK_KEY_TO_FILE.keys()),
}

TRACK_OWNER_FIRST = frozenset(
    {"contract", "service", "surface", "data", "ops", "track", "owner (default)"}
)


def human_pack_name(key: str) -> str:
    return {
        "appointment360": "Appointment360 (gateway)",
        "emailapis": "emailapis / emailapigo",
        "logsapi": "logs.api",
        "contact-ai": "contact.ai",
    }.get(key, key.replace("_", " ").title())


def extract_table_p0_p1(text: str) -> tuple[list[str], list[str]]:
    p0, p1 = [], []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        pr: str | None = None
        if cells[-1] in ("P0", "P1"):
            pr = cells[-1]
        elif len(cells) >= 3 and cells[1] in ("P0", "P1"):
            pr = cells[1]
        if pr is None:
            continue
        first = cells[0]
        fl = first.lower()
        if fl in ("task", "track", "field", "---") or first.startswith("---"):
            continue
        if len(cells) >= 3 and cells[1] not in ("P0", "P1") and fl in TRACK_OWNER_FIRST:
            continue
        task = re.sub(r"`+", "", first).strip()
        if len(task) < 4:
            continue
        if pr == "P0":
            p0.append(task)
        else:
            p1.append(task)
    return p0, p1


def extract_under_heading(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    hdr = "## " + heading
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == hdr:
            i += 1
            while i < len(lines):
                raw = lines[i]
                st = raw.strip()
                if st.startswith("---") and len(st) >= 3:
                    break
                if raw.startswith("##"):
                    break
                if st.startswith("- "):
                    s = re.sub(r"^-\s*\[[ x]\]\s*", "- ", st)
                    if len(s) > 4:
                        out.append(s[2:].strip())
                i += 1
            break
        i += 1
    return out


def extract_section_bullets(text: str, header: str) -> list[str]:
    lines = text.splitlines()
    out: list[str] = []
    target = ("## " + header).lower()
    i = 0
    while i < len(lines):
        if lines[i].strip().lower() == target:
            i += 1
            while i < len(lines) and not lines[i].startswith("##"):
                s = lines[i].strip()
                if s.startswith("- "):
                    s = re.sub(r"^-\s*\[[ x]\]\s*", "- ", s)
                    if len(s) > 4:
                        out.append(s[2:].strip())
                i += 1
            break
        i += 1
    return out


def extract_track_bullets(text: str, track: str) -> list[str]:
    """Bullets under `## {track} track` until next `## ` (not `###`)."""
    lines = text.splitlines()
    hdr = f"## {track} track"
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == hdr:
            i += 1
            while i < len(lines):
                raw = lines[i]
                if raw.startswith("## ") and not raw.startswith("###"):
                    break
                st = raw.strip()
                if st.startswith("- "):
                    s = re.sub(r"^-\s*\[[ x]\]\s*", "- ", st)
                    if len(s) > 4:
                        out.append(s[2:].strip())
                i += 1
            break
        i += 1
    return out


def extract_ops_bullets(text: str) -> list[str]:
    out: list[str] = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^##\s+Ops", line, re.I):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("##"):
                s = lines[j].strip()
                if s.startswith("- "):
                    s = re.sub(r"^-\s*\[[ x]\]\s*", "- ", s)
                    if len(s) > 4:
                        out.append(s[2:].strip())
                j += 1
            break
    return out


def non_table_pack_slices(text: str, patch_digit: int) -> list[str]:
    core = extract_under_heading(text, "Core tasks")
    harden = extract_under_heading(text, "Additional hardening")
    completion = extract_under_heading(text, "Completion gate")
    pool = core + harden + completion
    if not pool:
        return []
    n = len(pool)
    if n <= 6:
        if patch_digit <= 2:
            return pool
        if patch_digit <= 6:
            return pool
        return harden or pool
    t = max(2, n // 3)
    if patch_digit <= 2:
        return pool[: t * 2]
    if patch_digit <= 6:
        return pool[t:]
    return harden or pool[-8:] or pool


def track_section_bundle(text: str) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    c = extract_track_bullets(text, "Contract") or extract_section_bullets(text, "Contract tasks")
    s = extract_track_bullets(text, "Service") or extract_section_bullets(text, "Service tasks")
    surf = extract_track_bullets(text, "Surface") or extract_section_bullets(text, "Surface tasks")
    d = extract_track_bullets(text, "Data") or extract_section_bullets(text, "Data tasks")
    o = extract_track_bullets(text, "Ops") or extract_section_bullets(text, "Ops tasks")
    return c, s, surf, d, o


def pack_slices_for_patch(_minor: str, patch_digit: int, pack_path: Path) -> list[str]:
    text = pack_path.read_text(encoding="utf-8")
    p0, p1 = extract_table_p0_p1(text)
    ops = extract_ops_bullets(text)
    if not p0 and not p1:
        nt = non_table_pack_slices(text, patch_digit)
        if nt:
            return nt
        c, s, surf, d, o = track_section_bundle(text)
        if c or s or surf or d or o:
            if patch_digit <= 2:
                return c + s + d[: max(1, len(d) // 2 + 1)] if d else c + s
            if patch_digit <= 6:
                return surf + d + s
            tail = o or ops
            if tail:
                return tail
            return (surf[-12:] if surf else []) + (c[-8:] if c else [])
    if patch_digit <= 2:
        return p0
    if patch_digit <= 6:
        return p1
    return ops if ops else (p1[-3:] if len(p1) > 3 else p1)


def build_slices(patch_id: str) -> str:
    parts = patch_id.split(".")
    minor = f"{parts[0]}.{parts[1]}"
    p = int(parts[2])
    keys = MINOR_PRIMARY_PACKS.get(minor, [])
    lines = [
        "## Service task slices",
        "> Merged from era `4.x` extension/SN task packs (P0→`.0`–`.2`, P1→`.3`–`.6`, Ops→`.7`–`.9`).",
        "",
    ]
    any_content = False
    for key in keys:
        fn = PACK_KEY_TO_FILE.get(key)
        if not fn:
            continue
        path = ERA / fn
        if not path.exists():
            continue
        bullets = pack_slices_for_patch(minor, p, path)
        if not bullets:
            continue
        any_content = True
        lines.append(f"### {human_pack_name(key)}")
        for b in bullets[:40]:
            lines.append(f"- {b}")
        lines.append("")
    if not any_content:
        return ""
    return "\n".join(lines).rstrip() + "\n"


def micro_gate_block(minor: str, _patch_digit: int) -> str:
    fe = {
        "4.0": "Harbor charter — service inventory, CI/docs; minimal product UX.",
        "4.1": "Extension auth/session — `extension-auth.md`, storage + refresh flows.",
        "4.2": "SN scrape/save client surfaces; ingestion provenance display if any.",
        "4.3": "Sync/conflict narratives in extension or dashboard.",
        "4.4": "`extension-telemetry.md` / operator dashboards.",
        "4.5": "Popup MV3 — progress, retry, error UI.",
        "4.6": "Dashboard SN panels, history/source filters.",
        "4.7": "Campaign audience UX, preview/send confirmations.",
        "4.8": "`messages.contacts[]` consumers, optional AI panel, CSP.",
        "4.9": "Rate-limit and error surfaces; retry affordances.",
        "4.10": "Exit sweep — evidence/docs; avoid new UX unless ops-only.",
    }.get(minor, "See minor Frontend/extension scope.")
    rows = [
        (
            "**Contract**",
            "Extension/SN REST, GraphQL modules, CSP — `docs/backend/apis/` + endpoint matrices updated?",
            "Document at patch closeout.",
        ),
        (
            "**Service**",
            "SN scrape/save, Connectra upsert, jobs DAG, session refresh — smoke + idempotency?",
            "Document smoke paths.",
        ),
        (
            "**Surface**",
            "Extension popup, dashboard SN/campaign panels, operator flows changed?",
            "Document UX delta or N/A.",
        ),
        (
            "**Frontend**",
            "Which extension MV3 + dashboard routes/hooks for this patch?",
            fe + " Document at closeout.",
        ),
        (
            "**Data**",
            "Provenance fields, audience tables, `messages.contacts[]` — migrations + lineage?",
            "Document lineage or N/A.",
        ),
        (
            "**Ops**",
            "`logs.api` events, S3 evidence, runbooks, rate/retry — delta recorded?",
            "Document ops delta or N/A.",
        ),
    ]
    md = ["## Micro-gate", ""]
    md.append("| Track | Gate question | Answer / Evidence (fill at patch closeout) |")
    md.append("| --- | --- | --- |")
    for trk, q, ans in rows:
        md.append(f"| {trk} | {q} | {ans} |")
    md.append("")
    return "\n".join(md)


def fix_era_line(content: str) -> str:
    old = "- **Era:** [4.4 — Contact360 Extension and Sales Navigator maturity](./README.md)"
    new = (
        "- **Era:** `4.x` Extension/SN maturity — hub [`versions.md`](../versions.md) · minors start at "
        "[`4.0 — Harbor`](4.0%20%E2%80%94%20Harbor.md)"
    )
    return content.replace(old, new)


SLICE_HDR = "## Service task slices"


def strip_service_slices(head: str) -> str:
    i = head.find(SLICE_HDR)
    if i == -1:
        return head
    return head[:i].rstrip()


def enrich_one(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = fix_era_line(text)
    m = re.match(r"# (4\.\d+\.\d+) — .+", text)
    if not m:
        path.write_text(text, encoding="utf-8")
        return
    patch_id = m.group(1)
    minor = ".".join(patch_id.split(".")[:2])
    patch_digit = int(patch_id.split(".")[2])
    if "## Tasks" not in text or "## Evidence gate" not in text:
        path.write_text(text, encoding="utf-8")
        return
    parts = text.split("## Evidence gate", 1)
    head, tail = parts[0], "## Evidence gate" + parts[1]
    head = strip_service_slices(head)
    if "## Micro-gate" not in head:
        pre, rest = head.split("## Tasks", 1)
        mg = micro_gate_block(minor, patch_digit)
        head = pre.rstrip() + "\n\n" + mg + "\n## Tasks" + rest
    slices = build_slices(patch_id)
    if slices:
        head = head.rstrip() + "\n\n" + slices.rstrip() + "\n"
    if not head.endswith("\n\n"):
        head = head.rstrip() + "\n\n"
    path.write_text(head + tail, encoding="utf-8")


def main() -> None:
    if not ERA.is_dir():
        print("4.x era folder not found")
        return
    packs = [p for p in ERA.glob("*.md") if "task-pack" in p.name.lower()]
    if not packs:
        print("No *task-pack*.md files found; exiting.")
        return
    for path in sorted(ERA.glob("4.*.* — *.md")):
        enrich_one(path)
    print(f"Processed 4.x patch files in {ERA}")


if __name__ == "__main__":
    main()
