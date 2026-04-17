# Monorepo tech stack overview

> **Phase:** codebases  
> **Contact360** — AI-first, multi-tenant CRM (event-driven, API-first).

Single page tying apps/services to languages and frameworks.

---

## Frontend

- **`contact360.io/app`:** **Next.js 16** (App Router), React 19, TypeScript, **`graphql-request`** → `api.contact360.io/graphql`; custom CSS design system (`app/css/dashboard-kit.css`), **no Tailwind** — see `contact360.io/app/README.md`
- **`contact360.io/admin`:** **Django** + DRF + WhiteNoise, **session** auth + gateway **GraphQL** (`GRAPHQL_URL`); ops UI (jobs, billing, users, **system status** with `health.satelliteHealth`); static CSS (`static/admin/css/design-tokens.css`); deploy **admin.contact360.io** / **34.201.10.84** — see `contact360.io/admin/README.md`
- **Web / Admin (other):** React + Vite (or Next.js where SSR needed), TanStack Query, Tailwind
- **`contact360.extension`:** Chrome **MV3** (**side panel** only), vanilla JS + shared `ui/tokens.css` / `ui/components.css`; save/scrape via **`api.contact360.io/graphql`** → **`EC2/extension.server`** (`/v1/save-profiles`, `/v1/scrape`); GraphQL JWT — see `contact360.extension/README.md`, `docs/frontend/pages/extension-index.json`
- **Mobile:** Planned (React Native / Expo) — see phase 11 docs

---

## Backend services (canonical list)

| Service               | Responsibility                         | Language / runtime | Port (dev) |
| --------------------- | ---------------------------------------- | ------------------ | ---------- |
| **`contact360.io/api`** | **Central GraphQL gateway (FastAPI + Strawberry), JWT, Postgres, satellite HTTP clients** | **Python 3.11** | **8000** |
| `api-gateway`         | Routing, authn/z, rate limits            | Node or Go         | 8080       |
| `auth-service`        | Sessions, JWT, org membership            | Node               | 8101       |
| `crm-service`         | Contacts, companies, deals, activities | Node               | 8102       |
| `email-service`       | Send, track, webhooks, deliverability    | Node               | 8103       |
| `phone-service`       | SMS/voice providers, compliance          | Node               | 8104       |
| `campaign-service`    | Campaigns, sequences, templates          | Node               | 8105       |
| `ai-agent-service`    | LLM orchestration, tools, RAG            | Python / Node      | 8106       |
| `analytics-service`   | Event ingestion, scoring, aggregates     | Go                 | 8107       |
| `integration-service` | Third-party connectors, OAuth            | Node               | 8108       |
| `file-service`        | Uploads, CSV imports, presigned URLs     | Node               | 8109       |
| **`connectra` (`EC2/sync.server`)** | **Contact + company VQL search, dual-store PG+OpenSearch, CSV jobs (Asynq), S3 presign** | **Go 1.24 + Gin** | **8000** (compose; map `3000:8000` if needed) |
| **`email.server` (`EC2/email.server`)** | **Email finder/verify/patterns, S3 CSV jobs, job pause/resume; Asynq worker process** | **Go 1.24 + Gin** | **3000** (API + separate `cmd/worker`) |
| **`phone.server` (`EC2/phone.server`)** | **Phone satellite (stack derived from email.server); `/phone`, `/phone-patterns`, jobs `phoneapi_jobs`** | **Go 1.24 + Gin** | **3000** |
| **`s3storage.server` (`EC2/s3storage.server`)** | **Object storage satellite: multipart uploads, CSV analysis, metadata jobs (Redis + Asynq worker process)** | **Go + Gin** | **8087** (API; separate `cmd/worker`) |
| **`log.server` (`EC2/log.server`)** | **Logging satellite: HTTP ingest, in-memory query, S3 CSV flush, worker TTL sweep (Redis + Asynq)** | **Go + Gin** | **8091** (API; separate `cmd/worker`) |
| **`extension.server` (`EC2/extension.server`)** | **Sales Navigator scrape + `save-profiles`; Connectra bulk via `POST /internal/extension/upsert-bulk`; in-process worker pool (`cmd/worker` stub)** | **Go + Gin** | **8092** |
| **`ai.server` (`EC2/ai.server`)** | **Contact AI: Hugging Face chat, NL→VQL, Apollo URL→VQL, `/api/v1/ai-chats`, gemini-compatible routes; Asynq worker (`cmd/worker`)** | **Go + Gin** | **3000** |
| **`campaign.server` (`EC2/campaign.server`)** | **Campaigns, sequences, `/campaign-templates`, CQL search; multi-channel send (email + phone/LinkedIn stubs); Asynq worker (`cmd/worker`)** | **Go + Gin** | **9800** |

Shared libraries: `packages/shared-types`, `packages/shared-events` (Kafka contracts), `packages/shared-db`, `packages/ui`.

---

## Data

- **Postgres** — system of record, RLS per org
- **Redis** — cache, rate limits, short-lived tokens
- **Kafka** — domain events (`contact.created`, `email.opened`, …)
- **OpenSearch** — full-text search on CRM entities
- **Object storage** — S3-compatible for files and import blobs

---

## Source references

Canonical research lives under `docs/prd/` (architecture, deep-dive, API, schema, flows).

Machine-readable contracts: `docs/docs/json_schemas/` and per-folder `index.json`.

---

*Extend with implementation links as repos land.*
