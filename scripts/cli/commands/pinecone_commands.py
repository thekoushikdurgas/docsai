"""Pinecone ingestion + search commands for the `docs/` CLI."""

from __future__ import annotations

import sys
import time
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pinecone_integration import get_api_index, get_client, get_docs_index


app = typer.Typer(name="pinecone", help="Pinecone ingestion, search, and healthcheck")
console = Console()


def _hit_to_fields(hit: Any) -> Dict[str, Any]:
    fields = getattr(hit, "fields", None)
    if isinstance(fields, dict):
        return fields
    if isinstance(hit, dict):
        maybe = hit.get("fields")
        if isinstance(maybe, dict):
            return maybe
    return {}


def _hit_to_score(hit: Any) -> Optional[float]:
    try:
        # Some SDK versions expose dict-like access
        score = hit.get("_score") if isinstance(hit, dict) else hit["_score"]
        return float(score)
    except Exception:
        # Fallback: attempt attribute
        try:
            return float(getattr(hit, "_score"))
        except Exception:
            return None


@app.command()
def ingest_docs(
    era: Optional[str] = typer.Option(None, "--era", help="Only ingest one era (0-10)."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Chunk only; do not upsert."),
):
    """Ingest markdown docs into Pinecone."""

    console.print("[cyan]Ingesting docs into Pinecone...[/cyan]")
    from pinecone_integration.ingest_docs import ingest_docs as ingest_docs_func

    result = ingest_docs_func(era=era, dry_run=dry_run)
    console.print(Panel(json.dumps(result, indent=2), title="Ingest docs result", border_style="cyan"))


@app.command()
def ingest_api(
    profile: str = typer.Option(..., "--profile", "-p", help="CLI profile name (e.g. default)."),
    days: Optional[int] = typer.Option(7, "--days", "-d", help="Only ingest failures from last N days."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Chunk only; do not upsert."),
):
    """Ingest API test failures into Pinecone."""

    console.print("[cyan]Ingesting API failures into Pinecone...[/cyan]")
    from pinecone_integration.ingest_api import ingest_api as ingest_api_func

    result = ingest_api_func(profile=profile, days=days, dry_run=dry_run)
    console.print(Panel(json.dumps(result, indent=2), title="Ingest api result", border_style="cyan"))


@app.command()
def search(
    question: str = typer.Argument(..., help="Question / query text to search over docs."),
    namespace: str = typer.Option("docs_global", "--namespace", "-n", help="Pinecone namespace to search."),
    top_k: int = typer.Option(5, "--top-k", help="Top-K results to print."),
):
    """Semantic search over docs stored in Pinecone."""

    console.print(f"[cyan]Searching namespace: {namespace}[/cyan]")
    index = get_docs_index()
    from pinecone_integration.search import search as pinecone_search

    hits = pinecone_search(index, namespace=namespace, query_text=question, top_k=top_k)

    if not hits:
        console.print("[yellow]No matches found.[/yellow]")
        return

    table = Table(title="Pinecone search results", show_header=True, header_style="bold cyan")
    table.add_column("Score", justify="right")
    table.add_column("Doc Path")
    table.add_column("Heading")
    table.add_column("Snippet")

    for hit in hits[:top_k]:
        fields = _hit_to_fields(hit)
        doc_path = fields.get("doc_path", "")
        heading = fields.get("heading", "")
        content = fields.get("content", "")
        snippet = str(content).replace("\n", " ")
        if len(snippet) > 180:
            snippet = snippet[:180] + "..."
        score = _hit_to_score(hit)
        table.add_row(
            f"{score:.3f}" if score is not None else "-",
            str(doc_path),
            str(heading),
            snippet,
        )

    console.print(table)


@app.command()
def status():
    """Pinecone healthcheck: upsert a record, wait, then fetch it."""

    # Resolve index names from env vars.
    index_docs = None
    index_api = None
    try:
        index_docs = get_docs_index()
        index_api = get_api_index()
    except Exception as e:
        console.print(f"[red]Failed to initialize indexes: {e}[/red]")
        raise typer.Exit(1)

    namespaces = ["_healthcheck"]
    records_ok: List[str] = []
    records_fail: List[str] = []
    debug_rows: List[str] = []

    for idx_label, index in [("docs", index_docs), ("api", index_api)]:
        try:
            health_id = f"pinecone_health_{idx_label}_{int(time.time())}"
            for ns in namespaces:
                try:
                    stats_before = index.describe_index_stats()
                    debug_rows.append(f"{idx_label}:{ns} stats_before={stats_before}")
                except Exception as e:
                    debug_rows.append(f"{idx_label}:{ns} stats_before_error={e}")
                    stats_before = None

                index.upsert_records(
                    ns,
                    [
                        {
                            "_id": health_id,
                            # Be tolerant of field_map variations across existing indexes:
                            # some expect `content`, others expect `text`.
                            "content": f"Pinecone healthcheck ({idx_label})",
                            "text": f"Pinecone healthcheck ({idx_label})",
                            "kind": "healthcheck",
                        }
                    ],
                )

                time.sleep(10)

                try:
                    stats_after = index.describe_index_stats()
                    debug_rows.append(f"{idx_label}:{ns} stats_after={stats_after}")
                except Exception as e:
                    debug_rows.append(f"{idx_label}:{ns} stats_after_error={e}")
                    stats_after = None

                before_n = (
                    (stats_before or {}).get("namespaces", {}).get(ns, {}).get("vector_count")
                    if isinstance(stats_before, dict)
                    else None
                )
                after_n = (
                    (stats_after or {}).get("namespaces", {}).get(ns, {}).get("vector_count")
                    if isinstance(stats_after, dict)
                    else None
                )
                exists = before_n is not None and after_n is not None and int(after_n) > int(before_n)

                if exists:
                    records_ok.append(f"{idx_label}:{ns}")
                else:
                    records_fail.append(f"{idx_label}:{ns} (before={before_n}, after={after_n})")
        except Exception as e:
            records_fail.append(f"{idx_label}:error({e})")

    if records_fail:
        if debug_rows:
            console.print(Panel("\n".join(debug_rows[-20:]), title="Pinecone debug (tail)", border_style="yellow"))
        console.print(Panel("\n".join(records_fail), title="Pinecone healthcheck FAILED", border_style="red"))
        raise typer.Exit(1)

    console.print(Panel("\n".join(records_ok), title="Pinecone healthcheck OK", border_style="green"))


if __name__ == "__main__":
    # Convenience for direct execution.
    app()

