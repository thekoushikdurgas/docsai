from __future__ import annotations

from pathlib import Path

from .era_config import iter_minor_files


def _run_legacy_update_minors(era_idx: int, *, apply: bool) -> int:
    """Fallback helper that calls the existing per-era update_*_minors scripts."""
    from .. import maintenance_registry  # local import to avoid cycles

    return maintenance_registry.run_maintain_era(
        era_idx=era_idx,
        action="update-minors",
        dry_run=not apply,
    )


def update_era_minors(era_idx: int, docs_root: Path | None = None, *, apply: bool) -> int:
    """Update all minor files for a given era.

    Currently implemented as a thin wrapper around the legacy per-era
    `update_*_minors.py` scripts, exposed as a single entrypoint.
    """
    _ = docs_root

    minors = list(iter_minor_files(era_idx))
    if not minors:
        return 0

    rc = _run_legacy_update_minors(era_idx, apply=apply)
    return rc

