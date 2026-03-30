"""Replace task-pack (./README.md) links in 3.x patch files."""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "3. Contact360 contact and company data system"
PAT = re.compile(r"\[`([^`]+\-contact\-company[^`]+\.md)`\]\(\./README\.md\)")
LOGSAPI_INLINE = re.compile(
    r"\[`logsapi-contact-company-data-task-pack\.md`\]\(logsapi-contact-company-data-task-pack\.md\)"
)


def main() -> None:
    for p in sorted(ERA.glob("3.*.* — *.md")):
        t = p.read_text(encoding="utf-8")

        def repl(m: re.Match[str]) -> str:
            return f"**Service task slices** below (includes former `{m.group(1)}` scope)"

        nt, n = PAT.subn(repl, t)
        nt, n2 = LOGSAPI_INLINE.subn(
            "`contact360.import.*` event types per **Service task slices** below; ex-`logsapi-contact-company-data-task-pack.md`",
            nt,
        )
        if n or n2:
            p.write_text(nt, encoding="utf-8")
            print(p.name, n, n2)


if __name__ == "__main__":
    main()
