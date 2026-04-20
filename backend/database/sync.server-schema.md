# Connectra (`EC2/sync.server`) — PostgreSQL schema

Go module: `connectra.server`. Tables are ensured on startup via `connections.InitDB()` using Bun `CreateTable … IfNotExists`.

## Tables

### `companies`

| Column | Type | Notes |
|--------|------|--------|
| id | bigserial PK | |
| uuid | text UNIQUE NOT NULL | UUID5 from `lower(name)+lower(linkedin_url)` |
| name | text | |
| employees_count | bigint | |
| industries | text[] | |
| keywords | text[] | |
| address | text | |
| annual_revenue | bigint | |
| total_funding | bigint | |
| technologies | text[] | |
| city, state, country | text | lowercased on ingest |
| linkedin_url, website, normalized_domain | text | |
| facebook_url, twitter_url | text | |
| company_name_for_emails | text | |
| phone_number | text | |
| latest_funding | text | |
| latest_funding_amount | bigint | |
| last_raised_at | text | |
| linkedin_sales_url | text | Sales Navigator (Era 4) |
| created_at, updated_at, deleted_at | timestamptz | soft delete |

### `contacts`

| Column | Type | Notes |
|--------|------|--------|
| id | bigserial PK | |
| uuid | text UNIQUE | UUID5 from `first+last+linkedin` |
| first_name, last_name | text | lowercased |
| company_id | text | FK-style UUID to `companies.uuid` |
| email | text | |
| title | text | |
| departments | text[] | |
| mobile_phone, work_direct_phone, home_phone, other_phone | text | |
| email_status, seniority | text | |
| city, state, country | text | |
| linkedin_url | text | |
| facebook_url, twitter_url, website | text | |
| stage | text | campaigns (Era 10) |
| ai_score, lead_score | double precision | default 0 |
| recommendation_rank | bigint | default 0 |
| created_at, updated_at, deleted_at | timestamptz | |

### `jobs`

| Column | Type | Notes |
|--------|------|--------|
| id | bigserial PK | |
| uuid | text UNIQUE | Asynq task id |
| job_type | text | `insert_csv_file`, `export_csv_file` |
| data | jsonb | payload |
| status | text | open, in_queue, processing, paused, … |
| job_response | jsonb | progress / errors |
| retry_count, retry_interval | int | |
| run_after | timestamptz | nullable |
| created_at, updated_at | timestamptz | |

Redis mirrors hot job state (`sync:job:*`) for workers; Postgres is source of truth for listing.

### `filters` / `filters_data`

Filter metadata and precomputed facet values. Seed: [`EC2/sync.server/docs/sql/seed_filters_and_filters_data.sql`](../../EC2/sync.server/docs/sql/seed_filters_and_filters_data.sql).

## Migrations

- [`EC2/sync.server/migrations/001_connectra_additive_columns.sql`](../../EC2/sync.server/migrations/001_connectra_additive_columns.sql) — additive columns for existing databases.
- [`EC2/sync.server/migrations/002_contacts_linkedin_url_unique_optional.sql`](../../EC2/sync.server/migrations/002_contacts_linkedin_url_unique_optional.sql) — optional unique index on normalized `linkedin_url` (commented; run manually if needed).

## Internal HTTP: extension satellite bulk

- **`POST /internal/extension/upsert-bulk`** — implemented in [`EC2/sync.server/modules/extension`](../../EC2/sync.server/modules/extension); accepts the lightweight `{ contacts, companies }` shape from **extension.server** (not the same as `POST /contacts/batch-upsert` JSON array format).

## Public HTTP: `batch-upsert` (companies then contacts)

Aligned with [`DECISIONS.md`](../../DECISIONS.md) § Connectra:

- **`POST /companies/batch-upsert`** and **`POST /contacts/batch-upsert`** accept JSON **arrays** of company/contact objects (see Postman collection).
- **Success response** includes:
  - **`success`** — boolean.
  - **`company_uuids`** / **`contact_uuids`** — **ordered parallel to the request array** after bind/validation (same positions as input rows).
  - Optional correlation slices **`companies`** / **`contacts`** with minimal safe fields (e.g. uuid + linkedin_url + name) when enabled.
- **Failure:** return a **non-2xx** status (or explicit error contract), with **`success: false`** and an **`error`** message — **do not** return HTTP 200 with a silent failure for bulk operations.
- **extension.server save path** calls **companies batch-upsert first**, then **contacts batch-upsert**, aggregating UUID lists across chunks in stable order.

## OpenSearch

Index mappings: `EC2/sync.server/docs/contact_index_create.json`, `docs/company_index_create.json` (and `examples/` copies).
