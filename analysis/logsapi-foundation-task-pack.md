# logs.api task pack — era `0.x` (`lambda/logs.api`)

This pack decomposes **`lambda/logs.api`** work into Contract, Service, Surface, Data, and Ops tracks for foundation-era logging and query baseline.

| Track | Owner (default) | Priority |
| --- | --- | --- |
| Contract | Platform + security | P0 |
| Service | Backend (logs service) | P0 |
| Surface | DocsAI / admin docs | P1 |
| Data | Platform | P0 |
| Ops | Platform / DevOps | P0 |

## Contract tasks

- Define and freeze **`0.x`** log **event envelope** (required fields, optional metadata, versioning if any). (patch assignment: `0.3.0`–`0.3.2`)
- Update **`docs/backend/endpoints/logsapi_endpoint_era_matrix.json`** for `0.x` read/write/query routes. (patch assignment: `0.3.0`–`0.3.2`)
- Confirm **auth** model for write vs query (API key, internal network, future tenant scope) and document in `lambda/logs.api/docs/api.md`. (patch assignment: `0.3.0`–`0.3.2`)

## Service tasks

- Validate/implement service behavior for **`0.x`** event sources (gateway, jobs, selected Lambdas) and minimal query filters. (patch assignment: `0.3.0`–`0.3.2`)
- Verify **error envelope** and **health** behavior for consumers (`/health` or equivalent). (patch assignment: `0.3.0`–`0.3.2`)
- Align with **correlation**: `request_id`, `trace_id` propagation expectations from `contact360.io/api` middleware where applicable. (patch assignment: `0.3.0`–`0.3.2`)

## Surface tasks

- Confirm that there is **no product log-query UI** in `0.x` (no dashboard routes for log browsing). (patch assignment: `0.3.3`–`0.3.6`)
- Only provide health smoke via a `healthService` stub / wiring for logging service connectivity checks. (patch assignment: `0.3.3`–`0.3.6`)
- If admin/DocsAI tooling exists in your repo, document it as “admin-only (0.x)” and defer customer UI to later minors. (patch assignment: `0.3.3`–`0.3.6`)

## Data tasks

- Document **S3 CSV** layout, **prefix** (`logs/` or as implemented), **retention** policy target for `0.x`. (patch assignment: `0.3.0`–`0.3.2`)
- Record **query window** defaults (e.g. last N days) and performance expectations. (patch assignment: `0.3.0`–`0.3.2`)
- Cross-link **`docs/backend/database/logsapi_data_lineage.md`**; explicitly **no MongoDB** as canonical logs store. (patch assignment: `0.3.0`–`0.3.2`)

## Ops tasks

- Add **observability**: error rate, write lag, S3 upload failures (whatever is available in `0.x`). (patch assignment: `0.3.0`–`0.3.2`)
- Add **release validation** checklist for logging-impacting deploys. (patch assignment: `0.3.7`–`0.3.9`)
- Capture **rollback** note: disabling new writers vs replaying failed batches. (patch assignment: `0.3.3`–`0.3.6`)

## Release gate evidence (`0.x`)

- [ ] Sample write + read round-trip with redacted payload attached (patch assignment: `0.3.7`–`0.3.9`)
- [ ] Contract snippet or OpenAPI/README excerpt updated (patch assignment: `0.3.7`–`0.3.9`)
- [ ] Retention and PII handling sentence in `docs/audit-compliance.md` or service doc if behavior changes (patch assignment: `0.3.7`–`0.3.9`)

---

## Canonical persistence: **S3 CSV** (not MongoDB)

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Purge stale **MongoDB** references from internal docs / READMEs | P0 | Align with `0.x-master-checklist.md` | `0.3.0`–`0.3.2` |
| Cross-link [`docs/backend/database/logsapi_data_lineage.md`](../backend/database/logsapi_data_lineage.md) and `lambda/logs.api/docs/api.md` in PR template | P0 | | `0.3.0`–`0.3.2` |
| Writer path: explicit **bucket + prefix** per env in `.env.example` | P0 | | `0.3.0`–`0.3.2` |

## Static API key rotation

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Document single writer vs reader keys if split | P0 | Analysis: static key risk | `0.3.0`–`0.3.2` |
| Rotation runbook: dual-key acceptance window → retire old key | P0 | | `0.3.0`–`0.3.2` |
| No key in client-side dashboard bundles | P0 | Gateway-only writes in prod | `0.3.0`–`0.3.2` |

## Query scalability baseline

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Pagination contract: `limit` / `cursor` / `next_page_token` — **hard caps** | P0 | | `0.3.0`–`0.3.2` |
| Default **time window** for queries; document Big-O / scan avoidance | P0 | | `0.3.0`–`0.3.2` |
| Optional index manifest if metadata DB or auxiliary index is introduced | P1 | | `0.3.3`–`0.3.6` |

## Cache consistency and compliance

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| If in-memory cache used for reads: TTL + **invalidate on write** policy | P0 | Analysis: cache consistency | `0.3.0`–`0.3.2` |
| PII in log body fields — classification + redaction rules (`audit-compliance.md`) | P0 | | `0.3.0`–`0.3.2` |
| Tenant isolation: query filters must include tenant/service identifier where applicable | P0 | | `0.3.0`–`0.3.2` |

**Reference:** [`docs/codebases/logsapi-codebase-analysis.md`](../codebases/logsapi-codebase-analysis.md)
