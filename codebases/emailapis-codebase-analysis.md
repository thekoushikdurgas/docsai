# emailapis / emailapigo codebase deep analysis (Contact360 eras 0.x-10.x)

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Service summary

`lambda/emailapis` (Python FastAPI) and `lambda/emailapigo` (Go Gin) are Contact360's dual-runtime email execution services for finder, verifier, pattern add, and web-search fallback flows. They sit behind Appointment360 GraphQL and power both interactive and bulk email workloads.

## Runtime architecture

- Python entrypoint: `lambda/emailapis/app/main.py`
- Python router: `lambda/emailapis/app/api/v1/router.py`
- Go entrypoint: `lambda/emailapigo/main.go`
- Go router: `lambda/emailapigo/internal/api/router.go`
- Finder services: `app/services/email_finder_service.py`, `internal/services/email_finder_service.go`
- Verifier services: `app/services/email_verification_service.py`, `internal/services/email_verification_service.go`
- Pattern services: `app/services/email_pattern_service.py`, `internal/services/email_pattern_service.go`
- Data repositories: cache + pattern repositories in both runtimes

## API contract snapshot

- `POST /email/finder/`
- `POST /email/finder/bulk`
- `POST /email/single/verifier/`
- `POST /email/bulk/verifier/`
- `POST /email-patterns/add`
- `POST /email-patterns/add/bulk`
- `POST /web/web-search`
- `GET /health`, `GET /`

## Data model and persistence

### `email_finder_cache`

- Identity keys: `first_name`, `last_name`, `domain` (case-insensitive)
- Result fields: `email_found`, `email_source`
- Constraints: unique identity + lookup index
- Role: short-path cache hit before provider fanout

### `email_patterns`

- Keys: `uuid`, `company_uuid`, `domain`
- Pattern fields: `pattern_format`, `pattern_string`
- Metrics: `contact_count`, `success_rate`, `error_rate`
- Role: learned pattern persistence used by finder flows

## Provider orchestration and behavior

### Finder flow (both runtimes)

1. Cache lookup (`email_finder_cache`)
2. Parallel provider candidates:
   - Connectra
   - Pattern service
   - Generator
3. Race verification of candidates
4. Fallback discovery:
   - Web search
   - IcyPeas
5. Return normalized list and source attribution

### Verifier flow

- Python defaults commonly reference `truelist` + `icypeas`
- Go health and runtime prefer `mailvetter` + `icypeas` (`mailvetter_configured` check)
- Bulk paths use concurrency controls and stagger/timeout behavior

## Key findings and cross-service risks

1. Provider drift risk: Python/docs often reference `truelist`; Go runtime prioritizes `mailvetter`.
2. Status semantic drift risk: `valid`/`invalid`/`catchall`/`unknown` interpretation can differ across app, api, and runtime mapping.
3. Observability gap: correlation across app -> api -> jobs -> lambda is not consistently documented with one trace contract.
4. Contract drift risk: endpoint and payload assumptions in docs may lag runtime changes.
5. Bulk correctness risk: partial-batch error mapping and retry semantics require explicit cross-layer contract tests.

## Verified completion status from runtime

- [x] ✅ Both Python (`emailapis`) and Go (`emailapigo`) runtimes are live with API-key protected email workflows.
- [x] ✅ Core finder and verifier flows exist in both runtimes with provider fallback logic.
- [x] ✅ Pattern/cache repositories are present in both stacks and wired into finder behavior.
- [x] ✅ Both runtimes include batch logging handlers that can forward to centralized logs API.
- [ ] 🟡 In Progress: full parity between Python and Go endpoint contracts is not complete (Go router includes TODO parity note).

## Active risks and gap map

### Contract and provider drift

- [ ] ⬜ Incomplete: provider contract drift (`truelist` in Python/docs vs `mailvetter` in Go runtime schemas).
- [ ] ⬜ Incomplete: status vocabulary mapping is not formally frozen across gateway/jobs/runtimes (`valid|invalid|catchall|unknown|risky`).
- [ ] 🟡 In Progress: endpoint list parity exists for major paths, but full behavior/shape parity tests are partial.

### Security and deployment drift

- [ ] ⬜ Incomplete: wildcard CORS remains enabled in Python runtime.
- [ ] ⬜ Incomplete: sensitive key examples appear in docs/sample commands and should be sanitized.
- [ ] 🟡 In Progress: API key middleware exists in both runtimes, but rotation/secret-sourcing guidance is uneven.

