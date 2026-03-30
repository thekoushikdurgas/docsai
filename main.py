"""Interactive Contact360 Docs Agent menu (mirrors docs/cli.py)."""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

_DOCS_DIR = Path(__file__).resolve().parent
if str(_DOCS_DIR) not in sys.path:
    sys.path.insert(0, str(_DOCS_DIR))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
import cli as cli_mod

from scripts.models import Status
from scripts.paths import DEFAULT_CONTACT360_POSTMAN_ENV, DOCS_ROOT
from scripts.codebase_registry import load_registry
from scripts.scanner import ERA_FOLDERS, scan_all, scan_era_only
from scripts.contact360_era_guide import get_era_guide_entries, get_era_guide_entry
from scripts.stats import (
    era_guide_detail_panel,
    era_guide_summary_table,
    era_summary,
    file_detail,
    overall_dashboard,
    naming_inventory_table,
    naming_issues_table,
    task_audit_table,
)
from scripts.era_naming import apply_renames, find_naming_issues, plan_renames, scan_era_filenames
from scripts.task_auditor import audit_all, audit_era, find_duplicate_tasks
from scripts.task_filler import bulk_fill, deduplicate_file_tasks
from scripts.updater import bulk_update, list_scope_paths
from scripts.unused import find_unused_files
from scripts.cli_catalog import MENU_ENTRIES

console = Console()

DOCS_AGENT_VERSION = "1.2.0"


def _status_from_input(value: str) -> Status:
    try:
        return Status.from_cli(value)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise


def _hint(equivalent: str) -> None:
    console.print(f"[dim]Equivalent CLI:[/dim] [cyan]{equivalent}[/cyan]")


@dataclass(frozen=True, slots=True)
class MenuEntry:
    id: str
    section: str
    label: str
    risk: str  # read | write
    handler: Callable[[], None]
    cli_equivalent: str


def show_dashboard() -> None:
    cli_mod.cmd_scan()
    _hint("python cli.py scan")


def browse_by_era() -> None:
    scan_result = scan_all()
    for idx, name in enumerate(ERA_FOLDERS):
        console.print(f"{idx}. {name}")
    selected = Prompt.ask("Select era number", default="0")
    if not selected.isdigit():
        console.print("[red]Invalid era selection[/red]")
        return
    era_idx = int(selected)
    if era_idx < 0 or era_idx >= len(ERA_FOLDERS):
        console.print("[red]Era index out of range[/red]")
        return
    era_name = ERA_FOLDERS[era_idx]
    console.print(file_detail(scan_result, era_name))
    _hint(f"python cli.py stats --era {era_idx}")


def run_bulk_update() -> None:
    scope = Prompt.ask("Scope", choices=["file", "era", "all"], default="era")
    era_idx: int | None = None
    file_path: str | None = None
    if scope == "era":
        era_idx = int(Prompt.ask("Era number (0-10)", default="0"))
    elif scope == "file":
        file_path = Prompt.ask("Markdown file path")
    status_raw = Prompt.ask(
        "Target status",
        choices=["completed", "in_progress", "planned", "incomplete"],
        default="completed",
    )
    status = _status_from_input(status_raw)
    update_tasks = Confirm.ask("Update task bullet prefixes too?", default=True)
    try:
        paths = list_scope_paths(scope=scope, era=era_idx, file_path=file_path)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return
    preview = bulk_update(paths, status, update_tasks=update_tasks, dry_run=True)
    console.print(
        f"Dry run -> files: {preview['files']}, changed: {preview['changed']}, diff_lines: {preview['diff_lines']}"
    )
    if not Confirm.ask("Apply changes?", default=False):
        _hint("python cli.py update --status <s> --era N --dry-run")
        return
    summary = bulk_update(paths, status, update_tasks=update_tasks, dry_run=False)
    console.print(
        f"[green]Applied[/green] -> files: {summary['files']}, changed: {summary['changed']}, "
        f"diff_lines: {summary['diff_lines']}"
    )
    _hint("python cli.py update --status <s> --era N")


