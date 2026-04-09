"""
cli.py v2 — Contact360 Docs CLI
Typed documentation JSON lives directly under docs/ (envelopes with schema_version + kind).
Reference SQL and Postman collections stay alongside those trees.

Global options (before subcommand):
  -J, --machine-json   Machine-readable JSON on supported commands
  -q, --quiet          Suppress non-essential human output
  -v, --verbose        More detail / indented JSON
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Optional rich console ────────────────────────────────────────────────────
try:
    from rich.console import Console
    console = Console()
    def _rich_print(msg: str, style: str = "") -> None:
        console.print(msg, style=style)
except ImportError:
    def _rich_print(msg: str, style: str = "") -> None:  # type: ignore[misc]
        print(msg)

# ── Global CLI context (set in main() from argparse) ─────────────────────────
CLI_CTX: dict[str, Any] = {
    "quiet": False,
    "verbose": False,
    "machine_json": False,
}


def _want_json(args: argparse.Namespace | None) -> bool:
    if args is None:
        return bool(CLI_CTX.get("machine_json"))
    if bool(getattr(args, "global_json", False)):
        return True
    return bool(getattr(args, "json", False))


def _print(msg: str, style: str = "", *, force: bool = False) -> None:
    if CLI_CTX.get("quiet") and not force:
        return
    _rich_print(msg, style)


def _emit_json(data: Any, args: argparse.Namespace | None = None) -> None:
    """Always print JSON to stdout (used for -J / --json on commands)."""
    indent = 2 if (CLI_CTX.get("verbose") or (args and getattr(args, "verbose", False))) else None
    print(json.dumps(data, indent=indent, ensure_ascii=False))

# ── Paths ────────────────────────────────────────────────────────────────────
DOCS_ROOT = Path(__file__).resolve().parent
SCRIPTS_ROOT = DOCS_ROOT / "scripts"
DOCS_RESULT_DIR = DOCS_ROOT / "result"
DOCS_ERRORS_DIR = DOCS_ROOT / "errors"

sys.path.insert(0, str(DOCS_ROOT))

from scripts.paths import JSON_ROOT, MANIFEST_PATH

# ── JSON module imports ──────────────────────────────────────────────────────
from scripts.json_scanner import scan_all, group_by_kind, group_by_era, era_summary  # type: ignore
from scripts.json_auditor import audit_era, format_audit_report  # type: ignore
from scripts.json_filler import fill_era, fill_file  # type: ignore
from scripts.json_validator import validate_all, format_validation_report  # type: ignore
from scripts.json_updater import update_status, update_field, find_json_by_version, update_index_children  # type: ignore
from scripts.json_stats import (  # type: ignore
    task_report, format_task_report, era_guide_table, overview_stats
)

# ── Non-docs optional imports (SQL, API test, Pinecone, platform) ────────────
try:
    from scripts.paths import (  # type: ignore
        DATABASE_CSV_DIR, DATABASE_DIR, DEFAULT_CONTACT360_POSTMAN_ENV,
        POSTMAN_DIR, API_TEST_DIR,
    )
except ImportError:
    DATABASE_CSV_DIR = DATABASE_DIR = DEFAULT_CONTACT360_POSTMAN_ENV = POSTMAN_DIR = None
    API_TEST_DIR = SCRIPTS_ROOT / "api_test"

try:
    from scripts.postman_env import load_and_merge_env, preview_env_mapping, redact_env_display, resolve_postman_env_path  # type: ignore
    HAS_POSTMAN = True
except ImportError:
    HAS_POSTMAN = False

try:
    from scripts.platform.run_all import run_all as platform_run_all  # type: ignore
    HAS_PLATFORM = True
except ImportError:
    HAS_PLATFORM = False


# ═══════════════════════════════════════════════════════════════════════════════
# Docs commands (JSON-backed)
# ═══════════════════════════════════════════════════════════════════════════════

KIND_CHOICES = [
    "index", "hub", "era_task", "graphql_module", "endpoint_matrix", "page_spec", "document",
]


def cmd_scan(args: argparse.Namespace) -> int:
    """Scan typed JSON under docs/ and print overview dashboard."""
    docs = scan_all()
    by_kind = group_by_kind(docs)
    by_era = group_by_era(docs) if getattr(args, "by_era", False) else None
    by_status: dict[str, int] = {}
    if getattr(args, "by_status", False):
        for d in docs:
            s = d.get("status") or "unknown"
            by_status[s] = by_status.get(s, 0) + 1

    if _want_json(args):
        payload: dict[str, Any] = {
            "total_docs": len(docs),
            "by_kind": {k: len(v) for k, v in sorted(by_kind.items())},
        }
        if by_era is not None:
            payload["by_era"] = {str(k): len(v) for k, v in sorted(by_era.items(), key=lambda x: str(x[0]))}
        if by_status:
            payload["by_status"] = dict(sorted(by_status.items()))
        manifest_path = MANIFEST_PATH
        if manifest_path.exists():
            try:
                payload["manifest"] = json.loads(manifest_path.read_text(encoding="utf-8"))
            except Exception:
                payload["manifest"] = None
        _emit_json(payload, args)
        return 0

    _print(overview_stats())
    _print("")
    _print(f"[bold]Total JSON docs:[/bold] {len(docs)}")
    for kind, items in sorted(by_kind.items()):
        _print(f"  {kind:<20}: {len(items):>4}")
    if by_era is not None:
        _print("\n[bold]By era:[/bold]")
        for era_key, items in sorted(by_era.items(), key=lambda x: str(x[0])):
            _print(f"  {str(era_key):<12}: {len(items):>4}")
    if by_status:
        _print("\n[bold]By status:[/bold]")
        for st, n in sorted(by_status.items()):
            _print(f"  {st:<20}: {n:>4}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    """Print era-specific or global stats."""
    era = getattr(args, "era", None)
    kind_filter = getattr(args, "kind", None)

    if _want_json(args):
        if era is not None:
            s = era_summary(era)
            if kind_filter:
                docs = scan_all(era=era)
                s["filtered_by_kind"] = kind_filter
                s["filtered_count"] = sum(1 for d in docs if d.get("kind") == kind_filter)
            _emit_json(s, args)
        else:
            docs = scan_all()
            if kind_filter:
                docs = [d for d in docs if d.get("kind") == kind_filter]
            by_kind = group_by_kind(docs)
            _emit_json({
                "overview": "filtered" if kind_filter else "all",
                "kind_filter": kind_filter,
                "total_docs": len(docs),
                "by_kind": {k: len(v) for k, v in sorted(by_kind.items())},
            }, args)
        return 0

    if era is not None:
        s = era_summary(era)
        _print(f"Era {era} — {s['index_title'] or 'unknown'}")
        _print(f"  Total docs  : {s['total_docs']}")
        for kind, count in s["by_kind"].items():
            if kind_filter and kind != kind_filter:
                continue
            _print(f"  {kind:<20}: {count}")
        _print(f"  Statuses    : {s['status_counts']}")
        if kind_filter:
            _print(f"  [dim](filter --kind {kind_filter})[/dim]")
    else:
        if kind_filter:
            docs = scan_all()
            docs = [d for d in docs if d.get("kind") == kind_filter]
            by_kind = group_by_kind(docs)
            _print(f"Filtered to kind={kind_filter!r}: {len(docs)} docs")
            for k, items in sorted(by_kind.items()):
                _print(f"  {k:<20}: {len(items):>4}")
            _print("")
        _print(overview_stats())
        _print("")
        _print(era_guide_table())
    return 0


def cmd_era_guide(args: argparse.Namespace) -> int:
    """Show era guide."""
    era = getattr(args, "era", None)
    as_json = bool(getattr(args, "json", False) or _want_json(args))

    if as_json:
        docs = scan_all(era=era)
        indexes = [d for d in docs if d.get("kind") == "index"]
        if era is not None:
            extra = era_summary(era)
            _emit_json({"era": era, "summary": extra, "indexes": indexes}, args)
        else:
            _emit_json({"indexes": indexes}, args)
        return 0
    if era is not None:
        s = era_summary(era)
        _print(format_era_block(s))
    else:
        _print(era_guide_table())
    return 0


def format_era_block(s: dict) -> str:
    lines = [f"Era {s['era']}  {s.get('index_title','')}", "=" * 50]
    for kind, count in s.get("by_kind", {}).items():
        lines.append(f"  {kind}: {count}")
    return "\n".join(lines)


def cmd_audit_tasks(args: argparse.Namespace) -> int:
    era = getattr(args, "era", None)
    results = audit_era(era=era)
    bad = [r for r in results if not r.ok]
    summary_only = getattr(args, "summary_only", False)

    if _want_json(args) or getattr(args, "json", False):
        _emit_json({
            "total": len(results),
            "ok": sum(1 for r in results if r.ok),
            "with_issues": len(bad),
            "era": era,
            "files": [
                {
                    "path": r.path.relative_to(JSON_ROOT).as_posix(),
                    "ok": r.ok,
                    "issues": r.issues,
                    "track_counts": r.track_counts(),
                }
                for r in results
            ],
        }, args)
        return 1 if bad else 0

    if not summary_only:
        _print(format_audit_report(results))
    else:
        _print(f"Audited {len(results)} era_task files: {len(results) - len(bad)} ok, {len(bad)} with issues")
    return 1 if bad else 0


def cmd_fill_tasks(args: argparse.Namespace) -> int:
    file_path = getattr(args, "file", None)
    dry_run = args.dry_run and not args.apply
    era = None if getattr(args, "all", False) else getattr(args, "era", None)

    if file_path:
        p = Path(file_path)
        if not p.is_absolute():
            p = JSON_ROOT / file_path
        added = fill_file(p, dry_run=dry_run)
        if _want_json(args):
            _emit_json({"file": str(p), "dry_run": dry_run, "added": added}, args)
            return 0
        if any(added.values()):
            keys = [k for k, v in added.items() if v]
            mode = "[DRY]" if dry_run else "✓"
            _print(f"{mode} {p.name} → added tracks: {', '.join(keys)}")
        else:
            _print(f"No missing tracks in {p.name}")
        return 0
    modified = fill_era(era=era, dry_run=dry_run)
    if _want_json(args):
        _emit_json({"scope": "all" if era is None else f"era_{era}", "dry_run": dry_run, "modified_files": modified}, args)
        return 0
    _print(f"\nModified {modified} files" + (" (dry-run)" if dry_run else ""))
    return 0


def cmd_dedup_tasks(args: argparse.Namespace) -> int:
    """Detect duplicate task text across sibling era_task files."""
    from collections import defaultdict
    era = getattr(args, "era", None)
    dry_run = args.dry_run and not args.apply
    limit = getattr(args, "limit", 50) or 50
    min_locations = max(2, getattr(args, "min_locations", 2) or 2)

    docs = scan_all(era=era)
    era_tasks = [d for d in docs if d.get("kind") == "era_task"]
    TRACK_KEYS = ["contract", "service", "surface", "data", "ops"]
    text_map: dict[str, list[str]] = defaultdict(list)
    for d in era_tasks:
        tracks = d.get("task_tracks", {})
        for track in TRACK_KEYS:
            for item in tracks.get(track, []):
                txt = item.get("text", "").strip().lower()[:80]
                if txt:
                    text_map[txt].append(f"{d.get('_json_path','?')} [{track}]")

    dupes = {k: v for k, v in text_map.items() if len(v) >= min_locations}
    if _want_json(args):
        items = [{"text": k, "locations": v} for k, v in list(dupes.items())[:limit]]
        _emit_json({
            "dry_run": dry_run,
            "era": era,
            "duplicate_text_count": len(dupes),
            "min_locations": min_locations,
            "sample": items,
        }, args)
        return 0

    if not dupes:
        _print("No duplicate tasks found.")
        return 0
    _print(f"Found {len(dupes)} duplicate task texts (min_locations={min_locations}):")
    for text, locations in list(dupes.items())[:limit]:
        _print(f"\n  '{text[:60]}...' in:")
        for loc in locations:
            _print(f"    {loc}")
    if len(dupes) > limit:
        _print(f"\n  ... and {len(dupes) - limit} more (use --limit)")
    return 0


def cmd_task_report(args: argparse.Namespace) -> int:
    era = getattr(args, "era", None)
    report = task_report(era=era)
    if _want_json(args) or getattr(args, "json", False):
        _emit_json(report, args)
        return 0
    _print(format_task_report(report))
    return 0


def cmd_name_audit(args: argparse.Namespace) -> int:
    """Audit era_task filenames for canonical format."""
    era = getattr(args, "era", None)
    import re
    VERSION_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?\s*[—\-–]\s*(.+)$")
    docs = scan_all(era=era)
    era_tasks = [d for d in docs if d.get("kind") == "era_task"]
    findings: list[dict[str, str]] = []
    for d in era_tasks:
        src = d.get("source_path", "")
        fname = Path(src).stem
        m = VERSION_RE.match(fname)
        if not m:
            findings.append({"source_path": src, "issue": "non_canonical", "detail": fname})
        elif " — " not in fname and "—" not in fname:
            findings.append({"source_path": src, "issue": "missing_em_dash", "detail": fname})

    if _want_json(args) or getattr(args, "json", False):
        _emit_json({"total_era_tasks": len(era_tasks), "issue_count": len(findings), "issues": findings}, args)
        return 0 if len(findings) == 0 else 1

    for f in findings:
        _print(f"  ⚠ {f['issue']}: {f['source_path']}")
    if not findings:
        _print(f"All {len(era_tasks)} era_task filenames look canonical.")
    else:
        _print(f"\n{len(findings)} naming issue(s) found.")
    return 0 if not findings else 1


def cmd_rename_docs(args: argparse.Namespace) -> int:
    """Preview or apply canonical renames of era_task JSON files."""
    era = None if getattr(args, "all", False) else getattr(args, "era", None)
    apply = bool(getattr(args, "apply", False))
    docs = scan_all(era=era)
    era_tasks = [d for d in docs if d.get("kind") == "era_task"]
    renames: list[tuple[Path, Path]] = []
    for d in era_tasks:
        src = Path(d.get("source_path", ""))
        version = d.get("version", "")
        codename = d.get("codename", "")
        if not version:
            continue
        canonical_stem = f"{version} \u2014 {codename}" if codename else version
        current_stem = src.stem
        if current_stem != canonical_stem:
            json_path = JSON_ROOT / src.parent / (src.stem + ".json")
            new_json_path = JSON_ROOT / src.parent / (canonical_stem + ".json")
            renames.append((json_path, new_json_path))

    if _want_json(args):
        _emit_json({
            "apply": apply,
            "count": len(renames),
            "pairs": [{"from": o.name, "to": n.name, "from_path": str(o), "to_path": str(n)} for o, n in renames],
        }, args)
        if not apply:
            return 0

    if not renames:
        _print("All era_task JSON files already have canonical names.")
        return 0
    for old, new in renames:
        _print(f"  {'RENAME' if apply else 'DRY  '} {old.name} → {new.name}")
        if apply and old.exists():
            old.rename(new)
    _print(f"\n{len(renames)} file(s) to rename.")
    return 0


def _filter_results_by_kind(results: list, kind_filter: str | None) -> list:
    if not kind_filter:
        return results
    out = []
    for r in results:
        try:
            data = json.loads(r.path.read_text(encoding="utf-8"))
            if data.get("kind") == kind_filter:
                out.append(r)
        except Exception:
            continue
    return out


def cmd_validate_structure(args: argparse.Namespace) -> int:
    era = getattr(args, "era", None)
    kind_filter = getattr(args, "kind", None) or None
    use_jsonschema = getattr(args, "json_schema", False)
    show_ok = getattr(args, "show_ok", False)

    results = validate_all(era=era, use_jsonschema=use_jsonschema)
    results = _filter_results_by_kind(results, kind_filter)

    errors = sum(1 for r in results if not r.ok)
    if _want_json(args) or getattr(args, "json", False):
        _emit_json({
            "era": era,
            "kind_filter": kind_filter,
            "json_schema": use_jsonschema,
            "files": len(results),
            "files_with_errors": errors,
            "results": [
                {
                    "path": str(r.path.relative_to(JSON_ROOT)),
                    "ok": r.ok,
                    "errors": r.errors,
                    "warnings": r.warnings,
                }
                for r in results
            ],
        }, args)
        return 1 if errors else 0

    _print(format_validation_report(results, show_ok=show_ok))
    _print(f"\nFiles: {len(results)}  With errors: {errors}")
    return 1 if errors else 0


def cmd_validate_all(args: argparse.Namespace) -> int:
    write_latest = getattr(args, "write_latest", False)
    era = getattr(args, "era", None)
    use_jsonschema = getattr(args, "json_schema", False)

    started = datetime.now(timezone.utc).isoformat()
    results = validate_all(era=era, use_jsonschema=use_jsonschema)
    finished = datetime.now(timezone.utc).isoformat()

    errors = [r for r in results if not r.ok]
    err_n = sum(len(r.errors) for r in errors)
    warn_n = sum(len(r.warnings) for r in results)
    files_scanned = len(results)

    findings = []
    for r in results:
        for e in r.errors:
            findings.append({
                "path": str(r.path.relative_to(JSON_ROOT)),
                "severity": "error",
                "message": e,
            })
        for w in r.warnings:
            findings.append({
                "path": str(r.path.relative_to(JSON_ROOT)),
                "severity": "warning",
                "message": w,
            })

    payload = {
        "schema_version": 1,
        "tool": "contact360-docs-validate-json",
        "started_at": started,
        "finished_at": finished,
        "docs_root": str(DOCS_ROOT.resolve()),
        "summary": {
            "files_scanned": files_scanned,
            "errors": err_n,
            "warnings": warn_n,
            "total_findings": len(findings),
        },
        "findings": findings,
    }

    if _want_json(args) or getattr(args, "json", False):
        _emit_json(payload, args)

    if (not (_want_json(args) or getattr(args, "json", False))) or getattr(args, "verbose", False):
        _print(format_validation_report(results, show_ok=getattr(args, "show_ok", False)))
        _print(f"\nFiles scanned: {files_scanned}  Errors: {err_n}  Warnings: {warn_n}")

    if write_latest:
        DOCS_RESULT_DIR.mkdir(parents=True, exist_ok=True)
        DOCS_ERRORS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        result_path = DOCS_RESULT_DIR / f"validation-{stamp}.json"
        err_path = DOCS_ERRORS_DIR / f"validation-{stamp}.json"
        errors_only = [f for f in findings if f["severity"] == "error"]
        result_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        err_path.write_text(json.dumps({**payload, "findings": errors_only}, indent=2), encoding="utf-8")
        (DOCS_RESULT_DIR / "latest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        (DOCS_ERRORS_DIR / "latest.json").write_text(json.dumps({**payload, "findings": errors_only}, indent=2), encoding="utf-8")
        _print(f"Wrote {result_path.name} and latest.json", force=True)

    return 1 if err_n else 0


def _find_era_index_json(era: int) -> Path | None:
    for p in JSON_ROOT.rglob("index.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("kind") == "index" and data.get("era_index") == era:
                return p
        except Exception:
            continue
    return None


def _refresh_era_indexes_after_update(era: int | None, all_docs: bool, dry_run: bool) -> None:
    if dry_run:
        return
    if all_docs:
        for p in sorted(JSON_ROOT.rglob("index.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if data.get("era_index") is not None:
                    update_index_children(p)
            except Exception:
                continue
        return
    if era is not None:
        idx = _find_era_index_json(era)
        if idx:
            update_index_children(idx)


def cmd_update(args: argparse.Namespace) -> int:
    status = args.status
    era = getattr(args, "era", None)
    file_path = getattr(args, "file", None)
    all_docs = getattr(args, "all", False)
    dry_run = args.dry_run
    refresh_index = getattr(args, "refresh_index", False)

    if file_path:
        p = Path(file_path)
        if not p.is_absolute():
            p = JSON_ROOT / file_path
        if not p.exists():
            _print(f"ERROR: file not found: {p}", force=True)
            return 1
        if dry_run:
            _print(f"[DRY] would set {p.name} status → {status}")
        else:
            update_status(p, status)
            if refresh_index:
                idx = p.parent / "index.json"
                if idx.exists():
                    update_index_children(idx)
        if _want_json(args):
            _emit_json({"file": str(p), "status": status, "dry_run": dry_run, "refresh_index": refresh_index}, args)
        return 0

    docs = scan_all(era=era if not all_docs else None)
    era_tasks = [d for d in docs if d.get("kind") == "era_task"]
    updated: list[str] = []
    for d in era_tasks:
        jp_rel = d.get("_json_path", "")
        if not jp_rel:
            continue
        p = JSON_ROOT / jp_rel
        if dry_run:
            _print(f"[DRY] {jp_rel} → {status}")
        else:
            try:
                update_status(p, status)
                updated.append(jp_rel)
            except Exception as e:
                _print(f"ERROR {jp_rel}: {e}", force=True)

    if refresh_index and not dry_run:
        _refresh_era_indexes_after_update(era, all_docs, dry_run)

    if _want_json(args):
        _emit_json({
            "status": status,
            "era": era,
            "all": all_docs,
            "dry_run": dry_run,
            "refresh_index": refresh_index,
            "updated_files": updated,
        }, args)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List JSON files with titles."""
    era = getattr(args, "era", None)
    kind = getattr(args, "kind", None)
    limit = getattr(args, "limit", 0) or 0
    with_path = getattr(args, "with_path", False)
    search = (getattr(args, "search", None) or "").strip().lower()

    docs = scan_all(era=era)
    if kind:
        docs = [d for d in docs if d.get("kind") == kind]
    if search:
        docs = [
            d for d in docs
            if search in (d.get("title") or "").lower()
            or search in (d.get("source_path") or "").lower()
        ]

    if _want_json(args) or getattr(args, "json", False):
        rows = []
        subset = docs if limit <= 0 else docs[:limit]
        for d in subset:
            row = {
                "kind": d.get("kind"),
                "version": d.get("version"),
                "status": d.get("status"),
                "title": d.get("title"),
            }
            if with_path:
                row["json_path"] = d.get("_json_path")
                row["source_path"] = d.get("source_path")
            rows.append(row)
        _emit_json({"count": len(rows), "total_matched": len(docs), "items": rows}, args)
        return 0

    _print(f"{'Kind':<20}  {'Version':<10}  {'Status':<12}  {'Path' if with_path else 'Title'}")
    _print("-" * 80)
    shown = 0
    for d in docs:
        if limit and shown >= limit:
            break
        k = d.get("kind", "?")
        v = d.get("version") or ""
        s = d.get("status") or ""
        col = (d.get("_json_path") or "") if with_path else (d.get("title", "")[:50])
        _print(f"{k:<20}  {v:<10}  {s:<12}  {col}")
        shown += 1
    if limit and len(docs) > limit:
        _print(f"\n(showing {limit} of {len(docs)}; use --limit 0 for all)")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# Migration commands
