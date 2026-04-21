"""Environment file loading and SECRET_KEY resolution for production-like deploys."""

from __future__ import annotations

import os
from pathlib import Path


def _parse_env_file(path: Path) -> dict[str, str]:
    """Parse KEY=VAL lines (basic quoting like python-decouple). Ignores blanks and # comments."""
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    text = path.read_text(encoding="utf-8")
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, rest = line.partition("=")
        key = key.strip()
        if not key:
            continue
        val = rest.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        out[key] = val
    return out


def bootstrap_layered_env(project_root: Path | None = None) -> None:
    """
    Merge ``.env`` then ``.env.prod`` into ``os.environ`` for keys not already
    set in the process environment (exported vars / systemd / k8s always win).

    Values in ``.env.prod`` override the same key from ``.env`` when applying
    to the process (neither file beats an already-exported variable).

    Call **only** from ``production`` / ``staging`` settings, before
    ``from .base import *``, so ``os.getenv`` and ``decouple.config`` see the
    same values as on developers' machines with a single ``.env``.
    """
    root = project_root or Path(__file__).resolve().parent.parent.parent
    merged: dict[str, str] = {}
    for name in (".env", ".env.prod"):
        merged.update(_parse_env_file(root / name))
    for key, value in merged.items():
        if key not in os.environ:
            os.environ[key] = value


def resolve_secret_key(project_root: Path | None = None) -> str:
    """Prefer SECRET_KEY from the environment, then ``.env.prod``, then decouple's ``.env``."""
    root = project_root or Path(__file__).resolve().parent.parent.parent
    s = (os.environ.get("SECRET_KEY") or "").strip()
    if s:
        return s
    env_prod = root / ".env.prod"
    if env_prod.is_file():
        from decouple import Config, RepositoryEnv

        cfg = Config(RepositoryEnv(str(env_prod)))
        s = (cfg("SECRET_KEY", default="") or "").strip()
        if s:
            return s
    from decouple import config

    return (config("SECRET_KEY", default="") or "").strip()
