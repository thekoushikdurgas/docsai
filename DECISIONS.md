# Contact360 — architecture decisions log

Single source of truth for cross-cutting choices referenced by `docs/**/index.json` and flows. **Do not fork** alternate patterns without updating this file.

---

## Event and topic naming

- **Dot-case, lower snake segments:** `contact.created`, `email.opened`, `campaign.completed`.
- **Versioning:** payload schemas use filename suffix `.v1.json`; envelope sets `schema_version: "v1"`.
- **Keys:** Kafka message key is `org_id` for tenant locality; secondary ordering by entity id in headers when needed.
- **Engagement family:** diagrams group opens/clicks/replies under an `email.*` engagement family; concrete topics today: `email.opened`, `email.clicked`, `email.bounced`. Add **`email.replied`** when inbound reply parsers ship (payload schema TBD).

## SSE vs WebSocket (by surface)

| Surface | Transport | Rationale |
| ------- | ----------- | ---------- |
| AI chat token stream | **SSE** | One-way server→client, simple HTTP auth, works with standard proxies |
| Extension sidebar (Flow 5) | **SSE** | MV3-friendly one-way progressive updates while enrichment jobs complete |
| Campaign send progress (web) | **SSE** | Infrequent ticks; same middleware as AI |
| CRM contact detail “live” refresh after async scoring/search | **WebSocket (optional)** | Diagram for Flow 1 shows WebSocket push after Kafka consumers; use when sub-second duplex is worth connection cost |
| Collaborative document editing | **WebSocket (future)** | True duplex not yet in scope |

When both appear in diagrams, prefer **SSE** for new features unless the UI needs client→server continuous frames.

## ECS vs EKS

- **Default: ECS Fargate** for stateless services (faster ops, lower control-plane burden at early scale).
- **EKS reserved** if multi-region service mesh or GPU node pools become dominant drivers.
- Revisit when sustained **>500** long-lived workers or strict multi-tenant network policies require CNI features not comfortable on ECS.

## GraphQL status

- **Public API:** REST (+ OpenAPI) only.
- **GraphQL:** **Deferred** — potential internal federation for admin/analytics; see `docs/backend/graphql.modules/index.json`.

## Kafka vs BullMQ (boundary)

- **Kafka:** cross-service domain events, analytics hydration, webhook fan-out, audit trail inputs.
- **BullMQ / Redis queues:** intra-service job chunking with short TTL (CSV chunk processing, scheduled campaign waves, render batches) where global cross-service ordering is not required.
- **Rule of thumb:** if multiple services must observe it durably → Kafka; if single worker pool → BullMQ.

## Enrichment waterfall order

**Abstract tiers (policy):**

1. Internal / cache (zero marginal cost)
2. Tier-1 commercial provider (breadth)
3. Tier-2 specialist or regional provider
4. Manual research queue

**Concrete CSV pipeline (from Flow 2 diagram — illustrative, swap vendors under contract):**

`Pattern Engine (rules)` → **Hunter.io** → **Apollo** → **SMTP verify (mailbox ping)** → **ZeroBounce (catch-all / risky)**

Credit spend is **reserved upfront**, **settled** on partial completion per `EnrichmentJob.json` rules.

## SMS / WhatsApp compliance (India)

- **TRAI DND** and registry checks before outbound SMS and WhatsApp where applicable.
- Cache negative/positive outcomes in **Redis** with **~24h TTL** per destination key to avoid hammering registries while staying responsive to list updates.

## Connectra (`EC2/sync.server`) — contact / company satellite

- **Language:** Go 1.24, Gin; **module:** `connectra.server` (Git remote `connectra.server` repo).
- **Stores:** Postgres (Bun ORM) + OpenSearch for VQL; Redis for Asynq job queue + hot job hashes; S3 for CSV blobs.
- **Idempotency:** UUID5 from `(first_name,last_name,linkedin_url)` for contacts and `(name,linkedin_url)` for companies — must match extension + gateway normalization.
- **Auth to satellite:** `X-API-Key` only (no JWT on Connectra); gateway holds org context and forwards scoped calls.
- **Observability:** `GET /health` aggregates Postgres + Redis + OpenSearch pings; `X-Request-ID` echoed on all responses.

