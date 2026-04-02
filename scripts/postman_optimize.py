from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from rich.console import Console

from scripts.paths import DOCS_ROOT, POSTMAN_DIR


console = Console()


CANONICAL_ENVS = {
    "Contact360_Local.postman_environment.json",
    "Contact360_Production.postman_environment.json",
}


@dataclass(frozen=True)
class OptimizeResult:
    collections_scanned: int
    collections_changed: int
    env_files_seen: int
    env_files_removed: int


def _iter_collection_files() -> Iterable[Path]:
    yield from POSTMAN_DIR.glob("*.postman_collection.json")


def _iter_env_files() -> Iterable[Path]:
    yield from POSTMAN_DIR.glob("*.postman_environment.json")


def _normalize_url_block(url: dict) -> tuple[dict, bool]:
    """Ensure url.raw uses {{baseUrl}}/..., return (updated_url, changed)."""
    changed = False
    raw = url.get("raw")
    if isinstance(raw, str):
        # If raw is a full URL, replace scheme+host with {{baseUrl}}
        # Simple heuristic: split at "://", then at first "/" after host.
        if raw.startswith("http://") or raw.startswith("https://"):
            parts = raw.split("://", 1)[1]
            if "/" in parts:
                _host, rest = parts.split("/", 1)
                new_raw = "{{baseUrl}}/" + rest
            else:
                new_raw = "{{baseUrl}}"
            if new_raw != raw:
                url["raw"] = new_raw
                changed = True
    # Ensure host/path fields align with raw when using {{baseUrl}}
    raw = url.get("raw")
    if isinstance(raw, str) and raw.startswith("{{baseUrl}}"):
        url["host"] = ["{{baseUrl}}"]
        path_part = raw[len("{{baseUrl}}") :].lstrip("/")
        if path_part:
            url["path"] = path_part.split("/")
        else:
            url["path"] = []
        changed = True
    return url, changed


def _normalize_item(item: dict) -> bool:
    """Recursively normalize request URLs in a collection item."""
    changed = False
    if "request" in item and isinstance(item["request"], dict):
        req = item["request"]
        url = req.get("url")
        if isinstance(url, dict):
            new_url, ch = _normalize_url_block(url)
            if ch:
                req["url"] = new_url
                changed = True
    # Recurse into nested folders
    subitems = item.get("item")
    if isinstance(subitems, list):
        for sub in subitems:
            if isinstance(sub, dict) and _normalize_item(sub):
                changed = True
    return changed


def optimize_collections(apply: bool) -> tuple[int, int]:
    """Normalize URLs in all collection files; return (scanned, changed)."""
    scanned = 0
    changed = 0
    for path in _iter_collection_files():
        scanned += 1
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            console.print(f"[red]Skipping invalid JSON[/red]: {path.relative_to(DOCS_ROOT)} ({exc})")
            continue
        root_changed = False
        # Top-level items
        items = data.get("item")
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and _normalize_item(item):
                    root_changed = True
        if root_changed:
            changed += 1
            rel = path.relative_to(DOCS_ROOT)
            if apply:
                path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
                console.print(f"[cyan]Normalized[/cyan]: {rel}")
            else:
                console.print(f"[cyan]Would normalize[/cyan]: {rel}")
    return scanned, changed


def prune_env_files(apply: bool) -> tuple[int, int]:
    """Keep only canonical Contact360 Local/Production envs."""
    seen = 0
    removed = 0
    for path in _iter_env_files():
        seen += 1
        if path.name in CANONICAL_ENVS:
            continue
        rel = path.relative_to(DOCS_ROOT)
        if apply:
            path.unlink(missing_ok=True)
            console.print(f"[yellow]Removed env[/yellow]: {rel}")
            removed += 1
        else:
            console.print(f"[yellow]Would remove env[/yellow]: {rel}")
            removed += 1
    return seen, removed


def main(apply: bool = False, apply_env: bool = False) -> OptimizeResult:
    console.print(
        "[bold]Postman optimization[/bold] "
        f"(apply_collections={apply}, apply_env={apply_env}) under {POSTMAN_DIR.relative_to(DOCS_ROOT)}"
    )
    seen_env, removed_env = prune_env_files(apply=apply_env)
    scanned, changed = optimize_collections(apply=apply)
    console.print(
        f"[bold]Summary[/bold]: collections_scanned={scanned}, "
        f"collections_changed={changed}, env_files_seen={seen_env}, env_files_removed={removed_env}"
    )
    return OptimizeResult(
        collections_scanned=scanned,
        collections_changed=changed,
        env_files_seen=seen_env,
        env_files_removed=removed_env,
    )


if __name__ == "__main__":
    # Default: dry-run both collection and env changes
    main(apply=False, apply_env=False)

