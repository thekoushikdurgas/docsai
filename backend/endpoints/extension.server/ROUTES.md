# extension.server — route inventory (Era 0)

Source: [`EC2/extension.server/internal/api/router.go`](../../../../EC2/extension.server/internal/api/router.go).

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/health` | none | Liveness; JSON `{"status":"ok","service":"extension"}` |
| POST | `/v1/save-profiles` | `X-API-Key` or `api_key` | Parse `profiles[]`, dedupe, chunk, **companies then contacts** via Connectra **`POST /companies/batch-upsert`** and **`POST /contacts/batch-upsert`** |
| POST | `/v1/scrape` | same | Parse Sales Navigator HTML; optional `save: true` → same batch-upsert path |
| POST | `/v1/contacts/search` | same | Proxy → Connectra `POST /contacts/` (VQL) |
| POST | `/v1/companies/search` | same | Proxy → Connectra `POST /companies/` (VQL) |
| POST | `/v1/contacts/batch-upsert` | same | Proxy → Connectra `POST /contacts/batch-upsert` |
| POST | `/v1/companies/batch-upsert` | same | Proxy → Connectra `POST /companies/batch-upsert` |

**Connectra (sync.server):** Upserts use **`POST /companies/batch-upsert`** then **`POST /contacts/batch-upsert`**. Successful responses include **`company_uuids`** / **`contact_uuids`** (input order). **extension.server** also **falls back** to UUIDs from the outbound request payload if the upstream JSON omits those arrays (older Connectra builds).

**Worker pool:** Parallelism is an **in-process** bounded pool ([`internal/worker/pool.go`](../../../../EC2/extension.server/internal/worker/pool.go)), sized by **`EXTENSION_WORKERS`**. **`cmd/worker`** is a **stub** (idle loop) — there is **no Redis-backed queue** in this repo path.

Last updated: 2026-04-20.
