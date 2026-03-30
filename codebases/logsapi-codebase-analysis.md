# logs.api codebase deep analysis (Contact360 eras 0.x-10.x)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Service summary

`lambda/logs.api` is a FastAPI logging service using S3 CSV objects as canonical storage for log CRUD/query/search/statistics across Contact360 operational and audit workflows.

## Runtime architecture

- Entrypoint: `lambda/logs.api/app/main.py`
- Routing: `app/api/v1/endpoints/logs.py`, `app/api/v1/endpoints/health.py`
- Auth dependency: `app/api/dependencies.py` (`X-API-Key`)
- Service layer: `app/services/log_service.py`
- Data repository: `app/models/log_repository.py`
- Storage client: `app/clients/s3.py`
- Caching/monitoring: `app/utils/query_cache.py`, `query_monitor.py`, `cache_metrics.py`
- Deployment contract: `lambda/logs.api/template.yaml`

## Verified completion status from runtime

- [x] ✅ S3 CSV is the canonical persistence layer (repository and client paths are S3-backed).
- [x] ✅ Non-health log endpoints enforce API key auth using `Depends(verify_api_key)`.
- [x] ✅ Health endpoint uses cached status and background refresh path.
- [x] ✅ Lambda/IAM fallback behavior exists for empty credential values in config/client logic.
- [x] ✅ Coverage exists for basic API and cache/performance behavior (test scaffolding present).

## Active risks and gap map

### Security and deploy drift

- [ ] ⬜ Incomplete: app-level CORS is wildcard (`allow_origins=["*"]`).
- [ ] ⬜ Incomplete: SAM HttpApi CORS is wildcard (`AllowOrigins/Methods/Headers: "*"`).
- [ ] ⬜ Incomplete: `template.yaml` includes a real-looking default API key value; must be placeholder/secret reference only.
- [ ] 🟡 In Progress: docs promote secrets-manager usage, but deploy artifacts still allow insecure defaults.

### Contract correctness and resilience

- [ ] ⬜ Incomplete: ingest endpoints (`POST /logs`, `/logs/batch`) do not enforce idempotency keys.
- [ ] 🟡 In Progress: endpoint parity is improved (`POST /logs/delete` + `DELETE /logs` fallback), but contract tests are partial.
- [ ] ⬜ Incomplete: standardized cross-service error envelope and retry guidance are not fully locked across all handlers.

### Scale and data-model risk

- [ ] 🟡 In Progress: query caching and monitoring exist, but cache is process-local and non-distributed.
- [ ] ⬜ Incomplete: heavy CSV scan/query paths can degrade under higher throughput without secondary indexing/rollups.
- [ ] ⬜ Incomplete: tenant/trace lineage fields are not yet enforced as mandatory for all ingest paths.

### Platform alignment risk

- [ ] ⬜ Incomplete: `logs.api` still performs direct S3 operations and is not yet aligned to `s3storage` as unified storage control plane.
- [ ] 📌 Planned: define adapter path (`logs.api` <-> `s3storage`) without breaking existing log contracts.

## API contract snapshot

- `POST /logs`, `POST /logs/batch`
- `GET /logs`, `GET /logs/search`, `GET /logs/{log_id}`
- `PUT /logs/{log_id}`, `DELETE /logs/{log_id}`
- `POST /logs/delete`, `DELETE /logs`
- `GET /logs/statistics`
- `GET /health`, `GET /health/info`

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ S3 CSV contract is established as canonical storage for log records.
- [ ] 🟡 In Progress: keep `POST /logs/delete` and `DELETE /logs` behavior aligned and evidence-tested.
- [ ] ⬜ Incomplete: add idempotency contract (`X-Idempotency-Key`) for ingest endpoints.
- [ ] ⬜ Incomplete: lock unified response/error envelope and compatibility tests for all endpoints.
- [ ] 📌 Planned: publish externalized OpenAPI/partner contract for `8.x` consumption.

### Service pack

- [x] ✅ S3 health checks, repository write/read, and basic cache-aware query flow are implemented.
- [ ] 🟡 In Progress: improve query/caching behavior with deterministic stale-while-revalidate semantics.
- [ ] ⬜ Incomplete: add throughput-safe rollup/index strategy to reduce large CSV scan pressure.
- [ ] ⬜ Incomplete: enforce tenant/request/trace metadata requirements at write time.
- [ ] 📌 Planned: evaluate phased move to `s3storage` control-plane interfaces for storage operations.

