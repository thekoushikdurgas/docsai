# `job.server` (Hiring Signal)

**Path:** `EC2/job.server`  
**Module:** `github.com/thekoushikdurgas/job.server` (Git remote: `https://github.com/thekoushikdurgas/job.server.git`)

**Entrypoints:** [`main.go`](../../EC2/job.server/main.go) — HTTP API; [`cmd/worker/main.go`](../../EC2/job.server/cmd/worker/main.go) — Asynq + cron (optional **embedded** worker in API via `EMBEDDED_ASYNQ_WORKER=true`).

**Role:** Ingest public LinkedIn job listings via **Apify**, store them in **MongoDB** (`linkedin_jobs`, `apify_runs`), and optionally **upsert** linked companies and job posters as contacts in **Connectra (sync.server)** via the Connectra bridge. The API also **proxies read requests** to sync (company record, VQL contact lists for a `company_id`) so clients can **map jobs → company + contacts** without calling sync directly when `CONNECTRA_*` is set.

**HTTP:** **Gin**; routes under `/api/v1` with **`X-API-Key`** when `API_KEY` is non-empty; `GET /health` without key. See [`ROUTE-CLIENT-MATRIX.md`](../backend/endpoints/job.server/ROUTE-CLIENT-MATRIX.md) for the full table (jobs, runs, companies aggregation, **Connectra** mapping routes).

**Ops / local stack:** [`docker-compose.yml`](../../EC2/job.server/docker-compose.yml) — `job-api`, `job-worker`, Mongo, Redis; env via [`.env.example`](../../EC2/job.server/.env.example).

**Product surface:** The Contact360 **gateway** (`contact360.io/api`) proxies to this service with **`JobServerClient`**, GraphQL field **`hireSignal`**, and **`satelliteHealth` → `job_server`**. The **dashboard** lists roles at `/hiring-signals`.

**See also:** [`ROUTE-CLIENT-MATRIX.md`](../backend/endpoints/job.server/ROUTE-CLIENT-MATRIX.md) (routes + `JobServerClient` parity), [`AUTH-ENV.md`](../backend/endpoints/job.server/AUTH-ENV.md), [`EVENTS-BOUNDARY.md`](../backend/endpoints/job.server/EVENTS-BOUNDARY.md), [`job.server-schema.md`](../backend/database/job.server-schema.md) (Mongo), [`DECISIONS.md`](../DECISIONS.md) (Hiring signal), [`DEPLOYMENT-MATRIX.md`](../DEPLOYMENT-MATRIX.md), Postman [`EC2_job.server.postman_collection.json`](../backend/postman/EC2_job.server.postman_collection.json).

**Last reviewed:** 2026-04-25.
