"""
Era 0.x foundation smoke: verify env contract files exist for all 12 codebases.

Run from repo root via: python docs/scripts/era0_foundation_check.py
Exit 0 if all expected .env.example paths are present; non-zero otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Paths relative to repository root (directory containing docs/).
EXPECTED_ENV_EXAMPLES = [
    "contact360.io/api/.env.example",
    "contact360.io/app/.env.example",
    "contact360.io/root/.env.example",
    "contact360.io/admin/.env.example",
    "contact360.io/email/.env.example",
    "contact360.extension/.env.example",
    "EC2/email.server/.env.example",
    "EC2/s3storage.server/.env.example",
    "EC2/log.server/.env.example",
    "EC2/ai.server/.env.example",
    "EC2/email campaign/.env.example",
    "EC2/extension.server/.env.example",
]


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    missing: list[str] = []
    for rel in EXPECTED_ENV_EXAMPLES:
        p = root / rel
        if not p.is_file():
            missing.append(rel)
    if missing:
        print("Missing .env.example (Era 0.1 env contract):\n  - " + "\n  - ".join(missing))
        return 1
    print(f"OK: all {len(EXPECTED_ENV_EXAMPLES)} codebases have .env.example under {root}")
    print("\nHealth hints (verify in deployment):")
    print("  - contact360.io/api: GET /health")
    print("  - contact360.io/app: GET /api/health")
    print("  - contact360.io/root: GET /api/health")
    print("  - contact360.io/email: GET /api/health")
    print("  - contact360.extension FastAPI: GET /health")
    print("  - EC2/* Gin services: GET /health or /api/v1/health (per service README)")
    print("  - contact360.io/admin: GET /docs/api/v1/health/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
