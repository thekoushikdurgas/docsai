# Backend Service API Docs

Service-scoped API documentation index for standalone backend services.

## Current files

**Gateway & data plane**

- `appointment360.api.md` — `contact360.io/api` GraphQL gateway
- `connectra.api.md` — `contact360.io/sync` (contacts/companies/VQL)
- `jobs.api.md` — async jobs (email.server + sync.server; gateway `scheduler_jobs`)

**Workers & integrations**

- `s3storage.api.md` — object storage / presigned flows
- `logsapi.api.md` — `logs.api` ingest
- `emailapis.api.md` — `lambda/emailapis` + `lambda/emailapigo` (finder/verify family)

**Product services (REST or mixed)**

- `admin.api.md` — `contact360.io/admin`
- `contact.ai.api.md` — Contact AI Lambda HTTP/SSE
- `mailvetter.api.md` (canonical filename; supersedes legacy `mailvaiter` spelling)
- `salesnavigator.api.md`
- `emailcampaign.api.md` (REST campaign service index; deep contract still in `graphql.modules/` + matrices)

## Scope

- Documents service-local routes, auth models, payload contracts, and ops notes.
- Complements (not replaces) `docs/backend/graphql.modules/` module docs and endpoint matrices.

## Linking to `docs/backend/endpoints/`

Every `*.api.md` includes:

- **[endpoints/README.md](../endpoints/README.md)** — how operation JSON, `endpoints_index.json`, and matrices are organized.
- **[endpoints/endpoints_index.md](../endpoints/endpoints_index.md)** — master inventory (GraphQL `*_graphql.md` links + supplemental `*_endpoint_era_matrix.md` entries).
- **[endpoints/index.md](../endpoints/index.md)** — canonical **`graphql/OperationName` → file** map for the gateway (use with [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md)).
- **Service era matrix** — `../endpoints/<service>_endpoint_era_matrix.md` (same basename as `*.json` in that folder).

Trace **delegation** from gateway specs: open the relevant `*_graphql.md` and read **`lambda_services`** / **`db_tables_*`** to see which worker (this service) is called.

## Parity with `docs/codebases/`

- Registry: [docs/backend/README.md](../README.md#codebase-analysis-registry) — each row lists `micro.services.apis/*.md` where it applies.
- Each `*.api.md` should cross-link [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md), [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md), the service’s `*_endpoint_era_matrix.md`, and `*_data_lineage.md` where applicable.
- Deep route-level detail may still live in `docs/backend/graphql.modules/`, `docs/codebases/*-codebase-analysis.md`, and Postman folders—keep this directory as the **service hub** and navigation layer.

## Update protocol

1. Validate runtime service routes and auth behavior.
2. Update service API doc sections (request/response/error).
3. Sync endpoint matrix entries in `docs/backend/endpoints/`.
4. Sync lineage references in `docs/backend/database/`.
5. Sync Postman artifacts where route behavior changed.

## Small-task breakdown

- `Task 1 - Contract`: validate route/auth/payload details.
- `Task 2 - Runtime`: verify docs against implementation and deploy config.
- `Task 3 - Era`: align stage/era references with roadmap and versions.
- `Task 4 - Data`: align ownership and lineage references.
- `Task 5 - Validation`: ensure endpoint and Postman parity.
- `Task 6 - Evidence`: add proof notes for release gate packets.

## Cross-links

- `docs/README.md`
- `docs/backend/README.md`
- `docs/codebases/README.md`
- `docs/backend/graphql.modules/README.md`
- `docs/backend/endpoints/README.md`
- `docs/backend/database/README.md`
