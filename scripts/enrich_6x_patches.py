#!/usr/bin/env python3
"""
Enrich docs/6. Contact360 Reliability and Scaling/6.N.P — *.md with Micro-gate + Service task slices
from era `6.x` *-reliability-scaling-task-pack.md` files (P0→.0–.2, P1→.3–.6, Ops→.7–.9).
Handles `## Track A — Contract` … `E — Ops` tables and `## Contract track` bullet packs.
No-ops when task packs are absent.
"""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "6. Contact360 Reliability and Scaling"

PACK_KEY_TO_FILE = {
    "appointment360": "appointment360-reliability-scaling-task-pack.md",
    "connectra": "connectra-reliability-scaling-task-pack.md",
    "contact-ai": "contact-ai-reliability-scaling-task-pack.md",
    "emailapis": "emailapis-reliability-scaling-task-pack.md",
    "emailcampaign": "emailcampaign-reliability-scaling-task-pack.md",
    "jobs": "jobs-reliability-scaling-task-pack.md",
    "logsapi": "logsapi-reliability-scaling-task-pack.md",
    "mailvetter": "mailvetter-reliability-scaling-task-pack.md",
    "s3storage": "s3storage-reliability-scaling-task-pack.md",
    "salesnavigator": "salesnavigator-reliability-scaling-task-pack.md",
}

MINOR_PRIMARY_PACKS: dict[str, list[str]] = {
    "6.0": ["contact-ai", "appointment360", "logsapi", "jobs"],
    "6.1": [
        "appointment360",
        "connectra",
        "jobs",
        "logsapi",
        "mailvetter",
        "emailapis",
        "s3storage",
    ],
    "6.2": ["jobs", "connectra", "contact-ai", "appointment360", "emailapis"],
    "6.3": ["jobs", "emailcampaign", "mailvetter", "contact-ai"],
    "6.4": ["logsapi", "contact-ai", "appointment360", "jobs"],
    "6.5": ["connectra", "emailapis", "salesnavigator", "contact-ai"],
    "6.6": ["s3storage", "emailcampaign", "contact-ai", "jobs"],
    "6.7": ["s3storage", "logsapi", "jobs", "mailvetter"],
    "6.8": ["connectra", "appointment360", "mailvetter", "emailapis"],
    "6.9": list(PACK_KEY_TO_FILE.keys()),
    "6.10": list(PACK_KEY_TO_FILE.keys()),
}

TRACK_OWNER_FIRST = frozenset(
    {"contract", "service", "surface", "data", "ops", "track", "owner (default)"}
)

