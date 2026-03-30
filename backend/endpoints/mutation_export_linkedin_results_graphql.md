---
title: "graphql/ExportLinkedIn"
source_json: mutation_export_linkedin_results_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ExportLinkedIn

## Overview

Export contacts and companies by multiple LinkedIn URLs. Accepts LinkedInExportInput with urls array. Returns LinkedInExportResponse with separate contactExport and companyExport (each with exportId, downloadUrl, expiresAt, contactCount, companyCount, status), plus totalUrls, contactUrlsCount, companyUrlsCount, and unmatchedUrlsCount. Creates separate export jobs for contacts and companies. Credits: 1 credit per LinkedIn URL (FreeUser/ProUser only).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_export_linkedin_results_graphql |
| _id | mutation_export_linkedin_results_graphql-001 |
| endpoint_path | graphql/ExportLinkedIn |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 4.x |
| introduced_in | 4.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/linkedin/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/linkedinService.ts |


## GraphQL operation

```graphql
mutation ExportLinkedIn($input: LinkedInExportInput!) { linkedin { exportLinkedInResults(input: $input) { contactExport { exportId downloadUrl status } companyExport { exportId downloadUrl status } totalUrls contactUrlsCount companyUrlsCount unmatchedUrlsCount } } }
```

## Data & infrastructure

### db_tables_read

- contacts
- companies
- contacts_index
- companies_index

### db_tables_write

- jobs
- scheduler_jobs
- job_events

### lambda_services

- contact360.io/sync
- contact360.io/jobs
- lambda/s3storage

## Service / repository methods

### service_methods

- exportByLinkedInUrls
- exportLinkedInResults

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /linkedin | Linkedin Page | linkedinService | useLinkedIn | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/linkedin/page.tsx
- contact360.io/app/src/services/graphql/linkedinService.ts
- contact360.io/app/src/hooks/useLinkedIn.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_export_linkedin_results_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `contacts` — *no `tables/contacts.sql` snapshot in docs; see service lineage below*
- `companies` — *no `tables/companies.sql` snapshot in docs; see service lineage below*
- `contacts_index` — *no `tables/contacts_index.sql` snapshot in docs; see service lineage below*
- `companies_index` — *no `tables/companies_index.sql` snapshot in docs; see service lineage below*

### Write
- `jobs` — *no `tables/jobs.sql` snapshot in docs; see service lineage below*
- `scheduler_jobs` → [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql)
- `job_events` — *no `tables/job_events.sql` snapshot in docs; see service lineage below*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [Connectra (search / VQL)](../database/connectra_data_lineage.md)
- [S3 Storage](../database/s3storage_data_lineage.md)
- [TKD Jobs](../database/jobs_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`contact360.io/sync`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`contact360.io/jobs`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`lambda/s3storage`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_export_linkedin_results_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
