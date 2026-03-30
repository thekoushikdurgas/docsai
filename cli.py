"""CLI tool to manage documentation status and tracking."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console

from scripts.models import Status
from scripts.scanner import ERA_FOLDERS, scan_all, scan_era_only
from scripts.stats import (
    era_guide_detail_panel,
    era_guide_summary_table,
    era_summary,
    file_detail,
    overall_dashboard,
    naming_inventory_table,
    naming_issues_table,
    task_audit_table,
    track_coverage_table,
)
from scripts.contact360_era_guide import entries_to_json, get_era_guide_entries, get_era_guide_entry
from scripts.era_naming import apply_renames, find_naming_issues, plan_renames, scan_era_filenames
from scripts.task_auditor import audit_all, audit_era, find_duplicate_tasks
from scripts.task_filler import bulk_fill, deduplicate_file_tasks, fill_missing_tracks
from scripts.codebase_registry import load_registry
from scripts.updater import bulk_update, list_scope_paths
from scripts.duplicate_files import find_duplicate_groups
from scripts.maintenance_registry import run_maintain_era
from scripts.paths import (
    DATABASE_CSV_DIR,
    DATABASE_DIR,
    DEFAULT_CONTACT360_POSTMAN_ENV,
    DOCS_ERRORS_DIR,
    DOCS_RESULT_DIR,
    DOCS_ROOT,
    POSTMAN_DIR,
    SCRIPTS_ROOT,
)
from scripts.postman_env import (
    load_and_merge_env,
    preview_env_mapping,
    redact_env_display,
    resolve_postman_env_path,
)
from scripts.unused import find_unused_files, find_unused_for_prune, quarantine_paths

console = Console()

API_TEST_DIR = SCRIPTS_ROOT / "api_test"


def build_parser() -> argparse.ArgumentParser:
    """Build the command line argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="Docs status manager CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("scan", help="Scan docs and print dashboard + era summary")
    sub.add_parser("find-unused", help="Find files that are not referenced in any markdown file")

    stats_parser = sub.add_parser("stats", help="Print detailed status tables")
    stats_parser.add_argument("--era", type=int, help="Era index (0-10)")

    update_parser = sub.add_parser("update", help="Update status in docs")
    update_parser.add_argument(
        "--status", required=True, choices=["completed", "in_progress", "planned", "incomplete"]
    )
    update_scope = update_parser.add_mutually_exclusive_group(required=True)
    update_scope.add_argument("--era", type=int, help="Era index (0-10)")
    update_scope.add_argument("--file", type=str, help="Single markdown file path")
    update_scope.add_argument("--all", action="store_true", help="All era markdown files")
    update_parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    update_parser.add_argument("--no-tasks", action="store_true", help="Skip task bullet normalization")

    normalize_parser = sub.add_parser("normalize", help="Normalize status markers")
    normalize_parser.add_argument(
        "--status", default="completed", choices=["completed", "in_progress", "planned", "incomplete"]
    )
    normalize_parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")

    audit_tasks = sub.add_parser("audit-tasks", help="Audit missing/duplicate task tracks in era docs")
    audit_tasks.add_argument("--era", type=int, help="Era index 0-10 (default: all eras)")

    fill_tasks = sub.add_parser("fill-tasks", help="Inject missing ### track sections with generated bullets")
    fill_scope = fill_tasks.add_mutually_exclusive_group(required=True)
    fill_scope.add_argument("--era", type=int, help="Era index 0-10")
    fill_scope.add_argument("--file", type=str, help="Single markdown path under docs/")
    fill_scope.add_argument("--all", action="store_true", help="All era markdown files")
    fill_tasks.add_argument("--dry-run", action="store_true", help="Show changes without writing (default)")
    fill_tasks.add_argument("--apply", action="store_true", help="Write files (not dry-run)")

    dedup_tasks = sub.add_parser("dedup-tasks", help="Replace duplicate task bullets with patch-specific lines")
    dedup_scope = dedup_tasks.add_mutually_exclusive_group(required=True)
    dedup_scope.add_argument("--era", type=int, help="Era index 0-10")
    dedup_scope.add_argument("--all", action="store_true", help="All era markdown files")
    dedup_tasks.add_argument("--dry-run", action="store_true", help="Default: preview only")
    dedup_tasks.add_argument("--apply", action="store_true", help="Write files")

    task_report = sub.add_parser("task-report", help="Print per-track coverage table for era patch/minor files")
    task_report.add_argument("--era", type=int, help="Era index 0-10 (omit for all eras in one table)")

    name_audit = sub.add_parser(
        "name-audit",
        help="List era .md filenames: parsed version, codename, canonical form, duplicate detection",
    )
    name_audit.add_argument("--era", type=int, help="Era index 0-10 (omit for all 11 era folders)")

    rename_docs = sub.add_parser(
        "rename-docs",
        help="Rename versioned files to canonical `version — Codename.md` (Unicode em dash)",
    )
    rename_scope = rename_docs.add_mutually_exclusive_group(required=True)
    rename_scope.add_argument("--era", type=int, help="Single era index 0-10")
    rename_scope.add_argument("--all", action="store_true", help="All era folders")
    rename_docs.add_argument(
        "--apply",
        action="store_true",
        help="Perform renames (default is dry-run listing only)",
    )

    era_guide = sub.add_parser(
        "era-guide",
        help="Show Contact360 era map (0.x–10.x): master docs, pointers, execution checklist",
    )
    era_guide.add_argument("--era", type=int, help="Single era index 0-10 (omit for summary table of all eras)")
    era_guide.add_argument("--json", action="store_true", help="Machine-readable JSON (one or all eras)")

    val = sub.add_parser(
        "validate-structure",
        help="Validate markdown structure (hubs, era tasks, frontend pages, backend/apis, endpoints, codebases)",
    )
    val.add_argument("--prefix", type=str, default="", help="Relative path under docs/ (e.g. docs/docs or frontend/pages)")
    val.add_argument(
        "--kind",
        type=str,
        choices=[
            "hub",
            "era_task",
            "frontend_page",
            "backend_api",
            "endpoint_md",
            "codebase_analysis",
        ],
        default="",
        help="Filter to this DocKind (optional); default scan depends on kind (see docs/doc-folder-structure-policy.md)",
    )
    val.add_argument("--era", type=int, help="Era index 0-10 (scan that era folder only)")

    opt = sub.add_parser("optimize-docs", help="Aggregate health report or dry-run structure fix chain")
    opt_sub = opt.add_subparsers(dest="optimize_cmd", required=True)
    opt_sub.add_parser("report", help="Read-only: scan summary + audits + unused count")
    opt_fix = opt_sub.add_parser("fix-structure", help="fill-tasks + dedup-tasks + rename-docs chain")
    opt_fix.add_argument("--apply", action="store_true", help="Write files (default is dry-run for entire chain)")
    opt_fix.add_argument("--era", type=int, help="Limit fill/dedup to one era (rename still runs all when not set)")

    me = sub.add_parser("maintain-era", help="Run enrich / fix-readme-links / update-minors scripts for one era")
    me.add_argument("--era", type=int, help="Era index 0-10 (omit if --all)")
    me.add_argument("--all", action="store_true", help="Run for every era 0-10 sequentially")
    me.add_argument(
        "--action",
        required=True,
        choices=["enrich", "fix-readme-links", "update-minors"],
        help="Which maintenance script family to run",
    )
    me.add_argument("--apply", action="store_true", help="Execute scripts (default is dry-run preview)")
    me.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicit preview (default when --apply is omitted; silences typos vs global parse)",
    )

    dg = sub.add_parser("docs-gen", help="Patch creation and version flowchart helpers")
    dg_sub = dg.add_subparsers(dest="docs_gen_cmd", required=True)
    dg_cp = dg_sub.add_parser("create-patches", help="Delegate to docs_patch_creator")
    dg_cp.add_argument("--eras", type=str, default="", help="Comma-separated era numbers, e.g. 1,2,3")
    dg_cp.add_argument("--apply", action="store_true", help="Write patch docs")
    dg_cp.add_argument("--dry-run", action="store_true", help="Plan only (default if neither flag)")
    dg_cp.add_argument("--report-json", type=str, default="", help="Optional JSON report path")
    dg_fc = dg_sub.add_parser("flowcharts", help="Rewrite ## Flowchart in docs/versions/version_*.md")
    dg_fc.add_argument("--apply", action="store_true", help="Write files (otherwise print hint only)")

    fe = sub.add_parser("frontend", help="Frontend page spec utilities")
    fe_sub = fe.add_subparsers(dest="frontend_cmd", required=True)
    fe_sub.add_parser("link-endpoint-specs", help="Refresh AUTO:endpoint-links blocks in *_page.md")
    fe_aug = fe_sub.add_parser("augment-page-specs", help="Refresh AUTO:design-nav blocks in *_page.md")
    fe_aug.add_argument("--apply", action="store_true", help="Write files")
    fe_aug.add_argument("--dry-run", action="store_true", help="Show how many files would be processed")

    pr = sub.add_parser(
        "prune-unused",
        help="Quarantine files reported as unused (excludes era folders by default)",
    )
    pr.add_argument("--apply", action="store_true", help="Move files to quarantine (default: dry-run list)")
    pr.add_argument(
        "--quarantine",
        type=str,
        default="",
        help="Destination folder relative to docs/, default _quarantine/YYYY-MM-DD",
    )
    pr.add_argument(
        "--include-era-patches",
        action="store_true",
        help="Include unused candidates under era folders (unsafe)",
    )

    fd = sub.add_parser("find-duplicate-files", help="Report duplicate files by SHA-256 under docs/")
    fd.add_argument("--prefix", type=str, default="", help="Relative path under docs/ to scan")
    fd.add_argument(
        "--ext",
        type=str,
        default="",
        help="Comma-separated extensions to include, e.g. .md,.json (default: all non-huge files)",
    )

    at = sub.add_parser(
        "api-test",
        help="Run docs/scripts/api_test with optional Postman *.postman_environment.json",
    )
    at.add_argument(
        "--postman-env",
        type=str,
        default="",
        help="Postman environment JSON path, or name under docs/backend/postman/ (default: also DOCS_POSTMAN_ENV)",
    )
    at.add_argument(
        "--override-env",
        action="store_true",
        help="Apply Postman values even when the variable is already set in the environment",
    )
    at_sub = at.add_subparsers(dest="api_test_cmd", required=True)
    at_sub.add_parser("show-env", help="Print mapped env keys from Postman file (secrets redacted)")
    at_sub.add_parser("discover", help="Discover API endpoints from backend routers (AST)")
    at_sub.add_parser(
        "document",
        help="Discover, authenticate, hit endpoints, write reports under api_test/output/",
    )
    at_sub.add_parser("email-single", help="Batch-test /api/v2/email/single/ from CSV data/")
    at_sub.add_parser("login", help="Log in and print access token (api_token.py)")
    at_pat = at_sub.add_parser(
        "pattern-generator",
        help="Run email_pattern_generator.py; pass script args after --",
    )
    at_pat.add_argument(
        "pattern_generator_args",
        nargs=argparse.REMAINDER,
        default=[],
        help="Arguments forwarded to email_pattern_generator.py",
    )

    sq = sub.add_parser(
        "sql",
        help="PostgreSQL: run SQL files (docs/scripts/sql) or load CSV; uses scripts/data config",
    )
    sq_sub = sq.add_subparsers(dest="sql_cmd", required=True)
    sq_run = sq_sub.add_parser(
        "run",
        help="Execute a .sql file (dollar-quote aware split; default: scripts/sql/sqlline.sql)",
    )
    sq_run.add_argument(
        "--file",
        "-f",
        type=str,
        default="",
        help="Path (cwd, docs/, scripts/sql/, backend/database/)",
    )
    sq_run.add_argument("--dry-run", action="store_true", help="Parse only; no DB connection")
    sq_run.add_argument("--no-log-files", action="store_true", help="Skip result/ and error/ logs")
    sq_run.add_argument(
        "--strip-comments",
        action="store_true",
        help="Remove comments per statement before execute (after split)",
    )
    sq_run.add_argument(
        "--format-sql",
        action="store_true",
        help="Pretty-print each statement with sqlparse (optional dependency)",
    )
    sq_run.add_argument(
        "--write-processed",
        type=str,
        default="",
        help="Write processed SQL (strip/format) to this path",
    )

    sq_init = sq_sub.add_parser(
        "init-schema",
        help="Expand backend/database/init_schema.sql (\\i includes) and execute",
    )
    sq_init.add_argument("--dry-run", action="store_true", help="Parse expanded script only")
    sq_init.add_argument("--no-log-files", action="store_true", help="Skip writing log files")
    sq_init.add_argument("--strip-comments", action="store_true", help="Same as sql run")
    sq_init.add_argument("--format-sql", action="store_true", help="Same as sql run")
    sq_init.add_argument("--write-processed", type=str, default="", help="Same as sql run")

    sq_csv = sq_sub.add_parser(
        "load-csv",
        help="INSERT CSV rows (batched). Use --preset for backend/database/csv seeds.",
    )
    sq_csv.add_argument(
        "--preset",
        type=str,
        default="",
        help="subscription_plans | subscription_plan_periods | addon_packages | user_profiles",
    )
    sq_csv.add_argument(
        "--csv",
        type=str,
        default="",
        help="CSV path (cwd, docs/, database/, database/csv/). Not needed with --preset",
    )
    sq_csv.add_argument(
        "--table",
        type=str,
        default="",
        help="Target table (default from --preset when preset is set)",
    )
    sq_csv.add_argument("--schema", type=str, default="public", help="Schema (default public)")
    sq_csv.add_argument("--delimiter", type=str, default=",")
    sq_csv.add_argument("--encoding", type=str, default="utf-8")
    sq_csv.add_argument("--no-header", action="store_true", help="First row is data; use --columns")
    sq_csv.add_argument(
        "--columns",
        type=str,
        default="",
        help="Comma-separated column names (required when --no-header)",
    )
    sq_csv.add_argument(
        "--skip-leading-column",
        action="store_true",
        help="Ignore first column in each row (e.g. leading # index in seed CSVs)",
    )
    sq_csv.add_argument("--batch-size", type=int, default=200)

    _list_help = "List catalog commands (Docs Agent menu + extra CLI/scripts)"
    try:
        list_p = sub.add_parser("list", aliases=["ls"], help=_list_help)
    except TypeError:
        list_p = sub.add_parser("list", help=_list_help)
    list_p.add_argument("--json", action="store_true", help="Machine-readable JSON")
    list_p.add_argument(
        "--category",
        type=str,
        default="all",
        choices=["docs", "data", "api", "scripts", "all"],
        help="Filter by category (default: all)",
    )
    list_p.add_argument(
        "--include-scripts",
        action="store_true",
        help="Include maintenance script pointers (enrich_*, docs_patch_creator, …)",
    )

    va = sub.add_parser(
        "validate-all",
        help="Run structure + optional task/naming audits; write docs/result + docs/errors JSON",
    )
    va.add_argument(
        "--write-latest",
        action="store_true",
        help="Write timestamped JSON + result/latest.json and errors/latest.json",
    )
    va.add_argument("--skip-tasks", action="store_true", help="Skip era task audit")
    va.add_argument("--skip-naming", action="store_true", help="Skip filename naming audit")

    fmt = sub.add_parser(
        "format-structure",
        help="Format markdown (LF, trim trailing whitespace, EOF newline) — same scope as validate-structure",
    )
    fmt.add_argument("--prefix", type=str, default="", help="Same as validate-structure")
    fmt.add_argument(
        "--kind",
        type=str,
        choices=[
            "hub",
            "era_task",
            "frontend_page",
            "backend_api",
            "endpoint_md",
            "codebase_analysis",
        ],
        default="",
        help="Same as validate-structure",
    )
    fmt.add_argument("--era", type=int, help="Era index 0-10 (same as validate-structure)")
    fmt.add_argument(
        "--apply",
        action="store_true",
        help="Write files (default: dry-run — list paths that would change)",
    )

    fall = sub.add_parser(
        "format-all",
        help="Format markdown for validate-all structure scope (hubs + era tasks + frontend pages)",
    )
    fall.add_argument(
        "--apply",
        action="store_true",
        help="Write files (default: dry-run)",
    )
    fall.add_argument(
        "--include-prose",
        action="store_true",
        help="Also format backend/apis, backend/endpoints/*.md, codebases/*.md",
    )
    fall.add_argument(
        "--write-latest",
        action="store_true",
        help="Write docs/result/format-latest.json (+ timestamped copy)",
    )

    data_p = sub.add_parser("data", help="Data analysis, cleaning, and ingestion REPL")
    data_sub = data_p.add_subparsers(dest="data_cmd", required=True)
    d_acn = data_sub.add_parser("analyze-company-names", help="Categorize company names in DB (report)")
    d_acn.add_argument(
        "--dry-run",
        action="store_true",
        help="Print configured DB target only; do not connect (offline smoke test)",
    )
    d_cda = data_sub.add_parser("comprehensive-analysis", help="Company / keyword / title quality report")
    d_cda.add_argument(
        "--dry-run",
        action="store_true",
        help="Print configured DB target only; do not connect (offline smoke test)",
    )
    d_clean = data_sub.add_parser("clean-db", help="Clean companies & contacts tables (writes DB)")
    d_clean.add_argument("--dry-run", action="store_true", help="Print plan only; do not connect")
    d_clean.add_argument("--batch-size", type=int, default=1000, help="Ignored for dry-run")
    data_sub.add_parser("ingest-local", help="Interactive data ingestion menu (local/S3/generator)")

    return parser


