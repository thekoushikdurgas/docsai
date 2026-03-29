# Connectra service — data flow and contracts

**Code:** `contact360.io/sync/` (Go). Gateway calls Connectra via `contact360.io/api/app/clients/connectra_client.py`.

## REST endpoint table

| Endpoint | Purpose | Notes |
| --- | --- | --- |
| `POST /contacts/` | List contacts by VQL | Two-phase read (ES IDs + PG hydrate) |
| `POST /contacts/count` | Count contacts by VQL | ES-only count path |
| `POST /contacts/batch-upsert` | Upsert contacts in bulk | Parallel PG+ES+filter writes |
| `POST /companies/` | List companies by VQL | ES-driven search + PG hydrate |
| `POST /companies/count` | Count companies by VQL | ES-only count path |
| `POST /companies/batch-upsert` | Upsert companies in bulk | Parallel writes and dedup-safe UUID5 |
| `POST /common/batch-upsert` | Cross-entity upsert orchestrator | Coordinates contacts + companies upserts |
| `GET /common/upload-url` | Presigned upload URL helper | Supports large file ingestion flows |
| `POST /common/jobs` | List jobs | Polling/query view for batch jobs |
| `POST /common/jobs/create` | Create job | Starts async processing |
| `GET|POST /common/:service/filters` | Filter definition APIs | Contacts/companies taxonomy source |
| `GET|POST /common/:service/filters/data` | Filter facet value APIs | Backed by `filters_data` |
| `GET /health` | Health probe | liveness/readiness signal |

## Middleware chain

CORS -> gzip -> token-bucket rate limiter -> API key auth.

## Read paths

### `ListByFilters`

1. Build ES query from `VQLQuery` (`ToElasticsearchQuery`).
2. Fetch hits and IDs from ES.
3. Fetch authoritative rows from PG by UUID.
4. Join in-memory preserving ES order.
5. Optionally populate company rows via `company_config.populate`.

### `CountByFilters`

Counts directly in ES (`forCount=true`) to avoid PG hydration overhead.

## Write path (`batch-upsert`)

- Fan-out goroutines persist to PG and ES for contacts and companies.
- Additional facet derivation writes to `filters_data`.
- WaitGroup joins all branches before returning UUID list/error.

## Job engine details

- State model: `OPEN -> IN_QUEUE -> PROCESSING -> COMPLETED|FAILED -> RETRY_IN_QUEUED`.
- Two runners: `first_time` worker pool and single-thread retry runner.
- Buffered channel capacity: 1000.

## Streaming and performance characteristics

| Area | Characteristic |
| --- | --- |
| CSV handling | `io.Pipe` streaming to avoid full in-memory buffering |
| Read path | O(n) hash join after ES ID retrieval |
| Write path | Concurrent multi-store upsert for throughput |
| Stability | Context-aware shutdown and worker synchronization primitives |

## See also

- `docs/3. Contact360 contact and company data system/vql-filter-taxonomy.md`
- `docs/3. Contact360 contact and company data system/enrichment-dedup.md`
