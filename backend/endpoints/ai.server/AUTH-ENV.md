# ai.server — authentication and environment (Era 1)

## HTTP authentication

When **`AI_API_KEY`** is non-empty, all routes except **`GET /health`** and **`GET /health/ready`** require **`X-API-Key`** (or query **`api_key`**) to match.

## Go service (`EC2/ai.server`)

| Variable | Purpose |
|----------|---------|
| `AI_PORT` | HTTP listen port (default **3000**) |
| `AI_API_KEY` | Shared API key for private routes |
| `DATABASE_URL` | Optional Postgres for `ai_chats` / `ai_chat_messages` |
| `HF_API_KEY` | Hugging Face router (required for LLM + `/health/ready`) |
| `HF_CHAT_MODEL`, `HF_FALLBACK_MODELS`, `HF_EMBED_MODEL`, `HF_ROUTER_BASE` | HF model routing |
| `REDIS_ADDR` | Required for **`cmd/worker`** (Asynq) |
| `WORKER_CONCURRENCY` | Asynq worker concurrency (default **10**) |
| `CONNECTRA_API_URL`, `CONNECTRA_API_KEY` | sync.server (VQL) |
| `EMAIL_SERVER_API_URL`, `EMAIL_SERVER_API_KEY` | email.server finder |
| `PHONE_SERVER_API_URL`, `PHONE_SERVER_API_KEY` | phone.server finder |
| `S3STORAGE_SERVER_API_URL`, `S3STORAGE_SERVER_API_KEY` | Presign download |

See [`EC2/ai.server/.env.example`](../../../../EC2/ai.server/.env.example).

## Gateway (`contact360.io/api`)

| Variable | Purpose |
|----------|---------|
| `AI_SERVER_API_URL` | Base URL only (e.g. `http://16.176.172.50:3000`) |
| `AI_SERVER_API_KEY` | Must match `AI_API_KEY` on ai.server |
| `AI_SERVER_API_TIMEOUT` | HTTP client timeout |

Last updated: 2026-04-15.
