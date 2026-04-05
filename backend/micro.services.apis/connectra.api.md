# Connectra API (`EC2/sync.server`)

Go/Gin service (**Connectra**): VQL search against OpenSearch, Postgres-backed filters, batch upsert, CSV import/export **jobs**, and S3 presigned URL helpers. The Contact360 gateway uses **`CONNECTRA_BASE_URL`** with **`CONNECTRA_API_KEY`** on the **`X-API-Key`** header.

**Code:** `EC2/sync.server/cmd/server.go` (middleware, `GET /health`), `modules/contacts/routes.go`, `modules/companies/routes.go`, `modules/common/routes.go`.

**Default listen:** `:<PORT>` with **`PORT`** default **`8000`** (`conf.AppConfig.Port`).

---

## Operation inventory

| Method | Path | Auth |
| --- | --- | --- |
| `GET` | `/health` | `X-API-Key` |
| `POST` | `/contacts/` | `X-API-Key` |
| `POST` | `/contacts/count` | `X-API-Key` |
| `POST` | `/contacts/batch-upsert` | `X-API-Key` |
| `POST` | `/companies/` | `X-API-Key` |
| `POST` | `/companies/count` | `X-API-Key` |
| `POST` | `/companies/batch-upsert` | `X-API-Key` |
| `POST` | `/common/batch-upsert` | `X-API-Key` |
| `GET` | `/common/upload-url` | `X-API-Key` |
| `GET` | `/common/download-url` | `X-API-Key` |
| `POST` | `/common/jobs` | `X-API-Key` |
| `POST` | `/common/jobs/create` | `X-API-Key` |
| `GET` | `/common/jobs/:job_uuid` | `X-API-Key` |
| `POST` | `/common/jobs/:job_uuid/pause` | `X-API-Key` |
| `POST` | `/common/jobs/:job_uuid/resume` | `X-API-Key` |
| `POST` | `/common/jobs/:job_uuid/terminate` | `X-API-Key` |
| `GET` | `/common/:service/filters` | `X-API-Key` |
| `POST` | `/common/:service/filters/data` | `X-API-Key` |

`:service` must be exactly **`contact`** or **`company`** (`constants.ContactsService` / `CompaniesService`). Paths look like `/common/contact/filters`, not `contacts`.

---

## Configuration (environment)

Viper loads `.env` from the process working directory and merges **`AutomaticEnv()`** (uppercase env vars match `mapstructure` tags).

| Group | Variables (examples) | Purpose |
| --- | --- | --- |
| App | `API_KEY`, `PORT`, `APP_VERSION`, `APP_ENV`, `MAX_REQUESTS_PER_MINUTE`, `CORS_ALLOWED_ORIGINS` | API key (**required** for middleware), port, version string on `/health`, rate-limit bucket size, CORS (`*` or comma-separated origins) |
| PostgreSQL | `PG_DB_CONNECTION` or `PG_DB_HOST`, `PG_DB_PORT`, `PG_DB_DATABASE`, `PG_DB_USERNAME`, `PG_DB_PASSWORD`, `PG_DB_SSL`, `PG_DB_DEBUG` | Bun/PG client |
| OpenSearch | `OPEN_SEARCH_CONNECTION` or host/port/user/password, `OPEN_SEARCH_SSL`, `OPEN_SEARCH_AUTH`, `OPEN_SEARCH_DEBUG` | Search client |
| S3 | `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_REGION`, `S3_BUCKET`, `S3_ENDPOINT`, `S3_SSL`, `S3_DEBUG`, `S3_UPLOAD_URL_TTL_HOURS`, `S3_UPLOAD_FILE_PATH_PRIFIX` | Presigned URLs and CSV job I/O |
| Job worker | `JOB_IN_QUEUE_SIZE`, `PARALLEL_JOBS`, `TICKER_INTERVAL_MINUTES`, `BATCH_SIZE_FOR_INSERTION`, `JOB_TYPE` | Background job processor (`cmd/jobs.go`), not every HTTP handler |

---

## Global middleware

| Order | Middleware | Behavior |
| --- | --- | --- |
| 1 | `gin.Logger`, `gin.Recovery` | Request logging, panic recovery |
| 2 | CORS | `CORS_ALLOWED_ORIGINS` empty or `*` → allow all origins; else explicit list |
| 3 | Gzip | Default compression |
| 4 | **Rate limiter** | Token bucket: capacity = `MAX_REQUESTS_PER_MINUTE`, refill ~1/60 per second |
| 5 | **`APIKeyAuth`** | Header **`X-API-Key`** must equal `API_KEY` |

**Missing/wrong API key — `401`:**

```json
{
  "error": "ERR_UNAUTHORIZED: invalid or missing API key; provide a valid 'X-API-Key' header",
  "success": false
}
```

**Rate limit — `429`:**

```json
{
  "error": "ERR_RATE_LIMIT_EXCEEDED: too many requests; please try again later",
  "success": false
}
```

