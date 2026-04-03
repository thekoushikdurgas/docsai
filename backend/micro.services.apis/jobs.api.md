# Jobs surface (gateway + workers)

Scheduler jobs are **created and queried via Appointment360 GraphQL** (`scheduler_jobs` / job families). Heavy work runs on **`EC2/email.server`**, **`EC2/sync.server`**, and related workers — not a separate public REST “jobs service” URL for most product flows.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Jobs-related services in topology |
| [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md) | Job operations → tables / workers |
| [jobs_endpoint_era_matrix.md](../endpoints/jobs_endpoint_era_matrix.md) | Supplemental job-related HTTP routes where applicable |
| [jobs_data_lineage.md](../database/jobs_data_lineage.md) | `scheduler_jobs` and related ownership |

### GraphQL module

- [`graphql.modules/16_JOBS_MODULE.md`](../graphql.modules/16_JOBS_MODULE.md) — queries, mutations, payloads, idempotency notes.

### Gateway hub

- [appointment360.api.md](appointment360.api.md) — GraphQL entry point for all job CRUD and status.

## Role

- Email finder/verify/export/import pipelines, bulk processing, and admin visibility — coordinated through the gateway with worker execution on EC2.

## Related

- Email APIs / bulk: [`graphql.modules/15_EMAIL_MODULE.md`](../graphql.modules/15_EMAIL_MODULE.md)
- Runtime analysis: [jobs-codebase-analysis.md](../../codebases/jobs-codebase-analysis.md)