### Surface pack

- [x] ✅ Full log CRUD/query/search/statistics and health routes are available.
- [ ] 🟡 In Progress: complete admin/ops diagnostics wiring for cache state and slow-query traces.
- [ ] ⬜ Incomplete: provide consistent client-facing retry/action hints for transient failures.
- [ ] 📌 Planned: add partner-safe log views/export affordances for ecosystem integrations.

### Data pack

- [x] ✅ Hour-partitioned CSV object key pattern and retention intent (90-day lifecycle) are defined.
- [ ] 🟡 In Progress: align runtime evidence with retention/compliance documentation.
- [ ] ⬜ Incomplete: add lineage schema versioning and mandatory governance fields.
- [ ] 📌 Planned: legal-hold/compliance evidence overlays for campaign-era audit needs (`10.x`).

### Ops pack

- [x] ✅ API key auth check is enforced on non-health endpoints.
- [ ] ⬜ Incomplete: replace wildcard CORS in runtime and SAM template with explicit allowlists.
- [ ] ⬜ Incomplete: remove insecure default-like API key values from templates/examples.
- [ ] ⬜ Incomplete: expand integration/failure-path tests (invalid credentials, partial S3 failures, retries).
- [ ] 📌 Planned: add SLO dashboards and error-budget gates tied to logs query/write latency.

## Immediate execution queue (high impact)

- [x] ✅ Confirm canonical S3 CSV storage and remove MongoDB assumptions from runtime truth.
- [ ] ⬜ Incomplete: sanitize `template.yaml` API key default to placeholder-only and secrets-manager flow.
- [ ] ⬜ Incomplete: tighten CORS (app + SAM) to environment-specific allowlists.
- [ ] ⬜ Incomplete: add idempotency key support for `POST /logs` and `POST /logs/batch`.
- [ ] 🟡 In Progress: harden contract parity tests for delete/query/search/statistics responses.
- [ ] ⬜ Incomplete: add failure-path tests for S3 auth errors and partial write/read failure recovery.
- [ ] 🟡 In Progress: strengthen cache observability and stale refresh metrics in ops surfaces.
- [ ] ⬜ Incomplete: define cross-service mandatory fields (`tenant_id`, `trace_id`, `request_id`) and enforce validation.
- [ ] 📌 Planned: design migration path to use `s3storage` as storage control plane without API regressions.

## Cross-codebase log unification plan (`logs.api` as single logging system)

### Current adoption snapshot

- [x] ✅ `lambda/logs.api` provides central ingest/query/search/statistics API and is actively consumed by `contact360.io/api`.
- [x] ✅ `contact360.io/admin` has a dedicated `LogsApiClient` and logs surface integration.
- [ ] 🟡 In Progress: `contact360.io/api` still uses local Python logging infrastructure (`mongodb_log_handler.py` naming/adapter legacy) alongside forwarding to `logs.api`.
- [ ] ⬜ Incomplete: `contact360.io/jobs` contains direct `print(...)` progress lines in streaming processors.
- [ ] ⬜ Incomplete: multiple services still rely only on local service loggers (`logging`, custom `log_handler`, `console.log`) without `logs.api` shipping.

### Global migration principles (all codebases)

- [ ] ⬜ Incomplete: treat `logs.api` as the canonical sink for operational/audit events across backend services.
- [ ] ⬜ Incomplete: remove raw `print(...)` and `console.log(...)` from production paths; replace with structured logger adapters.
- [ ] 🟡 In Progress: keep local logger instances only as transport wrappers that emit to `logs.api` (not as separate source of truth).
- [ ] ⬜ Incomplete: enforce mandatory log fields (`service`, `tenant_id`, `request_id`, `trace_id`, `level`, `timestamp`).
- [ ] 📌 Planned: introduce CI guardrails blocking new direct console/print usage in runtime code.

### Execution pack A - gateway and admin canonicalization

- [ ] 🟡 In Progress: rename/refactor `mongodb_log_handler` in `contact360.io/api` to `logs_api_handler` semantics to eliminate legacy drift.
- [ ] ⬜ Incomplete: ensure every GraphQL resolver/service error path in `contact360.io/api` emits structured events via `LambdaLogsClient`.
- [ ] 🟡 In Progress: keep `contact360.io/admin` logs dashboard on `logs.api` and remove fallback ambiguity where possible.
- [ ] ⬜ Incomplete: standardize auth/key rotation and retry behavior across gateway/admin log clients.
- [ ] 📌 Planned: add end-to-end evidence tests (gateway/admin action -> log visible in `logs.api` query API).

