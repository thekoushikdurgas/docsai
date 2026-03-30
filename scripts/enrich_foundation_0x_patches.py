#!/usr/bin/env python3
"""
Enrich docs/0. Foundation.../0.N.P — *.md with Micro-gate + Service task slices
from *-foundation-task-pack.md (parsed by patch-assignment ranges).

**2026-03:** Foundation task packs were merged into per-patch files and the packs
were removed from the repo. This script only runs if those `*-foundation-task-pack.md`
files are restored alongside it.
"""
from __future__ import annotations

import re
from pathlib import Path

FOUNDATION = Path(__file__).resolve().parent.parent / "0. Foundation and pre-product stabilization and codebase setup"

RANGE_RE = re.compile(
    r"\(patch assignment:\s*`(0\.\d+\.\d+)`\s*[–-]\s*`(0\.\d+\.\d+)`\)",
    re.IGNORECASE,
)
# Table cell: | ... | P0 | ... | `0.1.0`–`0.1.2` |
CELL_RANGE_RE = re.compile(r"\|\s*`(0\.\d+\.\d+)`\s*[–-]\s*`(0\.\d+\.\d+)`\s*\|")

FRONTEND_BAND = {
    0: "N/A (doc-only).",
    1: "See minor `0.1` Frontend UX Surface Scope — shell/context stubs.",
    2: "N/A (data-layer only).",
    3: "`lib/toast.ts`, `lib/apiErrorHandler.ts`, error `Alert` pattern.",
    4: "`RoleContext`, logout, session redirect, 403 page, rate-limit toast.",
    5: "`FilesUploadModal` stub, `useCsvUpload`, upload progress smoke.",
    6: "`JobsCard`, `JobsPipelineStats`, `useJobs`, status badges.",
    7: "`ContactsFilters` / `VQLQueryBuilder` stubs, loading skeleton.",
    8: "Full `MainLayout` / `Sidebar` / `ThemeContext`, admin constants sync.",
    9: "Extension popup stub, `graphqlSession.js`, `lambdaClient.js`.",
    10: "Production build green; `NEXT_PUBLIC_*` documented.",
}


def patch_tuple(v: str) -> tuple[int, int, int]:
    a, b, c = v.split(".")
    return int(a), int(b), int(c)


def in_range(p: str, lo: str, hi: str) -> bool:
    pt, lt, ht = patch_tuple(p), patch_tuple(lo), patch_tuple(hi)
    return lt <= pt <= ht


def extract_bullets_from_packs() -> list[tuple[str, str, str, str]]:
    """Returns list of (lo, hi, service_label, bullet_text) trimmed."""
    rows: list[tuple[str, str, str, str]] = []
    pack_files = sorted(FOUNDATION.glob("*-foundation-task-pack.md"))
    for pf in pack_files:
        service = pf.name.replace("-foundation-task-pack.md", "").replace("_", " ")
        if service == "appointment360":
            label = "Appointment360 (gateway)"
        elif service == "contact-ai":
            label = "contact.ai"
        elif service == "emailapis":
            label = "emailapis / emailapigo"
        elif service == "emailcampaign":
            label = "Email campaign"
        elif service == "logsapi":
            label = "logs.api"
        elif service == "mailvetter":
            label = "Mailvetter"
        elif service == "s3storage":
            label = "s3storage"
        elif service == "salesnavigator":
            label = "Sales Navigator"
        elif service == "jobs":
            label = "Jobs (tkdjob)"
        elif service == "connectra":
            label = "Connectra"
        else:
            label = service
        text = pf.read_text(encoding="utf-8")
        for line in text.splitlines():
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith("#"):
                continue
            if "patch assignment" not in line and "`0." not in line:
                continue
            m = RANGE_RE.search(line)
            if not m:
                m = CELL_RANGE_RE.search(line)
            if not m:
                continue
            lo, hi = m.group(1), m.group(2)
            # bullet text: strip table pipes, leading - [ ]
            bt = line_stripped
            if bt.startswith("|"):
                parts = [c.strip() for c in bt.split("|")]
                parts = [p for p in parts if p]
                # task description usually first or second column
                bt = parts[0] if parts else bt
                if bt in ("P0", "P1", "—", "-") and len(parts) > 1:
                    bt = parts[1]
            bt = re.sub(r"\(patch assignment:.*?\)\s*$", "", bt).strip()
            bt = re.sub(r"^- \[[ x]\]\s*", "", bt)
            bt = re.sub(r"^📌\s*Planned:\s*", "", bt)
            if len(bt) < 3:
                continue
            rows.append((lo, hi, label, bt))
    return rows


