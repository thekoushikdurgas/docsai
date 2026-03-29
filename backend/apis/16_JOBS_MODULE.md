# Jobs (Scheduler) Module

## Overview

The Jobs module provides GraphQL queries and mutations for creating and tracking long-running jobs via the Tkdjob (Job Scheduler) API. Appointment360 validates the user, calls the tkdjob REST API to create a job, and stores a local record in `scheduler_jobs` for ownership and listing.
**Location:** `app/graphql/modules/jobs/`

**Tkdjob API:** Configured via `TKDJOB_API_URL` and `TKDJOB_API_KEY`.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `job` | `jobId` | ID! | `SchedulerJob` |
| `jobs` | `limit`, `offset`, `status`, `jobType` | Int, Int, String, String | `JobConnection` |
| **Mutations** | | | |
| `createEmailFinderExport` | `input` | CreateEmailFinderExportInput! | `SchedulerJob` |
| `createEmailVerifyExport` | `input` | CreateEmailVerifyExportInput! | `SchedulerJob` |
| `createEmailPatternImport` | `input` | CreateEmailPatternImportInput! | `SchedulerJob` (SuperAdmin) |
| `createContact360Export` | `input` | CreateContact360ExportInput! | `SchedulerJob` |
| `createContact360Import` | `input` | CreateContact360ImportInput! | `SchedulerJob` (SuperAdmin) |
| `createAppointmentImport` | `input` | CreateAppointmentImportInput! | `SchedulerJob` |
| `retryJob` | `input` | RetryJobInput! | success |

Use **camelCase** in variables (e.g. `inputCsvKey`, `outputPrefix`, `s3Bucket`, `retryCount`, `savedSearchId`). See Input Types and Variable naming below.

## Flow

1. Client uploads the input CSV to S3 via the **Upload module** (multipart upload) and receives an S3 `file_key` (S3 object key).
2. Client calls a GraphQL mutation (e.g. `jobs.createEmailFinderExport`) with that key as `input.input_csv_key`.
3. Appointment360 validates auth and (for some mutations) role (e.g. SuperAdmin).
4. Appointment360 calls the tkdjob REST API (e.g. POST /api/v1/jobs/email-export).
5. On success, a row is inserted into `scheduler_jobs` (job_id, user_id, job_type, status, request/response payload).
6. The created `SchedulerJob` is returned; the client can poll status via `jobs.job(jobId)` or tkdjob directly.

## Types

### SchedulerJob

```graphql
type SchedulerJob {
  id: ID!
  jobId: ID!
  userId: ID!
  jobType: String!
  status: String!
  requestPayload: JSON
  responsePayload: JSON
  statusPayload: JSON    # Live status from Tkdjob GET /api/v1/jobs/{jobId}/status
  timelinePayload: JSON  # Live timeline from Tkdjob GET /api/v1/jobs/{jobId}/timeline
  dagPayload: JSON       # Live DAG from Tkdjob GET /api/v1/jobs/{jobId}/dag
  createdAt: DateTime!
  updatedAt: DateTime
}
```

- **statusPayload**: Fetched lazily from Tkdjob when requested. Includes `status`, `progress_percent`, `processed_rows`, `total_bytes`, `job_response.runtime_errors`, etc. Returns `null` if Tkdjob is unreachable.
- **timelinePayload**: Lifecycle events (created, enqueued, started, completed, failed, retried). Returns `null` if Tkdjob is unreachable.
- **dagPayload**: DAG structure (root_uuid, nodes, edges). Returns `null` if Tkdjob is unreachable.

### JobConnection

```graphql
type JobConnection {
  jobs: [SchedulerJob!]!
  pageInfo: PageInfo!
}
```

## Queries

### job(jobId: ID!)

Get a single scheduler job by id. User can only access their own jobs unless Admin/SuperAdmin.

**Parameters:**

| Name  | Type | Required | Description        |
|-------|------|----------|--------------------|
| jobId | ID!  | Yes      | Scheduler job ID   |

### jobs(limit, offset, status, jobType)

List scheduler jobs for the current user with pagination and optional filters.

**Parameters:**

| Name   | Type  | Required | Description                    |
|--------|-------|----------|--------------------------------|
| limit  | Int   | No       | Max results                    |
| offset | Int   | No       | Skip                           |
| status | String| No       | Filter by status               |
| jobType| String| No       | Filter by job type             |

## Variable naming (camelCase)