## Email API (`EC2/email.server`) — finder / verify / patterns satellite

- **Language:** Go 1.24, Gin; **module:** `github.com/ayan/emailapigo` (optional rename to match `emailapis` Git remote — see `docs/backend/endpoints/email.server/MODULE-OPTIONAL.md`).
- **Workers:** Separate process [`cmd/worker`](../EC2/email.server/cmd/worker/main.go) — Asynq queues `mailtester`, `mailvetter`, `email_finder`, `email_pattern`, `default`; API enqueues only.
- **Stores:** Postgres (`emailapi_jobs`, patterns, finder cache); Redis for Asynq + per-job row hashes; S3 for CSV jobs.
- **Connectra:** Finder calls **`POST /contacts/`** on sync.server with `CONNECTRA_BASE_URL` + `CONNECTRA_API_KEY` before pattern/generator/verify.
- **Auth:** `X-API-Key` = `API_KEY`; gateway uses `EMAIL_SERVER_API_KEY` / `EMAIL_SERVER_API_URL`.
- **Observability:** `GET /health` pings Postgres + Redis (503 if degraded); `X-Request-ID` on responses.
- **Events:** No Kafka/webhooks from email.server — gateway polls `GET /jobs/:id/status` for `scheduler_jobs` with `source_service=email_server`.

## Phone API (`EC2/phone.server`) — satellite (Gin + Asynq)

- **Language:** Go 1.24, Gin; **module:** `github.com/thekoushikdurgas/phone.server` (Git remote `phone.server` repo).
- **Origin:** Scaffolded from the email satellite stack; public HTTP paths use **`/phone`** and **`/phone-patterns`**; Postgres jobs table **`phoneapi_jobs`**.
- **Workers:** Same pattern as email.server — separate [`cmd/worker`](../EC2/phone.server/cmd/worker/main.go), Asynq queues.
- **Auth:** `X-API-Key` = `API_KEY`; gateway **`PHONE_SERVER_API_URL`** / **`PHONE_SERVER_API_KEY`** ([`PhoneServerClient`](../contact360.io/api/app/clients/phone_server_client.py)).
- **Observability:** `GET /health` pings Postgres + Redis; `X-Request-ID` on responses.
- **Events:** No outbound webhooks documented — poll **`GET /jobs/:id/status`** for async jobs.

## Storage satellite (`EC2/s3storage.server`) — S3 + Redis + Asynq

- **Language:** Go (Gin); **module:** `contact360.io/s3storage` (optional rename vs Git remote `storage.server` — see [`docs/backend/endpoints/s3storage.server/MODULE-OPTIONAL.md`](backend/endpoints/s3storage.server/MODULE-OPTIONAL.md)).
- **HTTP:** Functional routes under **`/api/v1`**; **`X-API-Key`** or **`api_key`** query — see [`AUTH-ENV.md`](backend/endpoints/s3storage.server/AUTH-ENV.md).
- **Workers:** [`cmd/worker`](../EC2/s3storage.server/cmd/worker/main.go) — Asynq tasks `s3storage:metadata`, `s3storage:sync_metadata`; concurrency **`S3STORAGE_WORKER_CONCURRENCY`** (default **10**).
- **Stores:** **Redis** for multipart sessions and job hashes (not a Postgres queue table); **S3** for objects and `metadata.json`; CRM Postgres remains in the gateway.
- **Gateway:** **`S3STORAGE_SERVER_API_URL`** / **`S3STORAGE_SERVER_API_KEY`** ([`S3StorageEC2Client`](../contact360.io/api/app/clients/s3storage_client.py)); base URL without `/api/v1` suffix.
- **Observability:** `GET /api/v1/health`, `GET /api/v1/health/ready` (Redis + S3); **`X-Request-ID`** on all responses.
- **Events:** No Kafka from this satellite — poll **`GET /api/v1/jobs`** / **`GET /api/v1/jobs/:id`** for metadata job UX — see [`EVENTS-BOUNDARY.md`](backend/endpoints/s3storage.server/EVENTS-BOUNDARY.md).

## Logging satellite (`EC2/log.server`) — logsapi

