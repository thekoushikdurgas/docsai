"""Shared Micro-gate table helpers for era minor docs."""
from __future__ import annotations

import re

ARCHITECTURE_ROW = (
    "| **Architecture** | "
    "Go/Gin satellites only via Python GraphQL gateway (`contact360.io/api`); "
    "Next.js `NEXT_PUBLIC_GRAPHQL_URL`; Postgres-first / Redis exit per "
    "`docs/docs/data-stores-postgres.md`. |"
)


def ensure_architecture_row(text: str) -> str:
    """
    Insert Architecture track row after **Ops** in Micro-gate table if missing.
    Idempotent.
    """
    if "| **Architecture** |" in text:
        return text
    if "### Micro-gate reference" not in text:
        return text
    # First **Ops** row in file that is part of a gate table (pipe table)
    new, n = re.subn(
        r"(\| \*\*Ops\*\* \|[^\n]+\|)\n\n",
        r"\1\n" + ARCHITECTURE_ROW + "\n\n",
        text,
        count=1,
    )
    if n:
        return new
    return text
