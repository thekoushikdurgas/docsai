# Jobs codebase analysis (`contact360.io/jobs`)

**Surface:** Next.js (or aligned) UI for job lists, execution detail, and bulk operation progress where product routes jobs through the **Appointment360 GraphQL** gateway rather than a standalone REST “jobs service.”

## Runtime alignment

| Concern | Source of truth |
| --- | --- |
| GraphQL contract | [`docs/backend/graphql.modules/16_JOBS_MODULE.md`](../backend/graphql.modules/16_JOBS_MODULE.md) |
| Service hub | [`docs/backend/micro.services.apis/jobs.api.md`](../backend/micro.services.apis/jobs.api.md) |
| Endpoint matrix | [`docs/backend/endpoints/jobs_endpoint_era_matrix.md`](../backend/endpoints/jobs_endpoint_era_matrix.md) |
| Data lineage | [`docs/backend/database/jobs_data_lineage.md`](../backend/database/jobs_data_lineage.md) |
| Gateway | [`docs/backend/micro.services.apis/appointment360.api.md`](../backend/micro.services.apis/appointment360.api.md) |

## Verified behaviors (stub)

- Job rows are stored in **`scheduler_jobs`** (gateway-owned); workers on **email.server** and **sync.server** update payloads.
- **Era 2.4** focuses on bulk hardening: idempotency, retries, progress UX — see roadmap minors under `docs/2.x/`.

## Gaps / risks (stub)

- Confirm UI error surfaces match GraphQL `statusPayload` semantics per `jobFamily`.
- Align bulk re-run and stuck-job operator flows with admin + logs.

## Related analyses

- [`appointment360-codebase-analysis.md`](appointment360-codebase-analysis.md) — resolver and auth paths.
- [`emailapis-codebase-analysis.md`](emailapis-codebase-analysis.md) — email.server job execution.

*This file is a **navigation stub**; extend with repo-specific paths and verified behaviors when touching `contact360.io/jobs` code.*
