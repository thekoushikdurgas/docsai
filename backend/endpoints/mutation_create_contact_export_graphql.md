---
title: "graphql/CreateContactExport"
source_json: mutation_create_contact_export_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateContactExport

## Overview

Create a CSV export of selected contacts. Accepts CreateContactExportInput with contactIds (required, array of UUID, max 10000). Creates export job via ConnectraClient. Returns ExportResponse with exportId (UUID), downloadUrl (presigned S3 URL, valid 24h), expiresAt (DateTime), contactCount (Int), status (enum: pending, processing, completed, failed). Credits: 1 credit per 100 contacts (FreeUser/ProUser only). UserExport record created (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_contact_export_graphql |
| _id | mutation_create_contact_export_graphql-001 |
| endpoint_path | graphql/CreateContactExport |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 3.x |
| introduced_in | 3.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/exports/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/exportsService.ts |


## GraphQL operation

```graphql
mutation CreateContactExport($input: CreateContactExportInput!) { exports { exportContacts(input: $input) { exportId downloadUrl expiresAt contactCount status } } }
```

## Data & infrastructure

### db_tables_read

- contacts
- contacts_index

### db_tables_write

- jobs
- scheduler_jobs

### lambda_services

- contact360.io/sync
- contact360.io/jobs
- lambda/s3storage

## Service / repository methods

### service_methods

- exportContacts

### repository_methods

- create_export

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | exportsService | useContactExport | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/contacts_page.json
- contact360.io/app/app/(dashboard)/contacts/page.tsx
- contact360.io/app/src/hooks/contacts/useContactExport.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_create_contact_export_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `3.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `contacts` — *no `tables/contacts.sql` snapshot in docs; see service lineage below*
- `contacts_index` — *no `tables/contacts_index.sql` snapshot in docs; see service lineage below*

### Write
- `jobs` — *no `tables/jobs.sql` snapshot in docs; see service lineage below*
- `scheduler_jobs` → [scheduler_jobs.sql](../database/tables/scheduler_jobs.sql)

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

*Generated from `mutation_create_contact_export_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