### Reliability and observability gaps

- [ ] ⬜ Incomplete: debug prints remain in critical code paths (`connectra_client.py`, batch log handlers).
- [ ] ⬜ Incomplete: idempotency/replay contract is missing for bulk verifier/finder operations.
- [ ] 🟡 In Progress: provider retry/backoff behavior exists, but circuit-breaker and degradation policy is not unified.

## Current execution packs (small tasks by status)

### Contract pack

- [x] ✅ Base endpoint families and auth boundary are established in both runtimes.
- [ ] 🟡 In Progress: align request/response schemas between Python and Go for all finder/verifier endpoints.
- [ ] ⬜ Incomplete: freeze canonical provider set and migration policy (`truelist`/`mailvetter` interoperability).
- [ ] ⬜ Incomplete: lock status vocabulary contract and unknown/risky mapping policy.
- [ ] 📌 Planned: publish external/private contract versioning and deprecation policy for `8.x`.

### Service pack

- [x] ✅ Finder/verifier/pattern services and data repositories are implemented in both stacks.
- [ ] 🟡 In Progress: improve bulk concurrency and timeout behavior consistency across Python and Go.
- [ ] ⬜ Incomplete: remove debug print paths and replace with structured logger events.
- [ ] ⬜ Incomplete: add bulk idempotency keys and replay-safe handling.
- [ ] 📌 Planned: unify provider resilience controls (rate-limit strategy, circuit-breaker profile).

### Surface pack

- [x] ✅ Health/root and core email operation surfaces are available.
- [ ] 🟡 In Progress: harmonize error envelopes and caller-facing retry hints.
- [ ] ⬜ Incomplete: close parity gaps for Go routes marked as TODO and ensure docs/runtime consistency.
- [ ] 📌 Planned: partner-safe docs/examples for public/private API consumption.

### Data pack

- [x] ✅ Cache/pattern entities and persistence layers are present.
- [ ] 🟡 In Progress: enforce lineage fields for request/user/trace across all writes and responses.
- [ ] ⬜ Incomplete: stabilize metric field semantics (`success_rate`, `error_rate`) across runtimes.
- [ ] 📌 Planned: add long-window rollups and evidence bundles for campaign/compliance flows.

### Ops pack

- [x] ✅ Runtime startup checks and diagnostics endpoints exist in both services.
- [ ] ⬜ Incomplete: tighten CORS and secret hygiene in templates/docs.
- [ ] ⬜ Incomplete: add integration/failure-path tests covering provider outages and fallback storms.
- [ ] 🟡 In Progress: centralize observability via logs API adapters in both runtimes.
- [ ] 📌 Planned: add SLO dashboards and error-budget release gates.

## Era-by-era completion map (`0.x.x` to `10.x.x`)

### `0.x.x - Foundation and pre-product stabilization and codebase setup`

- [x] ✅ Completed: dual runtime foundations (Python/Go), auth middleware, and core endpoint surfaces are established.
- [ ] 🟡 In Progress: remove foundational drift between Python and Go contracts.
- [ ] ⬜ Incomplete: sanitize debug output and finalize baseline contract tests.

### `1.x.x - Contact360 user and billing and credit system`

- [ ] 🟡 In Progress: credit-impact email operations are integrated through gateway flows.
- [ ] ⬜ Incomplete: enforce deterministic credit lineage fields on all email operations.
- [ ] 📌 Planned: add billing anomaly alerts tied to email operation outcomes.

### `2.x.x - Contact360 email system`

- [x] ✅ Completed: core finder/verifier and bulk endpoint capabilities are in production shape.
- [ ] ⬜ Incomplete: freeze provider contract (`mailvetter` vs `truelist`) and status vocabulary.
- [ ] ⬜ Incomplete: add idempotency/replay guarantees for bulk endpoints and retries.

### `3.x.x - Contact360 contact and company data system`

- [ ] 🟡 In Progress: contact/company enrichment uses email service paths with Connectra coupling.
- [ ] ⬜ Incomplete: add deterministic candidate merge and enrichment lineage evidence.
- [ ] 📌 Planned: add drift detection between enrichment outputs and verification statuses.

### `4.x.x - Contact360 Extension and Sales Navigator maturity`

