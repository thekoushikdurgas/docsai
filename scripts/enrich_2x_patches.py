#!/usr/bin/env python3
"""
Enrich docs/2. Contact360 email system/2.N.P — *.md with Micro-gate + Service task slices
from *-email-system-task-pack.md (P0→.0–.2, P1→.3–.6, Ops→.7–.9).
No-ops when task packs are absent.
"""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "2. Contact360 email system"

PACK_KEY_TO_FILE = {
    "appointment360": "appointment360-email-system-task-pack.md",
    "connectra": "connectra-email-system-task-pack.md",
    "contact-ai": "contact-ai-email-system-task-pack.md",
    "emailapis": "emailapis-email-system-task-pack.md",
    "emailcampaign": "emailcampaign-email-system-task-pack.md",
    "jobs": "jobs-email-system-task-pack.md",
    "logsapi": "logsapi-email-system-task-pack.md",
    "mailvetter": "mailvetter-email-system-task-pack.md",
    "s3storage": "s3storage-email-system-task-pack.md",
    "salesnavigator": "salesnavigator-email-system-task-pack.md",
}

# From 2.x-master-checklist.md — Minor to primary task packs
MINOR_PRIMARY_PACKS: dict[str, list[str]] = {
    "2.0": ["appointment360", "emailapis", "mailvetter", "jobs"],
    "2.1": ["emailapis", "appointment360"],
    "2.2": ["mailvetter", "emailapis", "appointment360"],
    "2.3": ["appointment360", "logsapi"],
    "2.4": ["jobs", "s3storage", "emailapis", "mailvetter"],
    "2.5": ["appointment360"],
    "2.6": ["emailapis"],
    "2.7": ["mailvetter"],
    "2.8": ["logsapi", "jobs"],
    "2.9": ["appointment360", "logsapi"],
    "2.10": list(PACK_KEY_TO_FILE.keys()),
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


def pack_slices_for_patch(_minor: str, patch_digit: int, pack_path: Path) -> list[str]:
    text = pack_path.read_text(encoding="utf-8")
    p0, p1 = extract_table_p0_p1(text)
    ops = extract_ops_bullets(text)
    if not p0 and not p1:
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
        "> Merged from era `2.x` email system task packs (P0→`.0`–`.2`, P1→`.3`–`.6`, Ops→`.7`–`.9`).",
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
        "2.0": "Email Studio Finder/Verifier; `docs/frontend/emailapis-ui-bindings.md`.",
        "2.1": "Finder/pattern UI + emailapigo routing — see minor.",
        "2.2": "Verifier surfaces + status mapping — see minor.",
        "2.3": "Results table + activity — see minor.",
        "2.4": "Bulk upload, jobs progress, download — `files`/`jobs` UI bindings.",
        "2.5": "`contact360.io/email` inbox/detail — credential security gate.",
        "2.6": "Provider/status badges — no vocabulary drift.",
        "2.7": "Verifier progress + failed states vs jobs UI.",
        "2.8": "Telemetry timelines if enabled — `logsapi` bindings.",
        "2.9": "Credit + audit indicators; role-gated controls.",
        "2.10": "Ops/health only unless exposing status externally.",
    }.get(minor, "See minor **Frontend** / UI scope.")
    rows = [
        (
            "**Contract**",
            "GraphQL email/jobs/upload or Lambda/Mailvetter REST changed? Diff vs `docs/backend/apis/`; bulk job idempotency?",
            "Document at patch closeout.",
        ),
        (
            "**Service**",
            "Finder/verifier/bulk stream smoke; provider routing + error envelopes unchanged or versioned?",
            "Document smoke paths.",
        ),
        (
            "**Surface**",
            "Email Studio, bulk job UI, or `/email` mailbox changed? Loading/error/progress contracts?",
            "Document UX delta or N/A.",
        ),
        (
            "**Frontend**",
            "Which routes/hooks must change for this patch?",
            fe + " Document at closeout.",
        ),
        (
            "**Data**",
            "`email_finder_cache`, patterns, job rows, Mailvetter store, S3 artifacts — migrations + lineage?",
            "Document migrations/lineage or N/A.",
        ),
        (
            "**Ops**",
            "Multipart/queue alerts, rollback/runbook delta for email-impacting releases?",
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
    old = "- **Era:** [2.2 — Contact360 email system](./README.md)"
    new = "- **Era:** `2.x` Email system — hub [`versions.md`](../versions.md) · minors start at [`2.0 — Email Foundation`](2.0%20%E2%80%94%20Email%20Foundation.md)"
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
    m = re.match(r"# (2\.\d+\.\d+) — .+", text)
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
        print("2.x era folder not found")
        return
    if not any(ERA.glob("*-email-system-task-pack.md")):
        print("No *-email-system-task-pack.md files found; exiting.")
        return
    for path in sorted(ERA.glob("2.*.* — *.md")):
        enrich_one(path)
    print(f"Processed 2.x patch files in {ERA}")


if __name__ == "__main__":
    main()
