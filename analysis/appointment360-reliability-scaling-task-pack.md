# Appointment360 (contact360.io/api) — Era 6.x Reliability & Scaling Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Document SLO targets (error budget 1.0%, latency p99 < 2s) in `docs/governance.md` | P0 |
| Define `/health/slo` endpoint contract: returns current error rate, budget consumed | P0 |
| Define `/health/db` response schema: pool size, overflow, active connections | P0 |
| Specify rate limit headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset` | P1 |
| Document idempotency contract: `X-Idempotency-Key` header, 24h TTL, replay semantics | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Enable `GraphQLRateLimitMiddleware`: set `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` > 0 in production | P0 |
| Enable `GraphQLMutationAbuseGuardMiddleware`: set `ABUSE_GUARDED_MUTATIONS` list | P0 |
| Enable `GraphQLIdempotencyMiddleware`: set `IDEMPOTENCY_REQUIRED_MUTATIONS` list | P0 |
| Enable `QueryComplexityExtension`: set `GRAPHQL_COMPLEXITY_LIMIT` to 100 | P0 |
| Enable `QueryTimeoutExtension`: set `GRAPHQL_QUERY_TIMEOUT` to 30s | P0 |
| Add `get_pool_stats()` to `db/session.py` and expose via `/health/db` | P0 |
| Add `check_pool_health()` and alert if `overflow > 0` | P0 |
| Configure database pool: `DATABASE_POOL_SIZE=25`, `DATABASE_MAX_OVERFLOW=50` | P0 |
| Move idempotency state to Redis for multi-replica shared state | P1 |
| Move abuse guard sliding window to Redis for multi-replica | P1 |
| Add `TTLCache` for user object with `USER_CACHE_TTL` (300s default) | P1 |
| Add `DataLoaders` for all foreign-key fetches to eliminate N+1 | P1 |
| Add query depth limit extension | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Dashboard status bar shows GraphQL latency from `X-Process-Time` header | P1 |
| Rate limit exceeded modal — parse `X-RateLimit-Remaining: 0` response and display warning | P1 |
| Retry-safe mutations: ensure billing/payment mutations send `X-Idempotency-Key` | P0 |
| Connection pool exhaustion banner: surface when `/health/db` shows pool full | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Create `idempotency_keys` table (fallback if Redis unavailable): key, response_hash, expires_at | P1 |
| Instrument DB session events: log slow queries (> 500ms) | P0 |
| Add `request_id` + `trace_id` to all log lines for correlation | P0 |
| Add `RED metrics` (rate, error, duration) aggregation store | P0 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure `REDIS_URL`, `ENABLE_REDIS_CACHE=true` for production | P1 |
| Set `GRAPHQL_MAX_BODY_BYTES=2097152` (2MB) in production | P0 |
| Load test: 500 concurrent `query contacts(query)` requests through gateway | P1 |
| Load test: 50 concurrent billing mutations with idempotency keys | P1 |
| Add alert: error rate > 1% in 5-minute window → PagerDuty | P1 |
| Add alert: DB pool overflow > 0 for > 60s → PagerDuty | P1 |
| Document SLO dashboard in ops runbook | P1 |

---

## Email app surface contributions (era sync)

- Existing resilience: loading/error states and spinner-driven async UX.
- Hardening backlog: retry/backoff, structured telemetry, boundary handling.