def normalize_all() -> None:
    status_raw = Prompt.ask(
        "Normalize all files to status",
        choices=["completed", "in_progress", "planned", "incomplete"],
        default="completed",
    )
    status = _status_from_input(status_raw)
    paths = list_scope_paths(scope="all")
    preview = bulk_update(paths, status, update_tasks=True, dry_run=True)
    console.print(
        f"Dry run -> files: {preview['files']}, changed: {preview['changed']}, diff_lines: {preview['diff_lines']}"
    )
    if not Confirm.ask("Apply normalize-all?", default=False):
        _hint("python cli.py normalize --status <s> --dry-run")
        return
    summary = bulk_update(paths, status, update_tasks=True, dry_run=False)
    console.print(
        f"[green]Normalized[/green] -> files: {summary['files']}, changed: {summary['changed']}, "
        f"diff_lines: {summary['diff_lines']}"
    )
    _hint("python cli.py normalize --status <s>")


def run_task_audit_menu() -> None:
    for idx, name in enumerate(ERA_FOLDERS):
        console.print(f"{idx}. {name}")
    scope = Prompt.ask("Era number (0-10) or 'all'", default="0")
    if scope.lower() == "all":
        cli_mod.cmd_audit_tasks(None)
        _hint("python cli.py audit-tasks")
        return
    if not scope.isdigit():
        console.print("[red]Invalid selection[/red]")
        return
    ei = int(scope)
    if ei < 0 or ei >= len(ERA_FOLDERS):
        console.print("[red]Out of range[/red]")
        return
    cli_mod.cmd_audit_tasks(ei)
    _hint(f"python cli.py audit-tasks --era {ei}")


def run_fill_tasks_menu() -> None:
    reg = load_registry()
    scope = Prompt.ask("Scope", choices=["era", "file", "all"], default="era")
    paths: list[Path]
    if scope == "file":
        fp = Prompt.ask("Markdown path under docs/")
        paths = [Path(fp) if Path(fp).is_absolute() else DOCS_ROOT / fp]
    elif scope == "era":
        ei = int(Prompt.ask("Era number (0-10)", default="0"))
        try:
            paths = list_scope_paths(scope="era", era=ei)
        except ValueError as exc:
            console.print(f"[red]{exc}[/red]")
            return
    else:
        paths = list_scope_paths(scope="all")
    apply_changes = Confirm.ask("Apply writes to disk? (No = dry run)", default=False)
    summary = bulk_fill(paths, registry=reg, dry_run=not apply_changes, dedup=False)
    label = "Applied" if apply_changes else "Dry run"
    console.print(
        f"[green]{label}[/green] -> files: {summary['files']}, changed: {summary['changed']}, "
        f"diff_lines: {summary['diff_lines']}"
    )
    _hint("python cli.py fill-tasks --era N [--apply]")


def run_dedup_tasks_menu() -> None:
    reg = load_registry()
    all_eras = Confirm.ask("Run on ALL eras?", default=False)
    if all_eras:
        era_indices = range(len(ERA_FOLDERS))
    else:
        ei = int(Prompt.ask("Era number (0-10)", default="0"))
        if ei < 0 or ei >= len(ERA_FOLDERS):
            console.print("[red]Era out of range[/red]")
            return
        era_indices = [ei]
    apply_changes = Confirm.ask("Apply writes to disk?", default=False)
    dry_run = not apply_changes
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
    label = "Applied" if apply_changes else "Dry run"
    console.print(f"[green]{label}[/green] -> files changed: {changed}, diff_lines (sum): {diff_lines}")
    _hint("python cli.py dedup-tasks --era N [--apply|--all]")


def run_name_audit_menu() -> None:
    scope = Prompt.ask("Era 0-10 or type 'all' for every folder", default="0")
    if scope.lower() == "all":
        ei: int | None = None
    else:
        if not scope.isdigit():
            console.print("[red]Invalid era[/red]")
            return
        ei = int(scope)
        if ei < 0 or ei >= len(ERA_FOLDERS):
            console.print("[red]Out of range[/red]")
            return
    records = scan_era_filenames(ei)
    issues = find_naming_issues(records)
    console.print(naming_inventory_table(records))
    if issues:
        console.print(naming_issues_table(issues))
        for issue in issues:
            if issue.code == "DUPLICATE_VERSION" and issue.paths:
                console.print(f"[red]Duplicate version key[/red]: {issue.detail}")
                for p in issue.paths[:15]:
                    console.print(f"  - {p.name}")
    else:
        console.print("[green]No naming issues.[/green]")
    _hint("python cli.py name-audit [--era N]")


