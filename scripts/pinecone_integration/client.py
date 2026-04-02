"""Pinecone client helpers for the `docs/` toolchain."""

from __future__ import annotations

import os
import sys
import importlib
from functools import lru_cache
from pathlib import Path
from typing import Optional, Type, Any

from dotenv import load_dotenv


@lru_cache(maxsize=1)
def _load_pinecone_sdk_pinecone_class() -> Type[Any]:
    """
    Load the actual Pinecone SDK `Pinecone` class.

    Note: this repository also has a local package directory named `pinecone/`
    (for our integration code), which would shadow `from pinecone import Pinecone`.
    To avoid that collision, we temporarily remove this integration path from
    `sys.path` and remove our local `pinecone` entry from `sys.modules` while
    importing the SDK.
    """

    integration_root = Path(__file__).resolve().parent.parent  # docs/scripts
    local_pkg = sys.modules.get("pinecone")

    # Snapshot sys.path so we can restore after import.
    original_sys_path = list(sys.path)
    try:
        # Remove our local package from the import cache.
        if "pinecone" in sys.modules:
            del sys.modules["pinecone"]

        # Remove the integration root from sys.path so the SDK is found.
        integration_root_resolved = integration_root.resolve()
        sys.path = [
            p
            for p in sys.path
            if _safe_resolve_path(p) != integration_root_resolved
        ]

        pinecone_sdk = importlib.import_module("pinecone")
        pinecone_cls = getattr(pinecone_sdk, "Pinecone", None)
        if pinecone_cls is None:
            raise ImportError("Pinecone SDK loaded but `Pinecone` class not found.")
        return pinecone_cls
    finally:
        sys.path = original_sys_path
        # Restore our local package object (so `pinecone.client` continues to work).
        if local_pkg is not None:
            sys.modules["pinecone"] = local_pkg


def _safe_resolve_path(p: str) -> Optional[Path]:
    try:
        return Path(p).resolve()
    except Exception:
        return None


def _load_env() -> None:
    """
    Load Pinecone env vars from the most likely locations.

    The existing docs CLI loads `docs/scripts/.env`; the Pinecone plan uses `docs/.env`.
    We support both so the module works regardless of which file the user created.
    """

    candidates = [
        # docs/scripts/.env (matches existing cli/config.py behavior)
        Path(__file__).resolve().parent.parent / ".env",
        # docs/.env (matches the plan + ignores in docs/.gitignore)
        Path(__file__).resolve().parents[2] / ".env",
    ]
    for p in candidates:
        if p.exists():
            load_dotenv(p)


_load_env()


def _require_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise RuntimeError(f"{key} not set (expected in .env)")
    return val


@lru_cache(maxsize=1)
def get_client():
    """Create a cached Pinecone client using `PINECONE_API_KEY`."""

    api_key = _require_env("PINECONE_API_KEY")
    PineconeCls = _load_pinecone_sdk_pinecone_class()
    return PineconeCls(api_key=api_key)


def _get_index_name(env_key: str, *, default: Optional[str] = None) -> str:
    val = os.getenv(env_key)
    if val:
        return val
    if default is not None:
        return default
    raise RuntimeError(f"{env_key} not set (expected in .env)")


def get_docs_index():
    """Return Pinecone Index handle for the docs RAG namespace strategy."""

    index_name = _get_index_name("PINECONE_INDEX_DOCS")
    return get_client().Index(index_name)


def get_api_index():
    """Return Pinecone Index handle for API test-result memory namespace strategy."""

    index_name = _get_index_name("PINECONE_INDEX_API")
    return get_client().Index(index_name)

