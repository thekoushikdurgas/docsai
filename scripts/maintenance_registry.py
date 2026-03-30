"""Dispatch era maintenance scripts (enrich, fix readme links, update minors)."""
from __future__ import annotations

import importlib
import re
from typing import Callable

from rich.console import Console

from .paths import DOCS_ROOT
from .scanner import ERA_FOLDERS

console = Console()

ENRICH_MODULES: dict[int, str] = {
    0: "scripts.enrich_foundation_0x_patches",
    1: "scripts.enrich_1x_patches",
    2: "scripts.enrich_2x_patches",
    3: "scripts.enrich_3x_patches",
    4: "scripts.enrich_4x_patches",
    5: "scripts.enrich_5x_patches",
    6: "scripts.enrich_6x_patches",
    7: "scripts.enrich_7x_patches",
    8: "scripts.enrich_8x_patches",
    9: "scripts.enrich_9x_patches",
    10: "scripts.enrich_10x_patches",
}

# Per-era fix_readme_links (no 0,1,2 in repo)
FIX_README_MODULES: dict[int, str] = {
    3: "scripts.fix_3x_patch_readme_links",
    4: "scripts.fix_4x_patch_readme_links",
    5: "scripts.fix_5x_patch_readme_links",
    6: "scripts.fix_6x_patch_readme_links",
    7: "scripts.fix_7x_patch_readme_links",
    8: "scripts.fix_8x_patch_readme_links",
    9: "scripts.fix_9x_patch_readme_links",
    10: "scripts.fix_10x_patch_readme_links",
}

UPDATE_MINORS_MODULES: dict[int, str] = {
    1: "scripts.update_1x_minors",
    2: "scripts.update_2x_minors",
    3: "scripts.update_3x_minors",
    4: "scripts.update_4x_minors",
    5: "scripts.update_5x_minors",
    6: "scripts.update_6x_minors",
    7: "scripts.update_7x_minors",
    8: "scripts.update_8x_minors",
    9: "scripts.update_9x_minors",
    10: "scripts.update_10x_minors",
}


def _patch_glob_pattern(era_idx: int) -> str:
    return f"{era_idx}.*.* — *.md"


def _dry_run_enrich(era_idx: int) -> None:
    era_dir = DOCS_ROOT / ERA_FOLDERS[era_idx]
    pat = _patch_glob_pattern(era_idx)
    n = len(list(era_dir.glob(pat))) if era_dir.is_dir() else 0
    console.print(f"[yellow]Dry-run[/yellow]: would run enrich on era {era_idx} (~{n} files matching {pat!r} under {era_dir.name})")


def _dry_run_fix(era_idx: int) -> None:
    era_dir = DOCS_ROOT / ERA_FOLDERS[era_idx]
    pat = _patch_glob_pattern(era_idx)
    n = len(list(era_dir.glob(pat))) if era_dir.is_dir() else 0
    console.print(
        f"[yellow]Dry-run[/yellow]: would run fix-readme-links on era {era_idx} (~{n} patch files)"
    )


def _dry_run_update_minors(era_idx: int) -> None:
    era_dir = DOCS_ROOT / ERA_FOLDERS[era_idx]
    rgx = re.compile(rf"^{era_idx}\.\d+\s+[—-].+\.md$")
    n = sum(1 for p in era_dir.glob("*.md") if rgx.match(p.name)) if era_dir.is_dir() else 0
    console.print(f"[yellow]Dry-run[/yellow]: would run update-minors on era {era_idx} (~{n} minor files)")


def _import_and_main(mod_name: str) -> int:
    mod = importlib.import_module(mod_name)
    main_fn: Callable[[], None] | None = getattr(mod, "main", None)
    if main_fn is None:
        console.print(f"[red]Module {mod_name} has no main()[/red]")
        return 2
    main_fn()
    return 0


def run_maintain_era(
    era_idx: int,
    action: str,
    *,
    dry_run: bool,
) -> int:
    """
    action: enrich | fix-readme-links | update-minors
    """
    if era_idx < 0 or era_idx > 10:
        console.print("[red]Era must be 0-10[/red]")
        return 2

    if action == "enrich":
        mod = ENRICH_MODULES.get(era_idx)
        if not mod:
            console.print(f"[red]No enrich module for era {era_idx}[/red]")
            return 2
        if dry_run:
            _dry_run_enrich(era_idx)
            return 0
        return _import_and_main(mod)

    if action == "fix-readme-links":
        mod = FIX_README_MODULES.get(era_idx)
        if not mod:
            console.print(
                f"[yellow]No fix-readme-links script for era {era_idx} (skipped in repo).[/yellow]"
            )
            return 0
        if dry_run:
            _dry_run_fix(era_idx)
            return 0
        return _import_and_main(mod)

    if action == "update-minors":
        mod = UPDATE_MINORS_MODULES.get(era_idx)
        if not mod:
            console.print(f"[red]No update-minors module for era {era_idx}[/red]")
            return 2
        if dry_run:
            _dry_run_update_minors(era_idx)
            return 0
        return _import_and_main(mod)

    console.print(f"[red]Unknown action {action!r}[/red]")
    return 2
