# job.server — MongoDB reference

**Server:** [`EC2/job.server`](../../../EC2/job.server) (Go, `github.com/thekoushikdurgas/job.server`).

## Collections (logical)

Indexes are ensured at startup in [`EC2/job.server/internal/clients/mongo.go`](../../../EC2/job.server/internal/clients/mongo.go) (`EnsureIndexes`). Exact field names follow BSON tags in [`EC2/job.server/internal/models/`](../../../EC2/job.server/internal/models/).

- **`apify_run`** — one document per Apify run / task correlation (`run_id`, status, actor id, timestamps).
- **`linkedin_job`** — normalized job rows from the Apify dataset (`linkedinJobId` unique, company linkage, `description`, location, employment fields, `companyUuid` when Connectra match exists).

## Redis

- **Asynq** queues (e.g. default + Apify-tagged work).
- **Locks** for scheduled scrape triggers to avoid double-fire.

## Parity

REST responses match [`JobServerClient`](../../../contact360.io/api/app/clients/job_server_client.py) expectations (`success`, `data`, `total` where applicable).

Last reviewed: 2026-04-25.
