#!/usr/bin/env python3
"""Update docs/2.x minor files: patch closure, micro-gate ref, drop master checklist + README task-pack links."""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "2. Contact360 email system"

MICRO_GATE = """### Micro-gate reference (apply at every `2.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | GraphQL email/jobs/upload or Lambda/Mailvetter REST changed? Diff vs `docs/backend/apis/`; bulk job idempotency documented? |
| **Service** | Finder/verifier/bulk paths still smoke; provider routing + error envelopes OK or versioned? |
| **Surface** | Email Studio, bulk job UI, or `/email` mailbox changed? Loading/error/progress contracts? |
| **Frontend** | Which routes/hooks apply (see **Frontend UX Surface Scope** / checklist in minor)? |
| **Data** | `email_finder_cache`, patterns, jobs, Mailvetter, S3 artifacts — migrations + lineage? |
| **Ops** | Multipart/queue durability, alerts, rollback/runbook delta for email releases? |

**Patch intent bands:** `.0` charter · `.1`–`.3` core path · `.4`–`.6` hardening · `.7`–`.8` integration · `.9` minor freeze / handoff.

"""


def minor_id_from_name(name: str) -> str:
    return name.split(" —", 1)[0].strip()


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    mid = minor_id_from_name(path.name)
    orig = text

    text = re.sub(
        r"- Shared checklist: \[`2\.x-master-checklist\.md`\]\(2\.x-master-checklist\.md\)\s*\n",
        "- **Patch closure:** Every codenamed patch file includes **Micro-gate** + **Service task slices**. "
        "Era hub: [`versions.md`](../versions.md).\n",
        text,
    )

    if "### Micro-gate reference" not in text:
        text = re.sub(
            r"(## Patch ladder \(`2\.\d+\.\d+` – `2\.\d+\.\d+`\))\n\n(Theme:)",
            r"\1\n\n" + MICRO_GATE + r"\2",
            text,
            count=1,
        )

    text = re.sub(
        r"Theme: ([^\n]+) — \[`2\.x-master-checklist\.md`\]\(2\.x-master-checklist\.md\)\.",
        rf"Theme: \1 — codenames in per-patch `{mid}.P — *.md` files.",
        text,
    )
    text = re.sub(
        r"Theme: ([^\n]+) — names in \[`2\.x-master-checklist\.md`\]\(2\.x-master-checklist\.md\)\.",
        rf"Theme: \1 — codenames in per-patch `{mid}.P — *.md` files.",
        text,
    )
    text = text.replace(
        "[`2.x-master-checklist.md`](2.x-master-checklist.md).",
        f"per-patch `{mid}.P — *.md` files.",
    )

    def repl_pack(m: re.Match[str]) -> str:
        pack = m.group(1)
        return (
            f"**Service task slices** in `{mid}.P` patch files "
            f"(scope from former `{pack}`)"
        )

    text = re.sub(
        r"\[`([^`]+\-email\-system[^`]+\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    text = re.sub(
        r"\[`2\.x-master-checklist\.md`\]\(2\.x-master-checklist\.md\)",
        "[`versions.md`](../versions.md) · per-patch Micro-gate in this folder",
        text,
    )

    text = re.sub(
        r"- 📌 Planned: All `2\.x-master-checklist\.md` cross-cutting items for final cut",
        "- 📌 Planned: Cross-cutting evidence in [`versions.md`](../versions.md) + per-patch **Micro-gate** closeouts",
        text,
    )

    text = text.replace("](../versions.md).\n## Scope", "](../versions.md).\n\n## Scope")

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("2.* — *.md")):
        if not re.match(r"^2\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
