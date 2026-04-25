# job.server — gateway client vs HTTP routes

Source of truth for parity checks:

- **Gateway:** [`contact360.io/api/app/clients/job_server_client.py`](../../../../contact360.io/api/app/clients/job_server_client.py)
- **Server:** [`EC2/job.server/internal/api/router.go`](../../../../EC2/job.server/internal/api/router.go) registers: [`jobs_handlers.go`](../../../../EC2/job.server/internal/api/jobs_handlers.go), [`job_connectra_handlers.go`](../../../../EC2/job.server/internal/api/job_connectra_handlers.go), [`company_connectra_handlers.go`](../../../../EC2/job.server/internal/api/company_connectra_handlers.go), [`runs_handlers.go`](../../../../EC2/job.server/internal/api/runs_handlers.go), [`companies_handlers.go`](../../../../EC2/job.server/internal/api/companies_handlers.go). Shared VQL helpers: [`vql_contacts.go`](../../../../EC2/job.server/internal/api/vql_contacts.go). **Connectra client:** [`internal/clients/connectra_client.go`](../../../../EC2/job.server/internal/clients/connectra_client.go) → **sync.server** (`CONNECTRA_BASE_URL`).

**GraphQL (dashboard):** namespace **`hireSignal`** on `POST /graphql` — see [`../contact360.io/ROUTE-CLIENT-MATRIX.md`](../contact360.io/ROUTE-CLIENT-MATRIX.md) (`JOB_SERVER_` env prefix).

Auth for **`/api/v1/*`**: header **`X-API-Key`** must match **`API_KEY`** when the server is configured with a **non-empty** `API_KEY` (gateway: **`JOB_SERVER_API_KEY`**). If **`API_KEY` is empty**, the middleware **does not** require a key in any `APP_ENV` (local use only; **set a non-empty `API_KEY` in production**).  
**`GET /health`** is on the **root** router and is **not** protected by the API key middleware (used for liveness; returns Mongo + Redis status).

| `JobServerClient` method | HTTP | Notes |
| ------------------------ | ---- | ----- |
| `health_check` | `GET /health` | Unauthenticated. Returns **`mongo`**, **`redis`**, and **`status`**: `ok` or `degraded` (503) if either backend fails. |
| `list_jobs` | `GET /api/v1/jobs` | Query: `limit`, `offset`, `title`, `company`, `location`, `employment_type`, `seniority`, `function` (case-insensitive regex on `seniority_level`, `function_category_v2`) |
| `get_job` | `GET /api/v1/jobs/{linkedinJobId}` | `id` path is LinkedIn job id |
| `jobs_stats` | `GET /api/v1/jobs/stats` | `total_jobs`, `jobs_with_company` |
| `list_runs` | `GET /api/v1/runs` | Query: `limit` (default 50) |
| `get_run` | `GET /api/v1/runs/{runId}` | |
| `trigger_scrape` | `POST /api/v1/runs` | JSON `StartScrapePayload` (`trigger`, `urls`/`count` or `SCRAPE_URLS`/`SCRAPE_COUNT`, …). **Asynchronous:** returns **202** and enqueues Asynq task `start_scrape` on Redis; **Apify** runs in a **worker** (`cmd/worker`, Docker `job-worker`, or API with `EMBEDDED_ASYNQ_WORKER=true`). `SCRAPE_URLS` may be a JSON array or one comma-separated string. Resolved `count` capped (see `maxScrapeRequestCount` in `runs_handlers.go`). |
| `list_companies` | `GET /api/v1/companies` | Query: `limit` (default 100) |
| `company_jobs` | `GET /api/v1/companies/{companyUuid}/jobs` | Query: `limit` (default 50) |
| `job_connectra_contacts` | `GET /api/v1/jobs/{linkedinJobId}/contacts` | GraphQL: `hireSignal { jobConnectraContacts( … ) }`. VQL via **sync.server** `POST /contacts`. Query: `page` (max 10), `limit` (max 100), `populateCompany`, `includePoster`. **409** if no `company_uuid` on the job. **503** if `CONNECTRA_*` unset. |
| `company_connectra_contacts` | `GET /api/v1/companies/{companyUuid}/contacts` | GraphQL: `hireSignal { connectraContactsForCompany( … ) }`. Same VQL, keyed by `companyUuid`. |
| `job_connectra_company` | `GET /api/v1/jobs/{linkedinJobId}/company` | GraphQL: `hireSignal { jobConnectraCompany(linkedinJobId) }`. **Job → Connectra** `GET /companies/{uuid}`. **409** / **404** / **503** as in job.server. |
| `company_connectra_record` | `GET /api/v1/companies/{companyUuid}/record` | GraphQL: `hireSignal { connectraCompany(companyUuid) }`. One Connectra company, no job row. |
| **App** | | Dashboard **`/hiring-signals`**: per-row **Connect** action (`JobConnectraModal`); company modal **Connectra** tab (profile + VQL people). |

**Implementation notes**

- **MongoDB** collections: **`linkedin_jobs`**, **`apify_runs`** (see [`job.server-schema.md`](../../database/job.server-schema.md)).
- **Ingestion:** Asynq + **Redis** for scrape/ingest tasks; **Apify** for actor runs; **Connectra bridge** (batch company/contact upsert) in [`EC2/job.server/internal/services/connectra_bridge.go`](../../../../EC2/job.server/internal/services/connectra_bridge.go) when `CONNECTRA_*` is set.
- **Read-through to sync:** Mapping routes call **sync.server** only when `CONNECTRA_BASE_URL` and `CONNECTRA_API_KEY` are set; otherwise they respond **503**. Contacts use **VQL** over **`POST /contacts`**, companies use **`GET /companies/{uuid}`** (see [sync.server `modules/`](../../../../EC2/sync.server/modules)).
- **Gin:** In [`main.go`](../../../../EC2/job.server/main.go), `GIN_MODE=release` or `APP_ENV=production` sets release mode; Docker compose may set `GIN_MODE=release` for the API (see `EC2/job.server/docker-compose.yml`).

**Last reviewed:** 2026-04-25.