# ═══════════════════════════════════════════════════════════════════════════════

def cmd_migrate(
    subcmd: str,
    dry_run: bool,
    *,
    migrate_verbose: bool = False,
) -> int:
    """Run JSON maintenance scripts (indexes, manifest, validate)."""
    if subcmd == "indexes":
        script = SCRIPTS_ROOT / "generate_indexes.py"
        args = [sys.executable, str(script)]
        if dry_run:
            args.append("--dry-run")
    elif subcmd == "manifest":
        script = SCRIPTS_ROOT / "build_manifest.py"
        args = [sys.executable, str(script)]
        if dry_run:
            args.append("--dry-run")
    elif subcmd == "validate":
        script = SCRIPTS_ROOT / "validate_migration.py"
        args = [sys.executable, str(script)]
        if migrate_verbose:
            args.append("--verbose")
    elif subcmd == "full":
        _print("[bold]Running docs JSON pipeline (indexes → manifest → validate)...[/bold]")
        steps = [
            (["indexes"], "Regenerate index children"),
            (["manifest"], "Build manifest"),
            (["validate"], "Validate JSON tree"),
        ]
        for step_args, label in steps:
            _print(f"\n[cyan]--- {label} ---[/cyan]")
            # Re-invoke via subprocess for simplicity
            step_script = SCRIPTS_ROOT / {
                "indexes": "generate_indexes.py",
                "manifest": "build_manifest.py",
                "validate": "validate_migration.py",
            }[step_args[0]]
            step_cmd = [sys.executable, str(step_script)] + step_args[1:]
            result = subprocess.run(step_cmd, cwd=str(DOCS_ROOT))
            if result.returncode != 0:
                _print(f"[red]Step failed: {label}[/red]")
                return result.returncode
        _print("\n[green]Full migration complete.[/green]")
        return 0
    else:
        _print(f"Unknown migrate sub-command: {subcmd}")
        return 1

    result = subprocess.run(args, cwd=str(DOCS_ROOT))
    return result.returncode


