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
| `pauseJob` | `input` | `PauseJobInput!` | `JSON!` |
| `resumeJob` | `input` | `ResumeJobInput!` | `JSON!` |
| `terminateJob` | `input` | `TerminateJobInput!` | `JSON!` |
| `pauseConnectraJob` | `jobUuid` | `String!` | `JSON!` |
| `resumeConnectraJob` | `jobUuid` | `String!` | `JSON!` |
| `terminateConnectraJob` | `jobUuid` | `String!` | `JSON!` |
| `retryJob` | `input` | `RetryJobInput!` | `JSON!` |

**Removed:** `createEmailPatternImport`, `createAppointmentImport` (legacy tkdjob-era).

Use **camelCase** in GraphQL variables. See Input Types below.

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

```graphql
type JobQuery {
  job(jobId: ID!): SchedulerJob!
  jobs(limit: Int = 25, offset: Int = 0, status: String = null, jobType: String = null, jobFamily: String = null): JobConnection!
}

type JobMutation {
  createEmailFinderExport(input: CreateEmailFinderExportInput!): SchedulerJob!
  createEmailVerifyExport(input: CreateEmailVerifyExportInput!): SchedulerJob!
  createContact360Export(input: CreateContact360ExportInput!): SchedulerJob!
  createContact360Import(input: CreateContact360ImportInput!): SchedulerJob!
  pauseJob(input: PauseJobInput!): JSON!
  resumeJob(input: ResumeJobInput!): JSON!
  terminateJob(input: TerminateJobInput!): JSON!
  pauseConnectraJob(jobUuid: String!): JSON!
  resumeConnectraJob(jobUuid: String!): JSON!
  terminateConnectraJob(jobUuid: String!): JSON!
  retryJob(input: RetryJobInput!): JSON!
}
```

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>`.

### `jobs.jobs` (query)

```json
{
  "query": "query ($limit: Int, $offset: Int, $jobFamily: String) { jobs { jobs(limit: $limit, offset: $offset, jobFamily: $jobFamily) { jobs { id jobType status sourceService } pageInfo { total limit offset } } } }",
  "variables": { "limit": 25, "offset": 0, "jobFamily": null }
}
```

### `jobs.createEmailFinderExport` (mutation)

```json
{
  "query": "mutation ($input: CreateEmailFinderExportInput!) { jobs { createEmailFinderExport(input: $input) { id jobId status jobFamily } } }",
  "variables": {
    "input": {
      "inputCsvKey": "upload/20260210_contacts.csv",
      "outputPrefix": "exports/",
      "csvColumns": null,
      "s3Bucket": null
    }
  }
}
```

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
| `retryJob` | email vs sync | **email.server:** rejected (use resume if paused). **sync.server:** only sets local `scheduler_jobs.status` to `open`; no Connectra HTTP retry call. |

## Input types (summary)

- **CreateEmailFinderExportInput** / **CreateEmailVerifyExportInput**: fields match email.server `S3CSVFinderRequest` / `S3CSVVerifyRequest` (`s3Bucket`, `inputCsvKey`, `outputPrefix`, optional `csvColumns`; verify also optional `provider`, default `mailtester`).
- **CreateContact360ImportInput** includes `importTarget` (GraphQL name) for import scope when applicable.
- **PauseJobInput** / **ResumeJobInput** / **TerminateJobInput**: `{ jobId: ID! }`.
- **RetryJobInput**: job id and optional retry metadata (see schema).

## Environment

- **Email jobs:** `LAMBDA_EMAIL_API_URL`, `LAMBDA_EMAIL_API_KEY`, `LAMBDA_EMAIL_API_TIMEOUT`
- **Sync / Connectra jobs:** `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY`, `CONNECTRA_TIMEOUT`

There is **no** `TKDJOB_*` configuration.

## Connectra native jobs API (`EC2/sync.server`)

The sync server has its own **`jobs`** table and HTTP API under **`/common/jobs`** (distinct from GraphQL `scheduler_jobs`, though gateway mutations may create rows in both places depending on flow).

| HTTP | Path | Purpose |
| --- | --- | --- |
| `POST` | `/common/jobs` | List jobs: body `{ "job_type", "status": [], "limit" }` |
| `POST` | `/common/jobs/create` | Create job: `job_type` **`insert_csv_file`** \| **`export_csv_file`**, `job_data` JSON, `retry_count` |
| `GET` | `/common/jobs/:job_uuid` | Fetch one job row |
| `POST` | `/common/jobs/:job_uuid/pause` \| `/resume` \| `/terminate` | Status transitions |

Worker-backed types and **`job_data`** shapes (S3 keys, export `vql`, `service` = `contact` \| `company`) are documented in **[connectra.api.md](../micro.services.apis/connectra.api.md)**. Postman: **[EC2_sync.server.postman_collection.json](../postman/EC2_sync.server.postman_collection.json)**.

GraphQL mutations **`pauseConnectraJob`**, **`resumeConnectraJob`**, **`terminateConnectraJob`** map to these pause/resume/terminate routes (see gateway resolvers).

## Email satellite native jobs (`EC2/email.server`)

For **`source_service=email_server`**, the gateway delegates pause/resume/terminate and status to the Go service’s **`emailapi_jobs`** + Redis/Asynq pipeline.

| HTTP (email.server) | Purpose |
| --- | --- |
| `GET /jobs` | List recent jobs (max 50) |
| `GET /jobs/:id/status` | Progress, `output_csv_key`, provider |
| `POST /jobs/:id/pause` | Pause |
| `POST /jobs/:id/resume` | Resume (must be paused) |
| `POST /jobs/:id/terminate` | Terminate + optional S3 merge |
| `POST /email/finder/s3` | Finder S3 CSV stream job (`202`) |
| `POST /email/verify/s3` | Verifier S3 CSV stream job (`202`) |

Full parameters and JSON bodies: **[emailapis.api.md](../micro.services.apis/emailapis.api.md)** · Postman: **[EC2_email.server.postman_collection.json](../postman/EC2_email.server.postman_collection.json)**.

## Related docs

- Database: `docs/backend/database/scheduler_jobs.sql`, `enums.sql` (`scheduler_job_status`)
- Satellite routes: `docs/backend/endpoints/EC2_GO_SATELLITE_ROUTES.md`
- Email HTTP API: [emailapis.api.md](../micro.services.apis/emailapis.api.md)
