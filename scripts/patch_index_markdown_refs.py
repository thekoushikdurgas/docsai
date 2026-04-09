"""
One-off string patches: replace markdown-era path copy in hub index JSON with JSON-native wording.

Targets files listed in TARGETS (paths relative to docs/).
Run from docs/: python scripts/patch_index_markdown_refs.py
Then re-run normalize_json_sources.py on changed files (or full tree).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_DOCS = Path(__file__).resolve().parent.parent
TARGETS = [
    _DOCS / "index.json",
]


def patch_text(s: str) -> str:
    s = re.sub(r"`(docs/docs/[a-z0-9-]+)\.md`", r"`\1.json`", s)
    s = re.sub(
        r"`(docs/\d+\.[^`]+/)README\.md`",
        r"`\1index.json`",
        s,
    )
    s = s.replace("`docs/docs/CLI_README.md`", "`docs/docs/cli.json`")
    s = s.replace("docs/docs/CLI_README.md", "docs/docs/cli.json")
    s = s.replace("`docs/docs/doc-folder-structure-policy.md`", "`docs/docs/governance.json`")
    s = s.replace("doc-folder-structure-policy.md", "governance.json")
    s = s.replace("STRATEGIC_ERAS_6-10_MASTER_PLAN_five_tracks.md", "errors/STRATEGIC_ERAS_6-10_MASTER_PLAN_five_tracks.json")
    s = s.replace("Canonical markdown hubs", "Canonical policy hubs (typed JSON)")
    s = s.replace("`docs/codebases/*.md`", "`docs/codebases/*.json`")
    s = s.replace("docs/codebases/*.md", "docs/codebases/*.json")
    s = s.replace("path/to/file.md", "path/to/file.json")
    s = s.replace("version — Codename.md", "version — Codename.json")
    s = s.replace("Light prose checks for `backend/endpoints/**/*.md`.", "Light prose checks for `backend/endpoints/**/*.json`.")
    s = s.replace("`python cli.py fill-tasks --file path/to/file.md`", "`python cli.py fill-tasks --file path/to/file.json`")
    s = s.replace(
        "`python cli.py find-duplicate-files [--prefix PATH] [--ext .md,.json]`",
        "`python cli.py find-duplicate-files [--prefix PATH] [--ext .json]`",
    )
    s = s.replace(
        "Sync hubs in the same change set when scope is broad: `architecture.md`, `versions.md`, `audit-compliance.md`, `docsai-sync.md` as per `docs/governance.md`.",
        "Sync hubs in the same change set when scope is broad: `docs/docs/architecture.json`, `versions.json`, `audit-compliance.json`, `docsai-sync.json` as per `docs/docs/governance.json`.",
    )
    s = s.replace("Refresh endpoint link blocks in `frontend/pages/*_page.md`.", "Refresh endpoint link blocks in `frontend/pages/*_page.json`.")
    s = s.replace("open `docs/versions.md`", "open `docs/docs/versions.json`")
    s = s.replace("`docs/versions.md`", "`docs/docs/versions.json`")
    s = s.replace("`docs/roadmap.md`", "`docs/docs/roadmap.json`")
    s = s.replace("`docs/audit-compliance.md`", "`docs/docs/audit-compliance.json`")
    s = s.replace("Verify compliance: `docs/audit-compliance.md`", "Verify compliance: `docs/docs/audit-compliance.json`")
    s = s.replace("Sync DocsAI constants per `docs/docsai-sync.md`", "Sync DocsAI constants per `docs/docs/docsai-sync.json`")
    s = s.replace("record release evidence in `docs/versions.md`", "record release evidence in `docs/docs/versions.json`")
    s = s.replace("From `docs/roadmap.md` and `docs/versions.md`", "From `docs/docs/roadmap.json` and `docs/docs/versions.json`")
    s = s.replace(
        "Long-form risk registers and era tasks live in **`docs/codebases/*-codebase-analysis.md`**",
        "Long-form risk registers and era tasks live in **`docs/codebases/*-codebase-analysis.json`**",
    )
    s = s.replace("run `era-guide --era N`; open era `README.md`", "run `era-guide --era N`; open era `index.json`")
    s = s.replace("era’s `README.md`", "era’s `index.json`")
    s = s.replace("open that era’s `README.md`", "open that era’s `index.json`")
    s = s.replace("active `X.Y.Z — …md`", "active `X.Y.Z — ….json`")
    s = s.replace("Work is planned in **every** era directory `docs/<0–10>. …/`, not only in `README.md`", "Work is planned in **every** era directory `docs/<0–10>. …/`, anchored by each folder’s `index.json`")
    s = s.replace("`X.Y.0 — …` (minor)", "`X.Y.0 — ….json` (minor)")
    s = s.replace("`X.Y.Z — …` (patch)", "`X.Y.Z — ….json` (patch)")
    s = re.sub(
        r"`(docs/(?:backend|frontend|codebases|commands|promsts)(?:/[^`]+)?/)README\.md`",
        r"`\1index.json`",
        s,
    )
    s = s.replace("CLI_README.md", "cli.json")
    s = re.sub(r"`README\.md`", "`index.json`", s)
    s = s.replace(
        "`hub`, `era_task`, `frontend_page` (tree layout), or prose: `backend_api`, `endpoint_md`, `codebase_analysis`",
        "`hub`, `era_task`, `page_spec` (tree layout), or `graphql_module`, `endpoint_matrix`, `document`",
    )
    return s


def patch_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    new = patch_text(raw)
    if new == raw:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    n = 0
    for path in TARGETS:
        if not path.exists():
            print(f"skip missing {path}", file=sys.stderr)
            continue
        if patch_file(path):
            print(f"patched {path.relative_to(_DOCS)}")
            n += 1
        else:
            print(f"unchanged {path.relative_to(_DOCS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
