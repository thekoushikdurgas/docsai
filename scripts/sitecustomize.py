"""
Startup hook automatically imported by Python (if present on sys.path).

Why this exists:
- When running scripts from `docs/scripts/` (e.g. `python scripts/api_cli.py ...`),
  Python sets `sys.path[0]` to `docs/scripts`.
- This repo contains a local package directory `docs/scripts/platform/`.
- Some third-party libs (e.g. `attrs`, used by `rich`) import the stdlib module `platform`.
- With `docs/scripts` first on `sys.path`, `import platform` can incorrectly resolve to the
  local `docs/scripts/platform/` package, which breaks those libs.

Fix:
- Force-load the real stdlib `platform` module and register it in `sys.modules`
  before third-party imports run.
"""

from __future__ import annotations

import importlib.util
import sys
import sysconfig
from pathlib import Path


def _force_stdlib_platform() -> None:
    stdlib_dir = sysconfig.get_paths().get("stdlib")
    if not stdlib_dir:
        return
    platform_py = Path(stdlib_dir) / "platform.py"
    if not platform_py.is_file():
        return

    spec = importlib.util.spec_from_file_location("platform", str(platform_py))
    if spec is None or spec.loader is None:
        return

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    sys.modules["platform"] = module


try:
    _force_stdlib_platform()
except Exception:
    # Never fail interpreter startup because of this workaround.
    pass