### Execution pack B - jobs and batch workers cleanup

- [ ] ⬜ Incomplete: replace `print(...)` progress output in `contact360.io/jobs` processors with structured logger calls.
- [ ] ⬜ Incomplete: add jobs-to-`logs.api` transport client (batch-safe, retry-aware, non-blocking) for long-running workers.
- [ ] ⬜ Incomplete: unify job log schema for row progress, checkpoints, retry, failure, and completion events.
- [ ] ⬜ Incomplete: ensure worker logging never breaks processing when `logs.api` is unavailable (buffer + fallback policy).
- [ ] 📌 Planned: add sampling controls for high-volume per-row logs to avoid cost spikes.

### Execution pack C - lambda service ecosystem alignment

- [ ] ⬜ Incomplete: inventory all `lambda/*` services using local `log_handler` patterns (`emailapis`, `s3storage`, others) and add `logs.api` emitters.
- [ ] ⬜ Incomplete: remove ad hoc console/print diagnostics from lambda runtime handlers in favor of structured events.
- [ ] 🟡 In Progress: align logger metadata fields across lambda services so cross-service queries work consistently.
- [ ] ⬜ Incomplete: provide shared SDK wrapper for Python/Go services to post batched logs to `logs.api`.
- [ ] 📌 Planned: add tenant-aware and source-aware enrichment (`source_service`, `deployment_env`, `version`) at adapter layer.

### Execution pack D - frontend and extension event routing

- [ ] ⬜ Incomplete: define browser-safe telemetry ingestion path (via gateway) so frontend and extension logs land in `logs.api`.
- [ ] ⬜ Incomplete: remove development `console.log` usage from production bundles and replace with telemetry client wrappers.
- [ ] 🟡 In Progress: classify which client-side events are operational logs vs analytics to avoid schema mixing.
- [ ] ⬜ Incomplete: add privacy filtering/redaction rules before forwarding frontend/extension events.
- [ ] 📌 Planned: add support tooling to correlate frontend trace IDs with backend `logs.api` entries.

### Next 5 smallest implementation tasks

