# Email API service (`EC2/email.server`)

Go/Gin microservice (`github.com/ayan/emailapigo` module paths in-repo: `EC2/email.server`). The Contact360 gateway calls it via **`LAMBDA_EMAIL_API_URL`** and **`LAMBDA_EMAIL_API_KEY`** (`X-API-Key` header).

**Primary code:** `EC2/email.server/internal/api/router.go` (`SetupRouter`).  
**Process entry:** `EC2/email.server/main.go` (HTTP on `PORT`, or Lambda adapter when `AWS_LAMBDA_FUNCTION_NAME` is set).

---

## Authentication and public routes

| Route | Auth |
| --- | --- |
| `GET /health` | **None** |
| `GET /` | **None** |
| All other routes below | **`X-API-Key`** must equal env **`API_KEY`** |

**Unauthorized (`401`):**

```json
{ "detail": "invalid or missing API key" }
```

Most error responses use **`{ "detail": "<message>" }`**. Validation/bind errors are typically **`400`**.

---

## Configuration (environment)

From `internal/config/config.go` (`env` tags). Critical vars:

| Variable | Default | Role |
| --- | --- | --- |
| `API_KEY` | _(required)_ | API authentication |
| `DATABASE_URL` | _(required)_ | GORM/Postgres (`emailapi_jobs`, patterns, etc.) |
| `PORT` | `3000` | HTTP listen port |
| `REDIS_ADDR` | `localhost:6379` | Asynq queues + job row cache |
| `CONNECTRA_BASE_URL` | required | Internal Connectra client |
| `CONNECTRA_API_KEY` | required | Connectra auth |
| `S3_BUCKET_NAME` | — | S3 CSV jobs / presign |
| `WEBSEARCH_ENABLED` | `false` | `/web/web-search` behavior |
| `ICYPEAS_ENABLED` | `true` | Feature flags with IcyPeas |

Optional: `TRUELIST_*`, `ICYPEAS_*`, `MAILVETTER_*`, `MAILTESTER_*`, `OPENAI_*`, `SCRAPINGDOG_*`, `PROJECT_NAME`, `VERSION`, `S3_PRESIGNED_URL_EXPIRATION`, `PROXY_ADDR`, `LAMBDA_LOGS_*`, etc.

---

## Operation inventory

| Method | Path | Auth |
| --- | --- | --- |
| `GET` | `/health` | Public |
| `GET` | `/` | Public |
| `GET` | `/jobs` | Key |
| `POST` | `/jobs/:id/pause` | Key |
| `POST` | `/jobs/:id/resume` | Key |
| `POST` | `/jobs/:id/terminate` | Key |
| `GET` | `/jobs/:id/status` | Key |
| `POST` | `/email/finder/` | Key |
| `POST` | `/email/finder/bulk` | Key |
| `POST` | `/email/finder/bulk/job` | Key |
| `POST` | `/email/finder/s3` | Key |
| `POST` | `/email/single/verifier/` | Key |
| `POST` | `/email/bulk/verifier/` | Key |
| `POST` | `/email/bulk/verifier/job` | Key |
| `POST` | `/email/verify/s3` | Key |
| `POST` | `/web/web-search` | Key |
| `POST` | `/email-patterns/add` | Key |
| `POST` | `/email-patterns/add/bulk` | Key |
| `POST` | `/email-patterns/predict` | Key |
| `POST` | `/email-patterns/predict/bulk` | Key |

---

## `GET /health`

**Response `200`:**

```json
{
  "status": "ok",
  "service": "<PROJECT_NAME>",
  "version": "<VERSION>",
  "diagnostics": {
    "api_key_configured": true,
    "database_configured": true,
    "truelist_configured": false,
    "mailvetter_configured": false,
    "icypeas_configured": false,
    "websearch_enabled": false,
    "icypeas_enabled": true,
    "s3_configured": true
  }
}
```

Booleans reflect non-empty API keys / URLs / bucket name (not live dependency checks).

---

## `GET /`