**Important:** The GraphQL schema uses camelCase for input/output fields. Use camelCase in variables (e.g. `inputCsvKey`, `outputPrefix`, `s3Bucket`, `csvColumns`, `retryCount`, `retryInterval`). Do not use snake_case (`input_csv_key`, `output_prefix`, etc.)—it will cause validation errors.

## Mutations

| Mutation | Tkdjob endpoint | Auth | Notes |
|----------|-----------------|------|-------|
| `createEmailFinderExport` | POST /api/v1/jobs/email-export | Authenticated | Tracks `BULK_EXPORT` feature usage; logs JOBS/EXPORT activity |
| `createEmailVerifyExport` | POST /api/v1/jobs/email-verify | Authenticated | Tracks `BULK_VERIFICATION` feature usage; logs JOBS/EXPORT activity |
| `createEmailPatternImport` | POST /api/v1/jobs/email-pattern-import | SuperAdmin only | Logs JOBS/IMPORT activity |
| `createContact360Export` | POST /api/v1/jobs/contact360-export | Authenticated | Optional `savedSearchId` links exports to Saved Searches; tracks `BULK_EXPORT` usage |
| `createContact360Import` | POST /api/v1/jobs/contact360-import | SuperAdmin only | Logs JOBS/IMPORT activity |
| `retryJob` | PUT /api/v1/jobs/{jobId}/retry | Authenticated | Retry failed job; user must own job or be Admin/SuperAdmin |

> **Saved Searches Integration:** `createContact360Export` accepts an optional `savedSearchId` argument (GraphQL), which is stored in `scheduler_jobs.request_payload.saved_search_id` and included in JOBS activities. This links Saved Searches, Contact360 exports, and job history.

## Input Types

### CreateContact360ImportInput (for createContact360Import mutation)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| s3Bucket | String! | Yes | - | S3 bucket (e.g. `appointment360uploads`) |
| s3Key | String! | Yes | - | S3 object key (file path from Upload) |
| outputPrefix | String | No | `imports/` | Output path prefix |
| csvColumns | JSON | No | null | Column mapping, e.g. `{ "linkedin_url_column": "linkedin_url" }` |
| chunkCount | Int | No | 8 | Chunk size |
| retryCount | Int | No | 3 | Retry attempts |
| retryInterval | Int | No | 5 | Minutes between retries |

Use camelCase in variables. Tkdjob expects snake_case (`s3_bucket`, `s3_key`, `output_prefix`, `csv_columns`, etc.).

### RetryJobInput (for retryJob mutation)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| jobId | ID! | Yes | - | Job ID to retry (e.g. `Import:uuid:prepare`) |
| retryCount | Int | No | 3 | Number of retry attempts |
| retryInterval | Int | No | 5 | Minutes between retries |
| runAfter | String | No | null | ISO datetime when to run (null = immediate) |
| data | JSON | No | null | Optional override for job data |
| priority | Int | No | null | Optional job priority (higher = more important) |

## Usage Example – Retry Job

```graphql
mutation RetryJob($input: RetryJobInput!) {
  jobs {
    retryJob(input: $input)
  }
}
```

Variables (camelCase):

```json
{
  "input": {
    "jobId": "Import:0ba322b4-a728-4742-96fa-cf30d64ed214:prepare",
    "retryCount": 3,
    "retryInterval": 5,
    "runAfter": null
  }
}
```

## Error Handling

- **ServiceUnavailableError** (503): Tkdjob API unavailable or request failed.
- **BadRequestError** (400): Invalid request or no job_uuid in scheduler response.
- **ForbiddenError** (403): SuperAdmin required (for pattern import, contact360 import) or access to another user's job denied.
- **NotFoundError** (404): Job not found for `job(jobId)` or `retryJob(jobId)`.
- **ValidationError** (422): Input validation failed.

## Task breakdown (for maintainers)

1. **Trace job(jobId):** JobQuery.job → SchedulerJobRepository.get_by_job_id; ownership check (user_id or Admin/SuperAdmin); SchedulerJob.from_model; statusPayload/timelinePayload/dagPayload fetched lazily from Tkdjob GET /jobs/{id}/status, /timeline, /dag.
2. **jobs list:** get_by_user_id with limit/offset/status/jobType; validate_pagination; return JobConnection with pageInfo.
3. **createEmailFinderExport:** Validate inputCsvKey (required); build payload (inputCsvKey, outputPrefix, rowLimit, chunkSize, emailColumn, csvColumns, retryCount, retryInterval, workflowId, s3Bucket); TkdjobClient.create_email_export; insert scheduler_jobs; track BULK_EXPORT usage and log JOBS/EXPORT activity.
4. **createContact360Export/createContact360Import:** Same pattern; optional savedSearchId on export; SuperAdmin for import; VQL/s3Key in payload.
5. **retryJob:** RetryJobInput (jobId, retryCount, retryInterval, runAfter, data, priority); verify job ownership or Admin/SuperAdmin; Tkdjob PUT /jobs/{jobId}/retry; return success.

