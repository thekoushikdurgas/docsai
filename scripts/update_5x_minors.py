"""Update docs/5.x minor files: patch closure, micro-gate before Patches, README task-pack links."""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "5. Contact360 AI workflows"

MICRO_GATE = """### Micro-gate reference (apply at every `5.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | Contact AI REST, GraphQL AI module, model mapping — `docs/backend/apis/` + endpoint matrices updated? |
| **Service** | `contact.ai`, `LambdaAIClient`, jobs AI envelope — smoke + message caps / idempotency? |
| **Surface** | Dashboard `/ai-chat`, utilities, admin AI — user-visible delta? |
| **Frontend** | Routes/hooks per `contact-ai-ui-bindings.md` / pages JSON? |
| **Data** | `ai_chats`, prompts, S3 AI artifacts — migrations + lineage docs? |
| **Ops** | AI cost/telemetry in `logs.api`, alerts, runbooks — recorded? |

**Patch ladder:** Codenames `Void` → `Bloom` per minor (`.0`–`.9`) — see patch table below.

"""


def minor_id_from_name(name: str) -> str:
    return name.split(" —", 1)[0].strip()


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
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
        r"\[`([^`]+(?:-ai-task-pack|-ai-workflows-task-pack)\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("5.* — *.md")):
        if re.match(r"^5\.\d+\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
