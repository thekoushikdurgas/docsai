# job.server — MongoDB reference

**Server:** [`EC2/job.server`](../../../EC2/job.server) (Go, `github.com/thekoushikdurgas/job.server`).

## Collections (actual names)

Constants in [`EC2/job.server/internal/clients/mongo.go`](../../../EC2/job.server/internal/clients/mongo.go): **`apify_runs`**, **`linkedin_jobs`**. Indexes are created in `EnsureIndexes` (idempotent on startup). BSON field names follow the `bson:"..."` tags in [`EC2/job.server/internal/models/`](../../../EC2/job.server/internal/models/).

- **`apify_runs`** — one document per Apify actor run (`run_id` unique, `status`, `actor_id`, `dataset_id`, `item_count`, `started_at`, …). Model: `ApifyRun`.
- **`linkedin_jobs`** — normalized job rows from the Apify dataset (`linkedin_job_id` unique). Includes `company_name`, `company_linkedin_url`, optional **`company_uuid`** (Connectra), optional **`poster_contact_uuid`**, `apify_run_id`, `raw_payload`, and listing fields (title, location, poster links, etc.). Model: `LinkedInJob`.

## Redis

- **Asynq** queues (e.g. default + Apify-tagged work).
- **Locks** for scheduled scrape triggers to avoid double-fire.

## Parity

REST responses used by the gateway’s [`JobServerClient`](../../../contact360.io/api/app/clients/job_server_client.py) use `success`, `data`, and `total` where applicable. **Connectra read-through** routes (`GET /jobs/:id/company`, `GET /jobs/:id/contacts`, `GET /companies/:uuid/contacts`, `GET /companies/:uuid/record`) are implemented in job.server and consumed by the gateway `hireSignal` queries — see [`ROUTE-CLIENT-MATRIX`](../endpoints/job.server/ROUTE-CLIENT-MATRIX.md).

**Last reviewed:** 2026-04-25.
