# Backend language strategy (Python GraphQL spine + Go/Gin services)

This document is the **canonical** statement of how programming languages are used across Contact360 backends. It resolves an apparent tension: **most** HTTP/RPC backends should move to **Go + Gin**, while the **primary product API** remains **Python**.

## Non-negotiable anchor

| Service | Role | Stack (canonical) |
| --- | --- | --- |
| **`contact360.io/api`** | **Appointment360** — sole GraphQL gateway for dashboard, extension, and orchestration | **Python** — FastAPI + Strawberry GraphQL, async SQLAlchemy, asyncpg |

This codebase is the **main backend**: auth, billing, credits, GraphQL modules, and downstream client orchestration. **There is no plan to replace it with Go** unless product/engineering explicitly launches a separate migration program (new GraphQL server in Go would be a multi-quarter program with contract freeze and dual-run).

## Target stack for satellite backends

**New services and rewrites** of non-gateway backends should standardize on:

- **Go 1.2x**, **Gin** for HTTP APIs
- **PostgreSQL** via `pgx` / sqlc where applicable
- Shared patterns with existing Go trees: `contact360.io/sync` (Connectra), `backend(dev)/mailvetter`, `backend(dev)/email campaign`, `lambda/emailapigo` (Go portions)

Examples of “satellite” backends: verification, campaign delivery workers, ingestion, AI edge services, thin adapters in `lambda/` that are not tied to Django.

## Long-lived exceptions (documented)

| Area | Current stack | Notes |
| --- | --- | --- |
| **`contact360.io/admin`** (DocsAI) | Django | Operational/docs surface; not the customer GraphQL API. Rewriting to Go is optional and independent of the gateway. |
| **`contact360.io/jobs`** (TKD Job) | Python, Kafka consumers | Scheduler/DAG ecosystem; any move to Go is a **dedicated** reliability/infra project, not implied by “Gin everywhere”. |
| **Legacy `lambda/*` Python** | FastAPI / Python | Migrate **per service** to Go when ownership and tests allow; until then, treat as supported. |

## Satellite migration inventory (EC2 Go targets)

| Service | Current (Python / legacy) | Target Go module / path | Blocker / notes | Evidence |
| --- | --- | --- | --- | --- |
| S3 Storage | `lambda/s3storage/` | `EC2/s3storage.server/` — `contact360.io/s3storage` | Multipart + metadata parity, Redis for Asynq | `EC2/s3storage.server/`, `docs/backend/services.apis/s3storage.api.md` |
| Logs API | `lambda/logs.api/` | `EC2/log.server/` — `contact360.io/logsapi` | S3 TTL sweep + flush semantics | `EC2/log.server/` |
| Contact AI / Resume AI | `backend(dev)/contact.ai/`, `resumeai/` | `EC2/ai.server/` — `contact360.io/ai` | HF router keys, chat store (Postgres optional) | `EC2/ai.server/` |
| Sales Navigator façade | `backend(dev)/salesnavigator/` | `EC2/extension.server/` — `contact360.io/extension` | Connectra bulk routes, scrape stays client-side | `EC2/extension.server/` |

## Documentation and era folders

- **Hub docs** (`docs/docs/*.md`, `docs/backend/README.md`) should describe **current** repos plus **target** language where it helps planning.
- **Era task packs** (`docs/0`–`10`, `docs/analysis/*`) are updated **incrementally** when a service ships a language change — do not bulk-replace historical analysis files in one pass without code evidence.

## Smaller tasks (rollout)

| # | Task |
| --- | --- |
| 1 | When adding a **new** microservice under `lambda/` or `backend(dev)/`, default to **Go + Gin** unless it must embed Python ML libraries. |
| 2 | For each existing **Python** satellite (`salesnavigator`, `contact.ai`, `resumeai`, Python `lambda/*`), maintain a **one-pager** in `docs/codebases/*` with “current vs target” and migration risks. |
| 3 | Keep **GraphQL schema and `docs/backend/apis/*`** aligned with **`contact360.io/api`** (Python) until a formal gateway migration exists. |
| 4 | Update **CI** matrices when a service switches language (build, test, Docker). |
| 5 | Mirror this strategy in **DocsAI** architecture constants when those files include language/stack bullets (`docs/docs/docsai-sync.md` workflow). **Done:** `contact360.io/admin/apps/architecture/constants.py` + blueprint **Notes** column. |

## Related

- Monorepo layout: `docs/docs/architecture.md`
- Backend operating map: `docs/docs/backend.md`
- Data stores: `docs/docs/data-stores-postgres.md`
- Consolidation plan (historical): `docs/plans/contact360_full_consolidation_b163ccfb.plan.md`
