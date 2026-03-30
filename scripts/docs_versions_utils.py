"""
Shared utilities for Contact360 docs "version file" renaming.

This project uses a convention:
  - Old:   version_X.Y.md
  - New:   X.Y — <Title>.md

The "Title" is sourced from the file header and/or a `Codename:` field.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


NON_WIN_FILENAME_CHARS = r'<>:"/\\|?*'

# U+2014 em dash, matches existing docs filenames (e.g. "2.0 — Email Foundation.md")
DASH = "—"


@dataclass(frozen=True)
class VersionRef:
    era: int
    minor: int

    @property
    def old_base(self) -> str:
        return f"version_{self.era}.{self.minor}.md"

    @property
    def new_prefix(self) -> str:
        # The numeric part must retain X.Y dots.
        return f"{self.era}.{self.minor}"


def parse_old_version_filename(filename: str) -> Optional[VersionRef]:
    """
    Parse filenames like: version_2.10.md
    """
    m = re.match(r"^version_(\d+)\.(\d+)\.md$", filename)
    if not m:
        return None
    return VersionRef(era=int(m.group(1)), minor=int(m.group(2)))


def sanitize_title_for_filename(title: str) -> str:
    """
    Make a title safe for Windows filenames while following the project's rule:
    - Keep dots only in the X.Y numeric prefix (handled elsewhere).
    - Remove dots from the title portion.
    """
    title = title.strip()
    # Remove common markdown decoration that can leak from extracted summaries.
    title = title.replace("*", "").replace("`", "").strip()

    # Project-specific rule: "so no ." in codename/title part.
    title = title.replace(".", "")

    # Replace forward slashes (historically present) to avoid path-like titles.
    title = title.replace("/", "-").replace("\\", "-")

    # Remove other characters invalid on Windows filenames.
    # (We replace them rather than deleting to keep word boundaries.)
    title = re.sub(f"[{re.escape(NON_WIN_FILENAME_CHARS)}]", "-", title)

    # Collapse repeated whitespace/hyphens.
    title = re.sub(r"\s+", " ", title)
    title = re.sub(r"-{2,}", "-", title).strip(" -")
    return title


_HEADER_RE = re.compile(r"^#\s*Version\s+(\d+)\.(\d+)\s*(?:—|-)\s*(.+?)\s*$")
_CODENAME_BULLET_RE = re.compile(
    r"^\s*-\s*(?:\*\*)?Codename(?:\*\*)?\s*:\s*(.+?)\s*$",
    re.IGNORECASE,
)
_CODENAME_KEYVALUE_RE = re.compile(r"Codename\s*:\s*(.+)")
_SUMMARY_BULLET_RE = re.compile(
    r"^\s*-\s*(?:\*\*)?Summary(?:\*\*)?\s*:\s*(.+?)\s*$",
    re.IGNORECASE,
)


def extract_title_from_version_file(text: str, era: int, minor: int) -> Optional[str]:
    """
    Extract the title/codename for a `version_X.Y.md` file.

    Tries in order:
    1) H1 header: "# Version 2.0 — Email Foundation"
    2) Bullet field: "- **Codename:** Email Foundation"
    3) Any line containing "Codename:" as a fallback.
    """
    # 1) Header
    for line in text.splitlines():
        line = line.rstrip("\n")
        m = _HEADER_RE.match(line)
        if m:
            e = int(m.group(1))
            n = int(m.group(2))
            if e == era and n == minor:
                return m.group(3).strip()

    # 2) Codename bullet field
    for line in text.splitlines():
        m = _CODENAME_BULLET_RE.match(line)
        if m:
            return m.group(1).strip()

    # 3) Fallback: any "Codename:" mention
    for line in text.splitlines():
        if "Codename" in line:
            m = _CODENAME_KEYVALUE_RE.search(line)
            if m:
                return m.group(1).strip()

    # 4) Fallback: derive from the first Summary sentence.
    # Many older templates use: "- **Summary:** <Title> — <rest of summary>"
    for line in text.splitlines():
        m = _SUMMARY_BULLET_RE.match(line)
        if not m:
            continue
        summary = m.group(1).strip()
        # Take the left side before the first em dash if present.
        if "—" in summary:
            left = summary.split("—", 1)[0].strip()
            if left:
                return left
        # Otherwise, take up to the first period (if any).
        if "." in summary:
            left = summary.split(".", 1)[0].strip()
            if left:
                return left
        # Last resort: use whole summary line.
        if summary:
            return summary

    return None


def compute_new_filename(era: int, minor: int, raw_title: str) -> str:
    title = sanitize_title_for_filename(raw_title)
    if not title:
        title = "Untitled"
    return f"{era}.{minor} {DASH} {title}.md"


def iter_markdown_files(root: Path) -> list[Path]:
    # We avoid external deps and keep it predictable.
    out: list[Path] = []
    for p in root.rglob("*.md"):
        if p.is_file():
            out.append(p)
    return out

