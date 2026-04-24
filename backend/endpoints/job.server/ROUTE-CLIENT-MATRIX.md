# job.server — gateway client vs HTTP routes

Source of truth for parity checks:

- **Gateway:** [`contact360.io/api/app/clients/job_server_client.py`](../../../../contact360.io/api/app/clients/job_server_client.py)
- **Server:** [`EC2/job.server/internal/api/router.go`](../../../../EC2/job.server/internal/api/router.go)

**GraphQL (dashboard):** namespace **`hireSignal`** on `POST /graphql` — see [`../contact360.io/ROUTE-CLIENT-MATRIX.md`](../contact360.io/ROUTE-CLIENT-MATRIX.md) (`JOB_SERVER_` env prefix).

Auth for **`/api/v1/*`**: header **`X-API-Key`** must equal satellite **`API_KEY`** (gateway: **`JOB_SERVER_API_KEY`**) when **`API_KEY`** is set on the server. In **`APP_ENV=development`** with **`API_KEY` empty**, the middleware can skip the key (local dev only).

| `JobServerClient` method | HTTP | Notes |
| ------------------------ | ---- | ----- |
| `health_check` | `GET /health` | No key path when `API_KEY` empty (dev) |
| `list_jobs` | `GET /api/v1/jobs` | Query: `limit`, `offset`, `title`, `company`, `location`, `employment_type` |
| `get_job` | `GET /api/v1/jobs/{linkedinJobId}` | `id` path is LinkedIn job id |
| `jobs_stats` | `GET /api/v1/jobs/stats` | `total_jobs`, `jobs_with_company` |
| `list_runs` | `GET /api/v1/runs` | Query: `limit` (default 50) |
| `get_run` | `GET /api/v1/runs/{runId}` | |
| `trigger_scrape` | `POST /api/v1/runs` | JSON `StartScrapePayload` (e.g. `trigger`); enqueues Asynq task `start_scrape` — **202** with `task_id` |
| `list_companies` | `GET /api/v1/companies` | Query: `limit` (default 100) |
| `company_jobs` | `GET /api/v1/companies/{companyUuid}/jobs` | Query: `limit` (default 50) |

**Implementation:** MongoDB for `linkedin_job` and `apify_run` documents; Asynq + Redis for scrape tasks; Apify for actor runs; optional Connectra batch upserts for companies/contacts.

Last reviewed: 2026-04-25.
