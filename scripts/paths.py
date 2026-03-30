"""Single source of truth for docs tree and repo roots (Contact360 docs CLI)."""
from __future__ import annotations

from pathlib import Path

# docs/scripts/ — this file
SCRIPTS_ROOT = Path(__file__).resolve().parent
# docs/
DOCS_ROOT = SCRIPTS_ROOT.parent
# monorepo root (parent of docs/)
REPO_ROOT = DOCS_ROOT.parent

# Canonical policy hubs live under docs/docs/
DOCS_HUB_DIR = DOCS_ROOT / "docs"

# Postman exports (Contact360 API env + collections)
POSTMAN_DIR = DOCS_ROOT / "backend" / "postman"
DEFAULT_CONTACT360_POSTMAN_ENV = POSTMAN_DIR / "Contact360_Local.postman_environment.json"

# Reference SQL schema and seeds (docs only; app backend may mirror)
DATABASE_DIR = DOCS_ROOT / "backend" / "database"
DATABASE_CSV_DIR = DATABASE_DIR / "csv"

# Validation JSON output (see ``python cli.py validate-all``)
DOCS_RESULT_DIR = DOCS_ROOT / "result"
DOCS_ERRORS_DIR = DOCS_ROOT / "errors"