def _status(value: str) -> Status:
    return Status.from_cli(value)


def cmd_scan() -> int:
    """Run a full scan and print the overall dashboard and era summary."""
    result = scan_all()
    console.print(overall_dashboard(result))
    console.print(era_summary(result))
    return 0


def cmd_stats(era: int | None) -> int:
    """Print detailed status tables for a specific era or the overall dashboard."""
    result = scan_all()
    if era is None:
        console.print(overall_dashboard(result))
        console.print(era_summary(result))
        return 0
    if era < 0 or era >= len(ERA_FOLDERS):
        console.print("[red]Era must be between 0 and 10[/red]")
        return 2
    console.print(file_detail(result, ERA_FOLDERS[era]))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Update documentation status labels dynamically based on scope arguments."""
    if args.file:
        scope = "file"
        file_path = str(Path(args.file))
        era = None
    elif args.era is not None:
        scope = "era"
        file_path = None
        era = args.era
    else:
        scope = "all"
        file_path = None
        era = None

    try:
        paths = list_scope_paths(scope=scope, era=era, file_path=file_path)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 2

    summary = bulk_update(
        paths=paths,
        new_status=_status(args.status),
        update_tasks=not args.no_tasks,
        dry_run=args.dry_run,
    )
    label = "Dry run" if args.dry_run else "Applied"
    console.print(
        f"{label} -> files: {summary['files']}, "
        f"changed: {summary['changed']}, diff_lines: {summary['diff_lines']}"
    )
    return 0


def cmd_find_unused() -> int:
    """Search for Markdown files that are not linked or referenced."""
    unused = find_unused_files()
    if not unused:
        console.print("[green]No unused files found![/green]")
        return 0
    console.print(f"[yellow]Found {len(unused)} potentially unused files:[/yellow]")
    for path in unused:
        try:
            rel_path = path.relative_to(DOCS_ROOT)
        except ValueError:
            rel_path = path
        console.print(f"- {rel_path}")
    return 0


def cmd_normalize(status: str, dry_run: bool) -> int:
    """Normalize the task status markers in all markdown files."""
    paths = list_scope_paths(scope="all")
    summary = bulk_update(
        paths=paths,
        new_status=_status(status),
        update_tasks=True,
        dry_run=dry_run,
    )
    label = "Dry run" if dry_run else "Applied"
    console.print(
        f"{label} -> files: {summary['files']}, "
        f"changed: {summary['changed']}, diff_lines: {summary['diff_lines']}"
    )
    return 0


def cmd_audit_tasks(era: int | None) -> int:
    """Print task audit tables for one era or all eras."""
    if era is None:
        data = audit_all()
        total = 0
        for _name, results in data.items():
            if not results:
                continue
            console.print(task_audit_table(results))
            total += len(results)
        console.print(f"[bold]Total audited files: {total}[/bold]")
        return 0
    if era < 0 or era >= len(ERA_FOLDERS):
        console.print("[red]Era must be between 0 and 10[/red]")
        return 2
    results = audit_era(era)
    console.print(task_audit_table(results))
    console.print(f"[bold]Audited files: {len(results)}[/bold]")
    return 0


def cmd_fill_tasks(args: argparse.Namespace) -> int:
    """Fill missing task tracks; dry-run unless --apply."""
    dry_run = not getattr(args, "apply", False)
    reg = load_registry()
    try:
        if args.file:
            fp = Path(args.file)
            paths = [fp if fp.is_absolute() else (DOCS_ROOT / fp)]
        elif args.era is not None:
            paths = list_scope_paths(scope="era", era=args.era)
        else:
            paths = list_scope_paths(scope="all")
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 2
    summary = bulk_fill(paths, registry=reg, dry_run=dry_run, dedup=False)
    label = "Dry run" if dry_run else "Applied"
    console.print(
        f"{label} -> files: {summary['files']}, changed: {summary['changed']}, "
        f"diff_lines: {summary['diff_lines']}, tracks_added_batches: {summary['tracks_added']}"
    )
    return 0


def cmd_dedup_tasks(args: argparse.Namespace) -> int:
    """Deduplicate task bullets within each era."""
    dry_run = not getattr(args, "apply", False)
    reg = load_registry()

    if getattr(args, "all", False):
        era_indices = range(len(ERA_FOLDERS))
    else:
        if args.era is None or args.era < 0 or args.era >= len(ERA_FOLDERS):
            console.print("[red]Era must be 0-10[/red]")
            return 2
        era_indices = [args.era]

    changed = 0
    diff_lines = 0
    for ei in era_indices:
        era_name = ERA_FOLDERS[ei]
        era_docs = [d for d in scan_era_only().files if d.era == era_name]
        dup_map = find_duplicate_tasks(era_docs)
        for path in sorted((DOCS_ROOT / era_name).glob("*.md")):
            ch, dl = deduplicate_file_tasks(path, ei, dup_map, reg, dry_run=dry_run)
            if ch:
                changed += 1
                diff_lines += dl
    label = "Dry run" if dry_run else "Applied"
    console.print(f"{label} -> files changed: {changed}, diff_lines (sum): {diff_lines}")
    return 0


def cmd_task_report(era: int | None) -> int:
    """Print track coverage table."""
    scan_result = scan_era_only()
    era_name: str | None
    if era is None:
        era_name = None
    elif era < 0 or era >= len(ERA_FOLDERS):
        console.print("[red]Era must be between 0 and 10[/red]")
        return 2
    else:
        era_name = ERA_FOLDERS[era]
    console.print(track_coverage_table(scan_result, era_name))
    return 0


def cmd_name_audit(era: int | None) -> int:
    """Show parsed filenames, duplicate version keys, malformed names, non-canonical separators."""
    if era is not None and (era < 0 or era >= len(ERA_FOLDERS)):
        console.print("[red]Era must be between 0 and 10[/red]")
        return 2
    records = scan_era_filenames(era)
    issues = find_naming_issues(records)
    console.print(naming_inventory_table(records))
    if issues:
        console.print(naming_issues_table(issues))
        for issue in issues:
            if issue.code == "DUPLICATE_VERSION" and issue.paths:
                console.print(f"[red]Duplicate version:[/red] {issue.detail}")
                for p in issue.paths[:12]:
                    console.print(f"  - {p}")
                if len(issue.paths) > 12:
                    console.print(f"  … ({len(issue.paths)} total)")
    else:
        console.print("[green]No naming issues detected.[/green]")
    dup_err = any(i.code == "DUPLICATE_VERSION" and i.severity == "error" for i in issues)
    n_warn = sum(1 for i in issues if i.severity == "warning")
    n_err = sum(1 for i in issues if i.severity == "error")
    console.print(f"[bold]Summary:[/bold] {len(records)} files, {n_err} error groups, {n_warn} warning groups")
    return 2 if dup_err else 0


def cmd_era_guide(era: int | None, json_flag: bool) -> int:
    """Print era guide summary table, full detail for one era, or JSON."""
    if json_flag:
        if era is not None:
            if era < 0 or era > 10:
                console.print("[red]Era must be between 0 and 10[/red]")
                return 2
            e = get_era_guide_entry(era)
            if e is None:
                console.print("[red]Unknown era[/red]")
                return 2
            print(entries_to_json([e]))
        else:
            print(entries_to_json(get_era_guide_entries()))
        return 0
    if era is not None:
        if era < 0 or era > 10:
            console.print("[red]Era must be between 0 and 10[/red]")
            return 2
        e = get_era_guide_entry(era)
        if e is None:
            console.print("[red]Unknown era[/red]")
            return 2
        console.print(era_guide_detail_panel(e))
        return 0
    console.print(era_guide_summary_table(get_era_guide_entries()))
    return 0


def cmd_rename_docs(args: argparse.Namespace) -> int:
    """Plan and optionally apply canonical renames (em dash, trimmed codename)."""
    dry_run = not getattr(args, "apply", False)
    if getattr(args, "all", False):
        era_arg: int | None = None
    else:
        if args.era is None or args.era < 0 or args.era >= len(ERA_FOLDERS):
            console.print("[red]Era must be 0-10[/red]")
            return 2
        era_arg = args.era
    records = scan_era_filenames(era_arg)
    pairs = plan_renames(records)
    skipped = [(o, n, r) for o, n, r in pairs if r == "SKIP_TARGET_EXISTS"]
    for old, new, reason in pairs:
        if reason == "SKIP_TARGET_EXISTS":
            console.print(f"[yellow]Would skip[/yellow] (target exists): {old.name} -> {new.name}")
        else:
            label = "rename" if not dry_run else "would rename"
            console.print(f"[cyan]{label}[/cyan]: {old.name} -> {new.name}")
    if skipped:
        console.print(f"[yellow]{len(skipped)} path(s) skipped (target already exists).[/yellow]")
    summary = apply_renames(pairs, dry_run=dry_run)
    lbl = "Dry run" if dry_run else "Applied"
    console.print(
        f"[bold]{lbl}[/bold]: planned={summary['planned']}, renamed={summary['renamed']}, "
        f"skipped={summary['skipped']}, errors={summary['errors']}"
    )
    return 0 if summary["errors"] == 0 else 1


def cmd_validate_structure(args: argparse.Namespace) -> int:
    from scripts.doc_structure import collect_structure_paths, kind_from_cli, validate_file

    kind = kind_from_cli(getattr(args, "kind", "") or "")
    paths = collect_structure_paths(
        prefix=(getattr(args, "prefix", "") or "").strip(),
        era_index=getattr(args, "era", None),
        kind=kind,
    )

    errors = 0
    warnings = 0
    for p in paths:
        for f in validate_file(p):
            try:
                rel = f.path.relative_to(DOCS_ROOT)
            except ValueError:
                rel = f.path
            msg = f"{rel}: [{f.severity}] {f.message}"
            if f.severity == "error":
                console.print(f"[red]{msg}[/red]")
                errors += 1
            else:
                console.print(f"[yellow]{msg}[/yellow]")
                warnings += 1
    console.print(f"[bold]Summary:[/bold] files={len(paths)}, errors={errors}, warnings={warnings}")
    return 1 if errors else 0


def cmd_format_structure(args: argparse.Namespace) -> int:
    from scripts.doc_format import format_file
    from scripts.doc_structure import collect_structure_paths, kind_from_cli

    kind = kind_from_cli(getattr(args, "kind", "") or "")
    paths = collect_structure_paths(
        prefix=(getattr(args, "prefix", "") or "").strip(),
        era_index=getattr(args, "era", None),
        kind=kind,
    )
    dry_run = not bool(getattr(args, "apply", False))
    changed = 0
    err_n = 0
    for p in paths:
        r = format_file(p, dry_run=dry_run)
        if r.error:
            console.print(f"[red]{_rel_json_path(p)}: {r.error}[/red]")
            err_n += 1
        elif r.changed:
            changed += 1
            rel = _rel_json_path(p)
            label = "would format" if dry_run else "formatted"
            console.print(f"[cyan]{label}[/cyan]: {rel}")
    mode = "dry-run" if dry_run else "apply"
    console.print(f"[bold]format-structure[/bold] ({mode}): files={len(paths)}, changed={changed}, errors={err_n}")
    return 1 if err_n else 0


def cmd_format_all(args: argparse.Namespace) -> int:
    from scripts.doc_format import format_file
    from scripts.doc_structure import collect_validate_all_structure_paths

    paths = collect_validate_all_structure_paths(include_prose=bool(getattr(args, "include_prose", False)))
    dry_run = not bool(getattr(args, "apply", False))
    write_latest = bool(getattr(args, "write_latest", False))

    changed = 0
    err_n = 0
    file_rows: list[dict] = []
    started = datetime.now(timezone.utc).isoformat()

    for p in paths:
        r = format_file(p, dry_run=dry_run)
        rel = _rel_json_path(p)
        if r.error:
            console.print(f"[red]{rel}: {r.error}[/red]")
            err_n += 1
            file_rows.append({"path": rel, "changed": False, "error": r.error})
        elif r.changed:
            changed += 1
            label = "would format" if dry_run else "formatted"
            console.print(f"[cyan]{label}[/cyan]: {rel}")
            file_rows.append({"path": rel, "changed": True, "error": None})
        else:
            file_rows.append({"path": rel, "changed": False, "error": None})

    finished = datetime.now(timezone.utc).isoformat()
    mode = "dry-run" if dry_run else "apply"
    console.print(
        f"[bold]format-all[/bold] ({mode}): files={len(paths)}, changed={changed}, errors={err_n}"
    )

    if write_latest:
        payload = {
            "schema_version": 1,
            "tool": "contact360-docs-format",
            "started_at": started,
            "finished_at": finished,
            "docs_root": str(DOCS_ROOT.resolve()),
            "invocation": {
                "argv": sys.argv[1:],
                "dry_run": dry_run,
                "include_prose": bool(getattr(args, "include_prose", False)),
            },
            "summary": {
                "files": len(paths),
                "changed": changed,
                "errors": err_n,
            },
            "files": file_rows,
        }
        DOCS_RESULT_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = DOCS_RESULT_DIR / f"format-{stamp}.json"
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        latest = DOCS_RESULT_DIR / "format-latest.json"
        latest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        try:
            console.print(f"[green]Wrote[/green] {out.relative_to(DOCS_ROOT)} and format-latest.json")
        except ValueError:
            console.print(f"[green]Wrote[/green] {out}")

    return 1 if err_n else 0


def cmd_optimize_report() -> int:
    result = scan_all()
    console.print(overall_dashboard(result))
    console.print(era_summary(result))
    data = audit_all()
    total_audited = 0
    for _name, results in data.items():
        if not results:
            continue
        console.print(task_audit_table(results))
        total_audited += len(results)
    console.print(f"[bold]Task audit files:[/bold] {total_audited}")
    records = scan_era_filenames(None)
    issues = find_naming_issues(records)
    console.print(f"[bold]Naming audit:[/bold] {len(records)} files, {len(issues)} issue group(s)")
    unused = find_unused_files()
    console.print(f"[bold]Find-unused (heuristic) candidates:[/bold] {len(unused)}")
    return 0


def cmd_optimize_fix_structure(args: argparse.Namespace) -> int:
    apply_writes = bool(getattr(args, "apply", False))
    dry_run = not apply_writes
    reg = load_registry()
    era_only = getattr(args, "era", None)

    try:
        if era_only is not None:
            paths = list_scope_paths(scope="era", era=era_only)
        else:
            paths = list_scope_paths(scope="all")
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 2

    summary = bulk_fill(paths, registry=reg, dry_run=dry_run, dedup=False)
    lbl = "Applied" if apply_writes else "Dry run"
    console.print(
        f"fill-tasks {lbl}: files={summary['files']}, changed={summary['changed']}, "
        f"diff_lines={summary['diff_lines']}, tracks_added={summary.get('tracks_added', 0)}"
    )

    era_indices: range | list[int]
    if era_only is not None:
        era_indices = [era_only]
    else:
        era_indices = range(len(ERA_FOLDERS))
    changed = 0
    diff_lines = 0
    for ei in era_indices:
        era_name = ERA_FOLDERS[ei]
        era_docs = [d for d in scan_era_only().files if d.era == era_name]
        dup_map = find_duplicate_tasks(era_docs)
        for path in sorted((DOCS_ROOT / era_name).glob("*.md")):
            ch, dl = deduplicate_file_tasks(path, ei, dup_map, reg, dry_run=dry_run)
            if ch:
                changed += 1
                diff_lines += dl
    console.print(f"dedup-tasks {lbl}: files changed={changed}, diff_lines={diff_lines}")

    if era_only is not None:
        rename_ns = argparse.Namespace(apply=apply_writes, all=False, era=era_only)
    else:
        rename_ns = argparse.Namespace(apply=apply_writes, all=True, era=None)
    return cmd_rename_docs(rename_ns)


def cmd_maintain_era_cli(args: argparse.Namespace) -> int:
    dry_run = not bool(getattr(args, "apply", False))
    action = args.action
    if getattr(args, "all", False):
        rc = 0
        for ei in range(len(ERA_FOLDERS)):
            r = run_maintain_era(ei, action, dry_run=dry_run)
            if r != 0:
                rc = r
        return rc
    if args.era is None or args.era < 0 or args.era > 10:
        console.print("[red]Provide --era 0-10 or --all[/red]")
        return 2
    return run_maintain_era(args.era, action, dry_run=dry_run)


def cmd_docs_gen_create_patches(args: argparse.Namespace) -> int:
    cmd: list[str] = [
        sys.executable,
        str(SCRIPTS_ROOT / "docs_patch_creator.py"),
        "--docs-root",
        str(DOCS_ROOT),
    ]
    if args.eras.strip():
        cmd.extend(["--eras", args.eras.strip()])
    if args.apply:
        cmd.append("--apply")
    else:
        cmd.append("--dry-run")
    if getattr(args, "report_json", "").strip():
        cmd.extend(["--report-json", args.report_json.strip()])
    r = subprocess.run(cmd, cwd=str(SCRIPTS_ROOT))
    return int(r.returncode)


def cmd_docs_gen_flowcharts(args: argparse.Namespace) -> int:
    if not getattr(args, "apply", False):
        console.print(
            "[yellow]Dry-run:[/yellow] pass --apply to rewrite ## Flowchart in docs/versions/version_*.md"
        )
        return 0
    r = subprocess.run(
        [sys.executable, str(SCRIPTS_ROOT / "apply_unique_flowcharts.py")],
        cwd=str(SCRIPTS_ROOT),
    )
    return int(r.returncode)


def cmd_frontend_link() -> int:
    from scripts import link_endpoint_specs

    return link_endpoint_specs.main()


def cmd_frontend_augment(args: argparse.Namespace) -> int:
    from scripts import augment_page_specs

    if getattr(args, "dry_run", False):
        n = 0
        if augment_page_specs.INDEX.is_file():
            n = sum(1 for _ in augment_page_specs.DIR.glob("*_page.md"))
        console.print(f"[yellow]Dry-run:[/yellow] would process up to {n} *_page.md under frontend/pages")
        return 0
    if not getattr(args, "apply", False):
        console.print("[yellow]Pass --apply to write, or --dry-run to preview count[/yellow]")
        return 2
    return augment_page_specs.main()


def cmd_prune_unused(args: argparse.Namespace) -> int:
    from datetime import datetime

    candidates = find_unused_for_prune(exclude_era_folders=not getattr(args, "include_era_patches", False))
    if not candidates:
        console.print("[green]No unused candidates (with current filters).[/green]")
        return 0
    q = getattr(args, "quarantine", "") or ""
    if not q.strip():
        q = f"_quarantine/{datetime.now().strftime('%Y-%m-%d')}"
    dest = DOCS_ROOT / q.replace("\\", "/").strip("/")
    if not getattr(args, "apply", False):
        console.print(f"[yellow]Dry-run:[/yellow] would quarantine {len(candidates)} file(s) under {dest}")
        for p in candidates[:50]:
            console.print(f"  - {p.relative_to(DOCS_ROOT)}")
        if len(candidates) > 50:
            console.print(f"  … and {len(candidates) - 50} more")
        return 0
    moved, errors = quarantine_paths(candidates, dest)
    console.print(f"[green]Moved {len(moved)} file(s) to {dest}[/green]")
    for e in errors:
        console.print(f"[red]{e}[/red]")
    return 1 if errors else 0


def _api_test_merged_environ(args: argparse.Namespace) -> dict[str, str] | None:
    """Build child process env; None means invalid --postman-env."""
    raw = (getattr(args, "postman_env", "") or "").strip() or os.environ.get("DOCS_POSTMAN_ENV", "").strip()
    override = bool(getattr(args, "override_env", False))
    base = os.environ.copy()
    if not raw:
        return base
    p = resolve_postman_env_path(raw, docs_root=DOCS_ROOT, postman_dir=POSTMAN_DIR)
    if p is None:
        console.print(f"[red]Postman environment file not found:[/red] {raw}")
        return None
    env, _ = load_and_merge_env(p, base=base, override_existing=override)
    return env


def cmd_api_test_show_env(args: argparse.Namespace) -> int:
    raw = (getattr(args, "postman_env", "") or "").strip() or os.environ.get("DOCS_POSTMAN_ENV", "").strip()
    if raw:
        p = resolve_postman_env_path(raw, docs_root=DOCS_ROOT, postman_dir=POSTMAN_DIR)
        if p is None:
            console.print(f"[red]Postman environment file not found:[/red] {raw}")
            return 2
    else:
        p = DEFAULT_CONTACT360_POSTMAN_ENV if DEFAULT_CONTACT360_POSTMAN_ENV.is_file() else None
        if p is None:
            console.print(
                "[red]No Postman file: pass --postman-env, set DOCS_POSTMAN_ENV, or add[/red] "
                f"[dim]{DEFAULT_CONTACT360_POSTMAN_ENV}[/dim]"
            )
            return 2
    mapped = preview_env_mapping(p)
    console.print(f"[bold]Mapped variables[/bold] [dim]({p})[/dim]:")
    for k in sorted(mapped.keys()):
        console.print(f"  {k}={redact_env_display(k, mapped[k])}")
    return 0


def cmd_api_test_subprocess(
    args: argparse.Namespace,
    script: str,
    forwarded: list[str] | None = None,
) -> int:
    env = _api_test_merged_environ(args)
    if env is None:
        return 2
    candidate = API_TEST_DIR / script
    script_path = candidate if candidate.is_file() else SCRIPTS_ROOT / script
    if not script_path.is_file():
        console.print(
            f"[red]Missing script:[/red] {candidate} (and not under {SCRIPTS_ROOT / script})"
        )
        return 2
    cmd = [sys.executable, str(script_path.resolve())] + (forwarded or [])
    proc = subprocess.run(cmd, cwd=str(SCRIPTS_ROOT), env=env)
    return int(proc.returncode)


def cmd_sql_run(args: argparse.Namespace) -> int:
    argv: list[str] = []
    if getattr(args, "file", "").strip():
        argv.extend(["--file", args.file.strip()])
    if getattr(args, "dry_run", False):
        argv.append("--dry-run")
    if getattr(args, "no_log_files", False):
        argv.append("--no-log-files")
    if getattr(args, "strip_comments", False):
        argv.append("--strip-comments")
    if getattr(args, "format_sql", False):
        argv.append("--format-sql")
    wp = (getattr(args, "write_processed", "") or "").strip()
    if wp:
        argv.extend(["--write-processed", wp])
    from scripts.sql.sql_runner import main as sql_main

    return sql_main(argv)


def cmd_sql_init_schema(args: argparse.Namespace) -> int:
    import tempfile

    from scripts.sql.psql_expand import expand_psql_includes
    from scripts.sql.sql_runner import SQLRunner

    init_path = DATABASE_DIR / "init_schema.sql"
    if not init_path.is_file():
        console.print(f"[red]Missing init script:[/red] {init_path}")
        return 2
    try:
        expanded = expand_psql_includes(init_path)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        return 2
    with tempfile.NamedTemporaryFile("w", suffix=".sql", delete=False, encoding="utf-8") as tf:
        tf.write(expanded)
        tmp = Path(tf.name)
    try:
        wp = (getattr(args, "write_processed", "") or "").strip()
        processed = Path(wp).expanduser() if wp else None
        runner = SQLRunner(
            tmp.resolve(),
            write_logs=not getattr(args, "no_log_files", False),
            dry_run=getattr(args, "dry_run", False),
            strip_comments=getattr(args, "strip_comments", False),
            format_sql=getattr(args, "format_sql", False),
            write_processed=processed,
        )
        return runner.run()
    finally:
        tmp.unlink(missing_ok=True)


def cmd_sql_load_csv(args: argparse.Namespace) -> int:
    from scripts.sql.csv_presets import get_preset, resolve_preset_csv
    from scripts.sql.csv_sql_loader import get_engine_from_config, load_csv_via_insert
    from scripts.sql.sql_paths import resolve_under_bases

    preset_name = (getattr(args, "preset", "") or "").strip()
    skip_leading = getattr(args, "skip_leading_column", False)
    table = (getattr(args, "table", "") or "").strip()
    csv_arg = (getattr(args, "csv", "") or "").strip()

    if preset_name:
        try:
            preset = get_preset(preset_name)
        except KeyError as exc:
            console.print(f"[red]{exc}[/red]")
            return 2
        try:
            csv_path = resolve_preset_csv(DATABASE_CSV_DIR, preset)
        except FileNotFoundError as exc:
            console.print(f"[red]{exc}[/red]")
            return 2
        table = table or preset.table
        skip_leading = skip_leading or preset.skip_leading_column
    else:
        if not csv_arg:
            console.print("[red]Provide --csv or --preset[/red]")
            return 2
        if not table:
            console.print("[red]--table is required without --preset[/red]")
            return 2
        bases = [Path.cwd(), DOCS_ROOT, SCRIPTS_ROOT, DATABASE_DIR, DATABASE_CSV_DIR]
        try:
            csv_path = resolve_under_bases(csv_arg, bases)
        except FileNotFoundError:
            console.print(f"[red]CSV not found:[/red] {csv_arg}")
            return 2

    cols = [c.strip() for c in args.columns.split(",") if c.strip()] if args.columns.strip() else None
    if getattr(args, "no_header", False) and not cols:
        console.print("[red]--no-header requires --columns[/red]")
        return 2
    try:
        engine = get_engine_from_config()
    except Exception as exc:
        console.print(f"[red]Database connection failed: {exc}[/red]")
        return 2
    try:
        n = load_csv_via_insert(
            engine,
            csv_path=csv_path,
            table=table,
            schema=args.schema,
            delimiter=args.delimiter,
            encoding=args.encoding,
            header=not args.no_header,
            columns=cols,
            skip_leading_column=skip_leading,
            batch_size=int(getattr(args, "batch_size", 200)),
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 2
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        return 2
    console.print(f"[green]Inserted {n} row(s) into {args.schema}.{table}.[/green]")
    return 0


def cmd_find_duplicate_files(args: argparse.Namespace) -> int:
    prefix = (getattr(args, "prefix", "") or "").strip()
    ext_raw = (getattr(args, "ext", "") or "").strip()
    extensions: frozenset[str] | None = None
    if ext_raw:
        extensions = frozenset(
            (p if p.startswith(".") else f".{p}")
            for x in ext_raw.split(",")
            if (p := x.strip().lower())
        )
    groups = find_duplicate_groups(prefix if prefix else None, extensions=extensions)
    if not groups:
        console.print("[green]No duplicate content groups found.[/green]")
        return 0
    for digest, paths in sorted(groups.items(), key=lambda x: (-len(x[1]), x[0])):
        console.print(f"[bold]{digest[:16]}…[/bold] ({len(paths)} files)")
        for p in paths:
            try:
                console.print(f"  - {p.relative_to(DOCS_ROOT)}")
            except ValueError:
                console.print(f"  - {p}")
    console.print(f"[bold]Total duplicate groups:[/bold] {len(groups)}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    from rich.table import Table

    from scripts.cli_catalog import EXTRA_CLI_COMMANDS, MENU_ENTRIES, STANDALONE_MAINTENANCE_SCRIPTS

    cat = (getattr(args, "category", None) or "all").lower()
    rows: list[dict] = []
    for e in MENU_ENTRIES:
        if cat != "all" and e.category != cat:
            continue
        rows.append(
            {
                "menu_id": e.menu_id,
                "section": e.section,
                "label": e.label,
                "risk": e.risk,
                "category": e.category,
                "cli": e.cli_equivalent,
            }
        )
    if getattr(args, "include_scripts", False):
        if cat in ("all", "scripts"):
            for script, desc in STANDALONE_MAINTENANCE_SCRIPTS:
                rows.append(
                    {
                        "menu_id": "",
                        "section": "scripts",
                        "label": desc,
                        "risk": "varies",
                        "category": "scripts",
                        "cli": f"python scripts/{script} (from docs/)",
                    }
                )
            for sec, cmd, desc in EXTRA_CLI_COMMANDS:
                rows.append(
                    {
                        "menu_id": "",
                        "section": sec,
                        "label": desc,
                        "risk": "read",
                        "category": "scripts",
                        "cli": f"python cli.py {cmd}",
                    }
                )

    if getattr(args, "json", False):
        print(json.dumps(rows, indent=2))
        return 0

    table = Table(title="Contact360 docs CLI catalog")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Section", max_width=36)
    table.add_column("Label", max_width=44)
    table.add_column("Risk")
    table.add_column("CLI", max_width=64)
    for r in rows:
        table.add_row(r["menu_id"], r["section"], r["label"], r["risk"], r["cli"])
    console.print(table)
    console.print("\n[dim]Full parser: `python cli.py -h`[/dim]")
    return 0


def cmd_data(args: argparse.Namespace) -> int:
    sub = getattr(args, "data_cmd", "")
    if sub == "analyze-company-names":
        if getattr(args, "dry_run", False):
            from scripts.config import get_default

            console.print(
                "[yellow]Dry-run:[/yellow] would query PostgreSQL at "
                f"{get_default('postgres.host')}:{get_default('postgres.port')}/"
                f"{get_default('postgres.database')} (set POSTGRES_* / config.json for a reachable DB)."
            )
            return 0
        from scripts.analysis.analyze_company_names import main as run_analyze

        return int(run_analyze())
    if sub == "comprehensive-analysis":
        if getattr(args, "dry_run", False):
            from scripts.config import get_default

            console.print(
                "[yellow]Dry-run:[/yellow] would query PostgreSQL at "
                f"{get_default('postgres.host')}:{get_default('postgres.port')}/"
                f"{get_default('postgres.database')} (set POSTGRES_* / config.json for a reachable DB)."
            )
            return 0
        from scripts.analysis.comprehensive_data_analysis import main as run_comp

        return int(run_comp())
    if sub == "clean-db":
        if getattr(args, "dry_run", False):
            bs = int(getattr(args, "batch_size", 1000))
            console.print(
                f"[yellow]Dry-run:[/yellow] would clean companies, companies_metadata, contacts, "
                f"contacts_metadata (batch_size={bs}). Omit --dry-run to execute."
            )
            return 0
        from scripts.cleaning.clean_database import main as run_clean

        return int(run_clean())
    if sub == "ingest-local":
        from scripts import data_repl

        data_repl.main()
        return 0
    return 2


def _rel_json_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(DOCS_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _structure_rule_id(kind: object, severity: str, message: str) -> str:
    kv = getattr(kind, "value", str(kind))
    slug = (message or "ISSUE")[:40].replace(" ", "_").replace("/", "_")
    return f"STRUCTURE_{kv}_{severity}_{slug}".upper()


def cmd_validate_all(args: argparse.Namespace) -> int:
    from scripts.doc_structure import DocKind, iter_paths_for_validation, validate_file
    from scripts.era_naming import find_naming_issues, scan_era_filenames
    from scripts.task_auditor import audit_era

    include_tasks = not bool(getattr(args, "skip_tasks", False))
    include_naming = not bool(getattr(args, "skip_naming", False))
    write_latest = bool(getattr(args, "write_latest", False))

    started = datetime.now(timezone.utc).isoformat()
    invocation = {
        "argv": sys.argv[1:],
        "write_latest": write_latest,
        "include_tasks": include_tasks,
        "include_naming": include_naming,
    }

    findings: list[dict] = []
    path_seen: set[str] = set()

    def consume_paths(paths: list[Path]) -> None:
        for p in paths:
            key = str(p.resolve())
            if key in path_seen:
                continue
            path_seen.add(key)
            for f in validate_file(p):
                findings.append(
                    {
                        "path": _rel_json_path(f.path),
                        "kind": f.kind.value if hasattr(f.kind, "value") else str(f.kind),
                        "severity": f.severity,
                        "rule_id": _structure_rule_id(f.kind, f.severity, f.message),
                        "message": f.message,
                        "line": f.line,
                    }
                )

    consume_paths(iter_paths_for_validation(kind_filter=DocKind.HUB))
    for ei in range(len(ERA_FOLDERS)):
        consume_paths(iter_paths_for_validation(era_index=ei, kind_filter=DocKind.ERA_TASK))
    consume_paths(iter_paths_for_validation(prefix="frontend/pages", kind_filter=DocKind.FRONTEND_PAGE))

    files_scanned = len(path_seen)

    if include_tasks:
        for ei in range(len(ERA_FOLDERS)):
            try:
                results = audit_era(ei)
            except ValueError:
                continue
            for r in results:
                rel = _rel_json_path(r.path)
                if r.empty_task_section:
                    findings.append(
                        {
                            "path": rel,
                            "kind": "era_task",
                            "severity": "error",
                            "rule_id": "TASK_NO_SECTION",
                            "message": "Missing ## Tasks or ## Task tracks",
                            "line": None,
                        }
                    )
                for mt in r.missing_tracks:
                    findings.append(
                        {
                            "path": rel,
                            "kind": "era_task",
                            "severity": "error",
                            "rule_id": f"TASK_MISSING_{mt.upper().replace(' ', '_')}",
                            "message": f"Missing or empty track: {mt}",
                            "line": None,
                        }
                    )
                for dup in r.duplicate_items[:50]:
                    findings.append(
                        {
                            "path": rel,
                            "kind": "era_task",
                            "severity": "warning",
                            "rule_id": "TASK_DUPLICATE_BULLET",
                            "message": dup[:800],
                            "line": None,
                        }
                    )

    if include_naming:
        records = scan_era_filenames(None)
        for issue in find_naming_issues(records):
            sev = issue.severity
            if issue.paths:
                for p in issue.paths:
                    findings.append(
                        {
                            "path": _rel_json_path(p),
                            "kind": "era_naming",
                            "severity": sev,
                            "rule_id": f"NAME_{issue.code}",
                            "message": issue.message,
                            "line": None,
                        }
                    )
            else:
                findings.append(
                    {
                        "path": "",
                        "kind": "era_naming",
                        "severity": sev,
                        "rule_id": f"NAME_{issue.code}",
                        "message": issue.message,
                        "line": None,
                    }
                )

    err_n = sum(1 for x in findings if x["severity"] == "error")
    warn_n = sum(1 for x in findings if x["severity"] == "warning")
    finished = datetime.now(timezone.utc).isoformat()
    payload: dict = {
        "schema_version": 1,
        "tool": "contact360-docs-validate",
        "started_at": started,
        "finished_at": finished,
        "docs_root": str(DOCS_ROOT.resolve()),
        "invocation": invocation,
        "summary": {
            "files_scanned": files_scanned,
            "errors": err_n,
            "warnings": warn_n,
            "total_findings": len(findings),
        },
        "findings": findings,
    }
    errors_only = [f for f in findings if f["severity"] == "error"]

    if not write_latest:
        console.print(
            f"[bold]Validate-all[/bold] (no write): files_scanned={files_scanned} "
            f"errors={err_n} warnings={warn_n}"
        )
        if err_n:
            for f in findings:
                if f["severity"] == "error":
                    console.print(f"  [red]{f.get('path','')}[/red] {f['rule_id']}: {f['message']}")
        return 1 if err_n else 0

    DOCS_RESULT_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_ERRORS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_path = DOCS_RESULT_DIR / f"validation-{stamp}.json"
    err_path = DOCS_ERRORS_DIR / f"validation-{stamp}.json"
    result_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    err_payload = {
        **{k: v for k, v in payload.items() if k not in ("findings", "summary")},
        "summary": {
            "files_scanned": files_scanned,
            "errors": len(errors_only),
            "warnings": 0,
            "total_findings": len(errors_only),
        },
        "findings": errors_only,
    }
    err_path.write_text(json.dumps(err_payload, indent=2), encoding="utf-8")
    (DOCS_RESULT_DIR / "latest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (DOCS_ERRORS_DIR / "latest.json").write_text(json.dumps(err_payload, indent=2), encoding="utf-8")
    try:
        console.print(
            f"[green]Wrote[/green] {result_path.relative_to(DOCS_ROOT)} , "
            f"{err_path.relative_to(DOCS_ROOT)} , latest.json (both dirs)"
        )
    except ValueError:
        console.print(f"[green]Wrote[/green] {result_path} , {err_path}")
    return 1 if err_n else 0


def main() -> int:
    """Main entrypoint for the CLI script."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        return cmd_scan()
    if args.command == "stats":
        return cmd_stats(args.era)
    if args.command == "update":
        return cmd_update(args)
    if args.command == "find-unused":
        return cmd_find_unused()
    if args.command == "normalize":
        return cmd_normalize(args.status, args.dry_run)
    if args.command == "audit-tasks":
        return cmd_audit_tasks(getattr(args, "era", None))
    if args.command == "fill-tasks":
        return cmd_fill_tasks(args)
    if args.command == "dedup-tasks":
        return cmd_dedup_tasks(args)
    if args.command == "task-report":
        return cmd_task_report(getattr(args, "era", None))
    if args.command == "name-audit":
        return cmd_name_audit(getattr(args, "era", None))
    if args.command == "rename-docs":
        return cmd_rename_docs(args)
    if args.command == "era-guide":
        return cmd_era_guide(getattr(args, "era", None), getattr(args, "json", False))
    if args.command == "validate-structure":
        return cmd_validate_structure(args)
    if args.command == "format-structure":
        return cmd_format_structure(args)
    if args.command == "format-all":
        return cmd_format_all(args)
    if args.command == "optimize-docs":
        if args.optimize_cmd == "report":
            return cmd_optimize_report()
        if args.optimize_cmd == "fix-structure":
            return cmd_optimize_fix_structure(args)
        return 2
    if args.command == "maintain-era":
        return cmd_maintain_era_cli(args)
    if args.command == "docs-gen":
        if args.docs_gen_cmd == "create-patches":
            return cmd_docs_gen_create_patches(args)
        if args.docs_gen_cmd == "flowcharts":
            return cmd_docs_gen_flowcharts(args)
        return 2
    if args.command == "frontend":
        if args.frontend_cmd == "link-endpoint-specs":
            return cmd_frontend_link()
        if args.frontend_cmd == "augment-page-specs":
            return cmd_frontend_augment(args)
        return 2
    if args.command == "prune-unused":
        return cmd_prune_unused(args)
    if args.command == "find-duplicate-files":
        return cmd_find_duplicate_files(args)
    if args.command == "api-test":
        if args.api_test_cmd == "show-env":
            return cmd_api_test_show_env(args)
        if args.api_test_cmd == "discover":
            return cmd_api_test_subprocess(args, "endpoint_discovery.py")
        if args.api_test_cmd == "document":
            return cmd_api_test_subprocess(args, "endpoint_documenter.py")
        if args.api_test_cmd == "email-single":
            return cmd_api_test_subprocess(args, "email_single.py")
        if args.api_test_cmd == "login":
            return cmd_api_test_subprocess(args, "api_token.py")
        if args.api_test_cmd == "pattern-generator":
            fwd = [x for x in getattr(args, "pattern_generator_args", []) if x]
            return cmd_api_test_subprocess(args, "email_pattern_generator.py", forwarded=fwd)
        return 2
    if args.command == "sql":
        if args.sql_cmd == "run":
            return cmd_sql_run(args)
        if args.sql_cmd == "init-schema":
            return cmd_sql_init_schema(args)
        if args.sql_cmd == "load-csv":
            return cmd_sql_load_csv(args)
        return 2
    if args.command == "list":
        return cmd_list(args)
    if args.command == "validate-all":
        return cmd_validate_all(args)
    if args.command == "data":
        return cmd_data(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