## Related

- **TkdjobClient:** `app/clients/tkdjob_client.py`
- **SchedulerJobRepository:** `app/repositories/scheduler_job.py`
- **Email Module:** Export/verify-export flows create jobs via this module.
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): Contact AI work runs synchronously through GraphQL + `LambdaAIClient`, not through tkdjob / `scheduler_jobs`.

## Documentation metadata

- Era: `5.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

## Direct TKD Job REST contract (source service)

### Endpoints

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/api/v1/jobs/bulk-insert/complete-graph` | POST | Insert arbitrary DAG (nodes + edges) |
| `/api/v1/jobs/email-export` | POST | Create `email_finder_export_stream` job |
| `/api/v1/jobs/email-verify` | POST | Create `email_verify_export_stream` job |
| `/api/v1/jobs/email-pattern-import` | POST | Create `email_pattern_import_stream` job |
| `/api/v1/jobs/contact360-import` | POST | Create `contact360_import_prepare` job |
| `/api/v1/jobs/contact360-export` | POST | Create `contact360_export_stream` job |
| `/api/v1/jobs/` | GET | List jobs with filtering |
| `/api/v1/jobs/{uuid}` | GET | Fetch a single job |
| `/api/v1/jobs/{uuid}/status` | GET | Fetch status and progress fields |
| `/api/v1/jobs/{uuid}/timeline` | GET | Fetch lifecycle event timeline |
| `/api/v1/jobs/{uuid}/dag` | GET | Fetch DAG nodes and edges |
| `/api/v1/jobs/{uuid}/retry` | PUT | Retry an existing job (optional override data/priority) |
| `/api/v1/jobs/validate/vql` | POST | Validate VQL syntax |
| `/api/v1/metrics` | GET | Prometheus metrics |
| `/api/v1/metrics/stats` | GET | JSON metrics |
| `/health`, `/health/live`, `/health/ready` | GET | Service health checks |

### Status vocabulary (canonical)

`open`, `in_queue`, `processing`, `completed`, `failed`, `retry`

Retry scheduling is triggered by `retry` status (not directly from `failed`).

### `statusPayload` field mapping

- `statusPayload.status` -> `job_node.status`
- `statusPayload.progress_percent` -> computed from `checkpoint_byte` and `total_bytes`
- `statusPayload.checkpoint_byte` -> `job_node.checkpoint_byte`
- `statusPayload.total_bytes` -> `job_node.total_bytes`
- `statusPayload.processed_rows` -> `job_node.processed_rows`
- `statusPayload.job_response` -> `job_node.job_response`

### Processor registry mapping

| `job_type` | Processor | Typical creator endpoint |
| --- | --- | --- |
| `email_finder_export_stream` | `email_finder_export_stream` | `POST /api/v1/jobs/email-export` |
| `email_verify_export_stream` | `email_verify_export_stream` | `POST /api/v1/jobs/email-verify` |
| `email_pattern_import_stream` | `email_pattern_import_stream` | `POST /api/v1/jobs/email-pattern-import` |
| `contact360_import_prepare` | `contact360_import_prepare` | `POST /api/v1/jobs/contact360-import` |
| `contact360_export_stream` | `contact360_export_stream` | `POST /api/v1/jobs/contact360-export` |
| `export_csv_file` | validation stub | DAG/manual use only |
| `insert_csv_file` | validation stub | DAG/manual use only |

### Known gaps

- Stale `processing` jobs require scheduler recovery loop to run.
- DAG degree-decrement failures can block downstream nodes.
- Service auth is currently shared `X-API-Key`, not role/user scoped.
- Legacy multi-node Contact360 DAG docs are reference-only; active flows are streaming processors listed above.

## Era binding correction

- This module is operationally relevant from `2.x` through `10.x` (not only `5.x`).

## Maintenance references

- Era index: `docs/backend/apis/JOBS_ERA_TASK_PACKS.md`
- Data lineage: `docs/backend/database/jobs_data_lineage.md`

