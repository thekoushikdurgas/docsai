# Mailvetter — 6.x Reliability & Scaling Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `6.x` — Reliability and scale hardening

## Contract track

- [ ] Define SLOs: p95 single verify latency, bulk completion SLA, queue lag thresholds.
- [ ] Define idempotent bulk job-create behavior.

## Service track

- [ ] Move rate limiter to Redis-backed distributed implementation.
- [ ] Add idempotency key support on bulk create endpoint.
- [ ] Add worker retry + dead-letter queue.
- [ ] Add clear `processing` and `failed` transitions for jobs.

## Surface track

- [ ] Add retry-state indicators in progress UI.
- [ ] Add per-job error summary panel.

## Data track

- [ ] Add `job_events` and `job_failures` tables.
- [ ] Add correlation IDs in job/result rows for traceability.

## Ops track

- [ ] Autoscaling policy based on Redis queue depth.
- [ ] Alerts on queue lag, error rate, webhook failure rate.
- [ ] Chaos test for Redis outage and DB transient failures.
