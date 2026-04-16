# extension.server — gateway parity (Era 10)

Checklist: Python [`SalesNavigatorServerClient`](../../../../contact360.io/api/app/clients/sales_navigator_client.py) vs [`internal/api/router.go`](../../../../EC2/extension.server/internal/api/router.go).

| Router | Client method | Status |
|--------|----------------|--------|
| `POST /v1/save-profiles` | `save_profiles` | Aligned |
| `POST /v1/scrape` | `scrape_html` | Aligned |

**Auth:** `BaseHTTPClient` sends **`X-API-Key`** — matches extension `apiKey` middleware.

**Env:** `SALES_NAVIGATOR_SERVER_*` ↔ extension `EXTENSION_*` / gateway settings — see [`AUTH-ENV.md`](./AUTH-ENV.md).

Last updated: 2026-04-15.
