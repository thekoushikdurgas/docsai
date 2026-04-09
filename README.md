# Contact360 Docs Hub

Machine-readable documentation for Contact360 lives as **typed JSON** under `docs/`, alongside **SQL** (`docs/backend/database/`), **Postman** exports (`docs/backend/postman/`), and other assets. Human-readable prose is preserved in each document’s `raw_markdown` field.

Each typed file also includes **`non_parsed_raw_markdown`**: YAML front matter (if any) plus body paragraphs whose text is **not** found inside a concatenation of structured string fields (title, section prose, table cells, task lines, etc.). It is **heuristic**—use it to spot gaps between source markdown and JSON, not as a second canonical copy. Recompute with `python scripts/backfill_non_parsed_raw_markdown.py` after large edits (or rely on `convert_md_to_json.py`, which sets it on new conversions).

## Layout

| Area | Role |
| --- | --- |
| `docs/docs/*.json` | Policy hubs (architecture, roadmap, versions, audit, governance, …) |
| `docs/0. …` – `docs/10. …` | Era execution docs (`index.json` + task JSON per minor/patch) |
| `docs/backend/` | GraphQL modules, endpoint matrices, database SQL/CSV, Postman |
| `docs/frontend/` | Page specs, design references, inventories |
| `docs/codebases/`, `docs/commands/`, `docs/promsts/`, `docs/tech/` | Deep dives, command matrix, prompts, stack checklists |
| `docs/json_schemas/` | JSON Schema for envelope + per-`kind` shapes |
| `docs/manifest.json` | Aggregate index of all typed JSON (run `build_manifest.py`) |

Optional **legacy** markdown (e.g. vendor READMEs) may still appear; the CLI and validators target **typed JSON** only (`schema_version` + `kind`).

## CLI (from `docs/`)

```bash
python cli.py scan
python cli.py stats --era 0
python cli.py audit-tasks --era 1
python cli.py validate-all
python cli.py validate-all --json-schema
python cli.py migrate full          # indexes → manifest → validate_migration
```

Interactive menu: `python main.py`.

## Maintenance pipeline

1. **`python scripts/generate_indexes.py`** — refresh `children[]` on each `index.json`.
2. **`python scripts/build_manifest.py`** — rebuild `docs/manifest.json`.
3. **`python scripts/validate_migration.py`** — envelope checks, era `index.json`, manifest parity, era_task tracks.

Legacy: `migrate archive` / `migrate convert` if you still import `.md` via `convert_md_to_json.py`.

## Pinecone / RAG

`python cli.py pinecone ingest-docs` runs `scripts/pinecone_integration/ingest_docs.py`, which chunks **`raw_markdown`** from typed JSON (and still accepts `.md` if present). Configure indexes in `.env` (see `.env.example`).

## CI

`.github/workflows/ci.yml` asserts core hub JSON files and `docs/manifest.json` exist.

## Related repos

Product code under `contact360.io/`; DocsAI mirrors may still read constants in `contact360.io/admin/apps/*/constants.py` — update those when hub **content** changes, even if the source file is now JSON in `docs/docs/`.
