"""Update docs/4.x minor files: patch closure, micro-gate ref, drop master checklist + README task-pack links."""
from __future__ import annotations

import re
from pathlib import Path

from .micro_gate_utils import ensure_architecture_row

ERA = Path(__file__).resolve().parent.parent / "4. Contact360 Extension and Sales Navigator maturity"

MICRO_GATE = """### Micro-gate reference (apply at every `4.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | Extension/SN REST, GraphQL modules, CSP — `docs/backend/apis/` + endpoint matrices updated? |
| **Service** | SN scrape/save, Connectra upsert, jobs DAG, session refresh — smoke + idempotency documented? |
| **Surface** | Extension popup, dashboard SN/campaign panels, operator flows changed? |
| **Frontend** | Extension MV3 + dashboard routes/hooks (see minor scope / `extension-auth.md`, `extension-telemetry.md`)? |
| **Data** | Provenance, audience tables, `messages.contacts[]` — migrations + lineage docs? |
| **Ops** | `logs.api` events, S3 evidence, runbooks, rate/retry — delta recorded? |

**Patch intent bands:** Codenames per minor — see **Patch ladder** table in this file (`.0` charter … `.9` seal/handoff).

"""


def minor_id_from_name(name: str) -> str:
    return name.split(" —", 1)[0].strip()


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    mid = minor_id_from_name(path.name)
    orig = text

    text = re.sub(
        r"- Shared checklist: \[`4\.x-master-checklist\.md`\]\(4\.x-master-checklist\.md\)\s*\n",
        "- **Patch closure:** Every codenamed patch file includes **Micro-gate** + **Service task slices**. "
        "Era hub: [`versions.md`](../versions.md).\n",
        text,
    )

    if "### Micro-gate reference" not in text:
        text = re.sub(
            r"(## Patch ladder \(`4\.\d+\.\d+` – `4\.\d+\.\d+`\))\n\n(Theme:)",
            r"\1\n\n" + MICRO_GATE + r"\2",
            text,
            count=1,
        )

    text = re.sub(
        r"Theme: ([^\n]+) — \[`4\.x-master-checklist\.md`\]\(4\.x-master-checklist\.md\)\.",
        rf"Theme: \1 — codenames in per-patch `{mid}.P — *.md` files.",
        text,
    )
    text = text.replace(
        "[`4.x-master-checklist.md`](4.x-master-checklist.md).",
        f"per-patch `{mid}.P — *.md` files.",
    )

    def repl_pack(m: re.Match[str]) -> str:
        pack = m.group(1)
        return (
            f"**Service task slices** in `{mid}.P` patch files "
            f"(scope from former `{pack}`)"
        )

    text = re.sub(
        r"\[`([^`]+\-(?:extension-sn|extension-salesnav)[^`]+\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    text = text.replace("](../versions.md).\n## Scope", "](../versions.md).\n\n## Scope")

    text = ensure_architecture_row(text)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("4.* — *.md")):
        if re.match(r"^4\.\d+\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
