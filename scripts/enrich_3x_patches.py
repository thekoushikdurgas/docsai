#!/usr/bin/env python3
"""
Enrich docs/3. Contact360 contact and company.../3.N.P — *.md with Micro-gate + Service task slices
from *contact-company* task packs (P0→.0–.2, P1→.3–.6, Ops→.7–.9).
No-ops when task packs are absent.
"""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "3. Contact360 contact and company data system"

PACK_KEY_TO_FILE = {
    "appointment360": "appointment360-contact-company-task-pack.md",
    "connectra": "connectra-contact-company-task-pack.md",
    "contact-ai": "contact-ai-contact-company-task-pack.md",
    "emailapis": "emailapis-contact-company-task-pack.md",
    "emailcampaign": "emailcampaign-contact-company-task-pack.md",
    "jobs": "jobs-contact-company-task-pack.md",
    "logsapi": "logsapi-contact-company-data-task-pack.md",
    "mailvetter": "mailvetter-contact-company-task-pack.md",
    "s3storage": "s3storage-contact-company-task-pack.md",
    "salesnavigator": "salesnavigator-contact-company-task-pack.md",
}

MINOR_PRIMARY_PACKS: dict[str, list[str]] = {
    "3.0": ["connectra", "appointment360", "logsapi"],
    "3.1": ["connectra", "appointment360"],
    "3.2": ["appointment360", "connectra"],
    "3.3": ["connectra", "appointment360"],
    "3.4": ["appointment360"],
    "3.5": ["jobs", "s3storage", "connectra", "appointment360"],
    "3.6": ["salesnavigator", "connectra", "emailapis"],
    "3.7": ["connectra", "logsapi", "jobs"],
    "3.8": ["connectra", "appointment360", "salesnavigator", "s3storage"],
    "3.9": ["logsapi", "appointment360", "connectra"],
    "3.10": list(PACK_KEY_TO_FILE.keys()),
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


def pack_slices_for_patch(_minor: str, patch_digit: int, pack_path: Path) -> list[str]:
    text = pack_path.read_text(encoding="utf-8")
    p0, p1 = extract_table_p0_p1(text)
    ops = extract_ops_bullets(text)
    if not p0 and not p1:
        nt = non_table_pack_slices(text, patch_digit)
        if nt:
            return nt
        c = extract_section_bullets(text, "Contract tasks")
        s = extract_section_bullets(text, "Service tasks")
        surf = extract_section_bullets(text, "Surface tasks")
        d = extract_section_bullets(text, "Data tasks")
        o = extract_section_bullets(text, "Ops tasks")
        if patch_digit <= 2:
            return c + s + d[: max(1, len(d) // 2 + 1)]
        if patch_digit <= 6:
            return surf + d + s
        return o or ops
    if patch_digit <= 2:
        return p0
    if patch_digit <= 6:
        return p1
    return ops if ops else p1[-3:] if len(p1) > 3 else p1


def build_slices(patch_id: str) -> str:
    parts = patch_id.split(".")
    minor = f"{parts[0]}.{parts[1]}"
    p = int(parts[2])
    keys = MINOR_PRIMARY_PACKS.get(minor, [])
    lines = [
        "## Service task slices",
        "> Merged from era `3.x` contact/company task packs (P0→`.0`–`.2`, P1→`.3`–`.6`, Ops→`.7`–`.9`).",
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
        "3.0": "`/contacts`, `/companies` shell; Connectra smoke — see minor.",
        "3.1": "VQL builder / taxonomy bindings — `vql-filter-taxonomy.md`.",
        "3.2": "Gateway ↔ Connectra parity; resolver error surfaces.",
        "3.3": "Search UX, relevance, regression hooks.",
        "3.4": "Saved search, export, drill-down modals.",
        "3.5": "Import/export modals, jobs progress — jobs UI bindings.",
        "3.6": "SN ingestion surfaces / provenance display if any.",
        "3.7": "Drift/diff admin views if exposed.",
        "3.8": "Extension capture / merge UX touchpoints.",
        "3.9": "Audit/telemetry dashboards if user-visible.",
        "3.10": "Exit sweep; minimal new UX unless ops-only.",
    }.get(minor, "See minor Frontend UX scope.")
    rows = [
        (
            "**Contract**",
            "GraphQL, Connectra REST, or VQL contract changed? Diff vs `docs/backend/apis/` + endpoint matrices.",
            "Document at patch closeout.",
        ),
        (
            "**Service**",
            "List/count/batch-upsert, gateway clients, processors — smoke + idempotency story intact?",
            "Document smoke paths.",
        ),
        (
            "**Surface**",
            "Dashboard contacts/companies or admin paths changed? Filters, exports, error UX?",
            "Document UX delta or N/A.",
        ),
        (
            "**Frontend**",
            "Which routes/hooks/components for this patch?",
            fe + " Document at closeout.",
        ),
        (
            "**Data**",
            "PG+ES lineage, enrichment/dedup, job artifacts — migrations + docs?",
            "Document lineage or N/A.",
        ),
        (
            "**Ops**",
            "Queues, drift jobs, logs PII rules, runbooks — delta recorded?",
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
    old = "- **Era:** [3.3 — Contact360 contact and company data system](./README.md)"
    new = "- **Era:** `3.x` Contact/company data — hub [`versions.md`](../versions.md) · minors start at [`3.0 — Twin Ledger`](3.0%20%E2%80%94%20Twin%20Ledger.md)"
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
    m = re.match(r"# (3\.\d+\.\d+) — .+", text)
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
        print("3.x era folder not found")
        return
    packs = list(ERA.glob("*contact-company*task-pack*.md"))
    if not packs:
        print("No *contact-company* task-pack files found; exiting.")
        return
    for path in sorted(ERA.glob("3.*.* — *.md")):
        enrich_one(path)
    print(f"Processed 3.x patch files in {ERA}")


if __name__ == "__main__":
    main()
