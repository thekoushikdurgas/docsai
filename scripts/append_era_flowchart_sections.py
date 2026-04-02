"""Append standard ## Flowchart blocks to era markdown files that lack them."""

from __future__ import annotations

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1]

FLOWCHART_BLOCK = """

## Flowchart

Five-track delivery (contract / service / surface / data / ops) for this doc:

```mermaid
flowchart LR
  contract[Contract]
  service[Service]
  surface[Surface]
  data[Data]
  ops[Ops]
  gate[Release gate]

  contract --> gate
  service --> gate
  surface --> gate
  data --> gate
  ops --> gate
```

**Master hub:** [`docs/docs/flowchart.md`](../docs/flowchart.md) — cross-system diagrams and era strip (`0.x` → `10.x`).
"""


def era_markdown_paths() -> list[Path]:
    out: list[Path] = []
    for p in DOCS.iterdir():
        if not p.is_dir():
            continue
        if not re.match(r"^\d+\.", p.name):
            continue
        out.extend(p.rglob("*.md"))
    return sorted(out)


def main() -> None:
    pattern = re.compile(r"(?m)^## Flowchart\s*$")
    for path in era_markdown_paths():
        text = path.read_text(encoding="utf-8")
        if pattern.search(text):
            continue
        path.write_text(text.rstrip() + FLOWCHART_BLOCK, encoding="utf-8")
        print("updated:", path.relative_to(DOCS.parent))


if __name__ == "__main__":
    main()
