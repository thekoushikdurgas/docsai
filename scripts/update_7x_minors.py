"""Update docs/7.x minor files: patch closure, micro-gate before Patches, strip Master Task Checklist."""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "7. Contact360 deployment"

MICRO_GATE = """### Micro-gate reference (apply at every `7.N.P`)

| Track | Gate question (must answer Yes or document waiver) |
| --- | --- |
| **Contract** | RBAC/authz, audit envelope, tenant isolation — `docs/backend/apis/` + `rbac-authz.md` + matrices updated? |
| **Service** | Handler guards, key rotation, retention hooks — parity tests + deployment gates documented? |
| **Surface** | Admin/ops governance UI, role-gated flows — operator-visible delta? |
| **Frontend** | Era 7 patterns (`tenant-security-observability.md`, components) — delta? |
| **Data** | Audit tables, lineage, legal-hold — `docs/backend/database/` migrations recorded? |
| **Ops** | CI/CD, drift checks, `contact360.io/admin/deploy/` runbooks — recorded? |

**Patch ladder:** See codename table below (`.0`–`.9` per minor; minors `7.6`–`7.9` use charter-style codenames).

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
    text = text.replace(
        "- Shared checklist: [`7.x-master-checklist.md`](7.x-master-checklist.md)\n",
        "",
    )
    text = re.sub(
        r"- \[docs/7\. Contact360 deployment/7\.x-master-checklist\.md\]\(7\.x-master-checklist\.md\)\n?",
        "- [`versions.md`](../versions.md) — era hub; **Micro-gate reference** (below) + per-patch **Micro-gate**\n",
        text,
    )
    mid = minor_id_from_name(path.name)
    orig = text

    if "**Patch closure:**" not in text:
        text = re.sub(
            r"(- \*\*Owner:\*\* [^\n]+\n)(\n+## Scope)",
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
        r"\[`([^`]+deployment-task-pack\.md)`\]\(\./README\.md\)",
        repl_pack,
        text,
    )

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)


def main() -> None:
    for path in sorted(ERA.glob("7.* — *.md")):
        if re.match(r"^7\.\d+\.\d+ — .+\.md$", path.name):
            continue
        process(path)


if __name__ == "__main__":
    main()
