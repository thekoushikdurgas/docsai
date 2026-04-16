# Gateway usage — `EmailServerClient` and GraphQL

## Python client

[`contact360.io/api/app/clients/email_server_client.py`](../../../../contact360.io/api/app/clients/email_server_client.py) — all REST paths listed in [ROUTE-CLIENT-MATRIX.md](ROUTE-CLIENT-MATRIX.md).

## GraphQL — Email module

[`app/graphql/modules/email/queries.py`](../../../../contact360.io/api/app/graphql/modules/email/queries.py) and [`mutations.py`](../../../../contact360.io/api/app/graphql/modules/email/mutations.py) call `EmailServerClient` for finder, verifier, patterns, web search, and job status helpers.

## GraphQL — Jobs module

[`app/graphql/modules/jobs/mutations.py`](../../../../contact360.io/api/app/graphql/modules/jobs/mutations.py):

- **Create email S3 jobs** — `createEmailFinderExport`, `createEmailVerifyExport`, and related flows call satellite methods such as `create_finder_s3_job` / `create_verifier_s3_job`, then persist **`scheduler_jobs`** with `source_service="email_server"`.
- **Pause / resume / terminate** — `pauseJob`, `resumeJob`, `terminateJob` call `EmailServerClient.pause_job` / `resume_job` / `terminate_job` when the row targets `email_server`.

[`app/graphql/modules/jobs/types.py`](../../../../contact360.io/api/app/graphql/modules/jobs/types.py) — **`statusPayload`** for `email_server` jobs is fetched from the satellite status API.

## Billing

[`scheduler_job_billing.py`](../../../../contact360.io/api/app/services/scheduler_job_billing.py) — `source_service == "email_server"` selects billable units from status payloads.

## Status JSON shape

`GET /jobs/:id/status` returns `{ "success": true, "data": { ... } }` with fields such as `progress_percent`, `processed_rows`, `output_csv_key`, `provider` (see [router handler](../../../../EC2/email.server/internal/api/router.go)).
