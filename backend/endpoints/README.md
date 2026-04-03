# Backend Endpoints Metadata

Endpoint metadata and parity-tracking guide for backend API surfaces.

## Scope

- Service-level era matrices (`*_endpoint_era_matrix.json`).
- Operation-level endpoint JSON files for GraphQL and REST routes.
- Aggregated inventory via `endpoints_index.json`.
- **Markdown views** (generated): all JSON above is mirrored under [`md/`](md/README.md) for reading in-repo and in doc portals. Regenerate with `python json_to_markdown_endpoints.py` from this folder.

## Folder reality snapshot

- This folder currently tracks a large endpoint inventory with both GraphQL and REST metadata.
- Service-era matrix files exist for core services (`appointment360`, `connectra`, `jobs`, `emailapis`, `contact_ai`, `salesnavigator`, `mailvetter`, `s3storage`, `logsapi`, `emailcampaign`, `admin`, `emailapp`).
- `endpoints_index.json` lists these matrices under `supplemental_indexes` (including `contact_ai_endpoint_era_matrix.json` and `salesnavigator_endpoint_era_matrix.json`) alongside the aggregated GraphQL inventory.
- Endpoint-level files are release-gate artifacts and must stay in parity with runtime contracts.

## Extension FastAPI (ingest) — `contact360.extension`

- REST: `POST /v1/save-profiles`, `POST /v1/scrape` (see [contact360.extension/app/api/v1/endpoints/scrape.py](../../contact360.extension/app/api/v1/endpoints/scrape.py)). Track alongside `salesnavigator` / `extension` era matrices when enriching request metadata (`extension_trace_id`, `scrape_mode`).

## Parity with `docs/codebases/`

- Registry: [docs/backend/README.md](../README.md#codebase-analysis-registry) maps each codebase analysis to matrices and GraphQL operation JSON here.
- When a matrix or `mutation_*` / `query_*` JSON changes, update the matching `docs/codebases/*-codebase-analysis.md` **contract / dependency** sections if behavior, auth, or era ownership shifted.

| Matrix file | Typical codebase analysis |
| --- | --- |
| `appointment360_endpoint_era_matrix.json` | `appointment360-codebase-analysis.md`, `app-codebase-analysis.md` |
| `connectra_endpoint_era_matrix.json` | `sync-codebase-analysis.md`, `connectra-codebase-analysis.md` |
| `jobs_endpoint_era_matrix.json` | `jobs-codebase-analysis.md` |
| `emailapis_endpoint_era_matrix.json` | `emailapis-codebase-analysis.md` |
| `s3storage_endpoint_era_matrix.json` | `s3storage-codebase-analysis.md` |
| `logsapi_endpoint_era_matrix.json` | `logsapi-codebase-analysis.md` |
| `contact_ai_endpoint_era_matrix.json` | `contact-ai-codebase-analysis.md` |
| `salesnavigator_endpoint_era_matrix.json` | `salesnavigator-codebase-analysis.md`, `extension-codebase-analysis.md` |
| `mailvetter_endpoint_era_matrix.json` | `mailvetter-codebase-analysis.md` |
| `emailcampaign_endpoint_era_matrix.json` | `emailcampaign-codebase-analysis.md` |
| `emailapp_endpoint_era_matrix.json` | `email-codebase-analysis.md` (Mailhub `contact360.io/email` REST consumer) |

## Why this matters

- Release gates rely on endpoint metadata consistency.
- Auth, RBAC, rate-limit, and lineage fields are compliance-critical.
- Frontend binding and backend module docs depend on this folder.

## Update protocol

1. Locate impacted endpoint JSON files.
2. Update contract and metadata fields (`era`, `introduced_in`, `deprecated_in`).
3. Verify security fields (`auth_required`, `rbac_roles`, rate-limit flags).
4. Update lineage fields (`db_tables_read`, `db_tables_write`, storage touchpoints).
5. Sync related docs (`graphql.modules`, `database`, `postman`, and frontend bindings).

## Topology & database linking (read next)

Keep **generated** artifacts (`index.md`, `endpoints_index.md`, `*_endpoint_era_matrix.md`, per-operation `*_graphql.md`) as produced by `json_to_markdown_endpoints.py`. For **human-authored** navigation, use these two hubs:

- **[SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)** — service registry (gateway, Connectra, workers), request-flow diagram, links from each surface to its era matrix and **data lineage** doc.
- **[ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)** — how GraphQL ops map to `index.md`, how `db_tables_read` / `db_tables_write` reference gateway snapshots vs **Connectra-owned** stores (`connectra_data_lineage.md`), and conventions for external stores.

Do **not** fold the full topology or linking spec into this README; that duplicates the hubs and goes stale. Summaries above are intentionally short.

## Markdown generation (JSON → MD)

1. **Inventory:** `json_to_markdown_endpoints.py` reads every `*.json` here (except none by default).
2. **Classify:** operation specs (`endpoint_id`), era matrices (`*_endpoint_era_matrix.json` or `route_groups` / `module_index` / `graphql_modules`), `endpoints_index.json`, `index.json`, or generic fallback.
3. **Emit:** `md/<basename>.md` — tables for identity, security, consumers; fenced blocks for GraphQL; era matrices expanded to navigable sections.
4. **Verify:** open [md/endpoints_index.md](md/endpoints_index.md) and spot-check a few operation files after JSON edits.

## Small-task breakdown

- `Task 1 - Inventory`: confirm endpoint naming and canonical path.
- `Task 2 - Contract`: validate request/response/error shapes.
- `Task 3 - Security`: validate auth/rbac/rate-limit policy metadata.
- `Task 4 - Lineage`: update data read/write and artifact metadata.
- `Task 5 - Parity`: validate parity against runtime and module docs.
- `Task 6 - Evidence`: include endpoint diff in release evidence pack.

## EC2 Go satellite HTTP inventory

Canonical route list for **`EC2/*.server/`** implementations (Gin, not yet fully mirrored in JSON matrices): **[EC2_GO_SATELLITE_ROUTES.md](EC2_GO_SATELLITE_ROUTES.md)**. When Go cutover is scheduled for a service, update the matching `*_endpoint_era_matrix.json` and regenerate markdown per **Markdown generation** above.

## Cross-links

- `docs/README.md`
- `docs/backend/README.md`
- `docs/codebases/README.md`
- `docs/backend/graphql.modules/README.md`
- `docs/backend/database/README.md`
- `docs/backend/postman/README.md`
