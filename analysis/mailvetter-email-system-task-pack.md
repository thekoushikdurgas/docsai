# Mailvetter — 2.x Email System Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `2.x` — Core email verification system (primary era)

## Codebase file map (high-value for `2.x`)

Grounded in [`docs/codebases/mailvetter-codebase-analysis.md`](../codebases/mailvetter-codebase-analysis.md).

| Area | Paths (start here) | Why it matters |
| --- | --- | --- |
| API process | `backend(dev)/mailvetter/cmd/api/main.go` | V1 routes + auth middleware + request handling |
| Worker process | `backend(dev)/mailvetter/cmd/worker/main.go` | Queue consumer + worker pool |
| V1 handlers | `backend(dev)/mailvetter/internal/handlers/validate.go` | Single + bulk validation entrypoints |
| Jobs handlers | `backend(dev)/mailvetter/internal/handlers/jobs.go` | `/v1/jobs/:job_id` status + results |
| Core verifier | `backend(dev)/mailvetter/internal/validator/logic.go` | DNS/SMTP/OSINT orchestration |
| Scoring | `backend(dev)/mailvetter/internal/validator/scoring.go` | Robust score model + explainability |
| DB/migrations | `backend(dev)/mailvetter/internal/store/db.go` | **Risk:** runtime migrations on startup |
| Queue client | `backend(dev)/mailvetter/internal/queue/client.go` | Redis tasks queue producer |
| Webhook dispatch | `backend(dev)/mailvetter/internal/webhook/dispatcher.go` | HMAC signing and callback delivery |
| Legacy UI | `backend(dev)/mailvetter/static/index.html` | Legacy operator UI (policy: deprecate/guard) |

## Contract track

- [ ] Freeze v1 endpoints: `POST /v1/emails/validate`, `POST /v1/emails/validate-bulk`, `GET /v1/jobs/:job_id`, `GET /v1/jobs/:job_id/results`.
- [ ] Freeze status vocabulary: `valid`, `invalid`, `catch_all`, `risky`, `unknown`.
- [ ] Freeze confidence score mapping and score breakdown schema.
- [ ] Freeze webhook callback payload contract.

## Service track

- [ ] Harden single verify path: syntax -> DNS -> SMTP -> scoring.
- [ ] Harden bulk job path: dedupe, plan checks, queueing, worker updates.
- [ ] Add explicit `failed` job status path for partial/system failures.
- [ ] Add retry and dead-letter handling for poisoned tasks.

## Surface track

- [ ] Map `/email` dashboard verifier tab to v1 contract fields.
- [ ] Ensure progress bars consume `processed/total/percentage` consistently.
- [ ] Show “why” diagnostics from `score_details` in verifier UI panel.

## Data track

- [ ] Normalize key verification columns in `results` for queryable analytics.
- [ ] Add job events timeline table (queued, started, completed, failed, retried).

## Ops track

- [ ] Load-test bulk verification throughput for 10k email payload.
- [ ] Add queue lag and worker saturation dashboards.
- [ ] Add SMTP provider timeout/error budget alerts.

---

## Hardening backlog (maps to `version_2.7` — Mailvetter Hardening)

Aligned with [`docs/codebases/mailvetter-codebase-analysis.md`](../codebases/mailvetter-codebase-analysis.md) **Immediate execution queue**.

### Distributed rate limiting

- [ ] Replace **in-memory** rate limiter with **Redis-backed** limiter safe for multiple API replicas.  
- [ ] Document degrade behavior when Redis is unavailable (fail closed vs open — pick explicitly).

### Migration discipline

- [ ] Move DB migrations out of **application startup** into an explicit **migration pipeline** (deploy job or init container).  
- [ ] Record migration ordering and rollback notes per release.

### Idempotency

- [ ] Add **idempotency keys** (header or body) for **bulk job create** so retries do not duplicate work or charges upstream.

### Secret isolation

- [ ] **Webhook signing secret** must not fall back to `API_SECRET_KEY`; provision and rotate independently.  
- [ ] Runbook: rotate webhook secret without breaking in-flight callbacks.

#### Env var contract (explicit)

- `WEBHOOK_SECRET_KEY` is **required** for webhook signing in hardened deployments.
- `API_SECRET_KEY` must never be used as a fallback for webhook signing (blast radius isolation).

### Legacy surface

- [ ] Freeze/deprecate **legacy** endpoints; keep **v1** as the canonical public contract.  
- [ ] Remove or feature-flag **legacy static UI** (`/upload`, `/status`) per deployment policy.

### Job lifecycle clarity

- [ ] Harden job status vocabulary: `pending` / `processing` / `completed` / `failed` with explicit **failed** for system/poison paths.  
- [ ] **Dead-letter** queue handling for poison tasks with alert.

### Verification

- [ ] Endpoint **parity tests** between OpenAPI/docs and runtime for all **v1** routes.

## Immediate execution queue (copy/paste gate for 2.7.x)

These are straight from the codebase analysis “Immediate execution queue”, expressed as actionable gates:

1. - [ ] Freeze/deprecate legacy endpoints; keep v1 as canonical API contract. (Targets: `internal/api/router.go`, legacy routes)
2. - [ ] Replace in-memory limiter with Redis-backed distributed limiter. (Targets: limiter middleware; Redis config)
3. - [ ] Move DB migrations out of runtime startup into explicit migration pipeline. (Targets: `internal/store/db.go`)
4. - [ ] Separate webhook secret from API secret (no fallback coupling). (Targets: webhook signing; env vars)
5. - [ ] Add idempotency keys for bulk job create endpoint. (Targets: `ValidateBulkHandler`, job create)
6. - [ ] Harden status vocabulary + explicit failure paths (`pending/processing/completed/failed`). (Targets: jobs/status mapping)
7. - [ ] Add endpoint parity tests between docs and runtime for all v1 routes. (Targets: tests folder + OpenAPI docs)
