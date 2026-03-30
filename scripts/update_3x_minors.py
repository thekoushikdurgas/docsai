#!/usr/bin/env python3
"""Update docs/3.x minor files: patch closure, micro-gate ref, drop master checklist + README task-pack links."""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "3. Contact360 contact and company data system"

MICRO_GATE = """### Micro-gate reference (apply at every `3.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | GraphQL, Connectra REST, or VQL changed? `docs/backend/apis/` + endpoint matrices updated? |
| **Service** | List/count/batch-upsert and gateway paths still smoke; idempotency documented? |
| **Surface** | Dashboard contacts/companies or related admin UX changed? |
| **Frontend** | Which routes/hooks apply (see minor UX scope / `dashboard-search-ux.md`)? |
| **Data** | PG+ES lineage, enrichment/dedup, job artifacts — docs + migrations? |
| **Ops** | Queues, drift tooling, logs PII rules, runbooks — delta recorded? |

**Patch intent bands (universal ladder):** `.0` Charter · `.1` Connectra · `.2` Gateway · `.3` Dashboard · `.4` Jobs/S3 · `.5` Satellite · `.6` Observability · `.7` Hardening · `.8` Evidence · `.9` Gate / handoff.

"""


def minor_id_from_name(name: str) -> str:
    return name.split(" —", 1)[0].strip()


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    mid = minor_id_from_name(path.name)
    orig = text

    text = re.sub(
        r"- Shared checklist: \[`3\.x-master-checklist\.md`\]\(3\.x-master-checklist\.md\)\s*\n",
        "- **Patch closure:** Every codenamed patch file includes **Micro-gate** + **Service task slices**. "
        "Era hub: [`versions.md`](../versions.md).\n",
        text,
    )

    if "### Micro-gate reference" not in text:
        text = re.sub(
            r"(## Patch ladder \(`3\.\d+\.\d+` – `3\.\d+\.\d+`\))\n\n(Theme:)",
            r"\1\n\n" + MICRO_GATE + r"\2",
            text,
            count=1,
        )

    text = re.sub(
        r"Theme: ([^\n]+) — \[`3\.x-master-checklist\.md`\]\(3\.x-master-checklist\.md\)\.",
        rf"Theme: \1 — codenames in per-patch `{mid}.P — *.md` files.",
        text,
    )
    text = text.replace(
        "[`3.x-master-checklist.md`](3.x-master-checklist.md).",
        f"per-patch `{mid}.P — *.md` files.",
    )

    def repl_pack(m: re.Match[str]) -> str:
        pack = m.group(1)
        return (
            f"**Service task slices** in `{mid}.P` patch files "
            f"(scope from former `{pack}`)"
        )

    text = re.sub(
        r"\[`([^`]+\-contact\-company[^`]+\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    text = text.replace("](../versions.md).\n## Scope", "](../versions.md).\n\n## Scope")

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("3.* — *.md")):
        if not re.match(r"^3\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
