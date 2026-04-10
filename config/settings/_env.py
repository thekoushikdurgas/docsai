"""Load SECRET_KEY from OS env, then .env.prod (EC2 / full-deploy), then .env via decouple."""

from __future__ import annotations

import os
from pathlib import Path


def resolve_secret_key(project_root: Path | None = None) -> str:
    """Prefer SECRET_KEY from the environment, then `.env.prod`, then decouple's default `.env`."""
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