- **Language:** Go (Gin); **module:** `contact360.io/logsapi` (Git remote `contactlogs` — see [`MODULE-OPTIONAL.md`](backend/endpoints/log.server/MODULE-OPTIONAL.md)).
- **HTTP:** Root paths (`/logs`, `/health`); **`X-API-Key`** / **`api_key`** when **`LOGSAPI_API_KEY`** is set — see [`AUTH-ENV.md`](backend/endpoints/log.server/AUTH-ENV.md).
- **Workers:** [`cmd/worker`](../EC2/log.server/cmd/worker/main.go) — Asynq scheduled tasks; **`WORKER_CONCURRENCY`** (default **2**; use **10** for a 10-worker pool); **Redis** required for workers — **not** a Postgres queue.
- **Stores:** In-memory ring buffer for queries; **S3** CSV under `logs/flush/...`; CRM Postgres remains in the gateway.
- **Gateway:** **`LOGS_SERVER_API_URL`** / **`LOGS_SERVER_API_KEY`** ([`LogsServerClient`](../contact360.io/api/app/clients/logs_client.py)).
- **Observability:** `GET /health`; **`X-Request-ID`** on responses.
- **Events:** Inbound HTTP only — gateway **pushes** logs; no Kafka from this service — see [`EVENTS-BOUNDARY.md`](backend/endpoints/log.server/EVENTS-BOUNDARY.md).

## Sales Navigator / extension satellite (`EC2/extension.server`)

