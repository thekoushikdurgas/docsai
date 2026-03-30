"""Find duplicate files by content hash under a prefix within docs/."""
from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path

from .doc_structure import resolve_docs_subpath
from .paths import DOCS_ROOT

# Skip VCS, caches, and validation JSON output dirs (latest.json duplicates timestamped files).
_SKIP_DIR_PARTS = frozenset(
    {
        ".git",
        "__pycache__",
        ".pytest_cache",
        "result",
        "errors",
    }
)


def _should_skip_path_for_duplicate_scan(path: Path, base: Path) -> bool:
    try:
        rel = path.resolve().relative_to(base.resolve())
    except ValueError:
        return True
    return any(part in _SKIP_DIR_PARTS for part in rel.parts)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_duplicate_groups(
    prefix: str | None = None,
    *,
    extensions: frozenset[str] | None = None,
) -> dict[str, list[Path]]:
    """
    Group files by SHA-256 digest. Default prefix is entire DOCS_ROOT.
    extensions: if set, only include files with these suffixes (e.g. {'.md', '.json'}).
    """
    if not prefix:
        base = DOCS_ROOT
    else:
        base = resolve_docs_subpath(prefix)
    if not base.exists():
        return {}
    files: list[Path] = []
    if base.is_file():
        files = [base]
    else:
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            if _should_skip_path_for_duplicate_scan(p, base):
                continue
            if extensions is not None and p.suffix.lower() not in extensions:
                continue
            # skip huge binaries in postman etc.
            try:
                if p.stat().st_size > 20 * 1024 * 1024:
                    continue
            except OSError:
                continue
            files.append(p)

    by_hash: dict[str, list[Path]] = defaultdict(list)
    for p in files:
        try:
            digest = _sha256(p)
        except OSError:
            continue
        by_hash[digest].append(p)
    return {d: paths for d, paths in by_hash.items() if len(paths) > 1}