def run_era_guide_menu() -> None:
    scope = Prompt.ask("All eras (a) or era number 0-10", default="a")
    if scope.lower() == "a":
        console.print(era_guide_summary_table(get_era_guide_entries()))
        _hint("python cli.py era-guide")
        return
    if not scope.isdigit():
        console.print("[red]Invalid era[/red]")
        return
    ei = int(scope)
    entry = get_era_guide_entry(ei)
    if entry is None:
        console.print("[red]Era out of range (use 0-10)[/red]")
        return
    console.print(era_guide_detail_panel(entry))
    _hint(f"python cli.py era-guide --era {ei}")


def run_rename_docs_menu() -> None:
    all_eras = Confirm.ask("Process ALL era folders?", default=False)
    ei: int | None = None if all_eras else int(Prompt.ask("Era number (0-10)", default="0"))
    if ei is not None and (ei < 0 or ei >= len(ERA_FOLDERS)):
        console.print("[red]Era out of range[/red]")
        return
    records = scan_era_filenames(ei)
    pairs = plan_renames(records)
    if not pairs:
        console.print("[green]Nothing to rename (already canonical or no versioned files).[/green]")
        return
    for old, new, reason in pairs:
        if reason == "SKIP_TARGET_EXISTS":
            console.print(f"[yellow]Skip[/yellow] (exists): {old.name} -> {new.name}")
        else:
            console.print(f"Would rename: {old.name} -> {new.name}")
    apply_changes = Confirm.ask("Apply these renames?", default=False)
    summary = apply_renames(pairs, dry_run=not apply_changes)
    lbl = "Dry run" if not apply_changes else "Applied"
    console.print(
        f"[bold]{lbl}[/bold]: planned={summary['planned']}, renamed={summary['renamed']}, "
        f"skipped={summary['skipped']}, errors={summary['errors']}"
    )
    _hint("python cli.py rename-docs --era N [--apply]")


def run_find_unused() -> None:
    cli_mod.cmd_find_unused()
    _hint("python cli.py find-unused")


def run_task_report_menu() -> None:
    scope = Prompt.ask("Era 0-10 or 'all'", default="all")
    if scope.lower() == "all":
        cli_mod.cmd_task_report(None)
        _hint("python cli.py task-report")
        return
    ei = int(scope)
    cli_mod.cmd_task_report(ei)
    _hint(f"python cli.py task-report --era {ei}")


def run_stats_menu() -> None:
    scope = Prompt.ask("Era 0-10 or Enter for full dashboard", default="")
    if not scope.strip():
        cli_mod.cmd_stats(None)
        _hint("python cli.py stats")
        return
    ei = int(scope)
    cli_mod.cmd_stats(ei)
    _hint(f"python cli.py stats --era {ei}")


def run_validate_structure_menu() -> None:
    prefix = Prompt.ask("Prefix under docs/ (blank = policy hub docs/docs)", default="docs/docs")
    era_raw = Prompt.ask("Era 0-10 only (blank to skip)", default="")
    ns = argparse.Namespace(
        prefix=prefix.strip(),
        kind="",
        era=int(era_raw) if era_raw.strip().isdigit() else None,
    )
    cli_mod.cmd_validate_structure(ns)
    _hint("python cli.py validate-structure [--prefix …] [--era N]")


def run_validate_all_json_menu() -> None:
    write = Confirm.ask("Write docs/result/latest.json and docs/errors/latest.json?", default=False)
    ns = argparse.Namespace(
        write_latest=write,
        skip_tasks=False,
        skip_naming=False,
    )
    rc = cli_mod.cmd_validate_all(ns)
    if rc != 0:
        console.print(f"[yellow]Exit code {rc} (see errors JSON if written)[/yellow]")
    _hint("python cli.py validate-all --write-latest [--skip-tasks] [--skip-naming]")


def _run_validate_structure_kind(kind: str, hint: str) -> None:
    """Run validate-structure for a fixed DocKind (backend_api, endpoint_md, codebase_analysis)."""
    ns = argparse.Namespace(prefix="", kind=kind, era=None)
    rc = cli_mod.cmd_validate_structure(ns)
    if rc != 0:
        console.print(f"[yellow]Exit code {rc} (structure errors)[/yellow]")
    _hint(hint)


