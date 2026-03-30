---
title: "graphql/AddEmailPatternBulk"
source_json: mutation_add_email_pattern_bulk_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/AddEmailPatternBulk

## Overview

Add multiple email patterns in one request. Delegates to Lambda Email runtime bulk pattern endpoint.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_add_email_pattern_bulk_graphql |
| _id | mutation_add_email_pattern_bulk_graphql-001 |
| endpoint_path | graphql/AddEmailPatternBulk |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-03-24T00:00:00.000000+00:00 |
| updated_at | 2026-03-24T00:00:00.000000+00:00 |
| era | 2.x |
| introduced_in | 2.0.0 |


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
| service_file | contact360.io/api/app/graphql/modules/email/mutations.py |
| router_file | contact360.io/app/src/services/graphql/emailService.ts |
| sql_file | docs/backend/apis/15_EMAIL_MODULE.md |


## GraphQL operation

```graphql
mutation AddEmailPatternBulk($input: AddEmailPatternBulkInput!) { email { addEmailPatternBulk(input: $input) { results { uuid companyUuid patternFormat patternString domain } success } } }
```

## Data & infrastructure

### db_tables_read

- email_patterns

### db_tables_write

- email_patterns

### lambda_services

- lambda/emailapis
- lambda/emailapigo

## Service / repository methods

### service_methods

- addEmailPatternBulk

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /email | Email Page | emailService.addEmailPatternBulk |  | secondary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/email_page.json

## Inventory

- **page_count:** 1
- **Source:** `mutation_add_email_pattern_bulk_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `email_patterns` — *no `tables/email_patterns.sql` snapshot in docs; see service lineage below*

### Write
- `email_patterns` — *no `tables/email_patterns.sql` snapshot in docs; see service lineage below*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [Email APIs](../database/emailapis_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`lambda/emailapis`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`lambda/emailapigo`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_add_email_pattern_bulk_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