# ═══════════════════════════════════════════════════════════════════════════════
# Non-docs commands — SQL, API test, Pinecone (delegated to subprocess)
# ═══════════════════════════════════════════════════════════════════════════════

def _run_script(script: str, extra_args: list[str], env_extra: dict | None = None) -> int:
    script_path = SCRIPTS_ROOT / script
    if not script_path.exists():
        _print(f"Script not found: {script_path}")
        return 1
    env = {**os.environ, **(env_extra or {})}
    result = subprocess.run([sys.executable, str(script_path)] + extra_args, env=env, cwd=str(DOCS_ROOT))
    return result.returncode


def cmd_pinecone(args: argparse.Namespace) -> int:
    sub = args.pinecone_cmd
    if sub == "ingest-docs":
        # Read raw_markdown from JSON files and pass to pinecone ingestion
        _print("Pinecone ingest — chunking typed docs JSON (raw_markdown or structured fallback) under docs/")
        return _run_script("pinecone_integration/ingest_docs.py", [])
    if sub == "query":
        _print(
            "Pinecone query: use scripts/pinecone_integration/search.search() from a configured Python env "
            "(no standalone query.py wrapper in this tree).",
            force=True,
        )
        return 1
    _print(f"Unknown pinecone sub-command: {sub}")
    return 1


