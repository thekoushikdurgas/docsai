# Jobs (Scheduler) Module

## Overview

The Jobs module provides GraphQL queries and mutations for creating and tracking long-running work. The Contact360 gateway validates the user, calls downstream satellites, and stores a row in `scheduler_jobs` for ownership and listing.

| Satellite | Env | Used for |
|-----------|-----|----------|
| **email.server** | `LAMBDA_EMAIL_API_URL`, `LAMBDA_EMAIL_API_KEY` | Email finder/verifier S3 bulk jobs; pause/resume/terminate; live `statusPayload` |
| **sync.server** (Connectra) | `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY` | Contact/company CSV import & VQL export; job rows updated as the worker progresses |

**Location:** `app/graphql/modules/jobs/`

GraphQL paths: `query { jobs { job(jobId: ...) jobs(limit: ..., jobFamily: ...) { ... } } }`, `mutation { jobs { createEmailFinderExport(...) { ... } } }`.

## Taxonomy (`scheduler_jobs`)

- **`source_service`**: `email_server` | `sync_server`
- **`job_family`**: `email_job` | `contact_job` | `company_job`
- **`job_subtype`**: `finder` | `verifier` | `import` | `export` (where applicable)
- **`job_type`**: string identifier (e.g. `email_finder_export_stream`, `contact360_export_stream`); stored as **TEXT** (see migration `20260410_0005`).

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** (under `jobs { ... }`) | | | |
| `job` | `jobId` | `ID!` | `SchedulerJob` |
| `jobs` | `limit`, `offset`, `status`, `jobType`, `jobFamily` | `Int`, `Int`, `String`, `String`, `String` | `JobConnection` |
| **Mutations** (under `jobs { ... }`) | | | |
| `createEmailFinderExport` | `input` | `CreateEmailFinderExportInput!` | `SchedulerJob` |
| `createEmailVerifyExport` | `input` | `CreateEmailVerifyExportInput!` | `SchedulerJob` |
| `createContact360Export` | `input` | `CreateContact360ExportInput!` | `SchedulerJob` |
| `createContact360Import` | `input` | `CreateContact360ImportInput!` | `SchedulerJob` (role-gated) |
| `pauseJob` | `input` | `PauseJobInput!` | `SchedulerJob` |
| `resumeJob` | `input` | `ResumeJobInput!` | `SchedulerJob` |
| `terminateJob` | `input` | `TerminateJobInput!` | `SchedulerJob` |
| `retryJob` | `input` | `RetryJobInput!` | `JSON` |

**Removed:** `createEmailPatternImport`, `createAppointmentImport` (legacy tkdjob-era).

Use **camelCase** in GraphQL variables. See Input Types below.

## Flow

1. Client uploads inputs via the **Upload** / S3 flow where required and obtains keys / VQL / options.
2. Client calls the appropriate GraphQL mutation under `jobs`.
3. The gateway calls **email.server** or **sync.server** and inserts/updates `scheduler_jobs` with `source_service`, `job_family`, and `job_subtype`.
4. The client lists jobs or opens **Jobs** in the app; `statusPayload` resolves from the email satellite when `source_service=email_server`, otherwise from stored DB payload for sync jobs.

## Types

### SchedulerJob

```graphql
type SchedulerJob {
  id: ID!
  jobId: ID!
  userId: ID!
  jobType: String!
  status: String!
  sourceService: String!
  jobFamily: String!
  jobSubtype: String
  requestPayload: JSON
  responsePayload: JSON
  statusPayload: JSON
  timelinePayload: JSON   # null (not available for current satellites)
  dagPayload: JSON        # null (not available for current satellites)
  createdAt: DateTime!
  updatedAt: DateTime
}
```

- **statusPayload**: For `email_server`, fetched from email satellite status API when requested. For `sync_server`, read from DB (optionally refreshed via Connectra `GET /common/jobs/:uuid` when implemented client-side).
- **timelinePayload** / **dagPayload**: Reserved; return `null` (no equivalent on current satellites).

### JobConnection

```graphql
type JobConnection {
  jobs: [SchedulerJob!]!
  pageInfo: PageInfo!
}
```

## Queries

### `job(jobId: ID!)`

Single scheduler job. User can only access their own jobs unless Admin/SuperAdmin.

### `jobs(limit, offset, status, jobType, jobFamily)`

List jobs for the current user. Optional **`jobFamily`** filter: `email_job` | `contact_job` | `company_job`.

## Mutations

| Mutation | Backend | Notes |
|----------|---------|--------|
| `createEmailFinderExport` | email.server S3 finder job | Feature usage / activities as implemented |
| `createEmailVerifyExport` | email.server S3 verifier job | |
| `createContact360Export` | sync.server `POST /common/jobs/create` | `service` field selects contact vs company family |
| `createContact360Import` | sync.server | `importTarget` in GraphQL maps to import scope |
| `pauseJob` / `resumeJob` / `terminateJob` | email.server only | Error if `source_service` is not `email_server` |
| `retryJob` | email vs sync | Email: satellite retry when available; sync: DB status update for worker |

## Input types (summary)

- **CreateContact360ImportInput** includes `importTarget` (GraphQL name) for import scope when applicable.
- **PauseJobInput** / **ResumeJobInput** / **TerminateJobInput**: `{ jobId: ID! }`.
- **RetryJobInput**: job id and optional retry metadata (see schema).

## Environment

- **Email jobs:** `LAMBDA_EMAIL_API_URL`, `LAMBDA_EMAIL_API_KEY`, `LAMBDA_EMAIL_API_TIMEOUT`
- **Sync / Connectra jobs:** `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY`, `CONNECTRA_TIMEOUT`

There is **no** `TKDJOB_*` configuration.

## Related docs

- Database: `docs/backend/database/scheduler_jobs.sql`, `enums.sql` (`scheduler_job_status`)
- Satellite routes: `docs/backend/endpoints/EC2_GO_SATELLITE_ROUTES.md`
