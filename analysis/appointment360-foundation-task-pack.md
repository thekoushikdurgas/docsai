# Appointment360 (contact360.io/api) — Era 0.x Foundation Task Pack

## Service identity

- **Codebase**: `contact360.io/api`
- **Role**: GraphQL gateway and primary API surface for all Contact360 dashboard operations
- **Runtime**: FastAPI + Strawberry GraphQL + asyncpg + PostgreSQL
- **Era anchor**: Minimal schema, bootstrap middleware, health endpoints, DB session lifecycle

---

## Contract track

| Task | Priority | Patch assignment |
| --- | --- | --- |
| Define minimal GraphQL schema with `Query { health }` and `Mutation { _empty }` root | P0 | `0.1.0`–`0.1.2` |
| Register `/health`, `/health/db`, `/health/logging`, `/health/slo` HTTP endpoints | P0 | `0.1.0`–`0.1.2` |
| Establish Pydantic `Settings` model with environment variable layout (`config.py`) | P0 | `0.1.0`–`0.1.2` |
| Document schema composition pattern (`schema.py` imports each module `Query`/`Mutation` class) | P0 | `0.1.0`–`0.1.2` |
| Write OpenAPI-compatible health spec (even though API is GraphQL-only) | P1 | `0.1.3`–`0.1.6` |

---

## Service track

| Task | Priority | Patch assignment |
| --- | --- | --- |
| Bootstrap FastAPI app with `app = FastAPI(...)` and basic exception handlers | P0 | `0.1.0`–`0.1.2` |
| Configure `CORSMiddleware` with `CORS_ORIGINS` from settings | P0 | `0.1.0`–`0.1.2` |
| Configure `CORSFriendlyTrustedHostMiddleware` with `TRUSTED_HOSTS` | P0 | `0.1.0`–`0.1.2` |
| Register `GZipMiddleware` (optional, behind config flag) | P0 | `0.1.0`–`0.1.2` |
| Register `REDMetricsMiddleware` for rate/error/duration tracking | P0 | `0.1.0`–`0.1.2` |
| Add `RequestIdMiddleware` + `TraceIdMiddleware` for distributed tracing | P0 | `0.1.0`–`0.1.2` |
| Add `TimingMiddleware` — write `X-Process-Time` to all responses | P0 | `0.1.0`–`0.1.2` |
| Register `DatabaseCommitMiddleware` — ensure session commit/rollback on every request | P0 | `0.1.0`–`0.1.2` |
| Create async engine and session factory in `db/session.py` | P0 | `0.1.0`–`0.1.2` |
| Write `get_db()` dependency: yield `AsyncSession`, commit, rollback on error | P0 | `0.1.0`–`0.1.2` |
| Add pool monitoring event listeners (`checkout`, `checkin`, `overflow`) | P1 | `0.1.3`–`0.1.6` |
| Configure Mangum handler for AWS Lambda execution target | P1 | `0.1.3`–`0.1.6` |
| Add `uvicorn` runner for EC2 execution target | P1 | `0.1.3`–`0.1.6` |
| Add Docker `Dockerfile` with multi-stage build (deps → runtime) | P1 | `0.1.3`–`0.1.6` |

---

## Surface track

| Task | Priority | Patch assignment |
| --- | --- | --- |
| Create empty placeholder modules for each planned dashboard page | P1 | `0.1.3`–`0.1.6` |
| Ensure GraphiQL IDE is available at `/graphql` (Strawberry default `graphiql=True`) | P1 | `0.1.3`–`0.1.6` |
| Establish `app/graphql/context.py` with `Context` dataclass (db, request, user, user_uuid, dataloaders) | P0 | `0.1.0`–`0.1.2` |
| Implement JWT extraction in context: read `Authorization: Bearer <token>` header, decode, load user | P0 | `0.1.0`–`0.1.2` |
| Stub `DataLoaders` class in `app/graphql/dataloaders.py` | P1 | `0.1.3`–`0.1.6` |
| Scaffold frontend auth contexts: `context/AuthContext.tsx` + `context/ThemeContext.tsx` | P0 | `0.1.0`–`0.1.2` |
| Scaffold frontend client/config: `lib/graphqlClient.ts`, `lib/tokenManager.ts`, `lib/config.ts` | P0 | `0.1.0`–`0.1.2` |
| Add a browser smoke target that calls gateway health and renders result (health module evidence) | P1 | `0.1.3`–`0.1.6` |

Cross-reference: `docs/frontend/components.md` (era `0.x` layout/components evidence for shell + auth/context primitives).

---

## Data track

| Task | Priority | Patch assignment |
| --- | --- | --- |
| Create `users` table: uuid, email, password_hash, role, is_active, created_at | P0 | `0.2.0`–`0.2.2` |
| Create `token_blacklist` table: token_hash, expires_at | P0 | `0.2.0`–`0.2.2` |
| Seed Alembic migration for initial schema | P0 | `0.2.0`–`0.2.2` |
| Document all table column types and constraints in `docs/backend/database/tables/` | P1 | `0.2.3`–`0.2.6` |

---

## Ops track

| Task | Priority | Patch assignment |
| --- | --- | --- |
| Write `.env.example` documenting all required environment variables | P0 | `0.10.0`–`0.10.2` |
| Add `startup.sh` and `run-dev.sh` scripts for local development | P0 | `0.10.0`–`0.10.2` |
| Write `README.md` with quick-start, environment setup, and GraphQL IDE note | P0 | `0.10.0`–`0.10.2` |
| Configure logging (structlog or stdlib) with correlation ID injection | P1 | `0.10.3`–`0.10.6` |
| Add Makefile targets: `dev`, `test`, `migrate`, `lint` | P1 | `0.10.3`–`0.10.6` |

---

## Email app surface contributions (era sync)

- Scaffolded `contact360.io/email` app shell, layout providers, and route partitions. (patch assignment: `0.1.3`–`0.1.6`)
- Established UI primitive baseline (buttons, inputs, tabs, table, checkbox). (patch assignment: `0.1.7`–`0.1.9`)