def _env_arg(args: argparse.Namespace) -> list[str]:
    """Build --env flag for api-test scripts."""
    env_file = getattr(args, "env", None) or DEFAULT_CONTACT360_POSTMAN_ENV
    if env_file:
        return ["--env", str(env_file)]
    return []


def cmd_api_test_show_env(args: argparse.Namespace) -> int:
    if not HAS_POSTMAN:
        _print("postman_env module not available")
        return 1
    env_path = resolve_postman_env_path(getattr(args, "env", None))
    env_data = load_and_merge_env(env_path)
    display = redact_env_display(env_data)
    _print(json.dumps(display, indent=2))
    return 0


def cmd_api_test_subprocess(args: argparse.Namespace, script_name: str, forwarded: list[str] | None = None) -> int:
    extra = _env_arg(args) + (forwarded or [])
    return _run_script(f"api_test/{script_name}", extra)


def _strip_remainder_prefix(argv: list[str]) -> list[str]:
    if argv and argv[0] == "--":
        return argv[1:]
    return argv


def cmd_sql_run(args: argparse.Namespace) -> int:
    return _run_script("sql/run.py", _strip_remainder_prefix(list(getattr(args, "sql_args", []))))


def cmd_sql_init_schema(args: argparse.Namespace) -> int:
    return _run_script("sql/init_schema.py", [])