- **Language:** Go (Gin); **module:** `contact360.io/extension` — Git remote [`extension.server.git`](https://github.com/thekoushikdurgas/extension.server) (see [`MODULE-OPTIONAL.md`](backend/endpoints/extension.server/MODULE-OPTIONAL.md)).
- **HTTP:** `GET /health`; **`POST /v1/save-profiles`**, **`POST /v1/scrape`** — **`X-API-Key`** / **`api_key`** when **`EXTENSION_API_KEY`** is set — see [`AUTH-ENV.md`](backend/endpoints/extension.server/AUTH-ENV.md).
- **Workers:** In-process pool ([`internal/worker/pool.go`](../EC2/extension.server/internal/worker/pool.go)); **`EXTENSION_WORKERS`** (default **8**). **`cmd/worker`** is a stub — **no Redis queue** in this path.
- **Connectra:** **`POST /internal/extension/upsert-bulk`** on **sync.server** maps extension DTOs to `UpsertCompany` / `UpsertContact` (including **`linkedin_url`** identity when email is absent).
- **Gateway:** **`SALES_NAVIGATOR_SERVER_API_URL`** / **`SALES_NAVIGATOR_SERVER_API_KEY`** ([`SalesNavigatorServerClient`](../contact360.io/api/app/clients/sales_navigator_client.py)).
- **Events:** Inbound HTTP only — see [`EVENTS-BOUNDARY.md`](backend/endpoints/extension.server/EVENTS-BOUNDARY.md).

## AI satellite (`EC2/ai.server`)

- **Language:** Go (Gin); **module:** `contact360.io/ai` — Git remote [`ai.server.git`](https://github.com/thekoushikdurgas/ai.server) — see [`MODULE-OPTIONAL.md`](backend/endpoints/ai.server/MODULE-OPTIONAL.md).
- **HTTP:** `GET /health`, `GET /health/ready`; **`/api/v1/*`** for gateway parity (`AIServerClient`); **`X-API-Key`** when **`AI_API_KEY`** set — see [`AUTH-ENV.md`](backend/endpoints/ai.server/AUTH-ENV.md).
- **Default port:** **3000** (e.g. `http://16.176.172.50:3000`).
- **Workers:** [`cmd/worker`](../EC2/ai.server/cmd/worker/main.go) — Asynq; **`WORKER_CONCURRENCY`** (default **10**); **Redis** required for workers.
- **Integrations:** Hugging Face router; optional **Postgres** `ai_chats`; HTTP to **Connectra** (VQL), **email.server** / **phone.server** finder, **s3storage** presign — see [`AI-SERVER-BOUNDARY.md`](backend/endpoints/ai.server/AI-SERVER-BOUNDARY.md).
- **Gateway:** **`AI_SERVER_API_URL`** / **`AI_SERVER_API_KEY`** ([`AIServerClient`](../contact360.io/api/app/clients/ai_client.py)).
- **Events:** Inbound HTTP + Redis-backed Asynq only — see [`EVENTS-BOUNDARY.md`](backend/endpoints/ai.server/EVENTS-BOUNDARY.md).

## Campaign satellite (`EC2/campaign.server`)

- **Language:** Go (Gin); **module:** `contact360.io/campaign` — Git remote [`campanign.server.git`](https://github.com/thekoushikdurgas/campanign.server.git) — see [`MODULE-OPTIONAL.md`](backend/endpoints/campaign.server/MODULE-OPTIONAL.md).
- **HTTP:** `GET /health`, `GET /health/ready`; **`/campaigns`**, **`/sequences`**, **`/campaign-templates`**, **`/cql/*`** with **`X-API-Key`** (`CAMPAIGN_API_KEY` or legacy `ADMIN_API_KEY`) — see [`AUTH-ENV.md`](backend/endpoints/campaign.server/AUTH-ENV.md).
- **Default port:** **9800** (e.g. `http://6.76.72.50:9800` — use a valid TCP port ≤ 65535).
- **Workers:** [`cmd/worker`](../EC2/campaign.server/cmd/worker/main.go) — Asynq; **`WORKER_CONCURRENCY`** (default **10**); task types `campaign:send`, `campaign:email`, `campaign:phone`, `campaign:linkedin`, `campaign:sequence_step`.
- **Integrations:** SMTP send; optional HTTP to **Connectra** (contact fetch for sequence trigger), **email.server** / **phone.server** clients in [`internal/satellite`](../EC2/campaign.server/internal/satellite); **S3** for template HTML/JSON — see [`CAMPAIGN-SERVER-BOUNDARY.md`](backend/endpoints/campaign.server/CAMPAIGN-SERVER-BOUNDARY.md).
- **Gateway:** **`CAMPAIGN_API_URL`** / **`CAMPAIGN_API_KEY`** ([`CampaignServiceClient`](../contact360.io/api/app/clients/campaign_service_client.py)).
- **Events:** Inbound HTTP + Redis-backed Asynq only — see [`EVENTS-BOUNDARY.md`](backend/endpoints/campaign.server/EVENTS-BOUNDARY.md).

## API Gateway (`contact360.io/api`)

- **Language / stack:** Python 3.11, **FastAPI**, **Strawberry GraphQL** (`POST /graphql`), **SQLAlchemy async** + **Alembic** for the gateway Postgres schema.
- **Auth:** JWT access tokens in GraphQL context; satellites use **`X-API-Key`** from env (`CONNECTRA_*`, `EMAIL_*`, `PHONE_*`, `AI_*`, `S3STORAGE_*`, `LOGS_*`, `CAMPAIGN_*`, `SALES_NAVIGATOR_*`, …).
- **Middleware (outermost first on request):** CORS → TrustedHost → ProxyHeaders → GraphQL rate limit → mutation abuse guard → idempotency → body size → trace/request IDs → timing → RED metrics → GZip (see `app/main.py` comment block).
- **Multi-channel:** GraphQL **`phone`** module proxies **phone.server** (parallel to **`email`**). **`campaignSatellite`** + **`campaigns`** mutations proxy **campaign.server** (incl. CQL parse/validate + template preview).
- **Health:** **`health.satelliteHealth`** runs best-effort **`GET /health`** (or s3storage/logs-specific probes) across configured satellites.
- **Git:** [`appointment360.git`](https://github.com/thekoushikdurgas/appointment360.git) — deploy `api.contact360.io` / `98.84.125.120`.
- **Docs:** `docs/backend/endpoints/contact360.io/*`, Postman `contact360.io-api.postman_collection.json`, DB `docs/backend/database/contact360.io-schema.md`.

## Row Level Security (RLS) pattern

- Session sets `SET LOCAL app.current_org_id = '<uuid>'` after JWT validation in CRM path.
- Policies: `org_id = current_setting('app.current_org_id')::uuid` on all tenant tables.
- **Superadmin** uses separate role without bypass in app queries; break-glass uses audited maintenance role.

---

*Last updated: 2026-04-15 (API Gateway decision added)*
