from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm, Prompt

from scripts.models import Status
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
from scripts.task_auditor import audit_era, find_duplicate_tasks
from scripts.task_filler import bulk_fill, deduplicate_file_tasks
from scripts.updater import bulk_update, list_scope_paths
from scripts.unused import find_unused_files

console = Console()


def _status_from_input(value: str) -> Status:
    """Safely cast string input to a Status enum."""
    try:
        return Status.from_cli(value)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise


def show_dashboard() -> None:
    """Print the overall codebase metrics dashboard."""
    scan_result = scan_all()
    console.print(overall_dashboard(scan_result))
    console.print(era_summary(scan_result))


def browse_by_era() -> None:
    """Prompt user to select an era and show its detailed tasks."""
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


def run_bulk_update() -> None:
    """Prompt user for scope and launch a bulk file update."""
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
        f"Dry run -> files: {preview['files']}, "
        f"changed: {preview['changed']}, diff_lines: {preview['diff_lines']}"
    )
    if not Confirm.ask("Apply changes?", default=False):
        return
    summary = bulk_update(paths, status, update_tasks=update_tasks, dry_run=False)
    console.print(
        f"[green]Applied[/green] -> files: {summary['files']}, "
        f"changed: {summary['changed']}, diff_lines: {summary['diff_lines']}"
    )


def normalize_all() -> None:
    """Normalize the task list status in all files unconditionally."""
    status_raw = Prompt.ask(
        "Normalize all files to status",
        choices=["completed", "in_progress", "planned", "incomplete"],
        default="completed",
    )
    status = _status_from_input(status_raw)
    paths = list_scope_paths(scope="all")
    preview = bulk_update(paths, status, update_tasks=True, dry_run=True)
    console.print(
        f"Dry run -> files: {preview['files']}, "
        f"changed: {preview['changed']}, diff_lines: {preview['diff_lines']}"
    )
    if not Confirm.ask("Apply normalize-all?", default=False):
        return
    summary = bulk_update(paths, status, update_tasks=True, dry_run=False)
    console.print(
        f"[green]Normalized[/green] -> files: {summary['files']}, "
        f"changed: {summary['changed']}, diff_lines: {summary['diff_lines']}"
    )


def scan_report() -> None:
    """Alias for show_dashboard."""
    show_dashboard()


def run_task_audit_menu() -> None:
    """Interactive task audit for one era or all."""
    for idx, name in enumerate(ERA_FOLDERS):
        console.print(f"{idx}. {name}")
    scope = Prompt.ask("Era number (0-10) or 'all'", default="0")
    if scope.lower() == "all":
        from scripts.task_auditor import audit_all

        data = audit_all()
        total = 0
        for _name, results in data.items():
            if results:
                console.print(task_audit_table(results))
                total += len(results)
        console.print(f"[bold]Total audited files: {total}[/bold]")
        return
    if not scope.isdigit():
        console.print("[red]Invalid selection[/red]")
        return
    ei = int(scope)
    if ei < 0 or ei >= len(ERA_FOLDERS):
        console.print("[red]Out of range[/red]")
        return
    results = audit_era(ei)
    console.print(task_audit_table(results))


def run_fill_tasks_menu() -> None:
    """Fill missing ### tracks with generated bullets."""
    reg = load_registry()
    scope = Prompt.ask("Scope", choices=["era", "file", "all"], default="era")
    paths: list[Path]
    if scope == "file":
        fp = Prompt.ask("Markdown path under docs/")
        paths = [Path(fp) if Path(fp).is_absolute() else Path(__file__).resolve().parent / fp]
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


def run_dedup_tasks_menu() -> None:
    """Replace duplicate bullets with patch-specific lines."""
    reg = load_registry()
    all_eras = Confirm.ask("Run on ALL eras?", default=False)
    docs_root = Path(__file__).resolve().parent
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
        for path in sorted((docs_root / era_name).glob("*.md")):
            ch, dl = deduplicate_file_tasks(path, ei, dup_map, reg, dry_run=dry_run)
            if ch:
                changed += 1
                diff_lines += dl
    label = "Applied" if apply_changes else "Dry run"
    console.print(f"[green]{label}[/green] -> files changed: {changed}, diff_lines (sum): {diff_lines}")


def run_name_audit_menu() -> None:
    """Show parsed era filenames and duplicate / malformed issues."""
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


def run_era_guide_menu() -> None:
    """Show master-docs → era map: all eras table or one era detail panel."""
    scope = Prompt.ask("All eras (a) or era number 0-10", default="a")
    if scope.lower() == "a":
        console.print(era_guide_summary_table(get_era_guide_entries()))
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


def run_rename_docs_menu() -> None:
    """Normalize filenames to `version — Codename.md` with em dash."""
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
    lbl = "Applied" if apply_changes else "Dry run"
    console.print(
        f"[bold]{lbl}[/bold]: planned={summary['planned']}, renamed={summary['renamed']}, "
        f"skipped={summary['skipped']}, errors={summary['errors']}"
    )


def run_find_unused() -> None:
    """Find and print unused markdown and component files."""
    unused = find_unused_files()
    if not unused:
        console.print("[green]No unused files found![/green]")
        return
    console.print(f"[yellow]Found {len(unused)} potentially unused files:[/yellow]")
    docs_root = Path(__file__).resolve().parent
    for path in unused:
        try:
            rel_path = path.relative_to(docs_root)
        except ValueError:
            rel_path = path
        console.print(f"- {rel_path}")


def run_menu() -> None:
    """Execute the interactive CLI menu loop."""
    while True:
        console.print("\n[bold]Docs CLI Manager[/bold]")
        console.print("1. Dashboard / Overview")
        console.print("2. Browse by Era")
        console.print("3. Bulk Update")
        console.print("4. Normalize All Status Markers")
        console.print("5. Scan & Report")
        console.print("6. Find Unused Files")
        console.print("7. Task Audit (empty/duplicate tracks)")
        console.print("8. Fill Empty Task Tracks (dry-run / apply)")
        console.print("9. Dedup Task Bullets (dry-run / apply)")
        console.print("10. Era filename audit (version + codename uniqueness)")
        console.print("11. Rename docs to canonical em-dash names (dry-run / apply)")
        console.print("12. Era guide (master docs map 0.x–10.x)")
        console.print("q. Quit")

        choice = Prompt.ask("Select option", default="1")
        if choice == "1":
            show_dashboard()
        elif choice == "2":
            browse_by_era()
        elif choice == "3":
            run_bulk_update()
        elif choice == "4":
            normalize_all()
        elif choice == "5":
            scan_report()
        elif choice == "6":
            run_find_unused()
        elif choice == "7":
            run_task_audit_menu()
        elif choice == "8":
            run_fill_tasks_menu()
        elif choice == "9":
            run_dedup_tasks_menu()
        elif choice == "10":
            run_name_audit_menu()
        elif choice == "11":
            run_rename_docs_menu()
        elif choice == "12":
            run_era_guide_menu()
        elif choice.lower() == "q":
            console.print("Goodbye.")
            return
        else:
            console.print("[yellow]Unknown option[/yellow]")


if __name__ == "__main__":
    run_menu()
