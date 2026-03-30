#!/usr/bin/env python3
"""
Enrich docs/1. Contact360 user and billing.../1.N.P — *.md with Micro-gate + Service task slices
from *-user-billing-task-pack.md files (P0→patches .0–.2, P1→.3–.6, Ops→.7–.9).
Run while task packs exist; after merge they are removed and this script no-ops.
"""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "1. Contact360 user and billing and credit system"

PACK_KEY_TO_FILE = {
    "appointment360": "appointment360-user-billing-task-pack.md",
    "connectra": "connectra-user-billing-task-pack.md",
    "contact-ai": "contact-ai-user-billing-task-pack.md",
    "emailapis": "emailapis-user-billing-credit-task-pack.md",
    "emailcampaign": "emailcampaign-user-billing-task-pack.md",
    "jobs": "jobs-user-billing-task-pack.md",
    "logsapi": "logsapi-user-billing-credit-task-pack.md",
    "mailvetter": "mailvetter-user-billing-task-pack.md",
    "s3storage": "s3storage-user-billing-task-pack.md",
    "salesnavigator": "salesnavigator-user-billing-task-pack.md",
}

# From 1.x-master-checklist.md — Minor to primary task packs
MINOR_PRIMARY_PACKS: dict[str, list[str]] = {
    "1.0": ["appointment360", "emailapis", "jobs", "connectra"],
    "1.1": ["appointment360", "jobs", "s3storage", "emailapis", "mailvetter"],
    "1.2": ["appointment360", "logsapi", "emailapis"],
    "1.3": ["appointment360", "s3storage", "logsapi"],
    "1.4": ["appointment360", "logsapi"],
    "1.5": ["appointment360", "logsapi"],
    "1.6": ["appointment360", "logsapi"],
    "1.7": ["appointment360"],
    "1.8": ["appointment360", "jobs"],
    "1.9": ["appointment360", "contact-ai"],
    "1.10": list(PACK_KEY_TO_FILE.keys()),
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
    """Parse task rows; support | Task | P0 | and | Task | P0 | Notes |; skip Track|Owner|P0."""
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
        # | Track | Owner | P0 | — last cell is P0 but middle is not priority
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
    """Lines starting with - or - [ ] after ## header until next ##."""
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
                    out.append(s[2:].strip())
                j += 1
            break
    return out


def pack_slices_for_patch(minor: str, patch_digit: int, pack_path: Path) -> list[str]:
    text = pack_path.read_text(encoding="utf-8")
    p0, p1 = extract_table_p0_p1(text)
    ops = extract_ops_bullets(text)
    # Non-table packs: section-based fallback
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
    lines = ["## Service task slices", "> Merged from era `1.x` user/billing task packs (P0→`.0`–`.2`, P1→`.3`–`.6`, Ops→`.7`–`.9`).", ""]
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
        for b in bullets[:40]:  # cap per pack per patch
            lines.append(f"- {b}")
        lines.append("")
    if not any_content:
        return ""
    return "\n".join(lines).rstrip() + "\n"


def micro_gate_block(minor: str, _patch_digit: int) -> str:
    fe = {
        "1.0": "`/login`, `/register`, credits badge, finder/verifier bindings — see minor doc.",
        "1.1": "Bulk upload + billing surfaces; credit warnings.",
        "1.2": "Usage dashboard, `CreditBudgetAlerts`, analytics hooks.",
        "1.3": "Payment proof upload, billing toasts, admin review links.",
        "1.4": "Usage page, `useUsage` / ledger UI.",
        "1.5": "Notification / low-credit cues in `MainLayout`.",
        "1.6": "Admin payment tables, approve/decline actions.",
        "1.7": "429 backoff UX, throttled client handling.",
        "1.8": "Pack expiry / renewal / grace UI.",
        "1.9": "2FA enrollment, security settings surfaces.",
        "1.10": "Production readiness; no new product UX unless ops-only status.",
    }.get(minor, "See minor `1.N` Frontend UX Surface Scope.")
    rows = [
        (
            "**Contract**",
            "GraphQL / REST changes? Diff vs `docs/backend/apis/` or task pack; billing idempotency keys if mutations touched.",
            "Document at patch closeout.",
        ),
        (
            "**Service**",
            "Auth, credit deduction, billing state machine, and downstream Lambdas still pass smoke?",
            "Document smoke paths.",
        ),
        (
            "**Surface**",
            "App / admin / root / extension billing UX changed? Role + entitlement checks?",
            "Document UX delta or N/A.",
        ),
        (
            "**Frontend**",
            "Which routes/components must render or change for this patch?",
            fe + " Document at closeout.",
        ),
        (
            "**Data**",
            "`credits`, `subscriptions`, `plans`, `payment_submissions`, usage/ledger — migrations + lineage?",
            "Document migrations/lineage or N/A.",
        ),
        (
            "**Ops**",
            "Billing observability, rollback, secret rotation; fraud/abuse delta for `1.10` patches.",
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
    old = "- **Era:** [1.1 — Contact360 user and billing and credit system](./README.md)"
    new = "- **Era:** `1.x` User/billing/credit — hub [`versions.md`](../versions.md) · minors start at [`1.0 — User Genesis`](1.0%20%E2%80%94%20User%20Genesis.md)"
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
    m = re.match(r"# (1\.\d+\.\d+) — .+", text)
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
        print("1.x era folder not found")
        return
    if not any(ERA.glob("*-user-billing*.md")):
        print("No *-user-billing*.md packs found; exiting.")
        return
    for path in sorted(ERA.glob("1.*.* — *.md")):
        enrich_one(path)
    print(f"Processed 1.x patch files in {ERA}")


if __name__ == "__main__":
    main()
