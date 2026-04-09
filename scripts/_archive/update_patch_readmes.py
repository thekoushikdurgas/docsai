import re
from pathlib import Path


def minor_re_for_era(era: int) -> re.Pattern[str]:
    # Match: {era}.{minor} — ... .md (NOT patch docs with three numeric components)
    # Minor docs have exactly two numeric segments before the dash: X.Y — ...
    return re.compile(rf"^{era}\.(?P<minor>\d+)\s*[—-]\s*.+\.md$")


def discover_minor_docs(era_dir: Path, era: int) -> list[tuple[int, Path]]:
    era_minor_re = minor_re_for_era(era)
    out: list[tuple[int, Path]] = []
    for p in era_dir.glob("*.md"):
        if p.name == "README.md":
            continue
        if p.name.endswith("x-master-checklist.md"):
            continue
        if p.name.endswith("-task-pack.md") or p.name.endswith("task-pack.md"):
            continue
        m = era_minor_re.match(p.name)
        if not m:
            continue
        minor = int(m.group("minor"))
        out.append((minor, p))
    out.sort(key=lambda t: t[0])
    return out


def replace_or_append_patch_section(readme_path: Path, new_section: str) -> None:
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    if "## Patch documents" not in text:
        out = text.rstrip() + "\n\n" + new_section
        readme_path.write_text(out, encoding="utf-8")
        return

    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Patch documents":
            start = i
            break
    if start is None:
        out = text.rstrip() + "\n\n" + new_section
        readme_path.write_text(out, encoding="utf-8")
        return

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") and lines[j].strip() != "## Patch documents":
            end = j
            break

    out = "\n".join(lines[:start] + new_section.splitlines() + lines[end:]).rstrip() + "\n"
    readme_path.write_text(out, encoding="utf-8")


def main() -> None:
    docs_root = Path("d:/code/ayan/contact/docs")
    for era_dir in sorted(d for d in docs_root.iterdir() if d.is_dir() and "." in d.name):
        prefix = era_dir.name.split(".", 1)[0]
        if not prefix.isdigit():
            continue
        era = int(prefix)
        readme_path = era_dir / "README.md"
        if not readme_path.exists():
            continue

        minor_docs = discover_minor_docs(era_dir, era)
        if not minor_docs:
            continue

        rows: list[str] = []
        for minor, p in minor_docs:
            label = p.name.replace(".md", "")
            rows.append("| `{0}.{1}` | [`{2}`](./{3}#patches) |".format(era, minor, label, p.name))

        new_section = "\n".join(
            [
                "## Patch documents",
                "",
                "| Minor | Patches link |",
                "| --- | --- |",
                *rows,
                "",
            ]
        )
        replace_or_append_patch_section(readme_path, new_section)

    print("readmes_updated")


if __name__ == "__main__":
    main()

