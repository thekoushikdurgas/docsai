"""
main.py v2 — Contact360 Docs Agent interactive menu
Documentation operations read typed JSON under docs/ (see scripts/paths.py).
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

_DOCS_DIR = Path(__file__).resolve().parent
if str(_DOCS_DIR) not in sys.path:
    sys.path.insert(0, str(_DOCS_DIR))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    console = Console()
    def _print(msg: str, style: str = "") -> None:
        console.print(msg, style=style)
    def _input(prompt: str, default: str = "") -> str:
        return Prompt.ask(prompt, default=default)
except ImportError:
    console = None  # type: ignore
    def _print(msg: str, style: str = "") -> None:  # type: ignore[misc]
        print(msg)
    def _input(prompt: str, default: str = "") -> str:  # type: ignore[misc]
        return input(f"{prompt} [{default}]: ") or default

DOCS_AGENT_VERSION = "2.1.0"
DOCS_ROOT = _DOCS_DIR

from scripts.paths import JSON_ROOT  # noqa: E402

# ─── JSON module imports ─────────────────────────────────────────────────────
from scripts.json_scanner import scan_all, group_by_kind, era_summary  # type: ignore
from scripts.json_auditor import audit_era, format_audit_report  # type: ignore
from scripts.json_filler import fill_era  # type: ignore
from scripts.json_stats import (  # type: ignore
    task_report, format_task_report, era_guide_table, overview_stats
)
from scripts.json_validator import validate_all, format_validation_report  # type: ignore


# ─── Menu entry infrastructure ───────────────────────────────────────────────

@dataclass(frozen=True)
class MenuEntry:
    id: str
    label: str
    handler: Callable[[], int]
    hint: str = ""


def _hint(cmd: str) -> None:
    _print(f"  [dim]CLI: python cli.py {cmd}[/dim]")


def _run_cli(*args: str) -> int:
    """Run a cli.py command via subprocess."""
    result = subprocess.run([sys.executable, str(DOCS_ROOT / "cli.py"), *args], cwd=str(DOCS_ROOT))
    return result.returncode


# ─── Menu handlers ───────────────────────────────────────────────────────────

def handle_scan() -> int:
    _hint("scan")
    return _run_cli("scan")


def handle_stats() -> int:
    era_str = _input("Era index (0-10, blank for all)", "")
    if era_str.strip().isdigit():
        _hint(f"stats --era {era_str}")
        return _run_cli("stats", "--era", era_str.strip())
    _hint("stats")
    return _run_cli("stats")


def handle_era_guide() -> int:
    era_str = _input("Era index (0-10, blank for summary)", "")
    if era_str.strip().isdigit():
        _hint(f"era-guide --era {era_str}")
        return _run_cli("era-guide", "--era", era_str.strip())
    _hint("era-guide")
    return _run_cli("era-guide")


def handle_list() -> int:
    era_str = _input("Era index (blank for all)", "")
    kind_str = _input("Kind filter (blank for all, e.g. era_task)", "")
    args = ["list"]
    if era_str.strip().isdigit():
        args += ["--era", era_str.strip()]
    if kind_str.strip():
        args += ["--kind", kind_str.strip()]
    _hint(" ".join(args))
    return _run_cli(*args)


def handle_audit_tasks() -> int:
    era_str = _input("Era index (0-10, blank for all)", "")
    if era_str.strip().isdigit():
        _hint(f"audit-tasks --era {era_str}")
        return _run_cli("audit-tasks", "--era", era_str.strip())
    _hint("audit-tasks")
    return _run_cli("audit-tasks")


def handle_fill_tasks() -> int:
    era_str = _input("Era index (0-10)", "")
    apply_str = _input("Apply changes? (y=write, n=dry-run)", "n")
    apply = apply_str.strip().lower() == "y"
    args = ["fill-tasks", "--era", era_str.strip() or "0"]
    if apply:
        args.append("--apply")
    else:
        args.append("--dry-run")
    _hint(" ".join(args))
    return _run_cli(*args)


def handle_dedup_tasks() -> int:
    era_str = _input("Era index (blank for all)", "")
    args = ["dedup-tasks"]
    if era_str.strip().isdigit():
        args += ["--era", era_str.strip()]
    else:
        args.append("--all")
    _hint(" ".join(args))
    return _run_cli(*args)


def handle_task_report() -> int:
    era_str = _input("Era index (blank for all)", "")
    if era_str.strip().isdigit():
        _hint(f"task-report --era {era_str}")
        return _run_cli("task-report", "--era", era_str.strip())
    _hint("task-report")
    return _run_cli("task-report")


def handle_validate() -> int:
    _hint("validate-all --write-latest")
    return _run_cli("validate-all", "--write-latest")


def handle_validate_structure() -> int:
    era_str = _input("Era index (blank for all)", "")
    args = ["validate-structure"]
    if era_str.strip().isdigit():
        args += ["--era", era_str.strip()]
    _hint(" ".join(args))
    return _run_cli(*args)


def handle_update_status() -> int:
    status = _input("New status (completed/in_progress/planned/incomplete)", "completed")
    target = _input("Target: era number OR file path (blank to skip)", "")
    args = ["update", "--status", status.strip()]
    if target.strip().isdigit():
        args += ["--era", target.strip()]
    elif target.strip():
        args += ["--file", target.strip()]
    else:
        args.append("--all")
        confirm = _input("Apply to ALL era_task docs? (y/n)", "n")
        if confirm.strip().lower() != "y":
            _print("Cancelled.")
            return 0
    dry = _input("Dry-run? (y/n)", "y")
    if dry.strip().lower() == "y":
        args.append("--dry-run")
    _hint(" ".join(args))
    return _run_cli(*args)


def handle_name_audit() -> int:
    era_str = _input("Era index (blank for all)", "")
    if era_str.strip().isdigit():
        _hint(f"name-audit --era {era_str}")
        return _run_cli("name-audit", "--era", era_str.strip())
    _hint("name-audit")
    return _run_cli("name-audit")


def handle_rename_docs() -> int:
    era_str = _input("Era index (blank for all)", "")
    apply_str = _input("Apply renames? (y=apply, n=dry-run)", "n")
    args = ["rename-docs"]
    if era_str.strip().isdigit():
        args += ["--era", era_str.strip()]
    else:
        args.append("--all")
    if apply_str.strip().lower() == "y":
        args.append("--apply")
    _hint(" ".join(args))
    return _run_cli(*args)


def handle_migrate_full() -> int:
    _print("[bold yellow]This will run the full migration pipeline.[/bold yellow]")
    confirm = _input("Proceed? (y/n)", "n")
    if confirm.strip().lower() != "y":
        return 0
    _hint("migrate full")
    return _run_cli("migrate", "full")


def handle_manifest() -> int:
    _hint("migrate manifest")
    return _run_cli("migrate", "manifest")


def handle_pinecone_ingest() -> int:
    _hint("pinecone ingest-docs")
    return _run_cli("pinecone", "ingest-docs")


def handle_pinecone_query() -> int:
    query = _input("Search query", "")
    if not query.strip():
        return 0
    _hint(f"pinecone query '{query}'")
    return _run_cli("pinecone", "query", query.strip())


def handle_platform_verify() -> int:
    _hint("platform-verify")
    return _run_cli("platform-verify")


def handle_exit() -> int:
    _print("Goodbye!")
    sys.exit(0)


# ─── Menu definition ─────────────────────────────────────────────────────────

MENU_ENTRIES: list[MenuEntry] = [
    MenuEntry("scan",           "📊  Overview dashboard (scan)",            handle_scan),
    MenuEntry("stats",          "📈  Era stats (stats)",                    handle_stats),
    MenuEntry("era-guide",      "🗺   Era guide / navigation",              handle_era_guide),
    MenuEntry("list",           "📋  List JSON docs",                       handle_list),
    MenuEntry("---",            "─── Task Management ───────────────",      lambda: 0),
    MenuEntry("audit-tasks",    "🔍  Audit task tracks",                    handle_audit_tasks),
    MenuEntry("fill-tasks",     "➕  Fill missing task tracks",             handle_fill_tasks),
    MenuEntry("dedup-tasks",    "🔁  Detect duplicate tasks",               handle_dedup_tasks),
    MenuEntry("task-report",    "📊  Task coverage report",                 handle_task_report),
    MenuEntry("---2",           "─── Validation ────────────────────",      lambda: 0),
    MenuEntry("validate-all",   "✅  Validate all JSON files",              handle_validate),
    MenuEntry("validate-struct","🏗   Validate structure",                   handle_validate_structure),
    MenuEntry("---3",           "─── Documentation Ops ─────────────",      lambda: 0),
    MenuEntry("update-status",  "✏️   Update doc status",                    handle_update_status),
    MenuEntry("name-audit",     "🏷   Audit filenames",                     handle_name_audit),
    MenuEntry("rename-docs",    "✏️   Rename docs to canonical form",        handle_rename_docs),
    MenuEntry("---4",           "─── Migration ──────────────────────",      lambda: 0),
    MenuEntry("manifest",       "📄  Rebuild manifest.json",                handle_manifest),
    MenuEntry("migrate-full",   "🚀  Run full migration pipeline",          handle_migrate_full),
    MenuEntry("---5",           "─── Platform ───────────────────────",      lambda: 0),
    MenuEntry("pinecone-ingest","📌  Pinecone: ingest docs",                handle_pinecone_ingest),
    MenuEntry("pinecone-query", "🔎  Pinecone: search",                     handle_pinecone_query),
    MenuEntry("platform-verify","🏥  Platform health check",                handle_platform_verify),
    MenuEntry("---6",           "────────────────────────────────────",      lambda: 0),
    MenuEntry("exit",           "🚪  Exit",                                  handle_exit),
]


# ─── Main loop ───────────────────────────────────────────────────────────────

def print_menu() -> None:
    _print(f"\n[bold cyan]Contact360 Docs Agent v{DOCS_AGENT_VERSION}[/bold cyan]")
    _print("[dim]All operations read typed JSON under docs/[/dim]\n")
    for i, entry in enumerate(MENU_ENTRIES):
        if entry.id.startswith("---"):
            _print(f"\n  {entry.label}")
        else:
            _print(f"  [{i:>2}] {entry.label}")


def run_menu() -> None:
    while True:
        print_menu()
        choice = _input("\nEnter number or command id (q to quit)", "")
        if choice.strip().lower() in ("q", "quit", "exit"):
            _print("Goodbye!")
            sys.exit(0)

        # Numeric choice
        if choice.strip().isdigit():
            idx = int(choice.strip())
            non_sep = [e for e in MENU_ENTRIES if not e.id.startswith("---")]
            if 0 <= idx < len(MENU_ENTRIES):
                entry = MENU_ENTRIES[idx]
            else:
                _print(f"[red]Invalid choice: {idx}[/red]")
                continue
        else:
            matches = [e for e in MENU_ENTRIES if e.id == choice.strip()]
            if not matches:
                _print(f"[red]Unknown command: {choice}[/red]")
                continue
            entry = matches[0]

        if entry.id.startswith("---"):
            continue

        try:
            result = entry.handler()
            if result != 0:
                _print(f"[yellow]Command returned exit code {result}[/yellow]")
        except KeyboardInterrupt:
            _print("\n[yellow]Interrupted[/yellow]")
        except Exception as e:
            _print(f"[red]Error: {e}[/red]")


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="Contact360 Docs Agent interactive menu")
    ap.add_argument("--cmd", type=str, help="Run a single command non-interactively (e.g. --cmd scan)")
    args = ap.parse_args()

    if args.cmd:
        # Non-interactive: run a single command
        cmd_map = {e.id: e.handler for e in MENU_ENTRIES if not e.id.startswith("---")}
        handler = cmd_map.get(args.cmd)
        if handler:
            sys.exit(handler())
        else:
            _print(f"Unknown command: {args.cmd}")
            sys.exit(1)
    else:
        run_menu()


if __name__ == "__main__":
    main()
