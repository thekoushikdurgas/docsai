# email.server — public vs private HTTP routes

Base path: server root (no `/v1` prefix).

## Public (no `X-API-Key`)

| Method | Path | Notes |
|--------|------|--------|
| GET | `/health` | Liveness; Postgres + Redis ping; **503** if degraded |
| GET | `/` | Service metadata and route index |

## Private (`X-API-Key` required)

All routes registered on `authGroup` ([`SetupRouter`](../../../../EC2/email.server/internal/api/router.go)):

| Prefix | Examples |
|--------|----------|
| `/jobs` | `GET /jobs`, `GET /jobs/:id/status`, `POST /jobs/:id/pause|resume|terminate` |
| `/email` | `POST /email/finder/`, `/finder/bulk`, `/finder/s3`, `/single/verifier/`, `/bulk/verifier/`, `/verify/s3`, `/pattern/s3` |
| `/web` | `POST /web/web-search` |
| `/email-patterns` | `POST /email-patterns/add`, `/add/bulk`, `/predict`, `/predict/bulk` |

Optional header on all routes: **`X-Request-ID`** (echoed or generated).
