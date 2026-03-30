"""Update docs/9.x minor files: patch closure, micro-gate before Patches, strip Master Task Checklist."""
from __future__ import annotations

import re
from pathlib import Path

from .micro_gate_utils import ensure_architecture_row

ERA = Path(__file__).resolve().parent.parent / "9. Contact360 Ecosystem integrations and Platform productization"

MICRO_GATE = """### Micro-gate reference (apply at every `9.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | Connector lifecycle, entitlement model — `docs/backend/apis/` + integration matrices updated? |
| **Service** | Multi-tenant enforcement, adapters, webhook delivery — smoke + parity documented? |
| **Surface** | Integrations UI, marketplace/admin, self-serve — delta? |
| **Frontend** | `docs/frontend/` hooks, partner flows, extension/email — delta? |
| **Data** | Tenant lineage, connector fields — `docs/backend/database/` updated? |
| **Ops** | SLA runbooks, partner onboarding, `connectors-commercial.md` / integration RC — recorded? |

**Patch ladder:** Codenames per minor — see patch table below (`Void`→`Bloom` unless minor defines a custom ladder).

"""


def minor_id_from_name(name: str) -> str:
    return name.split(" —", 1)[0].strip()


def strip_master_task_checklist(text: str) -> str:
    if "## Master Task Checklist" not in text:
        return text
    before, mid = text.split("## Master Task Checklist", 1)
    if "## Patches" not in mid:
        return text
    _, after = mid.split("## Patches", 1)
    return before.rstrip() + "\n\n## Patches" + after


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = strip_master_task_checklist(text)
    mid = minor_id_from_name(path.name)
    orig = text

    if "**Patch closure:**" not in text:
        text = re.sub(
            r"\n+## Patches\n",
            "\n- **Patch closure:** Every codenamed patch file includes **Micro-gate** + **Service task slices**. "
            "Era hub: [`versions.md`](../versions.md).\n\n## Patches\n",
            text,
            count=1,
        )

    if "### Micro-gate reference" not in text:
        text = re.sub(
            r"\n+## Patches\n",
            "\n" + MICRO_GATE + "## Patches\n",
            text,
            count=1,
        )

    def repl_pack(m: re.Match[str]) -> str:
        pack = m.group(1)
        return (
            f"**Service task slices** in `{mid}.P` patch files "
            f"(scope from former `{pack}`)"
        )

    text = re.sub(
        r"\[`([^`]+-ecosystem-productization-task-pack\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    text = ensure_architecture_row(text)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("9.* — *.md")):
        if re.match(r"^9\.\d+\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
