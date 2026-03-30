"""Inject architecture alignment bullets into era minor docs (## Task tracks)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from rich.console import Console

from .codebase_registry import ERA_SERVICE_MAP
from .paths import DOCS_ROOT
from .scanner import ERA_FOLDERS

console = Console()

MARKER = "**[architecture]**"
TRACK_HEADINGS = ("### Contract", "### Service", "### Surface", "### Data", "### Ops")
TASK_HEADERS = ("## Tasks", "## Task tracks")


def _minor_files(era_idx: int) -> list[Path]:
    era_dir = DOCS_ROOT / ERA_FOLDERS[era_idx]
    if not era_dir.is_dir():
        return []
    rgx = re.compile(rf"^{era_idx}\.\d+\s+[—-].+\.md$")
    return sorted(p for p in era_dir.glob("*.md") if rgx.match(p.name) and p.name != "README.md")


def _services_line(era_idx: int) -> str:
    svcs = ERA_SERVICE_MAP.get(era_idx, [])
    return ", ".join(f"`{s}`" for s in svcs) if svcs else "(see era hub)"


def _bullets_for_era(era_idx: int) -> dict[str, list[str]]:
    """Map track heading (### Contract) -> list of bullet lines to append."""
    sv = _services_line(era_idx)
    out: dict[str, list[str]] = {h: [] for h in TRACK_HEADINGS}

    out["### Contract"].append(
        f"- 📌 Planned: {MARKER} — Product **GraphQL** remains on `contact360.io/api` (Python); "
        "satellite HTTP contracts live under `docs/backend/apis/` and must stay versioned with gateway clients."
    )

    out["### Service"].append(
        f"- 📌 Planned: {MARKER} — **Go/Gin satellites** in scope for this era ({sv}): "
        "verify health endpoints, timeouts, and gateway downstream URLs in compose/config; "
        "no new Python satellites unless documented exception (`docs/docs/backend-language-strategy.md`)."
    )

    if era_idx in (1, 2, 3, 4, 5):
        out["### Surface"].append(
            "- 📌 Planned: "
            f"{MARKER} — **Next.js** customer surfaces (`contact360.io/app`, `root`, `email`, `joblevel-next`): "
            "standardise `NEXT_PUBLIC_GRAPHQL_URL` and GraphQL client; avoid calling Go services directly except documented REST exceptions."
        )

    if era_idx == 4:
        out["### Surface"].append(
            f"- 📌 Planned: {MARKER} — **Chrome extension**: GraphQL bearer + narrow `host_permissions`; "
            "align with `docs/tech/tech-extension-why-practices.md` for MV3 constraints."
        )

    out["### Data"].append(
        "- 📌 Planned: "
        f"{MARKER} — **PostgreSQL-first** per `docs/docs/data-stores-postgres.md`; "
        "gateway idempotency and sessions use Postgres."
    )

    if era_idx in (2, 6, 10):
        out["### Data"].append(
            "- 📌 Planned: "
            f"{MARKER} — **Redis exit**: campaign (Asynq) and mailvetter queues migrate to Postgres-backed workers "
            "or approved broker; remove `redis` from compose when no service depends on it."
        )

    out["### Ops"].append(
        "- 📌 Planned: "
        f"{MARKER} — **Observability**: correlate `X-Request-ID` gateway → satellites; "
        "rollback path documented per release."
    )

    if era_idx in (0, 7, 9):
        out["### Ops"].append(
            "- 📌 Planned: "
            f"{MARKER} — **Django DocsAI** (`contact360.io/admin`) is internal ops only; "
            "not exposed as the customer GraphQL path."
        )

    return out


def _section_span(lines: list[str], heading: str) -> tuple[int, int] | None:
    """Return [start, end) line indices for content under `heading` until next ### or ##."""
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        s = lines[j]
        if s.startswith("### ") or (s.startswith("## ") and not s.startswith("###")):
            end = j
            break
    return (start, end)


def _tasks_block_start(lines: list[str]) -> int | None:
    for i, line in enumerate(lines):
        if line.strip() in TASK_HEADERS:
            return i
    return None


def _inject_into_file(path: Path, bullets: dict[str, list[str]], *, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    lines = text.splitlines(keepends=True)
    plain = [ln.rstrip("\n") for ln in lines]

    if _tasks_block_start(plain) is None:
        console.print(f"[yellow]Skip (no ## Tasks/Task tracks): {path.name}[/yellow]")
        return False

    # Build insertions at section ends; apply from bottom to top so indices stay valid
    inserts: list[tuple[int, list[str]]] = []
    for heading, blist in bullets.items():
        if not blist:
            continue
        span = _section_span(plain, heading)
        if span is None:
            continue
        start, end = span
        section_text = "".join(lines[start:end])
        to_add = [b + "\n" for b in blist if b.strip() not in section_text]
        if to_add:
            inserts.append((end, to_add))

    if not inserts:
        return False
    inserts.sort(key=lambda x: x[0], reverse=True)
    new_lines = list(lines)
    for insert_at, chunk in inserts:
        new_lines[insert_at:insert_at] = chunk

    if dry_run:
        console.print(f"[cyan]Would update[/cyan] {path.name}")
        return True
    path.write_text("".join(new_lines), encoding="utf-8")
    console.print(f"[green]Updated[/green] {path.name}")
    return True


def run_era(era_idx: int, *, dry_run: bool) -> int:
    if era_idx < 0 or era_idx > 10:
        console.print("[red]Era must be 0-10[/red]")
        return 2
    bullets = _bullets_for_era(era_idx)
    paths = _minor_files(era_idx)
    if not paths:
        console.print(f"[yellow]No minor files for era {era_idx}[/yellow]")
        return 0
    n = 0
    for p in paths:
        if _inject_into_file(p, bullets, dry_run=dry_run):
            n += 1
    if dry_run:
        console.print(f"[yellow]Dry-run[/yellow]: would touch up to {n} file(s) in era {era_idx} (skip if {MARKER} already present).")
    else:
        console.print(f"Injected architecture bullets in {n} file(s) for era {era_idx}.")
    return 0


def main() -> None:
    """CLI: python -m scripts.inject_arch_tasks <era> [--apply]"""
    dry_run = "--apply" not in sys.argv
    era_s = sys.argv[1] if len(sys.argv) > 1 else ""
    if not era_s.isdigit():
        console.print("Usage: inject_arch_tasks <0-10> [--apply]")
        raise SystemExit(2)
    raise SystemExit(run_era(int(era_s), dry_run=dry_run))


if __name__ == "__main__":
    main()