_ERA_LINE_BAD = re.compile(
    r"- \*\*Era:\*\* \[6\.\d+ — Contact360 Reliability and Scaling\]\(\./README\.md\)"
)
_ERA_LINE_GOOD = (
    "- **Era:** `6.x` Reliability and Scaling — hub [`versions.md`](../versions.md) · minors start at "
    "[`6.0 — Reliability and Scaling era umbrella`](6.0%20%E2%80%94%20Reliability%20and%20Scaling%20era%20umbrella.md)"
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


def extract_track_bullets_prefix(text: str, prefix: str) -> list[str]:
    lines = text.splitlines()
    pfx = "## " + prefix
    out: list[str] = []
    i = 0
    while i < len(lines):
        st = lines[i].strip()
        if st.startswith(pfx):
            i += 1
            while i < len(lines):
                raw = lines[i]
                if raw.startswith("## ") and not raw.startswith("###"):
                    break
                s = raw.strip()
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


def extract_6x_track_abcde_tasks(text: str) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    lines = text.splitlines()
    a: list[str] = []
    b: list[str] = []
    c: list[str] = []
    d: list[str] = []
    e: list[str] = []
    current: list[str] | None = None
    for line in lines:
        st = line.strip()
        if st.startswith("## Track A"):
            current = a
        elif st.startswith("## Track B"):
            current = b
        elif st.startswith("## Track C"):
            current = c
        elif st.startswith("## Track D"):
            current = d
        elif st.startswith("## Track E"):
            current = e
        elif st.startswith("##") and not st.startswith("###"):
            current = None
        elif current is not None and st.startswith("|"):
            cells = [c.strip() for c in st.strip("|").split("|")]
            if len(cells) < 2:
                continue
            id0 = cells[0]
            if id0.upper() == "ID":
                continue
            if id0.startswith("---") or (len(id0) >= 3 and set(id0) <= {"-", ":", " "}):
                continue
            if not re.match(r"^[A-Ea-e]-", id0):
                continue
            task = re.sub(r"\*+", "", cells[1]).strip()
            if len(task) < 2:
                continue
            current.append(task)
    return a, b, c, d, e


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
    surf = (
        extract_track_bullets_prefix(text, "Surface track")
        or extract_track_bullets(text, "Surface")
        or extract_section_bullets(text, "Surface tasks")
    )
    d = (
        extract_track_bullets_prefix(text, "Database / data track")
        or extract_track_bullets(text, "Data")
        or extract_section_bullets(text, "Data tasks")
    )
    o = (
        extract_track_bullets_prefix(text, "Ops track")
        or extract_track_bullets(text, "Ops")
        or extract_section_bullets(text, "Ops tasks")
    )
    return c, s, surf, d, o


def contract_service_surface_data_ops_lists(text: str) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    c, s, surf, d, o = track_section_bundle(text)
    if c or s or surf or d or o:
        return c, s, surf, d, o
    a, b, cc, dd, ee = extract_6x_track_abcde_tasks(text)
    if a or b or cc or dd or ee:
        return a, b, cc, dd, ee
    return [], [], [], [], []


def pack_slices_for_patch(_minor: str, patch_digit: int, pack_path: Path) -> list[str]:
    text = pack_path.read_text(encoding="utf-8")
    p0, p1 = extract_table_p0_p1(text)
    ops = extract_ops_bullets(text)
    if not p0 and not p1:
        nt = non_table_pack_slices(text, patch_digit)
        if nt:
            return nt
        c, s, surf, d, o = contract_service_surface_data_ops_lists(text)
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
        "> Merged from era `6.x` reliability/scaling task packs (P0→`.0`–`.2`, P1→`.3`–`.6`, Ops→`.7`–`.9`).",
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
        "6.0": "Era umbrella / program charter; cross-service vocabulary.",
        "6.1": "RED metrics, `/health/slo`, error-budget policy wired in docs and dashboards.",
        "6.2": "Idempotent writes + reconciliation evidence across hot paths.",
        "6.3": "DLQ, replay authorization, worker graceful shutdown / stale recovery.",
        "6.4": "Correlated telemetry, trace IDs, logs.api query/stream SLO evidence.",
        "6.5": "Latency wave; Connectra / provider degradation runbooks.",
        "6.6": "S3 lifecycle, multipart durability, artifact integrity checks.",
        "6.7": "Cost reliability, budget guardrails, spend anomaly handling.",
        "6.8": "Abuse resilience, rate limits, security controls at scale.",
        "6.9": "RC hardening for 7.0 — `reliability-rc-hardening.md` gate.",
        "6.10": "Buffer minor — only when roadmap charters a hotfix rail.",
    }.get(minor, "See minor reliability scope in roadmap / minor doc.")
    rows = [
        (
            "**Contract**",
            "SLO/SLI, idempotency, DLQ envelope, trace propagation — `docs/backend/apis/` + matrices updated?",
            "Document at patch closeout.",
        ),
        (
            "**Service**",
            "Retry/DLQ, rate limits, abuse guards, HF/SMTP/provider paths — smoke + caps documented?",
            "Document smoke paths.",
        ),
        (
            "**Surface**",
            "Ops dashboards, `/status`, degraded-mode UX — delta for this patch?",
            "Document UX delta or N/A.",
        ),
        (
            "**Frontend**",
            "Dashboard/extension reliability patterns (`components.md` Era 6) touched?",
            fe + " Document at closeout.",
        ),
        (
            "**Data**",
            "Lineage, retention, Redis/DB-backed idempotency state — migrations recorded?",
            "Document lineage or N/A.",
        ),
        (
            "**Ops**",
            "SLO panels, alerts, chaos/runbook refs (`queue-observability.md`, RC) — delta?",
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
    return _ERA_LINE_BAD.sub(_ERA_LINE_GOOD, content)


SLICE_HDR = "## Service task slices"


def strip_service_slices(head: str) -> str:
    i = head.find(SLICE_HDR)
    if i == -1:
        return head
    return head[:i].rstrip()


def enrich_one(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = fix_era_line(text)
    m = re.match(r"# (6\.\d+\.\d+) — .+", text)
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
        print("6.x era folder not found")
        return
    packs = [p for p in ERA.glob("*.md") if "task-pack" in p.name.lower()]
    if not packs:
        print("No *task-pack*.md files found; exiting.")
        return
    for path in sorted(ERA.glob("6.*.* — *.md")):
        enrich_one(path)
    print(f"Processed 6.x patch files in {ERA}")


if __name__ == "__main__":
    main()
