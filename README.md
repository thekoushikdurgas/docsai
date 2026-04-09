# Contact360 Docs Hub

Machine-readable documentation for Contact360 is **typed JSON** under `docs/` (`schema_version` + `kind`), with **SQL** under `docs/backend/database/`, **Postman** exports under `docs/backend/postman/`, and JSON Schemas under `docs/json_schemas/`.

## Layout

| Area | Role |
| --- | --- |
| `docs/docs/*.json` | Policy hubs (architecture, roadmap, versions, governance, …) |
| `docs/0. …` – `docs/10. …` | Era execution docs (`index.json` + task JSON per minor/patch) |
| `docs/backend/` | GraphQL modules, endpoint matrices, database SQL/CSV, Postman |
| `docs/frontend/` | Page specs (`*_page.json`), design references |
| `docs/codebases/`, `docs/commands/`, `docs/promsts/`, `docs/tech/` | Analyses, command matrix, prompts, stack checklists |
| `docs/json_schemas/` | Envelope + per-`kind` JSON Schema |
| `docs/manifest.json` | Aggregate index (`python scripts/build_manifest.py`) |

Each typed file may include `raw_markdown` / `non_parsed_raw_markdown` only when needed for gap tracking or RAG; many docs omit `raw_markdown` when `non_parsed_raw_markdown` is empty. Envelope `source_path` is the path to that **`.json`** file under `docs/`; `sha256_source` fingerprints the document (see `scripts/normalize_json_sources.py`).

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

1. `python scripts/generate_indexes.py` — refresh `children[]` on each `index.json`.
2. `python scripts/build_manifest.py` — rebuild `docs/manifest.json`.
3. `python scripts/validate_migration.py` — envelopes, era indexes, manifest parity, era_task tracks.

After bulk edits to envelope metadata: `python scripts/normalize_json_sources.py`.

## Pinecone / RAG

`python cli.py pinecone ingest-docs` runs `scripts/pinecone_integration/ingest_docs.py`, which chunks **typed JSON** only (`raw_markdown` when present, else structured text flattening). Configure indexes in `.env` (see `.env.example`).

## Related repos

Product code under `contact360.io/`; DocsAI mirrors may read constants in `contact360.io/admin/apps/*/constants.py` — update those when hub **content** changes.

Legacy markdown conversion scripts live under `docs/scripts/_archive/` for reference only.
