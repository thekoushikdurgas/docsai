"""Replace task-pack (./README.md) and same-file pack links in 4.x patch files."""
from __future__ import annotations

import re
from pathlib import Path

ERA = Path(__file__).resolve().parent.parent / "4. Contact360 Extension and Sales Navigator maturity"
README_PACK = re.compile(
    r"\[`([^`]+\-(?:extension-sn|extension-salesnav)[^`]+\.md)`\]\(\./README\.md\)"
)
INLINE_PACK = re.compile(
    r"\[`([^`]+\-(?:extension-sn|extension-salesnav)[^`]+\.md)`\]\(\1\)"
)


def main() -> None:
    for p in sorted(ERA.glob("4.*.* — *.md")):
        t = p.read_text(encoding="utf-8")

        def repl_readme(m: re.Match[str]) -> str:
            return f"**Service task slices** below (includes former `{m.group(1)}` scope)"

        nt, n = README_PACK.subn(repl_readme, t)
        nt, n2 = INLINE_PACK.subn(
            lambda m: f"**Service task slices** below (ex-`{m.group(1)}`)",
            nt,
        )
        if n or n2:
            p.write_text(nt, encoding="utf-8")
            print(p.name, n, n2)


if __name__ == "__main__":
    main()