Most successful JSON responses include **`"success": true`**. Errors use **`"success": false`** and **`"error"`** with a stable `ERR_*` prefix (see `constants/errors_message.go`).

---

## `GET /health`

Liveness and diagnostics for GraphQL `vqlHealth` (gateway probes `CONNECTRA_BASE_URL` + API key).

**Headers:** `X-API-Key: <API_KEY>` (required).

**Response `200`:**

```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_seconds": 42,
  "service": "connectra",
  "diagnostics": {
    "database": true,
    "search_engine": true
  }
}
```

- `version`: `APP_VERSION`, or **`1.0.0`** if unset.
- `diagnostics.database` / `search_engine`: non-nil connection handles (`connections.PgDBConnection`, `connections.OpenSearchConnection`).

---

## VQL request body (`utilities.VQLQuery`)

Used by **`POST /contacts/`**, **`POST /contacts/count`**, **`POST /companies/`**, **`POST /companies/count`**.

```json
{
  "where": {
    "text_matches": {
      "must": [],
      "must_not": []
    },
    "keyword_match": {
      "must": {},
      "must_not": {}
    },
    "range_query": {
      "must": {},
      "must_not": {}
    }
  },
  "order_by": [
    { "order_by": "uuid", "order_direction": "desc" }
  ],
  "cursor": [],
  "select_columns": ["uuid", "first_name"],
  "company_config": {
    "populate": false,
    "select_columns": []
  },
  "page": 1,
  "limit": 25
}
```

**`text_matches.must[]` item** (`TextMatchStruct`): `text_value`, `filter_key`, `search_type` (`exact` \| `shuffle` \| `substring`), optional `slop`, `operator`, `fuzzy`.

**Pagination validation:** `limit` must be **≤ 100** (`MaxPageSize`); `page` must be **≤ 10** (`MaxOpenSearchPageNumber`). Violations → **`400`** with `ERR_PAGE_SIZE_EXCEEDED` or `ERR_PAGE_OUT_OF_RANGE`.

**Success — list:**

```json
{
  "data": [],
  "success": true
}
```

**Success — count:**

```json
{
  "count": 0,
  "success": true
}
```

(`count` is integer; shape from OpenSearch/count path.)

---

## Contacts

### `POST /contacts/`

**Body:** `VQLQuery` (JSON).  
**Response `200`:** `{ "data": <array of contact hits>, "success": true }`  
**Errors:** `400` / `500` with `{ "error": "...", "success": false }`.

### `POST /contacts/count`

**Body:** `VQLQuery`.  
**Response `200`:** `{ "count": <int>, "success": true }`.

### `POST /contacts/batch-upsert`

**Body:** JSON **array** of `PgContact` objects (not wrapped). Max **100** rows (`MaxPageSize`). Each contact must have valid UUIDs for contact and company.

**Response `200`:** `{ "success": true }`.

**Errors:** invalid UUIDs, batch too large, company lookup failures → **`400`** with message.

---

## Companies

Same patterns as contacts:

| Path | Body | Success |
| --- | --- | --- |
| `POST /companies/` | `VQLQuery` | `{ "data": [...], "success": true }` |
| `POST /companies/count` | `VQLQuery` | `{ "count": n, "success": true }` |
| `POST /companies/batch-upsert` | JSON array of company records | `{ "success": true }` |

---

## Common

### `POST /common/batch-upsert`

LinkedIn-style row import: **`BatchInsertRequest`**

```json
{
  "data": [
    {
      "first_name": "jane",
      "last_name": "doe",
      "person_linkedin_url": "https://linkedin.com/in/jane",
      "email": "j@example.com"
    }
  ]
}
```

`data` is **`[]map[string]string`**: required, non-empty, max length **100**.

**Response `200`:** `{ "message": "Batch upsert successful", "success": true }`.

### `GET /common/upload-url`

| Query | Required | Description |
| --- | --- | --- |
| `filename` | Yes | Original filename |
| `bucket` | No | Defaults to `S3_BUCKET` |

**Response `200`:**

```json
{
  "success": true,
  "upload_url": "https://...",
  "s3_key": "<prefix>/<uuid>_<filename>",
  "expires_in": "24h0m0s"
}
```

(`expires_in` is `S3_UPLOAD_URL_TTL_HOURS` as `time.Duration.String()`.)

### `GET /common/download-url`

| Query | Required |
| --- | --- |
| `s3_key` | Yes |
| `bucket` | No (defaults to `S3_BUCKET`) |

**Response `200`:** `{ "success": true, "download_url": "...", "s3_key": "...", "expires_in": "..." }`.

---

## Jobs (Postgres `jobs` table)

Worker-supported **`job_type`** values: **`insert_csv_file`**, **`export_csv_file`** (`constants/jobs.go`). Other types are rejected at processing time with `ERR_INVALID_JOB_TYPE`.

### `POST /common/jobs` — list

**Body (`ListJobsRequest`):**

```json
{
  "job_type": "",
  "status": ["open", "completed"],
  "limit": 50
}
```

