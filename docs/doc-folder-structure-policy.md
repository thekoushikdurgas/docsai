# Doc folder structure policy (Contact360)

Canonical policy hubs live under **`docs/docs/`** (this directory). Era execution docs live under **`docs/<0–10>. …/`** as flat `*.md` files.

## Standard README sections (subfolders under `docs/`)

Each major subtree should maintain a **README.md** with:

1. **Scope** — What the folder is for.
2. **Naming convention** — Filename patterns and link to `python cli.py name-audit` for era folders.
3. **Structure contract** — Required sections or formats (JSON schema pointers for machine artifacts).
4. **Index** — Table of key files or pointer to generated indexes (`endpoints_index.json`, etc.).
5. **Cross-links** — Parent hub [`docs/README.md`](../README.md), related `docs/codebases/` analyses.

## Structure model — folder inventory (Phase 1)

**Canonical Python module:** [`docs/scripts/doc_structure.py`](../scripts/doc_structure.py) defines `DocKind`, `ValidationFinding`, and `classify_path()` / `validate_file()` / `iter_paths_for_validation()`.

The dataclass **`StructureSpec`** (required sections / front matter / name pattern per kind) is **reserved for a future data-driven layer**; validators today are **hand-coded** per kind (`_hub_validator`, `_era_task_validator`, `_frontend_page_validator`, `_prose_markdown_validator` for backend/endpoints/codebases prose).

### Matrix: subtree → `DocKind` → automated checks

| Area | Path glob (under `docs/`) | `DocKind` | Structure validated? | Notes |
| --- | --- | --- | --- | --- |
| Policy hubs | `docs/*.md` | `hub` | **Yes** | Top-level `#`, minimum length; see `_hub_validator` |
| Version hub | `VERSION Contact360.md` (root) | `hub` | **Yes** | Same rule as other `docs/*.md` |
| Era execution | `<0–10>. …/*.md` | `era_task` | **Yes** (patch/minor) | `README.md` skipped; versioned files need `## Tasks` or `## Task tracks` + track subsections; see `_era_task_validator` |
| Frontend specs | `frontend/pages/*_page.md` | `frontend_page` | **Yes** | YAML front matter (`title`, `page_id`), `## Overview`; see `_frontend_page_validator` |
| Backend API prose | `backend/apis/**/*.md` | `backend_api` | **Yes (light)** | Top-level `#`, minimum length; `_prose_markdown_validator` |
| Endpoint detail | `backend/endpoints/**/*.md` | `endpoint_md` | **Yes (light)** | Same light prose checks |
| Endpoint machine | `backend/endpoints/**/*.json` | `endpoint_json` | **No** | Often generated; validate JSON elsewhere if needed |
| Codebase analyses | `codebases/**/*.md` | `codebase_analysis` | **Yes (light)** | Same light prose checks |
| Docs tooling | `scripts/**/*.py` | `tooling_script` | **No** | Not markdown; use linters / tests for Python |
| Analysis notes | `analysis/**/*.md` | `other` | **No** | Optional future kind |
| Flowcharts | `flowchart/**` | `other` | **No** | |
| Plans | `plans/**` | `other` | **No** | Often scratch / CI artifacts |
| Tech | `tech/**` | `other` | **No** | |
| Frontend (non-page) | `frontend/docs/**`, `frontend/excel/**` | `other` (typical) | **No** | `*.md` not matching `*_page.md` |
| Commands / prompts | `docs/commands/**`, `docs/promsts/**` | `other` | **No** | |

### Exceptions (usually excluded or special-cased)

| Location | Reason |
| --- | --- |
| `docs/result/*.json`, `docs/errors/*.json` | Output of `validate-all` / `format-all --write-latest`; gitignored by policy; not hub markdown |
| `docs/scripts/__pycache__`, `.git` | Not content |
| `backend/postman/*.json` | Collections/environments; not era docs |
| Large binaries / exports | Duplicate/unused tooling skips huge files |

### Phase 2 (implemented)

- **`backend_api`**, **`endpoint_md`**, **`codebase_analysis`**: light markdown checks (heading + length); CLI `--kind backend_api|endpoint_md|codebase_analysis` scans default prefixes (`backend/apis`, `backend/endpoints`, `codebases`).
- **`validate-all`** still focuses on hub + era + frontend structure + task/naming audits; run **`validate-structure --kind …`** for backend/codebase prose in CI if desired.

### Next steps (Phase 3+)

1. Drive **`StructureSpec`** from JSON/YAML **or** add stricter section-based rules per subtree README contract.
2. Stricter **`endpoint_json`** / schema checks (optional).
3. Expand unit tests under `docs/scripts/tests/`.

## Validation

Run from `docs/`:

```bash
python cli.py validate-structure --prefix docs/docs
python cli.py validate-structure --era 1 --kind era_task
python cli.py validate-structure --prefix frontend/pages --kind frontend_page
python cli.py validate-structure --kind backend_api
python cli.py validate-structure --kind endpoint_md
python cli.py validate-structure --kind codebase_analysis
```

### Full-tree JSON (`validate-all`)

```bash
python cli.py validate-all                  # print summary only
python cli.py validate-all --write-latest    # write docs/result/*.json and docs/errors/*.json
python cli.py validate-all --skip-tasks      # structure + naming only
python cli.py validate-all --skip-naming
```

**Schema (version 1)** — object written to `docs/result/latest.json`:

| Field | Type | Description |
| --- | --- | --- |
| `schema_version` | int | `1` |
| `tool` | string | `contact360-docs-validate` |
| `started_at` / `finished_at` | string | ISO-8601 UTC |
| `docs_root` | string | Absolute path to `docs/` |
| `invocation` | object | CLI flags used (`write_latest`, `include_tasks`, …) |
| `summary` | object | `files_scanned`, `errors`, `warnings`, `total_findings` |
| `findings` | array | Each item: `path`, `kind`, `severity` (`error`|`warning`), `rule_id`, `message`, `line` (nullable) |

`docs/errors/latest.json` uses the same shape but `findings` contains **errors only** and summary counts reflect that.

## Formatting (pairs with validation)

**Module:** [`docs/scripts/doc_format.py`](../scripts/doc_format.py) — LF newlines, trim trailing whitespace on each line, single trailing newline. Does not reflow paragraphs or reorder headings.

| Command | Scope | Notes |
| --- | --- | --- |
| `format-structure` | Same flags as `validate-structure` (`--prefix`, `--era`, `--kind`) | Default **dry-run** (lists paths that would change); add **`--apply`** to write. |
| `format-all` | Same markdown trees as `validate-all` structure scan (hubs + era tasks + frontend pages) | Optional **`--include-prose`** to add `backend/apis`, `backend/endpoints/*.md`, `codebases/*.md`. **`--write-latest`** writes `docs/result/format-latest.json` (+ timestamped `format-*.json`). |

```bash
python cli.py format-structure --kind backend_api          # dry-run
python cli.py format-structure --kind backend_api --apply
python cli.py format-all --apply
python cli.py format-all --apply --include-prose --write-latest
```

### Command catalog

```bash
python cli.py list
python cli.py list --json --category docs
python cli.py ls --include-scripts
```

## Maintenance entry points

- **Era batch scripts:** `python cli.py maintain-era --era N --action enrich|fix-readme-links|update-minors [--apply|--dry-run]`
- **Aggregate health:** `python cli.py optimize-docs report`
- **Interactive:** `python main.py` (Contact360 Docs Agent menu) — section **B** includes **B7–B9** (validate prose) and **B10–B11** (`format-structure` / `format-all`).
