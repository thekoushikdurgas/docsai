"""Backward-compatible shim for ``scripts.maintenance_registry``.

The implementation now lives in ``scripts.maintenance.maintenance_registry``.
Import ``scripts.maintenance.maintenance_registry`` directly in new code.
"""
from __future__ import annotations

from .maintenance.maintenance_registry import (  # noqa: F401
    ENRICH_MODULES,
    FIX_README_MODULES,
    UPDATE_MINORS_MODULES,
    run_maintain_era,
    run_inject_arch_tasks,
    run_rename_tech_docs,
)

