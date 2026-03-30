# Sales Navigator — 6.x Reliability & Scaling Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `6.x` — Contact360 Reliability and Scaling  
**Status:** Hardening: rate limits, idempotency, CORS, tracing

---

## Contract track

- [ ] Define SLOs for `save-profiles`:
  - p95 latency < 5s for 100 profiles
  - p99 latency < 15s for 500 profiles
  - Availability: 99.5% monthly
- [ ] Define `Retry-After` header semantics on `429` rate-limit responses
- [ ] Define partial success response contract: `{success: true, saved_count: N, errors: [...]}` is valid even with N < total
- [ ] Add `X-Request-ID` response header (pass-through or generate if absent)

## Service track

- [ ] Implement `TokenBucketRateLimiter` middleware (or equivalent):
  - Per-API-key: 100 req/min; configurable via env
  - Return `429` with `Retry-After` header on exhaustion
- [ ] Add chunk-level idempotency token: generate per save session; pass as Connectra request context for replay safety
- [ ] Add circuit breaker / retry budget around Connectra calls:
  - 3 retries with exponential backoff (already in `tenacity` config — confirm coverage)
  - Circuit opens after 5 consecutive `ConnectraAPIError` in 60s window
- [ ] Tighten CORS from `*` to explicit allowed origins (extension origin + dashboard origin)
- [ ] Add `X-Request-ID` correlation header to all responses (generate UUID4 if not provided)
- [ ] Implement proper timeout escalation: confirm adaptive timeout formula is correct

## Surface track

- [ ] Partial-save UX: show "18 saved, 2 failed" with per-failed-profile detail
- [ ] `SNRetryButton` — re-attempt only failed profiles (not full batch)
- [ ] `RetryAfterBanner` — show countdown when rate-limited
- [ ] Loading state improvements: chunked progress update (each chunk completion bumps progress)
- [ ] Error recovery: on Lambda timeout, show "Please try again — some profiles may have saved"

## Data track

- [ ] Chunk idempotency key: store per chunk in Connectra request metadata to prevent replay duplication
- [ ] Replay-safe ingest: same profile UUID + same data → no-op at Connectra level (confirm Connectra upsert semantics)
- [ ] Partial success tracking: log `{session_id, total, saved, failed, timestamp}` per save session

## Ops track

- [ ] Load test: 1000-profile batch — measure Lambda duration, Connectra throughput, error rate
- [ ] CloudWatch / observability:
  - Alarm: `save-profiles` error rate > 5%
  - Alarm: Lambda timeout rate > 1%
  - Alarm: Connectra `5xx` rate > 3%
- [ ] Dashboard: p95 latency by batch size
- [ ] Error budget: define burn rate alert thresholds
- [ ] Connectra availability dependency documented in runbook

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`

---

## Extension surface contributions (era sync)

### Era 6.x — Reliability & Scaling

**`extension/contact360` reliability patterns:**
- `utils/lambdaClient.js` — exponential back-off with jitter; `MAX_RETRIES = 3` (configurable)
- Request queueing: one batch at a time prevents Lambda API overload
- Adaptive timeout: increases per retry attempt to handle Lambda cold-starts
- Payload pruning: `pruneProfile()` reduces request size; improves throughput

**Tasks:**
- [ ] Benchmark `lambdaClient` under 100-profile batches with simulated Lambda cold-starts
- [ ] Document retry + jitter formula in extension README
- [ ] Add telemetry: log dedup ratios and error rates to Logs API per session
- [ ] Set CloudWatch alarm if `save-profiles` error rate > 5% per hour