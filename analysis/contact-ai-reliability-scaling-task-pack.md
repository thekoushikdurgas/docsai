# Contact AI — 6.x Reliability and Scaling Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `6.x` — Reliability and Scaling  
**Status:** SLO targets, SSE reliability, TTL, tracing

---

## Contract track

- [ ] Define SLO targets for contact.ai:
  - Sync message response p95 < 3s
  - SSE first-token latency p95 < 1s
  - Utility AI endpoints p95 < 2s
  - Availability target: 99.5%
- [ ] Document retry and timeout contract: max retries, backoff policy, `Retry-After` header behavior.
- [ ] Define SSE stream error format: `data: {"error": "<message>", "code": "<code>"}\n\n`.
- [ ] Document idempotency contract for `POST /message`: repeated calls with same payload must not create duplicate messages.

## Service track

- [ ] Add SSE stream error handling: catch Lambda timeout, HF stream abort; emit error event and close stream cleanly.
- [ ] Implement SSE client reconnect logic: `Last-Event-ID` support or state-based resume.
- [ ] Add optimistic lock (version column or ETag) to `ai_chats` to prevent concurrent message append races.
- [ ] Implement chat archival TTL: define max chat age; background Lambda to soft-delete stale chats.
- [ ] Add distributed tracing: AWS X-Ray or OTEL context propagation across Lambda invocations.
- [ ] Tune HF + Gemini retry budgets: max 2 retries on HF, then 1 Gemini attempt, then 503.
- [ ] Health endpoint improvements: `/health/db` must report connection pool state; add `/health/hf` for HF API reachability.

## Surface track

- [ ] Implement `AIErrorState` component: shows error type (timeout, rate limit, service unavailable) with retry CTA.
- [ ] Implement retry button: re-sends last failed message (cached in `AIChatContext`).
- [ ] Implement SSE reconnect in `useStreamMessage`: reconnect on stream abort with exponential backoff.
- [ ] Show `Retry-After` countdown in rate limit error state (use `RateLimitError.retryAfter`).
- [ ] Loading progress for long-running requests: indeterminate progress bar above chat input.

## Data track

- [ ] Add `version` column to `ai_chats` for optimistic concurrency control.
- [ ] Define and document TTL / archival strategy: chats older than N days → archived or deleted.
- [ ] Add lineage note to `contact_ai_data_lineage.md`: archival lifecycle and compliance retention.
- [ ] Confirm `updated_at` timestamp is updated atomically with `messages` JSONB on every write.

## Ops track

- [ ] Wire distributed tracing: X-Ray SDK in Lambda, trace propagation to HF/Gemini calls.
- [ ] Add alerting: PagerDuty/SNS alert on p95 latency breach and `503` rate spike.
- [ ] Lambda memory and timeout tuning: benchmark with production-scale message histories.
- [ ] Add contact.ai to the SLO dashboard (alongside jobs, emailapis, connectra).
- [ ] Runbook: steps to handle HF API outage (switch to Gemini-only mode, disable streaming).

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/frontend/contact-ai-ui-bindings.md`
