# Contact360 data stores (PostgreSQL-first)

This page is the **canonical** summary of which systems use PostgreSQL vs other stores. It complements **`docs/docs/architecture.md`**. **Which services are Python vs Go:** **`docs/docs/backend-language-strategy.md`**.

## Appointment360 (`contact360.io/api`)

| Concern | Store | Notes |
| --- | --- | --- |
| GraphQL idempotency | **PostgreSQL** (`graphql_idempotency_replays`) | Default `IDEMPOTENCY_BACKEND=postgres`. |
| Multipart upload sessions | **PostgreSQL** (`upload_sessions`) | Default `UPLOAD_SESSION_BACKEND=postgres`. In-memory `memory` is for single-process dev/tests only. |
| JWT blacklist / user data | **PostgreSQL** | — |
| **Redis** | **Removed** from this service | No `REDIS_URL`, upload Redis, or optional Redis cache in the FastAPI app. |

## Go workers (Redis is **bounded** to workers only)

| Service | Queue / coordination | Persistence | Migration path |
| --- | --- | --- | --- |
| `EC2/email campaign` (Go Gin) | **Asynq → Redis** | PostgreSQL for campaign data | Replace Asynq with a Postgres-backed queue (e.g. River) or external broker — **not** done in-repo yet. |
| `backend(dev)/mailvetter` (Go) | **Redis lists** + rate limiter | PostgreSQL for jobs/results | Reimplement queue with `SKIP LOCKED` / `LISTEN` or shared library; **not** done in-repo yet. |

Production **`docker-compose.prod.yml`** still runs a **`redis`** container **only** for these Go worker services (email campaign + mailvetter). No Python app or Next.js frontend in Contact360 depends on Redis.

## DocsAI (`contact360.io/admin`)

Optional **Redis** for Django cache and Django-Q **when** `USE_REDIS_CACHE=True`. Default is **LocMem** + ORM broker — no Redis required for single-instance deployments.

## Smaller tasks (remaining Redis → Postgres or broker change)

| Priority | Task | Owner path |
| --- | --- | --- |
| P0 | **Done:** Remove Redis from `contact360.io/api` (upload sessions, optional cache flags). | `contact360.io/api/` |
| P1 | **Email campaign:** Replace Asynq with a Postgres-backed queue (e.g. [River](https://github.com/riverqueue/river)) or keep Redis until a dedicated epic. | `backend(dev)/email campaign/` |
| P1 | **Mailvetter:** Replace Redis list queue with `SKIP LOCKED` job table (or shared queue lib); align rate limiter with Postgres or gateway. | `backend(dev)/mailvetter/...` |
| P2 | **Gate:** Remove **`redis`** service from root `docker-compose.prod.yml` only after **both** P1 queues (campaign + mailvetter) no longer bind to Redis; verify workers start and drain with Postgres-backed queues. | `docker-compose.prod.yml`, `deploy/env/*.env` |
| P3 | DocsAI: optional Django Redis cache — migrate to Postgres-backed cache or keep LocMem for single-instance. | `contact360.io/admin/` |
| Docs | Keep **`docs/docs/data-stores-postgres.md`** and **`docs/docs/architecture.md`** aligned when queue work lands. | `docs/` |

## Related

- Consolidation plan reference: `docs/plans/contact360_full_consolidation_b163ccfb.plan.md`
- AWS topology: `deploy/aws/SYSTEM_DESIGN.md`
