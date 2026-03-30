"""Update docs/8.x minor files: patch closure, micro-gate before Patches, strip Master Task Checklist."""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "8. Contact360 public and private apis and endpoints"

MICRO_GATE = """### Micro-gate reference (apply at every `8.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | Versioning, public vs private API surface, module/OpenAPI docs — `docs/backend/apis/` + endpoint matrices updated? |
| **Service** | `X-API-Key`, rate-limit headers, webhook/callback contracts — smoke + parity documented? |
| **Surface** | Developer docs, external portal, profile/API-key UX — delta? |
| **Frontend** | `public-api-surface.md`, hooks/bindings, extension/email — delta? |
| **Data** | External API lineage, audit fields — `docs/backend/database/` updated? |
| **Ops** | Postman, compatibility tests, replay runbooks — recorded? |

**Patch ladder:** Codenames per minor — see patch table below (`Void`→`Bloom` unless minor defines a custom ladder).

"""


def minor_id_from_name(name: str) -> str:
    return name.split(" —", 1)[0].strip()


def strip_master_task_checklist(text: str) -> str:
    if "## Master Task Checklist" not in text or "## Patches" not in text:
        return text
    before, mid = text.split("## Master Task Checklist", 1)
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
        r"\[`([^`]+(?:-api-endpoint-task-pack|-public-private-apis-task-pack)\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("8.* — *.md")):
        if re.match(r"^8\.\d+\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