def run_validate_backend_api_structure_menu() -> None:
    _run_validate_structure_kind(
        "backend_api",
        "python cli.py validate-structure --kind backend_api",
    )


def run_validate_endpoint_md_structure_menu() -> None:
    _run_validate_structure_kind(
        "endpoint_md",
        "python cli.py validate-structure --kind endpoint_md",
    )


def run_validate_codebase_structure_menu() -> None:
    _run_validate_structure_kind(
        "codebase_analysis",
        "python cli.py validate-structure --kind codebase_analysis",
    )


def run_format_structure_menu() -> None:
    """Same prompts as validate-structure; optional --apply after dry-run preview."""
    prefix = Prompt.ask("Prefix under docs/ (blank = policy hub docs/docs)", default="docs/docs")
    era_raw = Prompt.ask("Era 0-10 only (blank to skip)", default="")
    kind_raw = Prompt.ask(
        "Kind: blank default, or hub | era_task | frontend_page | backend_api | endpoint_md | codebase_analysis",
        default="",
    ).strip()
    apply = Confirm.ask("Write formatted files (--apply)? Default is dry-run only.", default=False)
    ns = argparse.Namespace(
        prefix=prefix.strip(),
        kind=kind_raw,
        era=int(era_raw) if era_raw.strip().isdigit() else None,
        apply=apply,
    )
    rc = cli_mod.cmd_format_structure(ns)
    if rc != 0:
        console.print(f"[yellow]Exit code {rc}[/yellow]")
    _hint("python cli.py format-structure [--prefix …] [--era N] [--kind …] [--apply]")


def run_format_all_menu() -> None:
    include_prose = Confirm.ask(
        "Also format backend/apis, backend/endpoints *.md, codebases/ (--include-prose)?",
        default=False,
    )
    apply = Confirm.ask("Write formatted files (--apply)?", default=False)
    write_latest = Confirm.ask("Write docs/result/format-latest.json (--write-latest)?", default=False)
    ns = argparse.Namespace(apply=apply, include_prose=include_prose, write_latest=write_latest)
    rc = cli_mod.cmd_format_all(ns)
    if rc != 0:
        console.print(f"[yellow]Exit code {rc}[/yellow]")
    _hint("python cli.py format-all [--apply] [--include-prose] [--write-latest]")


def run_optimize_report_menu() -> None:
    cli_mod.cmd_optimize_report()
    _hint("python cli.py optimize-docs report")


def run_optimize_fix_menu() -> None:
    cli_mod.cmd_optimize_fix_structure(argparse.Namespace(apply=False, era=None))
    if Confirm.ask("Apply full chain (--apply)?", default=False):
        cli_mod.cmd_optimize_fix_structure(argparse.Namespace(apply=True, era=None))
    _hint("python cli.py optimize-docs fix-structure [--apply]")


def run_optimize_combined_menu() -> None:
    pick = Prompt.ask("1=report  2=fix-structure", choices=["1", "2"], default="1")
    if pick == "1":
        run_optimize_report_menu()
    else:
        run_optimize_fix_menu()


def run_find_duplicates_menu() -> None:
    prefix = Prompt.ask("Prefix under docs/ (blank = all docs)", default="")
    if not prefix.strip():
        console.print(
            "[dim]Scanning entire docs/ can take several minutes; "
            "try [cyan]docs/docs[/cyan] or [cyan]frontend/pages[/cyan] for a quicker pass.[/dim]"
        )
    ns = argparse.Namespace(prefix=prefix.strip(), ext="")
    cli_mod.cmd_find_duplicate_files(ns)
    _hint("python cli.py find-duplicate-files [--prefix …]")


def run_prune_unused_menu() -> None:
    ns = argparse.Namespace(apply=False, quarantine="", include_era_patches=False)
    cli_mod.cmd_prune_unused(ns)
    if Confirm.ask("Quarantine listed files (--apply)?", default=False):
        cli_mod.cmd_prune_unused(
            argparse.Namespace(apply=True, quarantine="", include_era_patches=False)
        )
    _hint("python cli.py prune-unused [--apply] [--quarantine …]")


