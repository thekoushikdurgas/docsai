# extension.server — deploy (Era 7)

## Binary

- **API:** `go run ./cmd/api` or build `cmd/api` (module `contact360.io/extension`).
- **Worker stub:** `go run ./cmd/worker` — idle; optional future Redis queue not implemented.

## Listen address

- Default **`:8092`** (`EXTENSION_PORT`).
- Example public base: **`http://3.91.83.154:8092`** (align port with `EXTENSION_PORT` in systemd/env).

## Environment

See [`AUTH-ENV.md`](./AUTH-ENV.md). Connectra URL must reach **sync.server** (typically port **8000** on the same VPC).

## Git

Satellite repo remote: **`https://github.com/thekoushikdurgas/extension.server.git`** (see [`EC2/extension.server/.git/config`](../../../../EC2/extension.server/.git/config)).

## Verification (E2E smoke)

With **sync.server** on `:8000` and **extension.server** on `:8092`, matching **`CONNECTRA_API_KEY`** / **`APIKey`** and **`EXTENSION_API_KEY`**:

1. `GET http://localhost:8092/health` → 200.
2. `POST http://localhost:8000/internal/extension/upsert-bulk` with `X-API-Key` and a minimal `{ "contacts": [...], "companies": [...] }` body → 200 (requires DB/OpenSearch as usual).
3. `POST http://localhost:8092/v1/save-profiles` with `X-API-Key` and `profiles` including a **LinkedIn URL** in `id` and no email → extension forwards to Connectra; contact upserts by **`linkedin_url`** when email is absent.

Last updated: 2026-04-15.
