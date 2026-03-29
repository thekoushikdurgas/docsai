---
title: "graphql/ExportEmails"
source_json: mutation_export_emails_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ExportEmails

## Overview

Create email export jobs for CSV output using jobs module orchestration with email runtime execution paths.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_export_emails_graphql |
| _id | mutation_export_emails_graphql-001 |
| endpoint_path | graphql/ExportEmails |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-24T00:00:00.000000+00:00 |
| era | 3.x |
| introduced_in | 3.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user, admin, superadmin |
| rate_limited | False |
| access_control | "authenticated" |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/email/queries.py |
| router_file | contact360.io/app/src/services/graphql/emailService.ts |
| sql_file | docs/backend/apis/15_EMAIL_MODULE.md |


## GraphQL operation

```graphql
mutation ExportEmails($input: EmailExportInput!) { email { exportEmails(input: $input) { exportId status contactCount companyCount } } }
```

## Data & infrastructure

### db_tables_read

- scheduler_jobs

### db_tables_write

- scheduler_jobs

### lambda_services

- lambda/emailapis
- lambda/emailapigo
- contact360.io/jobs

## Service / repository methods

### service_methods

- exportEmails

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /jobs | Jobs Page | emailService | useCsvUpload | secondary | job_creation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/jobs_page.json
- docs/frontend/pages/email_page.json

## Inventory

- **page_count:** 1
- **Source:** `mutation_export_emails_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `3.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `scheduler_jobs` → [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql)

### Write
- `scheduler_jobs` → [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql)

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [Email APIs](../database/emailapis_data_lineage.md)
- [TKD Jobs](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`lambda/emailapis`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`lambda/emailapigo`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`contact360.io/jobs`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_export_emails_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