def run_maintain_era_menu() -> None:
    ei = int(Prompt.ask("Era 0-10", default="0"))
    action = Prompt.ask(
        "Action",
        choices=["enrich", "fix-readme-links", "update-minors"],
        default="enrich",
    )
    apply_writes = Confirm.ask("Apply (run scripts for real)?", default=False)
    ns = argparse.Namespace(era=ei, all=False, action=action, apply=apply_writes, dry_run=False)
    cli_mod.cmd_maintain_era_cli(ns)
    _hint(f'python cli.py maintain-era --era {ei} --action {action} {"--apply" if apply_writes else "--dry-run"}')


def run_docs_gen_menu() -> None:
    sub = Prompt.ask("docs-gen", choices=["create-patches", "flowcharts"], default="create-patches")
    if sub == "flowcharts":
        apply = Confirm.ask("Apply flowchart rewrite?", default=False)
        cli_mod.cmd_docs_gen_flowcharts(argparse.Namespace(apply=apply))
        _hint("python cli.py docs-gen flowcharts [--apply]")
        return
    eras = Prompt.ask("Eras (comma-separated, blank=all)", default="")
    apply = Confirm.ask("Apply writes?", default=False)
    cli_mod.cmd_docs_gen_create_patches(
        argparse.Namespace(eras=eras, apply=apply, dry_run=not apply, report_json="")
    )
    _hint("python cli.py docs-gen create-patches [--eras …] [--apply]")


def run_api_test_menu() -> None:
    console.print(
        "API helpers under [bold]scripts/api_test[/bold]: optional Postman env maps "
        "[dim]baseUrl → API_BASE_URL, email/password → TEST_USER_*[/dim]."
    )
    if DEFAULT_CONTACT360_POSTMAN_ENV.is_file():
        try:
            default_p = str(DEFAULT_CONTACT360_POSTMAN_ENV.relative_to(DOCS_ROOT))
        except ValueError:
            default_p = str(DEFAULT_CONTACT360_POSTMAN_ENV)
    else:
        default_p = ""
    raw = Prompt.ask(
        "--postman-env (path under docs/, or filename in backend/postman; empty = OS env only, show-env uses local default file if present)",
        default=default_p,
    ).strip()
    sub = Prompt.ask(
        "Command",
        choices=["show-env", "discover", "document", "email-single", "login", "cancel"],
        default="show-env",
    )
    if sub == "cancel":
        _hint('python cli.py api-test show-env  (with file: api-test --postman-env "backend/postman/....json" show-env)')
        return
    override = Confirm.ask("Override existing environment variables from Postman?", default=False)
    ns = argparse.Namespace(postman_env=raw, override_env=override, pattern_generator_args=[])
    if sub == "show-env":
        rc = cli_mod.cmd_api_test_show_env(ns)
    elif sub == "discover":
        rc = cli_mod.cmd_api_test_subprocess(ns, "endpoint_discovery.py")
    elif sub == "document":
        rc = cli_mod.cmd_api_test_subprocess(ns, "endpoint_documenter.py")
    elif sub == "email-single":
        rc = cli_mod.cmd_api_test_subprocess(ns, "email_single.py")
    else:
        rc = cli_mod.cmd_api_test_subprocess(ns, "api_token.py")
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint(f'python cli.py api-test --postman-env "<path>" {sub}  (--postman-env must come before the subcommand)')


def run_frontend_menu() -> None:
    sub = Prompt.ask("frontend", choices=["link-endpoint-specs", "augment-page-specs"], default="link-endpoint-specs")
    if sub == "link-endpoint-specs":
        cli_mod.cmd_frontend_link()
        _hint("python cli.py frontend link-endpoint-specs")
        return
    dry = Confirm.ask("Dry-run only (count files)?", default=True)
    if dry:
        cli_mod.cmd_frontend_augment(argparse.Namespace(apply=False, dry_run=True))
    elif Confirm.ask("Apply augment to *_page.md?", default=False):
        cli_mod.cmd_frontend_augment(argparse.Namespace(apply=True, dry_run=False))
    _hint("python cli.py frontend augment-page-specs [--dry-run|--apply]")


def run_data_analyze_company_names() -> None:
    dry = Confirm.ask("Dry-run only (print DB target, no query)?", default=True)
    ns = argparse.Namespace(data_cmd="analyze-company-names", dry_run=dry)
    rc = cli_mod.cmd_data(ns)
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint("python cli.py data analyze-company-names [--dry-run]")


