# Emailapis / Emailapigo — Era `6.x` Reliability & Scaling Task Pack

### Context

Era `6.x` hardens **lambda/emailapis** and **lambda/emailapigo** for predictable latency under bulk verification/finder traffic, provider degradation, and circuit/timeout safety. This pack replaces placeholder template variables and aligns tasks to roadmap **Stages 6.1, 6.4, 6.5, 6.8** (SLO, observability, performance, abuse resilience).

**Canonical endpoint matrix:** [`docs/backend/endpoints/emailapis_endpoint_era_matrix.json`](../backend/endpoints/emailapis_endpoint_era_matrix.json) — keep `6.x` behavioral notes in sync with this pack.

---

## Track A — Contract

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| A-6.1 | **SLO targets** | Publish service SLIs: **P95/P99** for finder/verify/pattern routes; **error-rate** budget; **provider success ratio**; map to dashboards (roadmap 6.1). | SRE + Backend |
| A-6.2 | **Bulk concurrency contract** | Max in-flight bulk operations per tenant; per-route concurrency caps; backoff when provider returns `429`/`503`. | Backend |
| A-6.3 | **Timeout & circuit contract** | Hard timeouts per provider; open circuit after **N** consecutive failures; half-open probe policy; document HTTP status mapping (`502` vs `503`). | Backend |
| A-6.4 | **Payload & era `6.x` matrix** | Freeze era `6.x` request/response compatibility; document breaking vs additive changes in `emailapis_endpoint_era_matrix.json`. | Backend + Docs |
| A-6.5 | **Trace contract** | Require `X-Trace-Id` (or traceparent) on ingress; propagate to provider adapter logs (roadmap 6.4). | Backend |

---

## Track B — Service

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| B-6.1 | **Concurrency hardening** | Implement worker pool / semaphore for bulk finder; avoid unbounded goroutine fan-out (roadmap 6.5). | Backend |
| B-6.2 | **Provider timeouts** | Configure dial + read deadlines per provider tier; align with contract table. | Backend |
| B-6.3 | **Circuit breaker** | Trip on error streak; emit metric `emailapis_circuit_open`; auto-recovery with jitter. | Backend |
| B-6.4 | **Health & readiness** | Liveness vs readiness: fail readiness when circuit open for **primary** provider (optional product policy). | DevOps |
| B-6.5 | **Rate limit alignment** | Coordinate with gateway `GRAPHQL_RATE_LIMIT_*` / abuse guard where emailapis is invoked from App — document fan-in. | Platform |

---

## Track C — Surface (API consumers & ops UI)

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| C-6.1 | **Retry UX guidance** | Document client retry: exponential backoff; **do not** retry `4xx` except `429` with `Retry-After`; surface `trace_id` in support errors. | Frontend + Docs |
| C-6.2 | **Degraded mode copy** | When fallback provider active, optional `warning` field in API contract for UIs (`components.md` Era 6 patterns). | Product + Backend |
| C-6.3 | **Progress / batch status** | Long-running bulk: polling or webhook contract; progress `%` for dashboard (`loading` / `error` / `retry` states). | Frontend |

---

## Track D — Data

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| D-6.1 | **`email_finder_cache` lineage** | TTL, invalidation on provider rule change; trace id on cache miss path. | Backend |
| D-6.2 | **`email_patterns` / persistence** | Audit fields for verify outcomes; PII handling in logs (`performance-storage-abuse.md` alignment). | Backend + Security |
| D-6.3 | **Idempotency for safe replays** | Where POST causes side effects, support idempotency key or natural key dedupe (align with jobs/email campaign patterns). | Backend |

---

## Track E — Ops

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| E-6.1 | **Dashboards** | Panels: request rate, P95 latency, error %, circuit state, provider latency breakdown. | SRE |
| E-6.2 | **Provider degradation runbook** | **Step 1:** Confirm incident vs provider outage. **Step 2:** Fail over to secondary if configured. **Step 3:** Reduce concurrency / enable queue. **Step 4:** Comms template. **Step 5:** Post-incident: adjust thresholds. | SRE |
| E-6.3 | **Load / chaos** | Game day: slow provider; verify timeout + circuit; no worker explosion. | SRE |
| E-6.4 | **Rollback** | Feature flags for provider routing; previous Lambda version alias. | DevOps |

---

## Provider degradation runbook (summary)

| Failure class | Symptoms | First actions | Escalation |
| --- | --- | --- | --- |
| Transient (`503`, timeouts) | Elevated 5xx, circuit half-open | Retry with backoff; check provider status | Increase timeout temporarily only if SLO allows |
| Provider `429` | Throttle errors | Shed load; reduce bulk concurrency | Partner with provider quota team |
| Permanent misconfig (`401/403`) | Auth errors spike | Rotate keys; fix allowlist | Stop traffic via flag |
| Data contract drift | Parse errors | Pin API version; hotfix client | |

---

## Endpoint matrix reference

- Update **[`emailapis_endpoint_era_matrix.json`](../backend/endpoints/emailapis_endpoint_era_matrix.json)** with `6.x` rows for: bulk finder, verify, pattern, health, and any Go proxy routes in **emailapigo**.
- Cross-link **[`appointment360_endpoint_era_matrix.json`](../backend/endpoints/appointment360_endpoint_era_matrix.json)** if App GraphQL resolvers call emailapis indirectly.

---

## Completion gate

- [ ] SLO table row for Emailapis added in [`slo-idempotency.md`](slo-idempotency.md).
- [ ] `emailapis_endpoint_era_matrix.json` includes era `6.x` reliability notes (timeouts, circuits, concurrency).
- [ ] Provider degradation runbook reviewed in tabletop exercise.
- [ ] Staging load test: bulk job completes within **P95** target without OOM or goroutine leak.
