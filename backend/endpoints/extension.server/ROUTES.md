# extension.server — route inventory (Era 0)

Source: [`EC2/extension.server/internal/api/router.go`](../../../../EC2/extension.server/internal/api/router.go).

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/health` | none | Liveness; JSON `{"status":"ok","service":"extension"}` |
| POST | `/v1/save-profiles` | `X-API-Key` or `api_key` | Parse `profiles[]`, dedupe, chunk (500), POST to Connectra `POST /internal/extension/upsert-bulk` |
| POST | `/v1/scrape` | same | Parse Sales Navigator HTML; optional `save: true` → same Connectra bulk path |

**Connectra bridge (sync.server):** `POST /internal/extension/upsert-bulk` is implemented in [`EC2/sync.server/modules/extension/controller.go`](../../../../EC2/sync.server/modules/extension/controller.go). It is **not** a separate process; extension calls it over HTTP with **`X-API-Key`** matching Connectra’s API key.

**Worker pool:** Parallelism is an **in-process** bounded pool ([`internal/worker/pool.go`](../../../../EC2/extension.server/internal/worker/pool.go)), sized by **`EXTENSION_WORKERS`**. **`cmd/worker`** is a **stub** (idle loop) — there is **no Redis-backed queue** in this repo path (unlike email.server Asynq).

Last updated: 2026-04-15.
