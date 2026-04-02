"""Backward-compatible shim for ``scripts.codebase_registry``.

The implementation now lives in ``scripts.metadata.codebase_registry``.
Import ``scripts.metadata.codebase_registry`` directly in new code.
"""
from __future__ import annotations

from .metadata.codebase_registry import (  # noqa: F401
    CODEBASES_DIR,
    APIS_DIR,
    FRONTEND_PAGES_DIR,
    ERA_SERVICE_MAP,
    load_registry,
)

