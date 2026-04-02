from __future__ import annotations

from pathlib import Path
from typing import Callable

from .era_config import iter_patch_files


def _run_legacy_enrich(era_idx: int, *, apply: bool) -> int:
    """Fallback helper that calls the existing per-era scripts via import.

    This keeps behaviour identical while we migrate call sites to this helper.
    """
    from .. import maintenance_registry  # local import to avoid cycles

    # Reuse existing dispatch logic (enrich action).
    return maintenance_registry.run_maintain_era(
        era_idx=era_idx,
        action="enrich",
        dry_run=not apply,
    )


def enrich_era(era_idx: int, docs_root: Path | None = None, *, apply: bool) -> int:
    """Enrich all patch files for a given era.

    For now this function delegates to the legacy per-era enrich_* scripts
    via `maintenance_registry.run_maintain_era` while still exposing a
    single entrypoint that callers can use.
    """
    # docs_root is accepted for future use; current legacy scripts resolve
    # paths relative to their own module locations.
    _ = docs_root

    # Validate that there is at least one candidate patch file, mainly to
    # give a clearer return value when the era folder is empty.
    patches = list(iter_patch_files(era_idx))
    if not patches:
        return 0

    rc = _run_legacy_enrich(era_idx, apply=apply)
    return rc