- [ ] ⬜ Incomplete: replace 2 known `print(...)` lines in `contact360.io/jobs` stream processors with structured logger calls.
- [ ] ⬜ Incomplete: create shared lint rule/check that fails on `print(...)` and `console.log(...)` in non-test runtime files.
- [ ] ⬜ Incomplete: add one unified Python `logs.api` emitter utility module and migrate one service as reference.
- [ ] 🟡 In Progress: rename legacy "mongodb" logging symbols/docs in `contact360.io/api` to `logs_api` naming.
- [ ] 📌 Planned: add cross-codebase adoption table (`integrated`, `hybrid`, `not integrated`) in each `docs/codebases/*.md`.

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x - Foundation and pre-product stabilization and codebase setup`

- [x] ✅ Completed: baseline logs API service contract, auth gate, S3 CSV persistence, and health endpoints exist.
- [ ] 🟡 In Progress: remove deployment/security drift (wildcard CORS + insecure template defaults).
- [ ] ⬜ Incomplete: close foundational contract tests for idempotency and deterministic error envelope.

### `1.x.x - Contact360 user and billing and credit system`

- [ ] 🟡 In Progress: gateway and admin flows already emit/query key operational logs through `logs.api`.
- [ ] ⬜ Incomplete: enforce mandatory billing/user lineage fields (`tenant_id`, `request_id`, `trace_id`) at ingest boundary.
- [ ] 📌 Planned: add billing-credit specific alert packs and log evidence gates for incidents.

### `2.x.x - Contact360 email system`

- [ ] 🟡 In Progress: email workflow events are partially represented through existing integration points.
- [ ] ⬜ Incomplete: migrate job/bulk worker print-style progress logging to structured `logs.api` events.
- [ ] ⬜ Incomplete: define high-volume ingest policy (sampling, batching, retry/fallback) for verifier/finder pipelines.

### `3.x.x - Contact360 contact and company data system`

- [ ] 📌 Planned: standardize contact/company enrichment taxonomy fields in `logs.api` contract.
- [ ] ⬜ Incomplete: add canonical filters and dashboards for dedupe/enrichment incident triage.
- [ ] 📌 Planned: enforce correlation IDs for contact/company data lineage tracing.

### `4.x.x - Contact360 Extension and Sales Navigator maturity`

- [ ] ⬜ Incomplete: route extension/Sales Navigator operational logs via backend ingestion into `logs.api`.
- [ ] 🟡 In Progress: classify extension events (operational vs analytics) and schema boundaries.
- [ ] 📌 Planned: add extension-to-backend trace correlation tooling in support views.

### `5.x.x - Contact360 AI workflows`

- [ ] 📌 Planned: define AI-safe logging schema (prompt/response metadata, redaction-safe fields).
- [ ] ⬜ Incomplete: implement payload minimization/redaction before writing AI-adjacent logs.
- [ ] 📌 Planned: AI workflow anomaly and cost diagnostics from `logs.api` statistics endpoints.

### `6.x.x - Contact360 Reliability and Scaling`

- [ ] 🟡 In Progress: cache/monitoring capabilities exist as a base for reliability controls.
- [ ] ⬜ Incomplete: add scalable rollup/index strategy beyond raw CSV scans.
- [ ] ⬜ Incomplete: introduce SLO/error-budget dashboards and threshold alerting.

### `7.x.x - Contact360 deployment`

- [ ] ⬜ Incomplete: sanitize all deploy templates/secrets flows (API key defaults, env guidance).
- [ ] ⬜ Incomplete: enforce environment-specific CORS and auth hardening in deployed stacks.
- [ ] 🟡 In Progress: maintain deployment docs for secrets manager and IAM-first credential usage.

### `8.x.x - Contact360 public and private apis and endpotints`

- [ ] 📌 Planned: publish stable external logs contract/OpenAPI guidance for partner-safe usage.
- [ ] ⬜ Incomplete: enforce idempotency and contract parity tests required for public API confidence.
- [ ] 📌 Planned: add policy controls for scoped API-key usage and endpoint-level governance.

### `9.x.x - Contact360 Ecosystem integrations and Platform productization`

- [ ] 📌 Planned: add tenant-scoped metering and quota controls for log ingestion/query.
- [ ] ⬜ Incomplete: add partner integration evidence bundles (traceability, retention proof, incident extracts).
- [ ] 📌 Planned: cross-service platform dashboards fed by unified `logs.api` schema.

### `10.x.x - Contact360 email campaign`

- [ ] 📌 Planned: define immutable campaign audit event schema and evidence retrieval contract.
- [ ] ⬜ Incomplete: add campaign compliance lineage fields and legal-hold aware retrieval paths.
- [ ] 📌 Planned: campaign release gates requiring log-based compliance and deliverability evidence.

## 2026 Gap Register (actionable)

### P0

- [ ] ⬜ Incomplete: `LOG-0.1` Remove insecure API key defaults/placeholders from deployment templates and examples.
- [ ] ⬜ Incomplete: `LOG-0.2` Replace wildcard CORS in both FastAPI middleware and SAM HttpApi config.
- [ ] ⬜ Incomplete: `LOG-0.3` Add idempotency key contract for ingest endpoints (`/logs`, `/logs/batch`).
- [ ] 🟡 In Progress: `LOG-0.4` Freeze endpoint/response parity with deterministic contract tests.

### P1/P2

- [ ] 🟡 In Progress: `LOG-1.1` Improve cache consistency evidence and stale-refresh observability.
- [ ] ⬜ Incomplete: `LOG-1.2` Add fault-injection tests for S3 permission/auth and transient failures.
- [ ] ⬜ Incomplete: `LOG-2.1` Enforce tenant/trace lineage fields and schema validation on writes.
- [ ] 📌 Planned: `LOG-2.2` Introduce scalable rollup/index strategy for large-window queries.

### P3+

- [ ] 📌 Planned: `LOG-3.1` Add distributed rate limiting and quota awareness.
- [ ] 📌 Planned: `LOG-3.2` SLO/error-budget dashboards for query and ingest paths.
- [ ] 📌 Planned: `LOG-4.1` Partner-safe exports/webhooks and compliance evidence APIs.
- [ ] 📌 Planned: `LOG-4.2` Storage-control-plane convergence with `s3storage`.
