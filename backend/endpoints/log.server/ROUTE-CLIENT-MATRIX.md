# log.server — gateway client vs HTTP routes

Source of truth for parity checks:

- **Gateway:** [`contact360.io/api/app/clients/logs_client.py`](../../../../contact360.io/api/app/clients/logs_client.py) (`LogsServerClient`, `get_logs_server_client`)
- **Server:** [`EC2/log.server/internal/api/router.go`](../../../../EC2/log.server/internal/api/router.go)

**Queue / persistence:** Async work uses **Redis + Asynq** in [`cmd/worker`](../../../../EC2/log.server/cmd/worker/main.go) (`logs:flush`, `logs:sweep`). There is **no PostgreSQL** in this service. Hot data is **in-memory**; periodic CSV snapshots go to **S3** under `logs/flush/YYYY/MM/DD/HH.csv`.

Auth for protected routes: header **`X-API-Key`** or query **`api_key`** must equal **`LOGSAPI_API_KEY`** when set (empty key disables auth for local dev).

| `LogsServerClient` method | HTTP | Notes |
|---------------------------|------|--------|
| `health_check` | `GET /health` | Liveness |
| `create_log` | `POST /logs` | Body maps to Go `store.Entry` via client (`meta` JSON for extra fields) |
| `create_logs_batch` | `POST /logs/batch` | JSON `{"items":[...]}`; max **100** per request (client chunks larger batches) |
| `query_logs` | `GET /logs` | `limit`, `offset`/`skip`, `level`, `logger`; response `items` + `total` |
| `search_logs` | `GET /logs/search` | Query param **`q`** (alias `query`), `limit`, `offset`/`skip` |
| `update_log` | `PUT /logs/:id` | `message`, `meta` (client maps `context` → `meta` JSON) |
| `delete_log` | `DELETE /logs/:id` | |
| `delete_logs_bulk` | `POST /logs/delete` | JSON filters: `level`, `logger`, `user_id`, `request_id`, `start_time`, `end_time` (RFC3339), or `ids` |
| `get_statistics` | — | **Not implemented** on Go service (`GET /logs/statistics` returns 404); GraphQL `logStatistics` uses [`LogStatsRepository`](../../../../contact360.io/api/app/repositories/log_stats_repository.py) |

**Public (no API key when `LOGSAPI_API_KEY` is set):** `GET /health` only.

Last reviewed: 2026-04-15.
