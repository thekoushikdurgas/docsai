---
title: "graphql/syncContacts"
source_json: mutation_sync_integration.json
generator: json_to_markdown_endpoints.py
---

# graphql/syncContacts

## Overview

syncContacts operation for backend docs expansion.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_sync_integration |
| _id | mutation_sync_integration-001 |
| endpoint_path | graphql/syncContacts |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | planned |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-03-24T00:00:00.000000+00:00 |
| updated_at | 2026-03-24T00:00:00.000000+00:00 |
| era | 8.x |
| introduced_in | 8.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/integrations/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/integrationService.ts |


## GraphQL operation

```graphql
mutation SyncContacts($input: SyncContactsInput!) { integrations { syncContacts(input: $input) { success syncedCount failedCount errors } } }
```

## Data & infrastructure

### db_tables_read

- contacts
- companies

### db_tables_write

- contacts
- companies
- contacts_index
- companies_index
- filters_data

### lambda_services

- contact360.io/sync
- backend(dev)/salesnavigator

## Service / repository methods

### service_methods

- syncContacts

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /integrations | Integrations Page | integrationService | useIntegrations | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/integrations/page.tsx
- contact360.io/app/src/services/graphql/integrationService.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_sync_integration.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `8.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `contacts` — *no `tables/contacts.sql` snapshot in docs; see service lineage below*
- `companies` — *no `tables/companies.sql` snapshot in docs; see service lineage below*

### Write
- `contacts` — *no `tables/contacts.sql` snapshot in docs; see service lineage below*
- `companies` — *no `tables/companies.sql` snapshot in docs; see service lineage below*
- `contacts_index` — *no `tables/contacts_index.sql` snapshot in docs; see service lineage below*
- `companies_index` — *no `tables/companies_index.sql` snapshot in docs; see service lineage below*
- `filters_data` — *no `tables/filters_data.sql` snapshot in docs; see service lineage below*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [Connectra (search / VQL)](../database/connectra_data_lineage.md)
- [Sales Navigator](../database/salesnavigator_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`contact360.io/sync`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`backend(dev)/salesnavigator`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_sync_integration.json`. Re-run `python json_to_markdown_endpoints.py`.*