def cmd_sql_load_csv(args: argparse.Namespace) -> int:
    return _run_script("sql/load_csv.py", _strip_remainder_prefix(list(getattr(args, "csv_args", []))))


def cmd_postman_optimize(args: argparse.Namespace) -> int:
    return _run_script("postman_env.py", ["--optimize"])


def cmd_platform_verify(args: argparse.Namespace) -> int:
    if not HAS_PLATFORM:
        _print("platform module not available")
        return 1
    return platform_run_all()


# ═══════════════════════════════════════════════════════════════════════════════
# Parser
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Contact360 Docs CLI v2 (JSON-backed)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Global options (place before the subcommand):\n"
            "  -J, --machine-json   JSON output on supported commands\n"
            "  -q, --quiet          Less console noise\n"
            "  -v, --verbose        More detail / pretty-printed JSON\n"
            "\n"
            "Examples:\n"
            "  python cli.py -J scan\n"
            "  python cli.py scan --by-era --by-status\n"
            "  python cli.py list --kind era_task --limit 20 --with-path\n"
            "  python cli.py validate-all --write-latest --json-schema\n"
            "  python cli.py migrate full\n"
        ),
    )
    parser.add_argument(
        "-J", "--machine-json",
        action="store_true",
        dest="global_json",
        help="Emit machine-readable JSON for commands that support it (alias for per-command --json where applicable)",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress non-essential human-readable output")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose human output or indented JSON")

    sub = parser.add_subparsers(dest="command", required=True)

    # ── Documentation commands ──────────────────────────────────────────────

    scan_p = sub.add_parser("scan", help="Scan docs/ typed JSON and print overview dashboard")
    scan_p.add_argument("--by-era", action="store_true", help="Include per-era counts (human or -J output)")
    scan_p.add_argument("--by-status", action="store_true", help="Include per-status counts")

    stats_p = sub.add_parser("stats", help="Print era stats or global overview")
    stats_p.add_argument("--era", type=int, metavar="N", help="Era index 0–10")
    stats_p.add_argument("--kind", choices=KIND_CHOICES, help="Filter counts to this document kind")

    guide_p = sub.add_parser("era-guide", help="Show era map and navigation")
    guide_p.add_argument("--era", type=int, metavar="N")
    guide_p.add_argument("--json", action="store_true", help="JSON output (same as global -J)")

    audit_p = sub.add_parser("audit-tasks", help="Audit task_tracks in era_task JSON files")
    audit_p.add_argument("--era", type=int, metavar="N")
    audit_p.add_argument("--json", action="store_true", help="JSON report per file")
    audit_p.add_argument("--summary-only", action="store_true", help="One-line summary only (human mode)")

    fill_p = sub.add_parser("fill-tasks", help="Inject missing task_track keys into era_task JSON")
    fill_scope = fill_p.add_mutually_exclusive_group(required=True)
    fill_scope.add_argument("--era", type=int, metavar="N")
    fill_scope.add_argument("--file", type=str, metavar="PATH", help="Path under docs/ or filename")
    fill_scope.add_argument("--all", action="store_true", help="All era_task files")
    fill_p.add_argument("--dry-run", action="store_true", default=True)
    fill_p.add_argument("--apply", action="store_true", help="Write files (default is dry-run)")
    fill_p.add_argument("--json", action="store_true", help="JSON result summary")

    dedup_p = sub.add_parser("dedup-tasks", help="Detect duplicate task text across era files")
    dedup_scope = dedup_p.add_mutually_exclusive_group(required=True)
    dedup_scope.add_argument("--era", type=int, metavar="N")
    dedup_scope.add_argument("--all", action="store_true")
    dedup_p.add_argument("--dry-run", action="store_true", default=True)
    dedup_p.add_argument("--apply", action="store_true")
    dedup_p.add_argument("--limit", type=int, default=50, metavar="N", help="Max duplicate groups to show (default 50)")
    dedup_p.add_argument(
        "--min-locations",
        type=int,
        default=2,
        metavar="N",
        help="Minimum occurrences to count as duplicate (default 2)",
    )
    dedup_p.add_argument("--json", action="store_true", help="JSON sample of duplicates")

    report_p = sub.add_parser("task-report", help="Per-track coverage across era_task docs")
    report_p.add_argument("--era", type=int, metavar="N")
    report_p.add_argument("--json", action="store_true", help="Emit raw report object as JSON")

    name_p = sub.add_parser("name-audit", help="Audit era_task filenames for canonical format")
    name_p.add_argument("--era", type=int, metavar="N")
    name_p.add_argument("--json", action="store_true", help="JSON list of issues")

    rename_p = sub.add_parser("rename-docs", help="Rename era_task JSON to canonical form")
    rename_scope = rename_p.add_mutually_exclusive_group(required=True)
    rename_scope.add_argument("--era", type=int, metavar="N")
    rename_scope.add_argument("--all", action="store_true")
    rename_p.add_argument("--apply", action="store_true", help="Perform renames (default is dry-run)")
    rename_p.add_argument("--json", action="store_true", help="JSON list of planned renames")

    val_p = sub.add_parser("validate-structure", help="Validate JSON envelopes and optional jsonschema")
    val_p.add_argument("--era", type=int, metavar="N")
    val_p.add_argument("--kind", choices=KIND_CHOICES, help="Only validate files of this kind")
    val_p.add_argument(
        "--json-schema",
        action="store_true",
        help="Also run jsonschema (slower; validates full document including raw_markdown)",
    )
    val_p.add_argument("--show-ok", action="store_true", help="List passing files in human report")
    val_p.add_argument("--json", action="store_true", help="JSON array of per-file results")

    val_all_p = sub.add_parser("validate-all", help="Full validation + optional result files")
    val_all_p.add_argument("--write-latest", action="store_true", help="Write result/latest.json under result/ and errors/")
    val_all_p.add_argument("--era", type=int, metavar="N")
    val_all_p.add_argument("--json-schema", action="store_true", dest="json_schema", help="Include jsonschema validation")
    val_all_p.add_argument("--show-ok", action="store_true", help="Include passing files in human output")
    val_all_p.add_argument("--json", action="store_true", help="Print validation payload to stdout")

    update_p = sub.add_parser("update", help="Update status field in JSON docs")
    update_p.add_argument("--status", required=True, choices=["completed", "in_progress", "planned", "incomplete"])
    update_scope = update_p.add_mutually_exclusive_group(required=True)
    update_scope.add_argument("--era", type=int, metavar="N")
    update_scope.add_argument("--file", type=str, metavar="PATH")
    update_scope.add_argument("--all", action="store_true")
    update_p.add_argument("--dry-run", action="store_true")
    update_p.add_argument(
        "--refresh-index",
        action="store_true",
        help="After writes, refresh index.json children for affected era(s)",
    )
    update_p.add_argument("--json", action="store_true", help="JSON summary of update")

    list_p = sub.add_parser("list", help="List JSON docs (titles or paths)")
    list_p.add_argument("--era", type=int, metavar="N")
    list_p.add_argument("--kind", choices=KIND_CHOICES)
    list_p.add_argument("--limit", type=int, default=0, metavar="N", help="Max rows (0 = no limit)")
    list_p.add_argument("--with-path", action="store_true", help="Show json_path instead of title")
    list_p.add_argument("--search", type=str, metavar="TEXT", help="Filter by substring in title or source_path")
    list_p.add_argument("--json", action="store_true", help="JSON array of rows")

    # ── Migration commands ──────────────────────────────────────────────────

    mig_p = sub.add_parser("migrate", help="Run migration pipeline scripts")
    mig_p.add_argument("--dry-run", action="store_true")
    mig_p.add_argument(
        "--migrate-verbose",
        action="store_true",
        dest="migrate_verbose",
        help="Forward --verbose to validate_migration.py",
    )
    mig_sub = mig_p.add_subparsers(dest="migrate_cmd", required=True)
    mig_sub.add_parser("indexes", help="Regenerate all index.json files")
    mig_sub.add_parser("manifest", help="Rebuild docs/manifest.json")
    mig_sub.add_parser("validate", help="Run validate_migration.py")
    mig_sub.add_parser("full", help="Regenerate index children, manifest, and run validate_migration")

    # ── Non-docs commands ───────────────────────────────────────────────────

    pin_p = sub.add_parser("pinecone", help="Pinecone vector search operations")
    pin_sub = pin_p.add_subparsers(dest="pinecone_cmd", required=True)
    pin_sub.add_parser("ingest-docs", help="Ingest JSON docs into Pinecone")
    pin_q = pin_sub.add_parser("query", help="Query Pinecone index")
    pin_q.add_argument("query", nargs="?")

    api_p = sub.add_parser("api-test", help="API testing utilities")
    api_sub = api_p.add_subparsers(dest="api_test_cmd", required=True)
    api_se = api_sub.add_parser("show-env", help="Show resolved Postman environment")
    api_se.add_argument("--env", type=str)
    for name in ("discover", "document", "email-single", "login"):
        sp = api_sub.add_parser(name)
        sp.add_argument("--env", type=str)
    pg = api_sub.add_parser("pattern-generator")
    pg.add_argument("--env", type=str)
    pg.add_argument("pattern_generator_args", nargs=argparse.REMAINDER)

    sql_p = sub.add_parser("sql", help="Database SQL operations")
    sql_sub = sql_p.add_subparsers(dest="sql_cmd", required=True)
    sql_run = sql_sub.add_parser("run", help="Run sql/run.py with forwarded args")
    sql_run.add_argument("sql_args", nargs=argparse.REMAINDER, help="Arguments after -- passed to script")
    sql_sub.add_parser("init-schema", help="Initialize schema via sql/init_schema.py")
    sql_load = sql_sub.add_parser("load-csv", help="Load CSV via sql/load_csv.py")
    sql_load.add_argument("csv_args", nargs=argparse.REMAINDER, help="Arguments forwarded to script")

    postman_p = sub.add_parser("postman-optimize", help="Optimize Postman environment")
    postman_p.add_argument("--env", type=str)

    sub.add_parser("platform-verify", help="Run platform health checks")

    return parser


