from __future__ import annotations

from pathlib import Path

from .era_config import iter_patch_files


def _run_legacy_fix_readme(era_idx: int, *, apply: bool) -> int:
    """Fallback helper that calls the existing per-era fix_*_patch_readme_links scripts."""
    from .. import maintenance_registry  # local import to avoid cycles

    return maintenance_registry.run_maintain_era(
        era_idx=era_idx,
        action="fix-readme-links",
        dry_run=not apply,
    )


def fix_era_readme_links(era_idx: int, docs_root: Path | None = None, *, apply: bool) -> int:
    """Fix patch README links for a given era.

    Initially delegates to legacy per-era fix_* scripts, but provides a
    single function that higher-level tooling can call.
    """
    _ = docs_root

    patches = list(iter_patch_files(era_idx))
    if not patches:
        return 0

    rc = _run_legacy_fix_readme(era_idx, apply=apply)
    return rc

