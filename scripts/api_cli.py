#!/usr/bin/env python3
"""Contact360 API Testing CLI (Typer). Run from ``docs/scripts/``:

    python api_cli.py test run
    python api_cli.py --help

Ensure ``docs/`` is on ``PYTHONPATH`` when running from other cwd (e.g. ``set PYTHONPATH=..`` from ``scripts/``).
"""
from __future__ import annotations

import importlib.util
import sys
import sysconfig
from pathlib import Path

import typer


def _force_stdlib_platform() -> None:
    """
    Ensure stdlib `platform` wins over local `scripts/platform/`.

    When executing `python scripts/api_cli.py ...`, `docs/scripts` becomes sys.path[0],
    which would otherwise shadow the stdlib `platform` module.
    """

    stdlib_dir = sysconfig.get_paths().get("stdlib")
    if not stdlib_dir:
        return
    platform_py = Path(stdlib_dir) / "platform.py"
    if not platform_py.is_file():
        return
    spec = importlib.util.spec_from_file_location("platform", str(platform_py))
    if spec is None or spec.loader is None:
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    sys.modules["platform"] = module


try:
    _force_stdlib_platform()
except Exception:
    pass


from rich.console import Console
from rich.panel import Panel

_SCRIPTS = Path(__file__).resolve().parent
_DOCS = _SCRIPTS.parent

# Ensure import precedence: `docs/scripts` BEFORE `docs/`.
_scripts_s = str(_SCRIPTS)
_docs_s = str(_DOCS)
if _scripts_s in sys.path:
    sys.path.remove(_scripts_s)
sys.path.insert(0, _scripts_s)
if _docs_s in sys.path:
    sys.path.remove(_docs_s)
sys.path.insert(1, _docs_s)

# Ensure `cli` resolves to `docs/scripts/cli/` package, not `docs/cli.py`.
try:
    _loaded_cli = sys.modules.get("cli")
    if _loaded_cli is not None and not hasattr(_loaded_cli, "__path__"):
        # A non-package module named `cli` was already imported; remove it.
        del sys.modules["cli"]
except Exception:
    pass

from cli.commands import ai_commands

try:
    from cli.commands import test_commands
except Exception:
    test_commands = None  # type: ignore[assignment]

try:
    from cli.commands import discover_commands
except Exception:
    discover_commands = None  # type: ignore[assignment]

try:
    from cli.commands import monitor_commands
except Exception:
    monitor_commands = None  # type: ignore[assignment]

try:
    from cli.commands import collection_commands
except Exception:
    collection_commands = None  # type: ignore[assignment]

try:
    from cli.commands import interactive_commands
except Exception:
    interactive_commands = None  # type: ignore[assignment]

try:
    from cli.commands import config_commands
except Exception:
    config_commands = None  # type: ignore[assignment]

try:
    from cli.commands import dashboard_commands
except Exception:
    dashboard_commands = None  # type: ignore[assignment]

app = typer.Typer(
    name="contact360-cli",
    help="AI Agentic CLI for Contact360 API Testing",
    add_completion=False,
)

if test_commands is not None:
    app.add_typer(test_commands.app, name="test")
if discover_commands is not None:
    app.add_typer(discover_commands.app, name="discover")
if monitor_commands is not None:
    app.add_typer(monitor_commands.app, name="monitor")
if collection_commands is not None:
    app.add_typer(collection_commands.app, name="collection")
if interactive_commands is not None:
    app.add_typer(interactive_commands.app, name="interactive")
if config_commands is not None:
    app.add_typer(config_commands.app, name="config")
if dashboard_commands is not None:
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