# ═══════════════════════════════════════════════════════════════════════════════
# Main dispatch
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    CLI_CTX["quiet"] = bool(getattr(args, "quiet", False))
    CLI_CTX["verbose"] = bool(getattr(args, "verbose", False))
    CLI_CTX["machine_json"] = bool(getattr(args, "global_json", False))

    cmd = args.command

    # Docs commands
    if cmd == "scan":
        return cmd_scan(args)
    if cmd == "stats":
        return cmd_stats(args)
    if cmd == "era-guide":
        return cmd_era_guide(args)
    if cmd == "audit-tasks":
        return cmd_audit_tasks(args)
    if cmd == "fill-tasks":
        return cmd_fill_tasks(args)
    if cmd == "dedup-tasks":
        return cmd_dedup_tasks(args)
    if cmd == "task-report":
        return cmd_task_report(args)
    if cmd == "name-audit":
        return cmd_name_audit(args)
    if cmd == "rename-docs":
        return cmd_rename_docs(args)
    if cmd == "validate-structure":
        return cmd_validate_structure(args)
    if cmd == "validate-all":
        return cmd_validate_all(args)
    if cmd == "update":
        return cmd_update(args)
    if cmd == "list":
        return cmd_list(args)

    # Migration
    if cmd == "migrate":
        mc = args.migrate_cmd
        dry = getattr(args, "dry_run", False)
        mig_verbose = getattr(args, "migrate_verbose", False)
        return cmd_migrate(mc, dry_run=dry, migrate_verbose=mig_verbose)

    # Non-docs
    if cmd == "pinecone":
        return cmd_pinecone(args)
    if cmd == "api-test":
        if args.api_test_cmd == "show-env":
            return cmd_api_test_show_env(args)
        if args.api_test_cmd == "pattern-generator":
            fwd = list(getattr(args, "pattern_generator_args", []))
            if fwd and fwd[0] == "--":
                fwd = fwd[1:]
            return cmd_api_test_subprocess(args, "email_pattern_generator.py", forwarded=fwd)
        script_map = {
            "discover": "endpoint_discovery.py",
            "document": "endpoint_documenter.py",
            "email-single": "email_single.py",
            "login": "api_token.py",
        }
        script = script_map.get(args.api_test_cmd)
        if script:
            return cmd_api_test_subprocess(args, script)
        return 2
    if cmd == "sql":
        if args.sql_cmd == "run":
            return cmd_sql_run(args)
        if args.sql_cmd == "init-schema":
            return cmd_sql_init_schema(args)
        if args.sql_cmd == "load-csv":
            return cmd_sql_load_csv(args)
        return 2
    if cmd == "postman-optimize":
        return cmd_postman_optimize(args)
    if cmd == "platform-verify":
        return cmd_platform_verify(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