def run_data_comprehensive_analysis() -> None:
    dry = Confirm.ask("Dry-run only (print DB target, no query)?", default=True)
    ns = argparse.Namespace(data_cmd="comprehensive-analysis", dry_run=dry)
    rc = cli_mod.cmd_data(ns)
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint("python cli.py data comprehensive-analysis [--dry-run]")


def run_data_clean_db() -> None:
    dry = Confirm.ask("Dry-run only (no DB writes)?", default=True)
    if not dry and not Confirm.ask("This WRITES to the database. Continue?", default=False):
        _hint("python cli.py data clean-db --dry-run")
        return
    ns = argparse.Namespace(data_cmd="clean-db", dry_run=dry, batch_size=1000)
    rc = cli_mod.cmd_data(ns)
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint("python cli.py data clean-db [--dry-run]")


def run_data_ingest_local() -> None:
    from scripts import data_repl

    data_repl.main()
    _hint("python cli.py data ingest-local")


def run_sql_menu() -> None:
    sub = Prompt.ask(
        "sql",
        choices=["run", "init-schema", "load-csv", "cancel"],
        default="run",
    )
    if sub == "cancel":
        _hint("python cli.py sql run")
        return
    if sub == "run":
        f = Prompt.ask("SQL file path (blank = default sqlline.sql)", default="").strip()
        ns = argparse.Namespace(
            file=f,
            dry_run=False,
            no_log_files=False,
            strip_comments=False,
            format_sql=False,
            write_processed="",
        )
        rc = cli_mod.cmd_sql_run(ns)
    elif sub == "init-schema":
        ns = argparse.Namespace(
            dry_run=False,
            no_log_files=False,
            strip_comments=False,
            format_sql=False,
            write_processed="",
        )
        rc = cli_mod.cmd_sql_init_schema(ns)
    else:
        preset = Prompt.ask("Preset name (or blank for manual --csv + --table)", default="").strip()
        ns = argparse.Namespace(
            preset=preset,
            csv="",
            table="",
            schema="public",
            delimiter=",",
            encoding="utf-8",
            no_header=False,
            columns="",
            skip_leading_column=False,
            batch_size=200,
        )
        rc = cli_mod.cmd_sql_load_csv(ns)
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint("python cli.py sql run|init-schema|load-csv …")


def run_api_discover_quick() -> None:
    raw = Prompt.ask("Postman env path (blank = default)", default="").strip()
    ns = argparse.Namespace(postman_env=raw, override_env=False, pattern_generator_args=[])
    rc = cli_mod.cmd_api_test_subprocess(ns, "endpoint_discovery.py")
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint('python cli.py api-test --postman-env "<path>" discover')


def run_api_document_quick() -> None:
    raw = Prompt.ask("Postman env path (blank = default)", default="").strip()
    ns = argparse.Namespace(postman_env=raw, override_env=False, pattern_generator_args=[])
    rc = cli_mod.cmd_api_test_subprocess(ns, "endpoint_documenter.py")
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint('python cli.py api-test --postman-env "<path>" document')


def run_api_login_quick() -> None:
    raw = Prompt.ask("Postman env path (blank = default)", default="").strip()
    ns = argparse.Namespace(postman_env=raw, override_env=False, pattern_generator_args=[])
    rc = cli_mod.cmd_api_test_subprocess(ns, "api_token.py")
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint('python cli.py api-test --postman-env "<path>" login')


def run_api_email_single_quick() -> None:
    raw = Prompt.ask("Postman env path (blank = default)", default="").strip()
    ns = argparse.Namespace(postman_env=raw, override_env=False, pattern_generator_args=[])
    rc = cli_mod.cmd_api_test_subprocess(ns, "email_single.py")
    if rc != 0:
        console.print(f"[red]Exit code {rc}[/red]")
    _hint('python cli.py api-test --postman-env "<path>" email-single')


def run_list_catalog_menu() -> None:
    ns = argparse.Namespace(json=False, category="all", include_scripts=False)
    cli_mod.cmd_list(ns)
    _hint("python cli.py list [--json] [--category docs|data|api|scripts|all]")


