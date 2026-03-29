# Connectra Codebase Analysis (`contact360.io/sync`)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Purpose and role

Connectra is Contact360's search and data-intelligence core for `3.x` contact/company workflows and downstream eras (`4.x`-`10.x`). It provides VQL-powered read APIs, deterministic idempotent upserts, filter metadata hydration, and batch job processing for CSV-based import/export.

## Current architecture snapshot

- **Runtime:** Go 1.24+, Gin HTTP server, Cobra CLI entrypoint.
- **Data plane:** PostgreSQL (`contacts`, `companies`, `jobs`, `filters`, `filters_data`) + Elasticsearch (`contacts_index`, `companies_index`).
- **Read model:** Two-phase query (`VQL -> ES IDs -> PG hydrate -> in-memory join`).
- **Write model:** Parallel fan-out writes (PG+ES for contacts and companies + `filters_data`).
- **Middleware:** CORS -> gzip -> token-bucket rate limiter -> API key auth.
- **API groups:** `/contacts`, `/companies`, `/common`, plus `/health`.
- **Job engine:** Buffered queue with worker pools (`first_time` and `retry`) and state transitions.

## Route surface

- `POST /contacts/`, `POST /contacts/count`, `POST /contacts/batch-upsert`
- `POST /companies/`, `POST /companies/count`, `POST /companies/batch-upsert`
- `POST /common/batch-upsert`, `GET /common/upload-url`
- `POST /common/jobs`, `POST /common/jobs/create`
- `GET|POST /common/:service/filters`, `GET|POST /common/:service/filters/data`
- `GET /health`

## Core mechanics

### VQL and query execution

- `exact` -> `match_phrase` (+ optional `slop`)
- `shuffle` -> `match` (+ fuzzy/operator tuning)
- `substring` -> ngram-backed matching field path
- `keyword_match` and `range_query` support exact and numeric/date boundaries

### Parallel write flow

`BulkUpsertToDb` executes five concurrent stores and joins on `WaitGroup` completion:

1. PG contacts
2. ES contacts
3. PG companies
4. ES companies
5. `filters_data` facet rows

### Job engine

State progression: `OPEN -> IN_QUEUE -> PROCESSING -> COMPLETED|FAILED -> RETRY_IN_QUEUED`.

- Primary runner: `first_time` worker pool
- Retry runner: single worker
- Queue capacity: 1000 buffered channel

### Idempotency and dedup

- Contacts UUID5 key: `firstName + lastName + linkedinURL`
- Companies UUID5 key: `name + linkedinURL`
- Filter facet UUID5 key: `filterKey + service + value`

## Strengths

- Strong throughput profile via goroutines/channel-based concurrency.
- Deterministic IDs enable repeatable batch upserts and conflict-safe retries.
- Two-phase read keeps search relevance in ES and authoritative records in PG.
- `io.Pipe()` streaming model supports large CSV workloads with bounded memory.

## Gaps and risks

- Single in-memory queue can lose pending work on abrupt process crash.
- API key and rate-limit policy need stricter rotation and tenant partitioning.
- `AllowAllOrigins` CORS posture is too broad for hardened environments.
- ES/PG drift detection and reconciliation automation are not first-class.

## Era mapping (`0.x`-`10.x`)

| Era | Connectra concern | Small-task decomposition |
| --- | --- | --- |
| `0.x` | Service bootstrap | API key baseline, index bootstrap scripts, health checks |
| `1.x` | Credit-aware usage | Search/export volume guards and billing event alignment |
| `2.x` | Bulk email pipeline | CSV contract stability, column mapping, stream import/export |
| `3.x` | Core data system | VQL freeze, filter taxonomy, dual-write and dedup integrity |
| `4.x` | Extension/SN ingest | Provenance fields and idempotent sync from SN sources |
| `5.x` | AI workflows | AI-readable attributes and enrichment artifact lookup paths |
| `6.x` | Reliability/scaling | Query P95 SLO, job success SLI, retry/DLQ hardening |
| `7.x` | Deployment governance | RBAC on write/export, audit evidence, tenant isolation |
| `8.x` | Public/private APIs | Versioned REST contracts, partner keys, webhook-ready job events |
| `9.x` | Productization | Quota-aware throttling and connector-safe filter contracts |
| `10.x` | Campaign runtime | Audience query stability, suppression filter compliance, export controls |

## Immediate execution queue

1. Add persistent queue backing for job durability.
2. Add ES-PG reconciliation job and drift diagnostics.
3. Add per-tenant rate limiting and API key scope model.
4. Add contract-parity tests for VQL operators and filter metadata.
5. Add release gates for batch-upsert idempotency evidence.

## Suggested owner map

- **Connectra service owner:** Search/Data Engineering
- **Gateway contract owner:** Appointment360/API team
- **UI contract owner:** Dashboard data-experience team
- **Ops owner:** Platform reliability team

## Release gate checklist

- 📌 Planned: VQL taxonomy changes mirrored in `docs/3. Contact360 contact and company data system/vql-filter-taxonomy.md`.
- 📌 Planned: Endpoint/table bindings updated in `docs/backend/apis/` and `docs/backend/endpoints/*.json`.
- 📌 Planned: ES mapping changes include integration tests for list/count/filter paths.
- 📌 Planned: Batch-upsert contract changes include rollback and replay/idempotency evidence.
- 📌 Planned: `docs/versions.md` and era task-pack docs updated for impacted eras.

## 2026 Gap Register (actionable)

- `SYNC-0.1`: Add request correlation IDs and propagation.
- `SYNC-0.2`: Replace wildcard CORS with env allowlist policy.
- `SYNC-1.x`: Scoped keys + per-tenant rate limiting + usage metering.
- `SYNC-2.4`: Add idempotency support on job-creation paths.
- `SYNC-3.x`: Partner webhook/replay contract and campaign evidence integration.
