# Era 6.1–6.2: SLO baseline and idempotency

This stage establishes a practical reliability baseline in the API gateway.

## Per-service SLO targets (initial program table)

Use these as **starting targets**; tune per environment with product + SRE. Map concrete numbers to dashboards in the **6.1** window (`docs/roadmap.md` Stage 6.1).

| Service | Availability (monthly) | Latency P95 (primary API) | Notes |
| --- | --- | --- | --- |
| **Appointment360** (gateway) | 99.9% | GraphQL mutations/reads: agree baseline in staging | `GET /health/slo`, RED metrics |
| **Connectra** | 99.9% | Query P95 per era `6.x` **Service task slices** (Connectra) | Search + GraphQL |
| **Contact AI** | 99.5% | SSE/stream path: TTFT + error rate | Tracing (`6.4 — Observability and correlated telemetry.md`) |
| **SalesNavigator** | 99.5% | Edge APIs per codebase analysis | CORS + rate limits |
| **Mailvetter** | 99.9% | Outbound pipeline latency | Redis distributed limiter |

**Evidence:** Export dashboard links in [`reliability-rc-hardening.md`](reliability-rc-hardening.md) at RC.

## RED metrics baseline

- Middleware: `contact360.io/api/app/core/middleware.py` → `REDMetricsMiddleware`
- Health endpoint: `GET /health/slo`
- Returned metrics:
  - `requests_total`
  - `errors_total` (5xx and unhandled exceptions)
  - `error_rate_pct`
  - `avg_duration_ms`
  - `requests_per_second`
  - `in_flight`
- Error budget status is computed using `SLO_ERROR_BUDGET_PERCENT`.

## Idempotency for high-risk writes

- Middleware: `GraphQLIdempotencyMiddleware`
- Scope: `POST /graphql` only
- Guarded mutations are configured by `IDEMPOTENCY_REQUIRED_MUTATIONS`
  (default: `subscribe,purchaseAddon,submitPaymentProof,approvePayment,declinePayment`)
- Key header: `X-Idempotency-Key`
- Behavior:
  - If key is present and the same guarded mutation/key is repeated inside TTL,
    cached successful response is replayed with `X-Idempotent-Replay: true`.
  - Strict enforcement is opt-in via `IDEMPOTENCY_ENFORCE_GRAPHQL_MUTATIONS=true`.
  - Cache TTL is controlled by `IDEMPOTENCY_TTL_SECONDS`.

## Redis migration checklist (cross-node idempotency)

Gateway idempotency must not rely on **in-process** memory in multi-instance production.

| Step | Action | Owner |
| --- | --- | --- |
| 1 | Provision Redis (`REDIS_URL`) with persistence appropriate for idempotency TTL | DevOps |
| 2 | Implement Redis-backed store behind same middleware interface | Backend |
| 3 | Load test: duplicate mutation hits different pods → still **one** side effect | QA |
| 4 | Key namespace: prefix with `idempotency:` + tenant + mutation hash | Backend |
| 5 | TTL aligned with `IDEMPOTENCY_TTL_SECONDS`; memory cap / eviction policy reviewed | SRE |
| 6 | Fail-open vs fail-closed policy documented for Redis outage | SRE + Product |
| 7 | Rollout: canary region → full; watch duplicate-billing KPI | Release Eng |

## Operational notes

- Current cache may be in-process memory during early phases; **production multi-instance requires Redis** (see checklist above).
- Keep guarded mutation list focused on side-effecting billing/bulk/sync writes (`6.2 — Idempotent writes and reconciliation.md`).

## References

- [`6.1 — SLO and error-budget baseline.md`](6.1 — SLO and error-budget baseline.md), [`6.2 — Idempotent writes and reconciliation.md`](6.2 — Idempotent writes and reconciliation.md)
- [`appointment360-codebase-analysis.md`](../codebases/appointment360-codebase-analysis.md)