- [ ] 📌 Planned: define extension-origin email metadata and source tags.
- [ ] ⬜ Incomplete: implement extension-safe retry and diagnostics contracts across runtimes.
- [ ] 📌 Planned: add replay/support runbooks for extension-triggered email failures.

### `5.x.x - Contact360 AI workflows`

- [ ] 📌 Planned: define AI-assisted payload boundaries for finder/ranking flows.
- [ ] ⬜ Incomplete: add safe redaction/minimization for AI-context logging fields.
- [ ] 📌 Planned: add confidence lineage for AI-assisted email decisions.

### `6.x.x - Contact360 Reliability and Scaling`

- [ ] 🟡 In Progress: concurrency and retry controls exist but are runtime-specific.
- [ ] ⬜ Incomplete: unify provider degradation strategy and circuit behavior.
- [ ] ⬜ Incomplete: add SLO/error-budget metrics for bulk success, latency, and fallback rates.

### `7.x.x - Contact360 deployment`

- [x] ✅ Completed: env-driven configuration and health diagnostics exist in both runtimes.
- [ ] ⬜ Incomplete: sanitize template/docs secret examples and tighten CORS defaults.
- [ ] 🟡 In Progress: deployment parity checks for provider readiness and DB dependencies.

### `8.x.x - Contact360 public and private apis and endpotints`

- [ ] 🟡 In Progress: API surface is broad but versioned external contract is not fully frozen.
- [ ] ⬜ Incomplete: finalize partner-safe error envelope and compatibility tests.
- [ ] 📌 Planned: publish stable integration examples and SDK semantics.

### `9.x.x - Contact360 Ecosystem integrations and Platform productization`

- [ ] 📌 Planned: add tenant-aware quotas/throttles and entitlement policy hooks.
- [ ] ⬜ Incomplete: add cross-service trace correlation standards for partner investigations.
- [ ] 📌 Planned: generate SLA evidence packs for ecosystem channels.

### `10.x.x - Contact360 email campaign`

- [ ] 📌 Planned: define campaign verification contract and immutable evidence model.
- [ ] ⬜ Incomplete: retain campaign compliance lineage and legal-hold compatible artifacts.
- [ ] 📌 Planned: enforce campaign release gate tied to deliverability/compliance metrics.

## Immediate execution queue (high impact)

- [ ] ⬜ Incomplete: remove remaining debug prints and ad hoc console logging from runtime-critical paths.
- [ ] ⬜ Incomplete: unify provider naming contract across Python/Go/docs (`mailvetter`/`truelist`) with migration notes.
- [ ] ⬜ Incomplete: add bulk idempotency key support and replay tests for finder/verifier operations.
- [ ] 🟡 In Progress: close Python-Go endpoint parity gaps and resolve Go router TODO scope.
- [ ] ⬜ Incomplete: tighten CORS and sanitize secrets/examples in templates and API docs.
- [ ] 🟡 In Progress: standardize logs API emission fields and trace IDs across both runtimes.
- [ ] 📌 Planned: add SLO dashboards and provider degradation runbooks.

## 2026 Gap Register (actionable)

### P0

- [ ] ⬜ Incomplete: `EPA-0.1` Lock canonical endpoint inventory and remove Python/Go/docs drift.
- [ ] ⬜ Incomplete: `EPA-0.2` Remove sensitive key examples and enforce secret-safe docs/templates.
- [ ] ⬜ Incomplete: `EPA-0.3` Remove debug prints and dead code paths in critical services.
- [ ] ⬜ Incomplete: `EPA-0.4` Align provider contract (`mailvetter` vs `truelist`) across runtimes.

### P1/P2

- [ ] ⬜ Incomplete: `EPA-2.1` Freeze status vocabulary (`valid|invalid|catchall|unknown`) with policy for `risky`.
- [ ] ⬜ Incomplete: `EPA-2.2` Add bulk idempotency contract and replay tests.
- [ ] 🟡 In Progress: `EPA-2.3` Unify retry/backoff and provider degradation behavior.
- [ ] 📌 Planned: `EPA-2.4` Add trace lineage contract (`tenant_id`, `request_id`, `trace_id`) across layers.

### P3+

- [ ] 📌 Planned: `EPA-3.1` Partner-safe API contract package and compatibility automation.
- [ ] 📌 Planned: `EPA-3.2` Ecosystem SLA evidence and integration diagnostics.
- [ ] 📌 Planned: `EPA-4.x` Campaign compliance evidence and immutable verification lineage.
