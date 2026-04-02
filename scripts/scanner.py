"""Backward-compatible shim for ``scripts.scanner``.

Core implementation now lives in ``scripts.core.scanner``.
Import from ``scripts.core.scanner`` in new code.
"""
from __future__ import annotations

from .core.scanner import (  # noqa: F401
    ERA_FOLDERS,
    extract_service_task_slices,
    extract_track_sections,
    parse_file,
    scan_all,
    scan_era_only,
)

