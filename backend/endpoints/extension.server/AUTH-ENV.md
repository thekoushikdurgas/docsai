# extension.server — authentication and environment (Era 1)

## HTTP authentication (extension API)

When **`EXTENSION_API_KEY`** is non-empty, all routes except **`GET /health`** require **`X-API-Key`** or query **`api_key`** to match. Empty key disables the check (dev only).

## Go service (`EC2/extension.server`)

| Variable | Purpose |
|----------|---------|
| `EXTENSION_PORT` | HTTP listen port (default **8092**) |
| `EXTENSION_API_KEY` | Shared API key for `/v1/*` |
| `EXTENSION_WORKERS` | In-process pool size for Connectra chunks (default **8**) |
| `CONNECTRA_API_URL` | sync.server base URL (no path), e.g. `http://localhost:8000` |
| `CONNECTRA_API_KEY` | **Must equal** sync.server `APIKey` — sent as **`X-API-Key`** (not Bearer) |

See [`EC2/extension.server/.env.example`](../../../../EC2/extension.server/.env.example).

## Connectra (`EC2/sync.server`)

Uses **`X-API-Key`** globally after `/health` ([`middleware/authMiddleware.go`](../../../../EC2/sync.server/middleware/authMiddleware.go)). Extension’s Connectra client must use the same header — implemented in [`internal/connectra/client.go`](../../../../EC2/extension.server/internal/connectra/client.go).

## Gateway (`contact360.io/api`)

| Variable | Purpose |
|----------|---------|
| `SALES_NAVIGATOR_SERVER_API_URL` | Base URL of extension.server (e.g. `http://3.91.83.154:8092`) |
| `SALES_NAVIGATOR_SERVER_API_KEY` | Must match **`EXTENSION_API_KEY`** on the Go service |
| `SALES_NAVIGATOR_SERVER_TIMEOUT` | HTTP client timeout |

Client: [`SalesNavigatorServerClient`](../../../../contact360.io/api/app/clients/sales_navigator_client.py) — uses **`X-API-Key`** via `BaseHTTPClient`.

Last updated: 2026-04-15.
