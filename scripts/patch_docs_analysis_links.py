"""Rewrite markdown links from docs/analysis and docs/plans to imported paths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Files under docs/ (any depth) except docs/analysis: replace relative ../analysis/ and ../plans/
PATTERNS = [
    (re.compile(r"\(\.\./analysis/"), r"(../../contact360.io/root/docs/imported/analysis/"),
    (re.compile(r"\(\.\./plans/"), r"(../../contact360.io/root/docs/imported/plans/"),
    (re.compile(r"`docs/analysis/"), r"`contact360.io/root/docs/imported/analysis/"),
    (re.compile(r"`docs/plans/"), r"`contact360.io/root/docs/imported/plans/"),
]


def should_process(p: Path) -> bool:
    parts = p.relative_to(ROOT).parts
    if len(parts) < 2 or parts[0] != "docs":
        return False
    if parts[1] == "analysis":
        return False
    if p.suffix.lower() != ".md":
        return False
    return True


def main() -> None:
    for path in ROOT.joinpath("docs").rglob("*.md"):
        if not should_process(path):
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        for rx, repl in PATTERNS:
            new = rx.sub(repl, new)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
