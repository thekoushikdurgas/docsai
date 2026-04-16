# Connectra — public vs private HTTP routes

Base path: server root (no `/v1` prefix today).

## Public (no `X-API-Key`)

| Method | Path | Notes |
|--------|------|--------|
| GET | `/health` | Liveness / dependency checks |

## Private (`X-API-Key` required)

All routes below `middleware.APIKeyAuth()`:

- `/common/*` — batch upsert, S3 URLs, jobs, filters  
- `/contacts/*` — VQL list/count, batch-upsert, CRUD, upsert, bulk  
- `/companies/*` — same pattern for companies  

Optional header on all routes: **`X-Request-ID`** (echoed on response if generated).
