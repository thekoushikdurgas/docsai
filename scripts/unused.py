from __future__ import annotations

from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parent.parent

IGNORED_DIRS = {
    "__pycache__",
    "scripts",
    ".git",
    "venv",
    "ideas",
    "backend/postman",
    ".pytest_cache",
}
IGNORED_FILES = {
    "README.md",
    "main.py",
    "cli.py",
}


def get_all_files() -> list[Path]:
    """Get all non-ignored files in the docs directory."""
    all_files = []
    for path in DOCS_ROOT.rglob("*"):
        if not path.is_file():
            continue
        # Check if it's in an ignored directory
        rel_path_posix = path.relative_to(DOCS_ROOT).as_posix()
        in_ignored_dir = any(
            rel_path_posix == ignored or rel_path_posix.startswith(ignored + "/")
            for ignored in IGNORED_DIRS
        )
        if in_ignored_dir:
            continue
        if path.name in IGNORED_FILES:
            continue
        all_files.append(path)
    return all_files


def get_all_markdown_contents() -> list[str]:
    """Get contents of all markdown files to search for references."""
    contents = []
    for path in DOCS_ROOT.rglob("*.md"):
        rel_path_posix = path.relative_to(DOCS_ROOT).as_posix()
        in_ignored_dir = any(
            rel_path_posix == ignored or rel_path_posix.startswith(ignored + "/")
            for ignored in IGNORED_DIRS
        )
        if in_ignored_dir:
            continue
        try:
            contents.append(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return contents


def find_unused_files() -> list[Path]:
    """Find all files that are not referenced in any markdown file."""
    all_files = get_all_files()
    contents = get_all_markdown_contents()
    
    unused_files = []
    for file_path in all_files:
        is_used = False
        filename = file_path.name
        
        # Heuristic: is the exact filename present in any of the markdown contents?
        for content in contents:
            if filename in content:
                is_used = True
                break
        
        if not is_used:
            unused_files.append(file_path)
            
    return sorted(unused_files)
