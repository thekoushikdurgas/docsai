"""Idempotent Pinecone index creation for the `docs/` toolchain.

This script creates (if missing):
- `PINECONE_INDEX_DOCS` (docs RAG namespace strategy)
- `PINECONE_INDEX_API` (API test memory namespace strategy)

Indexes are configured for integrated embeddings:
- model: `llama-text-embed-v2`
- metric: `cosine`
- field_map: `text=content`
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from typing import List

from .client import get_client


def _require_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise RuntimeError(f"{key} not set (expected in .env)")
    return val


def _pc_cli_available() -> bool:
    return shutil.which("pc") is not None or shutil.which("pc.exe") is not None


def _run_pc(args: List[str]) -> subprocess.CompletedProcess[str]:
    if not _pc_cli_available():
        raise RuntimeError(
            "Pinecone CLI (`pc`) not found in PATH. Install it and authenticate first."
        )
    return subprocess.run(args, check=False, capture_output=True, text=True)


def _ensure_index_exists(pc: object, index_name: str) -> None:
    if pc.has_index(index_name):
        print(f"OK: index already exists: {index_name}")
        return

    # Create via Pinecone CLI (integrated embeddings setup is configured here).
    print(f"Creating Pinecone index: {index_name}")
    cmd = [
        "pc",
        "index",
        "create",
        "-n",
        index_name,
        "-m",
        "cosine",
        "-c",
        "aws",
        "-r",
        "us-east-1",
        "--model",
        "llama-text-embed-v2",
        "--field_map",
        "text=content",
    ]
    proc = _run_pc(cmd)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Failed to create index {index_name}.\n"
            f"Exit code: {proc.returncode}\n"
            f"STDOUT:\n{proc.stdout}\n"
            f"STDERR:\n{proc.stderr}\n"
        )

    # Idempotency / eventual consistency: wait for index to be ready.
    print(f"Waiting for index to become ready: {index_name}")
    time.sleep(10)
    if not pc.has_index(index_name):
        # This should be rare; has_index is a coarse check.
        raise RuntimeError(f"Index {index_name} still not visible after creation.")


def main() -> int:
    index_docs = _require_env("PINECONE_INDEX_DOCS")
    index_api = _require_env("PINECONE_INDEX_API")

    pc = get_client()

    try:
        _ensure_index_exists(pc, index_docs)
        _ensure_index_exists(pc, index_api)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

