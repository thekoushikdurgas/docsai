# Reliability RC hardening (Era 6 — Stage 6.9)

Release-candidate gate for the **6.x reliability era**: operational readiness, not feature work. Use this doc before promoting a build to production or a named RC.

## Preconditions (must be green)

| Check | Where / how |
| ----- | ------------- |
| API process health | `GET /health` on `contact360.io/api` |
| DB pool / connectivity | `GET /health/db` |
| Logging pipeline | `GET /health/logging` |
| SLO / error budget snapshot | `GET /health/slo` — `status` should be `healthy` unless error budget policy explicitly allows breach |
| GraphQL abuse guards | Env: `GRAPHQL_MAX_BODY_BYTES`, `MUTATION_ABUSE_GUARD_RPM`, `ABUSE_GUARDED_MUTATIONS` reviewed for target tier |
| Idempotency on billing writes | [`slo-idempotency.md`](slo-idempotency.md) — clients send `X-Idempotency-Key` for guarded mutations in production |
| Trace correlation | [`queue-observability.md`](queue-observability.md) — `X-Trace-Id` propagated through gateways and workers |

## RC smoke suite (manual or automated)

Run after deploy to staging; repeat subset after production cutover.

1. **Auth** — login, refresh token, expired-token handling (see `docs/extension-auth.md` for extension parity).
2. **Billing** — `subscribe` / `purchaseAddon` / `submitPaymentProof` with idempotency keys; verify no duplicate side effects on retry.
3. **Credits** — deduction path blocks at zero; usage ledger consistent.
4. **Bulk / upload** — multipart upload session; job enqueue visible in scheduler (if applicable).
5. **Connectra** — `ListByFilters` / count smoke against staging VQL contract (`docs/vql-filter-taxonomy.md`); P95 sample within SLO band.
6. **Contact AI** — non-streaming send; **SSE stream** path stable for **N** minutes (reconnect + trace id in logs).
7. **SalesNavigator** — smoke CORS preflight + hot endpoint; rate limit returns `429` under synthetic burst (staging flag).
8. **Mailvetter** — outbound path respects Redis limiter; no duplicate sends on controlled retry (`docs/codebases/mailvetter-codebase-analysis.md`).
9. **Jobs / campaign** — DLQ depth nominal; **dry-run** replay authorized (evidence in era `6.x` **Service task slices** — jobs / queues).
10. **Logs.api** — sample query completes under timeout; trace lookup works for injected `X-Trace-Id`.
11. **S3 storage** — multipart **complete** idempotency spot check (era `6.x` **Service task slices** — S3 / `6.6`).
12. **Emailapis** — provider timeout/circuit returns bounded error (no hang); `trace_id` in logs.
13. **AI chat (baseline)** — non-streaming path (`docs/ai-workflows.md`) if not covered above.

## Incident runbook (minimal)

1. Confirm scope: API vs DB vs downstream Lambda vs Connectra.
2. Collect `X-Request-Id` / `X-Trace-Id` from failing responses.
3. Check `/health/slo` and application logs (Lambda Logs API when enabled).
4. If abuse throttles fire (`429`), verify `MUTATION_ABUSE_GUARD_RPM` and client retry behavior.
5. Roll back via previous deployment artifact; document root cause before re-release.

## Sign-off

| Role | Name | Date | Build SHA | Notes |
| ---- | ---- | ---- | --------- | ----- |
| Engineering | | | | |
| SRE / Ops | | | | |
| Product (if RC) | | | | |

**RC is not approved** until preconditions and smoke suite are recorded for the **build SHA** (git commit) deployed to staging/production candidate.
