"""CLI tool to manage documentation status and tracking."""
from __future__ import annotations

import argparse
import sys
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
from scripts.unused import find_unused_files

console = Console()


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
    docs_root = Path(__file__).resolve().parent
    for path in unused:
        try:
            rel_path = path.relative_to(docs_root)
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
    docs_root = Path(__file__).resolve().parent
    reg = load_registry()
    try:
        if args.file:
            fp = Path(args.file)
            paths = [fp if fp.is_absolute() else (docs_root / fp)]
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
    docs_root = Path(__file__).resolve().parent
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
        for path in sorted((docs_root / era_name).glob("*.md")):
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
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
