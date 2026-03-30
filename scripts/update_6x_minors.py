"""Update docs/6.x minor files: patch closure, micro-gate before Patches, strip Master Task Checklist."""
from __future__ import annotations

import re
from pathlib import Path

from .micro_gate_utils import ensure_architecture_row

ERA = Path(__file__).resolve().parent.parent / "6. Contact360 Reliability and Scaling"

MICRO_GATE = """### Micro-gate reference (apply at every `6.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | SLO/SLI, idempotency, DLQ envelope, trace headers — `docs/backend/apis/` + endpoint matrices updated? |
| **Service** | Retry/DLQ, rate limits, provider degradation — smoke paths + idempotency stores documented? |
| **Surface** | Ops dashboards, `/status`, degraded UX — user/operator-visible delta? |
| **Frontend** | Era 6 patterns in `docs/frontend/components.md` / pages JSON — delta? |
| **Data** | Lineage docs, Redis/DB idempotency, retention — migrations recorded? |
| **Ops** | SLO panels, alerts, chaos/runbooks (`queue-observability.md`, RC) — recorded? |

**Patch ladder:** Codenames `Void` → `Bloom` per minor (`.0`–`.9`) — see patch table below.

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
            r"(- \*\*Owner:\*\* [^\n]+\n)(\n## Scope)",
            r"\1- **Patch closure:** Every codenamed patch file includes **Micro-gate** + **Service task slices**. "
            r"Era hub: [`versions.md`](../versions.md).\n\2",
            text,
            count=1,
        )

    if "### Micro-gate reference" not in text:
        text = text.replace("\n## Patches\n", "\n" + MICRO_GATE + "## Patches\n", 1)

    def repl_pack(m: re.Match[str]) -> str:
        pack = m.group(1)
        return (
            f"**Service task slices** in `{mid}.P` patch files "
            f"(scope from former `{pack}`)"
        )

    text = re.sub(
        r"\[`([^`]+reliability-scaling-task-pack\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    text = ensure_architecture_row(text)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("6.* — *.md")):
        if re.match(r"^6\.\d+\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
