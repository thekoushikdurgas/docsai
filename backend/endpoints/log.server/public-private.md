# log.server — public vs private routes

## Public (no `X-API-Key` when `LOGSAPI_API_KEY` is set)

| Method | Path |
|--------|------|
| GET | `/health` |

## Private (`api_key`)

All **`/logs`** and **`/logs/*`** routes (create, batch, list, search, get, delete, bulk delete).

Last updated: 2026-04-15.
