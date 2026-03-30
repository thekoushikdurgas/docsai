from __future__ import annotations

from rich.panel import Panel
from rich.table import Table

from .contact360_era_guide import EraGuideEntry
from .models import DocFile, ScanResult, Status, TaskAuditResult, TRACK_NAMES
from .era_naming import EraFilenameRecord, NamingIssue


def overall_dashboard(scan_result: ScanResult) -> Panel:
    counts = scan_result.by_status()
    lines = [
        f"Total files: {len(scan_result.files)}",
        f"Completed: {counts.get(Status.COMPLETED, 0)}",
        f"In Progress: {counts.get(Status.IN_PROGRESS, 0)}",
        f"Planned: {counts.get(Status.PLANNED, 0)}",
        f"Incomplete: {counts.get(Status.INCOMPLETE, 0)}",
        f"Unknown: {counts.get(Status.UNKNOWN, 0)}",
        f"Task bullets: {scan_result.total_tasks()}",
        f"Tasks missing prefixes: {scan_result.total_tasks_without_prefix()}",
    ]
    return Panel("\n".join(lines), title="Docs Status Dashboard")


def era_summary(scan_result: ScanResult) -> Table:
    table = Table(title="Era Summary")
    table.add_column("Era")
    table.add_column("Files", justify="right")
    table.add_column("Completed", justify="right")
    table.add_column("In Progress", justify="right")
    table.add_column("Planned", justify="right")
    table.add_column("Incomplete", justify="right")
    table.add_column("Unknown", justify="right")

    by_era = scan_result.by_era()
    for era in sorted(by_era):
        docs = by_era[era]
        status_counts = _status_counts(docs)
        table.add_row(
            era,
            str(len(docs)),
            str(status_counts[Status.COMPLETED]),
            str(status_counts[Status.IN_PROGRESS]),
            str(status_counts[Status.PLANNED]),
            str(status_counts[Status.INCOMPLETE]),
            str(status_counts[Status.UNKNOWN]),
        )
    return table


def file_detail(scan_result: ScanResult, era: str) -> Table:
    table = Table(title=f"Files in {era}")
    table.add_column("Version")
    table.add_column("Type")
    table.add_column("Status")
    table.add_column("Tasks", justify="right")
    table.add_column("Missing Prefix", justify="right")
    table.add_column("Path")

    docs = sorted(
        (doc for doc in scan_result.files if doc.era == era),
        key=lambda d: (d.file_type, d.version, d.path.name),
    )
    for doc in docs:
        table.add_row(
            doc.version,
            doc.file_type,
            doc.status.label,
            str(doc.task_count),
            str(doc.tasks_without_prefix),
            str(doc.path),
        )
    return table


def _status_counts(docs: list[DocFile]) -> dict[Status, int]:
    counts = {status: 0 for status in Status}
    for doc in docs:
        counts[doc.status] = counts.get(doc.status, 0) + 1
    return counts


def task_audit_table(results: list[TaskAuditResult]) -> Table:
    """Rich table: Version, Era, Coverage%, Missing Tracks, Dup count, Path."""
    table = Table(title="Task audit (patch/minor)")
    table.add_column("Version")
    table.add_column("Era", max_width=36, overflow="ellipsis")
    table.add_column("Cov%", justify="right")
    table.add_column("Missing")
    table.add_column("Dups", justify="right")
    table.add_column("Path", overflow="ellipsis")

    for r in sorted(results, key=lambda x: (x.era, x.version, str(x.path))):
        miss = ",".join(r.missing_tracks[:3])
        if len(r.missing_tracks) > 3:
            miss += "…"
        table.add_row(
            r.version,
            r.era,
            f"{r.coverage_pct:.0f}",
            miss or "—",
            str(len(r.duplicate_items)),
            str(r.path),
        )
    return table


