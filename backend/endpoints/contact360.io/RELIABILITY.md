# Reliability

- **REST:** `/health`, `/health/db`, `/health/logging`, `/health/slo`, `/health/token-blacklist`.
- **GraphQL:** `health.apiHealth`, `health.vqlHealth`, `health.satelliteHealth` (authenticated satellite pings).
- **Idempotency:** Postgres-backed `graphql_idempotency_replays` + middleware on selected mutations.
- **Abuse guard:** Postgres `graphql_abuse_guard_events` + RPM limits on billing mutations.
- **Token blacklist:** Periodic cleanup; stats exposed via health.
- **SLO:** `SLO_ERROR_BUDGET_PERCENT` + RED metrics middleware.