- `limit`: optional; **0** means repository default **25** (`DefaultPageSize`); max **100** (`MaxPageSize`).

**Response `200`:** `{ "data": [ { ...job row... } ], "success": true }`.

### `POST /common/jobs/create`

**Body (`CreateJobRequest`):**

```json
{
  "job_type": "insert_csv_file",
  "job_data": {
    "s3_key": "path/to/file.csv",
    "s3_bucket": "optional-override"
  },
  "retry_count": 0
}
```

**`insert_csv_file`** — `job_data` unmarshals to **`InsertFileJobData`**: `s3_key`, `s3_bucket` (optional; defaults to configured bucket).

**`export_csv_file`** — `job_data` unmarshals to **`ExportFileJobData`:**

```json
{
  "s3_bucket": "optional",
  "service": "contact",
  "vql": {
    "where": { "text_matches": { "must": [], "must_not": [] }, "keyword_match": { "must": {}, "must_not": {} }, "range_query": { "must": {}, "must_not": {} } } },
    "select_columns": ["uuid", "email"],
    "page": 1,
    "limit": 100
  }
}
```

**`service`** must be **`contact`** or **`company`** (matches filter service constants). Export requires non-empty **`vql.select_columns`**.

**Response `201`:** `{ "message": "Job created successfully", "success": true }`.

### `GET /common/jobs/:job_uuid`

**Response `200`:** `{ "data": { ... }, "success": true }` where `data` is a **`ModelJobs`** row:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | uint64 | |
| `uuid` | string | |
| `job_type` | string | |
| `data` | object (JSON) | Original `job_data` |
| `status` | string | e.g. `open`, `paused`, `processing`, `completed`, `failed`, `terminated` |
| `job_response` | object | Runtime errors, messages, `s3_key` for exports |
| `retry_count`, `retry_interval` | int | |
| `run_after` | ISO time or null | |
| `created_at`, `updated_at` | ISO time | |

**Not found:** **`500`** with `ERR_JOB_NOT_FOUND` (handler maps repository empty list to this error) — treat as missing job.

### `POST /common/jobs/:job_uuid/pause` | `resume` | `terminate`

**Response `200`:**

```json
{ "job_uuid": "<uuid>", "status": "paused", "success": true }
```

(`resume` → `"status": "open"`; `terminate` → `"terminated"`.)

**Not found:** **`404`** with `{ "error": "...", "success": false }` when job UUID does not exist.

---

## Filters

### `GET /common/:service/filters`

Returns filter definitions for **`contact`** or **`company`**. Invalid service → **`500`** with `ERR_UNSUPPORTED_SERVICE`.

**Response `200`:** `{ "data": [...], "success": true }`.

### `POST /common/:service/filters/data`

**Body (`FiltersDataQuery`):**

```json
{
  "filter_key": "title",
  "search_text": "",
  "page": 1,
  "limit": 20
}
```

Server sets **`service`** from the path (`:service`). `limit` validated with **`ValidatePageSize`** (≤ **100**).

**Response `200`:**

```json
{
  "data": [
    { "value": "...", "display_value": "..." }
  ],
  "success": true
}
```

---

## GraphQL gateway mapping (summary)

| Connectra HTTP | Gateway docs |
| --- | --- |
| VQL list/count, batch-upsert, filters | [03_CONTACTS_MODULE.md](../graphql.modules/03_CONTACTS_MODULE.md), [04_COMPANIES_MODULE.md](../graphql.modules/04_COMPANIES_MODULE.md) |
| `/common/jobs*`, CSV worker jobs | [16_JOBS_MODULE.md](../graphql.modules/16_JOBS_MODULE.md) |
| `GET /health` | [08_HEALTH_MODULE.md](../graphql.modules/08_HEALTH_MODULE.md) |

The gateway **`scheduler_jobs`** table and GraphQL **`jobs.*`** mutations are a **separate** orchestration layer; they may call Connectra (`POST /common/jobs/create`, etc.) depending on mutation — see Jobs module.

---

## Related docs

| Doc | Purpose |
| --- | --- |
| [03_CONTACTS_MODULE.md](../graphql.modules/03_CONTACTS_MODULE.md) | GraphQL Contacts → Connectra |
| [04_COMPANIES_MODULE.md](../graphql.modules/04_COMPANIES_MODULE.md) | GraphQL Companies → Connectra |
| [08_HEALTH_MODULE.md](../graphql.modules/08_HEALTH_MODULE.md) | `vqlHealth` probe |
| [16_JOBS_MODULE.md](../graphql.modules/16_JOBS_MODULE.md) | Scheduler vs Connectra jobs |
| [09_USAGE_MODULE.md](../graphql.modules/09_USAGE_MODULE.md) | Usage / feature overview (jobs list is gateway DB) |
| [11_ACTIVITIES_MODULE.md](../graphql.modules/11_ACTIVITIES_MODULE.md) | Activity logging |
| [../postman/EC2_sync.server.postman_collection.json](../postman/EC2_sync.server.postman_collection.json) | Postman collection |