def track_coverage_table(scan_result: ScanResult, era: str | None) -> Table:
    """Per-file checkmarks for each of five tracks under ## Tasks."""
    title = f"Track coverage — {era}" if era else "Track coverage — all scanned files"
    table = Table(title=title)
    table.add_column("Version")
    table.add_column("Type")
    for t in TRACK_NAMES:
        table.add_column(t[:4], justify="center")

    docs = [
        d
        for d in scan_result.files
        if (era is None or d.era == era)
        and d.file_type in ("patch", "minor")
        and d.era != "top-level"
    ]
    for doc in sorted(docs, key=lambda d: (d.era, d.version, d.path.name)):
        present = {ts.name for ts in doc.track_sections if ts.items}
        row = [doc.version, doc.file_type]
        for t in TRACK_NAMES:
            row.append("✓" if t in present else "—")
        table.add_row(*row)
    return table


def naming_inventory_table(records: list[EraFilenameRecord]) -> Table:
    """Parsed version/codename per era markdown file (excludes README)."""
    table = Table(title="Era filename inventory")
    table.add_column("Version")
    table.add_column("Kind")
    table.add_column("Codename", max_width=36, overflow="ellipsis")
    table.add_column("OK", justify="center")
    table.add_column("Filename", overflow="ellipsis")

    for r in sorted(records, key=lambda x: (x.era_folder, x.version, x.path.name)):
        if r.kind == "other":
            table.add_row("—", "other", r.stem[:36], "—", r.path.name)
        else:
            canon = "Y" if r.is_canonical else "N"
            table.add_row(r.version, r.kind, r.codename[:36], canon, r.path.name)
    return table


def naming_issues_table(issues: list[NamingIssue]) -> Table:
    """Grouped duplicate / malformed / non-canonical naming issues."""
    table = Table(title="Era filename issues")
    table.add_column("Code")
    table.add_column("Severity")
    table.add_column("Message", max_width=56, overflow="ellipsis")
    table.add_column("Files", justify="right")

    for i in issues:
        table.add_row(i.code, i.severity, i.message, str(len(i.paths)))
    return table


def era_guide_summary_table(entries: list[EraGuideEntry]) -> Table:
    """Compact table: index, semver band, title, core concern (truncated)."""
    table = Table(title="Contact360 era guide (master docs → eras 0.x–10.x)")
    table.add_column("Ix", justify="right")
    table.add_column("Era")
    table.add_column("Title", max_width=44, overflow="ellipsis")
    table.add_column("Core concern", max_width=48, overflow="ellipsis")
    for e in entries:
        table.add_row(str(e.index), e.label, e.title, e.core_concern)
    return table


def era_guide_detail_panel(entry: EraGuideEntry) -> Panel:
    """Full breakdown for one era: scope, pointers, master files, execution checklist."""
    lines: list[str] = [
        f"[bold]{entry.label}[/bold] — {entry.title}",
        "",
        "[bold]Core concern[/bold]",
        entry.core_concern,
        "",
        "[bold]Scope[/bold]",
        *[f"  • {s}" for s in entry.scope_lines],
        "",
        "[bold]Era README[/bold]",
        f"  {entry.era_readme_rel}",
        "",
        "[bold]Pointers[/bold]",
        f"  Roadmap: {entry.roadmap_pointer}",
        f"  Versions: {entry.versions_pointer}",
        f"  Architecture: {entry.architecture_pointer}",
        f"  Frontend: {entry.frontend_pointer}",
        f"  Audit: {entry.audit_pointer}",
        "",
        "[bold]Master files[/bold]",
    ]
    for path, why in entry.master_files:
        lines.append(f"  • [cyan]{path}[/cyan] — {why}")
    lines.extend(
        (
            "",
            "[bold]Execution checklist (small tasks)[/bold]",
            *[f"  {t}" for t in entry.execution_tasks],
        )
    )
    return Panel("\n".join(lines), title=f"Era {entry.index}", expand=False)