Discovery JSON: `service`, `version`, `description`, `status`, `endpoints` map (`health`, `docs`, `email_finder` → `/email`, `email_verification` → `/email`, `email_patterns` → `/email-patterns`).

---

## Jobs (Postgres `emailapi_jobs` + Redis)

### `GET /jobs`

Returns up to **50** most recent jobs (fixed query in router).

**Response `200`:**

```json
{
  "total": 0,
  "jobs": [
    {
      "id": "uuid-string",
      "provider": "finder",
      "status": "running",
      "total_emails": 100,
      "completed": 0,
      "unknown_count": 0,
      "avg_duration_ms": 0,
      "done": false,
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

### `GET /jobs/:id/status`

**Response `200`:**

```json
{
  "success": true,
  "data": {
    "uuid": "<job id>",
    "job_title": "finder job",
    "job_type": "finder",
    "status": "processing",
    "processed_rows": 10,
    "progress_percent": 50,
    "credits": 10,
    "created_at": "...",
    "updated_at": "...",
    "provider": "finder_s3",
    "done": false,
    "output_csv_key": "optional/prefix/jobid.csv"
  }
}
```

`job_type` is **`finder`** if provider name contains `"finder"`, else **`verification`**. `status` becomes **`completed`** when `done` is true; running jobs may show as **`processing`**.

**`404`:** `{ "detail": "job not found" }`.

### `POST /jobs/:id/pause`

**Response `200`:** `{ "job_id": "<id>", "status": "paused" }`  
**`404`:** job missing. **`400`:** job already completed.

### `POST /jobs/:id/resume`

Requires job **`paused`**. **Response `200`:** `{ "job_id": "<id>", "status": "running" }`.  
**`400`:** not paused or already completed. **`404`:** not found.

### `POST /jobs/:id/terminate`

Terminates job, may trigger S3 merge in background for S3-backed jobs, deletes Postgres row. **Response `200`:**

```json
{
  "job_id": "<id>",
  "status": "terminated",
  "message": "job completely removed, remaining items merging to S3 (if applicable)"
}
```

---

## Email finder

### `POST /email/finder/`

**Query parameters (required):** `first_name`, `last_name`, `domain`.

**Response `200`:**

```json
{
  "emails": [
    { "uuid": "", "email": "a@b.com", "status": "", "source": "" }
  ],
  "total": 1,
  "success": true
}
```

Errors: **`400`** missing params; other statuses from `internal/errors` mapping.

### `POST /email/finder/bulk`

**Body:**

```json
{
  "items": [
    { "first_name": "Jane", "last_name": "Doe", "domain": "example.com" }
  ]
}
```

**Constraints:** `items` length **1–50** (`BulkEmailFinderRequest`).

**Response `200`:**

```json
{
  "processed_count": 1,
  "total_requested": 1,
  "total_successful": 1,
  "results": [
    {
      "first_name": "Jane",
      "last_name": "Doe",
      "domain": "example.com",
      "emails": [],
      "source": "",
      "total": 0,
      "success": true,
      "error": ""
    }
  ]
}
```

Per-item failures set `success: false` and `error`.

### `POST /email/finder/bulk/job`

Async Asynq job. **Response `202`:**

```json
{
  "job_id": "<uuid>",
  "queued": 10,
  "status_url": "/jobs/<uuid>/status"
}
```

### `POST /email/finder/s3`

**Body (`S3CSVFinderRequest`):**

```json
{
  "s3_bucket": "my-bucket",
  "input_csv_key": "upload/input.csv",
  "output_prefix": "exports/",
  "csv_columns": {
    "first_name": "First Name",
    "last_name": "Last Name",
    "domain": "Website"
  }
}
```

**`csv_columns`** must include keys **`first_name`**, **`last_name`**, **`domain`** (values = CSV header names).

**Response `202`:** `{ "job_id", "status_url", "message" }` — streaming/enqueue runs in background.

---

## Email verification

### `POST /email/single/verifier/`

**Body (`SingleEmailVerifierRequest`):**

```json
{
  "email": "user@example.com",
  "provider": "mailtester"
}
```

**`provider`:** `mailvetter` \| `mailtester` \| `icypeas` \| `truelist`.

**Response `200`:**

```json
{
  "result": {
    "email": "user@example.com",
    "status": "valid"
  },
  "success": true
}
```

`status` values include `valid`, `invalid`, `catchall`, `unknown`, `risky`.

### `POST /email/bulk/verifier/`

**Body:**

```json
{
  "provider": "mailtester",
  "emails": ["a@b.com"]
}
```

**Constraints:** **1–10000** emails. Providers: `mailvetter`, `mailtester`, `icypeas`, `truelist`.

**Response `200`:**

```json
{
  "results": [
    {
      "email": "a@b.com",
      "status": "valid",
      "email_state": null,
      "email_sub_state": null
    }
  ],
  "total": 1,
  "valid_count": 1,
  "invalid_count": 0,
  "catchall_count": 0,
  "unknown_count": 0,
  "success": true
}
```

### `POST /email/bulk/verifier/job`

**Response `202`:** same shape as finder bulk job (`job_id`, `queued`, `status_url`). Uses mailtester or mailvetter queue depending on `provider`.

### `POST /email/verify/s3`

**Body (`S3CSVVerifyRequest`):**

```json
{
  "s3_bucket": "my-bucket",
  "input_csv_key": "upload/emails.csv",
  "output_prefix": "verified/",
  "csv_columns": { "email": "Email Column" },
  "provider": "mailtester"
}
```

**`csv_columns.email`** required; **`provider`** defaults to **`mailtester`** if empty.

**Response `202`:** `{ "job_id", "status_url", "message" }`.

---

## Web search

### `POST /web/web-search`

**Body:**

```json
{
  "full_name": "Jane Doe",
  "company_domain": "example.com"
}
```

**Response `200`:** JSON from `WebSearchService.DiscoverEmail` (structure depends on OpenAI/DuckDuckGo pipeline). **`500`** on failure.

---

## Email patterns

### `POST /email-patterns/add`

**Body (`EmailPatternRequest`):**

```json
{
  "company_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "domain": "example.com"
}
```

**Response `201`:** `AddEmailPatternResponse` (`uuid`, `company_uuid`, `pattern_format`, `pattern_string`, `is_auto_extracted`, `domain`, `contact_count`, `created_at`, `updated_at`).

### `POST /email-patterns/add/bulk`

**Body:** `{ "items": [ EmailPatternRequest, ... ] }` (min 1 item).

**Response `201`:** bulk result from service (same family as single add).

### `POST /email-patterns/predict`

**Body:**

```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "domain": "example.com"
}
```

**Response `200`:** `{ "domain", "patterns": [...], "total", "success": true }`.

### `POST /email-patterns/predict/bulk`

**Body:** `{ "items": [ { "first_name", "last_name", "domain" }, ... ] }`.

**Response `200`:** `{ "results": [...], "total", "success": true }`.

---

## GraphQL gateway mapping

| Concern | Doc |
| --- | --- |
| GraphQL email operations | [15_EMAIL_MODULE.md](../graphql.modules/15_EMAIL_MODULE.md) |
| Scheduler jobs + S3 exports | [16_JOBS_MODULE.md](../graphql.modules/16_JOBS_MODULE.md) |
| Postman collection | [EC2_email.server.postman_collection.json](../postman/EC2_email.server.postman_collection.json) |

---

## Legacy / parallel documentation

Older matrices referred to `lambda/emailapis` (Python) and `lambda/emailapigo`. **`EC2/email.server`** is the maintained Gin implementation whose routes match the table above. For endpoint-era matrices and data lineage, still see:

- [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md)
- [emailapis_endpoint_era_matrix.md](../endpoints/emailapis_endpoint_era_matrix.md)
- [emailapis_data_lineage.md](../database/emailapis_data_lineage.md)