def slices_for_patch(patch_id: str, all_rows: list[tuple[str, str, str, str]]) -> str:
    by_svc: dict[str, list[str]] = {}
    for lo, hi, label, bt in all_rows:
        if in_range(patch_id, lo, hi):
            by_svc.setdefault(label, []).append(bt)
    if not by_svc:
        return ""
    lines = ["## Service task slices", "> Merged from era `0.x` foundation task packs (per patch band).", ""]
    for svc in sorted(by_svc.keys()):
        lines.append(f"### {svc}")
        for b in by_svc[svc]:
            lines.append(f"- {b}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def micro_gate_block(patch_id: str) -> str:
    n = int(patch_id.split(".")[1])
    p = int(patch_id.split(".")[2])
    if n == 0:
        na = "N/A — doc-only era (waiver: evidence from `0.1+`)."
        rows = [
            ("**Contract**", na),
            ("**Service**", na),
            ("**Surface**", na),
            ("**Frontend**", na),
            ("**Data**", na),
            ("**Ops**", na),
        ]
    else:
        fe = FRONTEND_BAND.get(n, "See minor `0.N` docs.")
        rows = [
            (
                "**Contract**",
                "Document Yes/No at closeout — API diff vs `docs/backend/apis/` or “no contract change”.",
            ),
            (
                "**Service**",
                "Document smoke: affected services boot + health pass.",
            ),
            (
                "**Surface**",
                "Document UX/admin/extension delta or N/A.",
            ),
            ("**Frontend**", fe + " Document scaffold delta or N/A at closeout."),
            (
                "**Data**",
                "Migrations / lineage / S3 prefixes updated or N/A.",
            ),
            (
                "**Ops**",
                "Rollback / secrets / CI / runbook delta or N/A.",
            ),
        ]
    md = ["## Micro-gate", ""]
    md.append("| Track | Gate question | Answer / Evidence (fill at patch closeout) |")
    md.append("| --- | --- | --- |")
    questions = [
        (
            "**Contract**",
            "Did any public or internal API surface change? If yes: diff vs `docs/backend/apis/` or pack; if no: “no contract change”.",
        ),
        (
            "**Service**",
            "Do critical paths for this patch still boot, health-check, and pass the defined smoke for affected services?",
        ),
        (
            "**Surface**",
            "Did UI, extension, or admin behavior change? If yes: UX evidence + role checks; if no: N/A.",
        ),
        (
            "**Frontend**",
            "Which foundation-era components/routes must render or be scaffolded? List by name or N/A.",
        ),
        (
            "**Data**",
            "Migrations, index mappings, S3 prefixes, or lineage docs updated and linked?",
        ),
        (
            "**Ops**",
            "Rollback path, secrets, CI step, or runbook delta recorded?",
        ),
    ]
    for (trk, q), (_, ans) in zip(questions, rows):
        md.append(f"| {trk} | {q} | {ans} |")
    md.append("")
    return "\n".join(md)


def fix_era_line(content: str) -> str:
    old = "- **Era:** [0.0 — Foundation and pre-product stabilization and codebase setup](./README.md)"
    new = "- **Era:** `0.x` Foundation — docs hub [`versions.md`](../versions.md) · minors start at [`0.0 — Pre-repo baseline`](0.0%20%E2%80%94%20Pre-repo%20baseline.md)"
    return content.replace(old, new)


def enrich_one(path: Path, rows: list[tuple[str, str, str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    text = fix_era_line(text)
    m = re.match(r"# (0\.\d+\.\d+) — .+", text)
    if not m:
        return
    patch_id = m.group(1)
    if "## Micro-gate" in text:
        path.write_text(text, encoding="utf-8")
        return
    if "## Tasks" not in text or "## Evidence gate" not in text:
        path.write_text(text, encoding="utf-8")
        return
    mg = micro_gate_block(patch_id)
    slices = slices_for_patch(patch_id, rows)
    pre, rest = text.split("## Tasks", 1)
    mid, ev = rest.split("## Evidence gate", 1)
    out = (
        pre.rstrip()
        + "\n\n"
        + mg
        + "\n## Tasks"
        + mid.rstrip()
        + "\n\n"
        + (slices + "\n" if slices else "")
        + "## Evidence gate"
        + ev
    )
    path.write_text(out, encoding="utf-8")


def main() -> None:
    pack_files = list(FOUNDATION.glob("*-foundation-task-pack.md"))
    if not pack_files:
        print("No *-foundation-task-pack.md files found; merge already applied or packs missing. Exiting.")
        return
    rows = extract_bullets_from_packs()
    for path in sorted(FOUNDATION.glob("0.*.* — *.md")):
        enrich_one(path, rows)
    print(f"Enriched {len(list(FOUNDATION.glob('0.*.* — *.md')))} patch files.")


if __name__ == "__main__":
    main()
