# ai.server — route inventory (Era 0)

Source: [`EC2/ai.server/internal/api/router.go`](../../../../EC2/ai.server/internal/api/router.go).

## Public

| Method | Path | Notes |
|--------|------|--------|
| GET | `/health` | Liveness |
| GET | `/health/ready` | Requires `HF_API_KEY`; optional DB ping if `DATABASE_URL` set |

## Authenticated (`X-API-Key` or `api_key` when `AI_API_KEY` set)

### Gateway parity (`contact360.io/api` [`AIServerClient`](../../../../contact360.io/api/app/clients/ai_client.py))

| Method | Path |
|--------|------|
| POST | `/chat` and `/api/v1/chat` |
| GET | `/api/v1/ai-chats/` (query `limit`, `offset`) |
| POST | `/api/v1/ai-chats/` |
| GET | `/api/v1/ai-chats/:id/` |
| PUT | `/api/v1/ai-chats/:id/` |
| DELETE | `/api/v1/ai-chats/:id/` |
| POST | `/api/v1/ai-chats/:id/message` (body `message` or `content`) |
| POST | `/api/v1/ai-chats/:id/message/stream` |
| POST | `/api/v1/gemini/email/analyze` |
| POST | `/api/v1/gemini/company/summary` |
| POST | `/api/v1/gemini/parse-filters` |

### Extensions

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/vql/parse` | NL → VQL JSON (`query`, `target`: contacts\|companies) |
| POST | `/api/v1/apollo/to-vql` | Apollo URL → VQL JSON |
| POST | `/api/v1/contact/enrich` | Connectra + optional email/phone finder + HF summary |
| POST | `/api/v1/company/enrich` | Connectra + HF summary |
| POST | `/api/v1/storage/presign` | S3 presign download via s3storage.server |

### Legacy (backward compatible)

| Prefix | Purpose |
|--------|---------|
| `/ai/email/analyze`, `/ai/company/summary`, `/ai/filters/parse`, `/ai/rag/match` | Original paths |
| `/ai-chats/*` | Same as v1 without `/api/v1` prefix |

## Asynq worker (`cmd/worker`)

Task types: `ai:resume_parse`, `ai:ats_score`, `ai:vql_parse`, `ai:contact_enrich`, `ai:company_score`. Concurrency from `WORKER_CONCURRENCY` (default **10**).

Last updated: 2026-04-15.
