#!/usr/bin/env python3
"""Contact360 API Testing CLI (Typer). Run from ``docs/scripts/``:

    python api_cli.py test run
    python api_cli.py --help

Ensure ``docs/`` is on ``PYTHONPATH`` when running from other cwd (e.g. ``set PYTHONPATH=..`` from ``scripts/``).
"""
from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

_SCRIPTS = Path(__file__).resolve().parent
_DOCS = _SCRIPTS.parent
for _p in (_DOCS, _SCRIPTS):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from cli.commands import ai_commands
from cli.commands import collection_commands
from cli.commands import config_commands
from cli.commands import dashboard_commands
from cli.commands import discover_commands
from cli.commands import interactive_commands
from cli.commands import monitor_commands
from cli.commands import test_commands

app = typer.Typer(
    name="contact360-cli",
    help="AI Agentic CLI for Contact360 API Testing",
    add_completion=False,
)

app.add_typer(test_commands.app, name="test")
app.add_typer(discover_commands.app, name="discover")
app.add_typer(monitor_commands.app, name="monitor")
app.add_typer(collection_commands.app, name="collection")
app.add_typer(interactive_commands.app, name="interactive")
app.add_typer(config_commands.app, name="config")
app.add_typer(dashboard_commands.app, name="dashboard")
app.add_typer(ai_commands.app, name="ai")

console = Console()


@app.command("version")
def show_version() -> None:
    """Show CLI version."""
    from cli import __version__

    console.print(f"Contact360 CLI v{__version__}")


@app.callback(invoke_without_command=True)
def cli_root(ctx: typer.Context) -> None:
    """Contact360 API Testing CLI."""
    if ctx.invoked_subcommand is None:
        console.print(
            Panel.fit(
                "[bold cyan]Contact360 API Testing CLI[/bold cyan]\n\n"
                "AI-powered automation for API testing, monitoring, and management.\n\n"
                "[yellow]Available Commands:[/yellow]\n"
                "  test          - Run API tests\n"
                "  discover      - Discover and sync endpoints\n"
                "  monitor       - Continuous monitoring\n"
                "  collection    - Postman collection management\n"
                "  interactive   - Interactive REPL mode\n"
                "  config        - Configuration management\n"
                "  dashboard     - View dashboards and trends\n"
                "  ai            - AI agentic features\n\n"
                "Use [cyan]python api_cli.py <command> --help[/cyan] for more.\n"
                "Example: [cyan]python api_cli.py test run[/cyan]",
                border_style="cyan",
            )
        )
        raise typer.Exit()


if __name__ == "__main__":
    app()
