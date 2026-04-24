# `job.server` (Hiring Signal)

**Path:** `EC2/job.server`  
**Module:** `github.com/thekoushikdurgas/job.server` (Git remote: `https://github.com/thekoushikdurgas/job.server.git`)

**Role:** Ingest public LinkedIn job listings via **Apify**, store them in **MongoDB**, and optionally **upsert** linked companies and contacts in **Connectra (sync.server)**. Exposes a **Gin** REST API under `/api/v1` and a separate **`cmd/worker`** for **Asynq** + cron-scheduled scrapes.

**Product surface:** The Contact360 **gateway** (`contact360.io/api`) proxies to this service with **`JobServerClient`**, GraphQL field **`hireSignal`**, and **`satelliteHealth` → `job_server`**. The **dashboard** lists roles at `/hiring-signals`.

**See also:** [`docs/backend/endpoints/job.server/ROUTE-CLIENT-MATRIX.md`](../backend/endpoints/job.server/ROUTE-CLIENT-MATRIX.md), [`docs/DECISIONS.md`](../DECISIONS.md) (job.server section), [`docs/DEPLOYMENT-MATRIX.md`](../DEPLOYMENT-MATRIX.md).

Last reviewed: 2026-04-25.
