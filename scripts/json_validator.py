"""
json_validator.py — replaces doc_structure.py
Validates JSON files against their kind-specific schema using jsonschema.
Falls back to structural checks if jsonschema is not installed.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.paths import JSON_ROOT, JSON_SCHEMAS_DIR

SCHEMAS_DIR = JSON_SCHEMAS_DIR

try:
    import jsonschema  # type: ignore
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

REQUIRED_ENVELOPE = [
    "schema_version",
    "kind",
    "source_path",
    "sha256_source",
    "generated_at",
    "title",
    "non_parsed_raw_markdown",
]

KIND_REQUIRED: dict[str, list[str]] = {
    "index": ["folder", "children"],
    "hub": ["sections"],
    "era_task": ["task_tracks"],
    "graphql_module": ["module_name", "operations"],
    "endpoint_matrix": ["tables"],
    # uses_endpoints may be legitimately empty in some specs
    "page_spec": [],
    "document": ["sections"],
}

_schema_cache: dict[str, Any] = {}
_schema_store_cache: dict[str, Any] | None = None
_SCHEMA_BASE: str | None = None


def _schema_store() -> tuple[str, dict[str, Any]] | None:
    """Load all *.schema.json into a URI → schema map (file URIs + each document's $id)."""
    global _schema_store_cache, _SCHEMA_BASE
    if not HAS_JSONSCHEMA:
        return None
    if _schema_store_cache is not None and _SCHEMA_BASE is not None:
        return _SCHEMA_BASE, _schema_store_cache
    base = SCHEMAS_DIR.resolve().as_uri() + "/"
    store: dict[str, Any] = {}
    for p in sorted(SCHEMAS_DIR.glob("*.schema.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        file_uri = p.resolve().as_uri()
        store[file_uri] = doc
        rid = doc.get("$id")
        if isinstance(rid, str):
            store[rid] = doc
            # jsonschema often resolves relative $ref (e.g. common_envelope.schema.json) against
            # the canonical $id base and produces .../common_envelope.schema.json — map that too.
            if not rid.endswith(".schema.json"):
                store[f"{rid}.schema.json"] = doc
    _SCHEMA_BASE = base
    _schema_store_cache = store
    return base, store


def _resolver_for_schema(schema: dict[str, Any]) -> Any | None:
    """Resolver anchored on the schema being validated (correct relative $ref resolution)."""
    packed = _schema_store()
    if packed is None:
        return None
    base, store = packed
    try:
        from jsonschema import RefResolver as _RefResolver  # type: ignore
        return _RefResolver(base_uri=base, referrer=schema, store=store)
    except Exception:
        return None


def load_schema(kind: str) -> Any | None:
    if kind in _schema_cache:
        return _schema_cache[kind]
    schema_path = SCHEMAS_DIR / f"{kind}.schema.json"
    if not schema_path.exists():
        return None
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        _schema_cache[kind] = schema
        return schema
    except Exception:
        return None


class ValidationResult:
    def __init__(self, path: Path):
        self.path = path
        self.errors: list[str] = []
        self.warnings: list[str] = []

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


def validate_file(path: Path, use_jsonschema: bool = False) -> ValidationResult:
    result = ValidationResult(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        result.add_error(f"JSON parse error: {e}")
        return result

    # Envelope checks
    for field in REQUIRED_ENVELOPE:
        if field not in data:
            result.add_error(f"missing envelope field: {field}")

    np = (data.get("non_parsed_raw_markdown") or "").strip()
    has_raw = "raw_markdown" in data
    raw_val = data.get("raw_markdown")
    if np:
        if not has_raw or not isinstance(raw_val, str) or not raw_val.strip():
            result.add_error(
                "non_parsed_raw_markdown is non-empty but raw_markdown is missing or empty"
            )
    elif has_raw:
        result.add_error(
            "raw_markdown must be omitted when non_parsed_raw_markdown is empty"
        )

    kind = data.get("kind", "")
    if kind not in {"index", "hub", "era_task", "graphql_module", "endpoint_matrix", "page_spec", "document"}:
        result.add_error(f"unknown kind: {kind!r}")
        return result

    # Kind-specific required fields
    for field in KIND_REQUIRED.get(kind, []):
        if field not in data:
            result.add_error(f"missing kind field: {field}")

    # jsonschema validation (opt-in; slower — validates full instance including raw_markdown)
    if use_jsonschema and HAS_JSONSCHEMA:
        schema = load_schema(kind)
        if schema:
            try:
                res = _resolver_for_schema(schema)
                if res is not None:
                    jsonschema.validate(instance=data, schema=schema, resolver=res)
                else:
                    jsonschema.validate(instance=data, schema=schema)
            except jsonschema.ValidationError as e:
                result.add_error(f"schema: {e.message} at {list(e.absolute_path)}")
            except Exception as e:
                result.add_warning(f"schema validation skipped: {e}")

    return result


def validate_all(era: int | None = None, use_jsonschema: bool = False) -> list[ValidationResult]:
    from scripts.json_scanner import iter_json_files, load_envelope

    results: list[ValidationResult] = []
    for p in iter_json_files():
        env = load_envelope(p)
        if env is None:
            continue
        if era is not None:
            ei = env.get("era_index")
            if ei is None:
                ei = env.get("era")
            if ei != era:
                continue
        results.append(validate_file(p, use_jsonschema=use_jsonschema))
    return results


def format_validation_report(results: list[ValidationResult], show_ok: bool = False) -> str:
    lines = []
    ok = sum(1 for r in results if r.ok)
    err = len(results) - ok
    lines.append(f"Validated {len(results)} files: {ok} ok, {err} with errors\n")
    for r in results:
        if r.ok and not show_ok:
            continue
        rel = r.path.relative_to(JSON_ROOT) if r.path.is_relative_to(JSON_ROOT) else r.path
        status = "✅" if r.ok else "❌"
        lines.append(f"  {status} {rel}")
        for e in r.errors:
            lines.append(f"     ERROR: {e}")
        for w in r.warnings:
            lines.append(f"     WARN:  {w}")
    return "\n".join(lines)
