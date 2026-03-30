"""Inject ## Stack references into era README.md pointing at docs/tech/ canonical files."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from rich.console import Console

from .paths import DOCS_ROOT
from .scanner import ERA_FOLDERS

console = Console()

SECTION_HEADING = "## Stack references"
REL_TECH = "../tech"  # from era README to docs/tech/

# Relative paths from era folder README (one level down from docs/)
LINKS = {
    "go_why": f"[Go/Gin — why & practices]({REL_TECH}/tech-go-gin-why-practices.md)",
    "go_100": f"[Go/Gin — 100-point checklist]({REL_TECH}/tech-go-gin-checklist-100.md)",
    "next_why": f"[Next.js — why & practices]({REL_TECH}/tech-nextjs-why-practices.md)",
    "next_100": f"[Next.js — 100-point checklist]({REL_TECH}/tech-nextjs-checklist-100.md)",
    "ext_why": f"[Browser extension — why & practices]({REL_TECH}/tech-extension-why-practices.md)",
    "ext_100": f"[Browser extension — 100-point checklist]({REL_TECH}/tech-extension-checklist-100.md)",
    "dj_why": f"[Django — why & practices]({REL_TECH}/tech-django-why-practices.md)",
    "dj_100": f"[Django — 100-point checklist]({REL_TECH}/tech-django-checklist-100.md)",
}

# Hub doc for Redis/Postgres (not under tech/)
DATA_HUB = "[PostgreSQL vs Redis (canonical)](../docs/data-stores-postgres.md)"


def _lines_for_era(era_idx: int) -> list[str]:
    """Bullet lines as markdown list items."""
    base = [
        LINKS["go_why"],
        LINKS["go_100"],
        LINKS["next_why"],
        LINKS["next_100"],
    ]
    if era_idx == 0:
        return [base[0], base[2]]  # why only for foundation
    if era_idx == 4:
        return base + [LINKS["ext_why"], LINKS["ext_100"]]
    if era_idx == 7:
        return base + [LINKS["dj_why"], LINKS["dj_100"]]
    if era_idx == 10:
        return base + [DATA_HUB]
    if era_idx in (1, 2, 3, 5, 6, 8, 9):
        return base
    return base


def _build_section(era_idx: int) -> str:
    lines = _lines_for_era(era_idx)
    body = "\n".join(f"- {ln}" for ln in lines)
    return (
        f"{SECTION_HEADING}\n\n"
        "Framework and stack reference material (rename-safe paths under `docs/tech/`):\n\n"
        f"{body}\n\n"
    )


def run_era(era_idx: int, *, dry_run: bool) -> int:
    if era_idx < 0 or era_idx > 10:
        console.print("[red]Era must be 0-10[/red]")
        return 2
    readme = DOCS_ROOT / ERA_FOLDERS[era_idx] / "README.md"
    if not readme.is_file():
        console.print(f"[red]Missing {readme}[/red]")
        return 2
    text = readme.read_text(encoding="utf-8")
    if SECTION_HEADING in text:
        console.print(f"[yellow]Skip (already has {SECTION_HEADING}): {readme.name}[/yellow]")
        return 0
    block = _build_section(era_idx)
    # Insert before final cross-links or at end
    m = re.search(r"^## (Tasks|Cross-links)", text, re.MULTILINE)
    if m:
        insert_at = m.start()
        new_text = text[:insert_at].rstrip() + "\n\n" + block + "\n" + text[insert_at:].lstrip()
    else:
        new_text = text.rstrip() + "\n\n" + block + "\n"
    if dry_run:
        console.print(f"[cyan]Would add {SECTION_HEADING} to[/cyan] {readme}")
        return 0
    readme.write_text(new_text, encoding="utf-8")
    console.print(f"[green]Added {SECTION_HEADING} to[/green] {readme}")
    return 0


def main() -> None:
    dry_run = "--apply" not in sys.argv
    era_s = sys.argv[1] if len(sys.argv) > 1 else ""
    if not era_s.isdigit():
        console.print("Usage: inject_tech_links <0-10> [--apply]")
        raise SystemExit(2)
    raise SystemExit(run_era(int(era_s), dry_run=dry_run))


if __name__ == "__main__":
    main()
