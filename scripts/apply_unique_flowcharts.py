"""Replace ## Flowchart sections in docs/versions/version_*.md with unique diagrams."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from unique_version_flowcharts import (
    FLOWCHART_BLOCK_PATTERN,
    build_flowchart_section,
)

ROOT = Path(__file__).resolve().parents[1]
VERSIONS_DIR = ROOT / "docs" / "versions"


def parse_version(name: str) -> tuple[int, int] | None:
    m = re.match(r"version_(\d+)\.(\d+)\.md$", name)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def main() -> None:
    updated = 0
    for path in sorted(VERSIONS_DIR.glob("version_*.md")):
        parsed = parse_version(path.name)
        if not parsed:
            continue
        major, minor = parsed
        text = path.read_text(encoding="utf-8")
        new_section = build_flowchart_section(major, minor)
        new_text, n = FLOWCHART_BLOCK_PATTERN.subn(new_section, text, count=1)
        if n != 1:
            raise RuntimeError(f"Expected one Flowchart block in {path}")
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            updated += 1
    print(f"Rewrote Flowchart section in {updated} files.")


if __name__ == "__main__":
    main()
