# job.server — events and integrations boundary

- **No Kafka / product webhooks** from this service. Progress for Apify work is stored in **Mongo** (`apify_run`) and polled; **Asynq** runs background scrape + ingest tasks.
- **HTTP trigger:** `POST /api/v1/runs` enqueues a **start_scrape** task. Idempotency for **cron** vs manual triggers is coordinated via **Redis** `SETNX`-style keys in the worker (see `EC2/job.server/internal/worker`).
- **Apify:** Outbound calls to the Apify API; dataset pages are read into **`linkedin_job`** and optionally synced to **Connectra** when configured.
- **Connectra:** Outbound `POST` batch upserts; not inbound events from Connectra to job.server.
- **Dashboard:** Uses gateway GraphQL **`hireSignal { … }`**, not this HTTP port directly from the browser.

For gateway aggregation, **`health.satelliteHealth`** includes a **`job_server`** row when `JOB_SERVER_API_URL` and `JOB_SERVER_API_KEY` are set.

Last reviewed: 2026-04-25.