HANDLERS: dict[str, Callable[[], None]] = {
    "A1": show_dashboard,
    "A2": browse_by_era,
    "A3": run_era_guide_menu,
    "A4": run_task_report_menu,
    "A5": run_stats_menu,
    "B1": run_task_audit_menu,
    "B2": run_name_audit_menu,
    "B3": run_validate_structure_menu,
    "B4": run_find_unused,
    "B5": run_find_duplicates_menu,
    "B6": run_validate_all_json_menu,
    "B7": run_validate_backend_api_structure_menu,
    "B8": run_validate_endpoint_md_structure_menu,
    "B9": run_validate_codebase_structure_menu,
    "B10": run_format_structure_menu,
    "B11": run_format_all_menu,
    "C1": run_fill_tasks_menu,
    "C2": run_dedup_tasks_menu,
    "C3": run_rename_docs_menu,
    "C4": run_optimize_combined_menu,
    "D1": run_bulk_update,
    "D2": normalize_all,
    "E1": run_maintain_era_menu,
    "E2": run_docs_gen_menu,
    "E3": run_frontend_menu,
    "E4": run_prune_unused_menu,
    "E5": run_api_test_menu,
    "F1": run_data_analyze_company_names,
    "F2": run_data_comprehensive_analysis,
    "F3": run_data_clean_db,
    "F4": run_data_ingest_local,
    "F5": run_sql_menu,
    "G1": run_api_discover_quick,
    "G2": run_api_document_quick,
    "G3": run_api_login_quick,
    "G4": run_api_email_single_quick,
    "G5": run_list_catalog_menu,
}


def build_menu() -> list[MenuEntry]:
    out: list[MenuEntry] = []
    for e in MENU_ENTRIES:
        h = HANDLERS.get(e.menu_id)
        if h is None:
            continue
        out.append(
            MenuEntry(
                id=e.menu_id,
                section=e.section,
                label=e.label,
                risk=e.risk,
                handler=h,
                cli_equivalent=e.cli_equivalent,
            )
        )
    return out


def print_command_catalog_help() -> None:
    console.print(
        "\n[bold]CLI quick reference[/bold] (from [cyan]docs/[/cyan]): run [cyan]python cli.py list[/cyan] for full table.\n"
        "  Docs: scan, stats, audit-tasks, validate-structure (B7–B9), format-structure (B10) / format-all (B11), …\n"
        "  Data: [cyan]python cli.py data analyze-company-names[/cyan] | comprehensive-analysis | clean-db | ingest-local\n"
        "  SQL:  [cyan]python cli.py sql run[/cyan] | init-schema | load-csv\n"
        "  API:  [cyan]python scripts/api_cli.py test run[/cyan] (Typer API CLI from [cyan]docs/scripts/[/cyan])\n"
    )


def run_list_inline() -> None:
    cli_mod.cmd_list(argparse.Namespace(json=False, category="all", include_scripts=False))


def run_menu() -> None:
    entries = build_menu()
    by_id = {e.id: e for e in entries}
    header = (
        f"[bold]Contact360 Docs Agent[/bold]  v{DOCS_AGENT_VERSION}  [dim](run from docs/)[/dim]\n"
        "[dim]A=Orient  B=Measure (B1–B11 validate + format)  C=Fix  D=Status  E=Maintain  F=Data  G=API[/dim]\n"
        "[dim]l=list commands  ?=help  q=quit[/dim]"
    )
    while True:
        console.print(Panel.fit(header, border_style="cyan", title="Menu"))
        current_section = ""
        for e in entries:
            if e.section != current_section:
                current_section = e.section
                console.print(f"\n[bold]{current_section}[/bold]")
            risk = f"[red]{e.risk}[/red]" if e.risk == "write" else "[green]read[/green]"
            console.print(f"  {e.id:3}  {e.label}  ({risk})")
        console.print("\n  l    List all CLI commands (table)")
        console.print("  ?    Short CLI help")
        console.print("  q    Quit")

        choice = Prompt.ask("Select option", default="A1").strip()
        cl = choice.lower()
        if cl == "q":
            console.print("Goodbye.")
            return
        if cl == "l":
            run_list_inline()
            continue
        if cl == "?":
            print_command_catalog_help()
            continue
        entry = by_id.get(choice)
        if entry is None:
            console.print("[yellow]Unknown option[/yellow]")
            continue
        try:
            entry.handler()
        except Exception as exc:
            console.print(f"[red]Error: {exc}[/red]")


if __name__ == "__main__":
    run_menu()
