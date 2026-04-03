# Jobs data lineage (`scheduler_jobs`)

Gateway-owned rows in **`scheduler_jobs`** represent long-running work delegated to **email.server**, **sync.server**, and related workers.

## References

- DDL: [`scheduler_jobs.sql`](scheduler_jobs.sql), [`crud/scheduler_jobs.sql`](crud/scheduler_jobs.sql)
- GraphQL: [`16_JOBS_MODULE.md`](../graphql.modules/16_JOBS_MODULE.md)
- Hub: [`micro.services.apis/jobs.api.md`](../micro.services.apis/jobs.api.md)

*Expand with column-level ownership and worker payload conventions as needed.*
