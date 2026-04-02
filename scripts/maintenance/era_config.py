from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional

from ..paths import DOCS_ROOT
from ..scanner import ERA_FOLDERS


@dataclass(frozen=True)
class EraConfig:
    """Per-era configuration for maintenance helpers."""

    idx: int
    folder: str
    patch_glob: str  # e.g. "3.*.* — *.md"
    minor_glob: str  # e.g. "3.* — *.md"


ERA_CONFIG: Dict[int, EraConfig] = {
    i: EraConfig(
        idx=i,
        folder=ERA_FOLDERS[i],
        patch_glob=f"{i}.*.* — *.md",
        minor_glob=f"{i}.* — *.md",
    )
    for i in range(len(ERA_FOLDERS))
}


def era_dir(era_idx: int) -> Path:
    return DOCS_ROOT / ERA_FOLDERS[era_idx]


def iter_patch_files(era_idx: int) -> Iterable[Path]:
    cfg = ERA_CONFIG[era_idx]
    root = era_dir(era_idx)
    if not root.is_dir():
        return []
    return sorted(root.glob(cfg.patch_glob))


def iter_minor_files(era_idx: int) -> Iterable[Path]:
    cfg = ERA_CONFIG[era_idx]
    root = era_dir(era_idx)
    if not root.is_dir():
        return []
    return sorted(p for p in root.glob(cfg.minor_glob) if " — " in p.name and "." in p.name.split(" ", 1)[0])

