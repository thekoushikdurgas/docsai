#!/usr/bin/env python3
"""Update docs/1.x minor files: patch closure, micro-gate ref, drop master checklist + README task-pack links."""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "1. Contact360 user and billing and credit system"

MICRO_GATE = """### Micro-gate reference (apply at every `1.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | Did any GraphQL / REST contract change? Diff vs `docs/backend/apis/`; billing idempotency keys documented? |
| **Service** | Auth, credit deduction, and billing paths still smoke for affected services? |
| **Surface** | App, admin, root, or extension billing UX changed? Role + entitlement checks? |
| **Frontend** | Which routes/components apply for this minor (see **Frontend UX Surface Scope**)? |
| **Data** | Migrations or lineage for credits, subscriptions, usage/ledger, payment proofs? |
| **Ops** | Observability, rollback, secrets; fraud/abuse runbooks where relevant? |

**Patch intent bands:** `.0` charter · `.1`–`.2` P0-heavy **Service task slices** · `.3`–`.6` P1 / surface-data · `.7`–`.9` ops + minor freeze.

"""


def minor_id_from_name(name: str) -> str:
    return name.split(" —", 1)[0].strip()


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    mid = minor_id_from_name(path.name)
    orig = text

    text = re.sub(
        r"- Shared checklist: \[`1\.x-master-checklist\.md`\]\(1\.x-master-checklist\.md\)\s*\n",
        "- **Patch closure:** Every codenamed patch file includes **Micro-gate** + **Service task slices**. "
        "Era hub: [`versions.md`](../versions.md).\n",
        text,
    )

    if "### Micro-gate reference" not in text:
        text = re.sub(
            r"(## Patch ladder \(`1\.\d+\.\d+` – `1\.\d+\.\d+`\))\n\n(Theme:)",
            r"\1\n\n" + MICRO_GATE + r"\2",
            text,
            count=1,
        )

    text = re.sub(
        r"Theme: ([^\n]+) — \[`1\.x-master-checklist\.md`\]\(1\.x-master-checklist\.md\)\.",
        rf"Theme: \1 — codenames in per-patch `{mid}.P — *.md` files.",
        text,
    )
    text = text.replace(
        "[`1.x-master-checklist.md`](1.x-master-checklist.md).",
        f"per-patch `{mid}.P — *.md` files.",
    )

    def repl_pack(m: re.Match[str]) -> str:
        pack = m.group(1)
        return (
            f"**Service task slices** in `{mid}.P` patch files "
            f"(scope from former `{pack}`)"
        )

    text = re.sub(
        r"\[`([^`]+\-user\-billing[^`]+\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    text = text.replace(
        "All `*-user-billing-task-pack.md` files",
        f"**Service task slices** merged into each `{mid}.P — *.md` patch file",
    )

    text = re.sub(
        r"— see \[`appointment360-user-billing-task-pack\.md`\]\([^\)]+\)\.\s*",
        f"— see **Service task slices** on `{mid}.P` patch files. ",
        text,
    )
    text = re.sub(
        r"with \[`emailapis-user-billing-credit-task-pack\.md`\]\([^\)]+\)\.",
        f"with **Service task slices** on `{mid}.P` patch files.",
        text,
    )

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("1.* — *.md")):
        if not re.match(r"^1\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
