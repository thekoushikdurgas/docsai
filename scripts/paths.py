"""Single source of truth for docs tree and repo roots (Contact360 docs CLI)."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

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

# ── JSON-native documentation (typed envelopes: schema_version + kind) ─────
# All converted / authored doc JSON lives directly under docs/, not docs/json/.
DOC_JSON_ROOT = DOCS_ROOT
# Historical name used across scripts (same as DOC_JSON_ROOT).
JSON_ROOT = DOC_JSON_ROOT

# JSON Schema files for doc envelope validation (draft 2020-12 $defs)
JSON_SCHEMAS_DIR = DOCS_ROOT / "json_schemas"

# Aggregate manifest built by scripts/build_manifest.py
MANIFEST_PATH = DOCS_ROOT / "manifest.json"

# Path segments: skip these anywhere in the relative path when scanning *.json
_DOC_JSON_SKIP_PARTS = frozenset(
    {"json_schemas", "result", "errors", "_archive", ".git", "__pycache__"}
)


def iter_doc_json_paths() -> Iterator[Path]:
    """
    Yield every *.json under docs/ that could be a typed doc envelope.
    Excludes schemas, CI output folders, manifest, and obvious non-doc trees.
    Postman / other JSON without schema_version is filtered later at load time.
    """
    for p in sorted(DOC_JSON_ROOT.rglob("*.json")):
        rel = p.relative_to(DOC_JSON_ROOT)
        if _DOC_JSON_SKIP_PARTS.intersection(rel.parts):
            continue
        if p.name == "manifest.json" and len(rel.parts) == 1:
            continue
        yield p
