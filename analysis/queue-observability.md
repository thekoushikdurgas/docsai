# Era 6.3–6.4: Queue resilience and observability baseline

This stage captures minimum controls for resilient async processing and debuggable logs.

## Trace and correlation

- Middleware: `TraceIdMiddleware` in `contact360.io/api/app/core/middleware.py`
- Request flow:
  - Reads `X-Trace-Id` if provided by caller.
  - Falls back to `X-Request-Id` or generated UUID.
  - Persists in request state and echoes `X-Trace-Id` in response headers.
- Goal: correlate gateway logs with downstream logs (`logs.api`, workers, and lambdas).

## Queue reliability guardrails (runbook baseline)

- Keep job enqueue/dequeue operations idempotent (use stable identifiers per export/import/sync job).
- Route poison messages to DLQ and expose replay tooling in scheduler services.
- Capture trace IDs in queued payload metadata so replay/debug retains context.

## DLQ / replay runbook

Use this section with **Service task slices** in `docs/6. Contact360 Reliability and Scaling/` patch files — jobs/tkdjob coverage under [`6.3 — Queue DLQ and worker resilience`](6.3%20%E2%80%94%20Queue%20DLQ%20and%20worker%20resilience.md) (and related `6.N.P` patches); Asynq/email-campaign queue scope in the same era’s patch ladder (**Service task slices** for `emailcampaign`).

### Failure classification

| Class | Definition | Examples | Default action |
| --- | --- | --- | --- |
| **Transient** | Retryable; may succeed later | `503`, DB deadlock, timeout, broker lag | Retry with backoff → DLQ if max attempts |
| **Permanent** | Bad payload or invariant violated | Schema validation, unknown enum, auth to third party | **No** blind retry → DLQ + bug ticket |
| **Poison** | Crashes worker repeatedly | NPE, panic loop | DLQ + quarantine message; fix code |

### Operator playbook

1. **Identify:** DLQ depth alert or stuck processing (`/metrics` / dashboard).
2. **Triage:** Pull sample message; read `failure_class`, `last_error`, `trace_id`.
3. **Authorize replay:** Only approved operators/service accounts (`jobs` pack **A-6.4**).
4. **Replay:** Single-message first; verify `job_events` (or equivalent) audit entry.
5. **Bulk replay:** Rate-limited; monitor error budget and downstream (email/SMS providers).
6. **Post-incident:** If permanent class misclassified, update classifier + docs.

### Replay authorization

- Document which roles/API keys may call replay endpoints per environment.
- All replay actions should emit an audit event (who, when, which message id).

## Next implementation increment

- Add explicit DLQ/replay endpoints in job scheduler adapters and document failure classes
  (transient vs permanent), retry caps, and replay authorization policy — **tracked in**
  **Service task slices** in `6.x` jobs-related patch files (`docs/6. Contact360 Reliability and Scaling/6.*.* — *.md`).
