---
title: "graphql/GetContactFilters"
source_json: get_contact_filters_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetContactFilters

## Overview

Get filter definitions available for contact filtering. No input required. Returns array of FilterDefinition with key (filter field name), type (data type: string, number, boolean, date, enum), label (display label), displayName (human-readable name), operators (supported filter operators), options (for enum types, array of valid values), isDerived (whether filter is computed), isActive (whether filter is enabled). Used by frontend filter builder UI.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_contact_filters_graphql |
| _id | get_contact_filters_graphql-001 |
| endpoint_path | graphql/GetContactFilters |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-19T12:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 2.x |
| introduced_in | 2.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/contacts/queries.py |
| router_file | contact360/dashboard/src/services/graphql/contactsService.ts |


## GraphQL operation

```graphql
query GetContactFilters { contacts { contactFilters { key type label displayName operators options isDerived isActive } } }
```

## Data & infrastructure

### db_tables_read

- filters
- filters_data

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- contactFilters

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | contactsService | useContactsFilters | primary | filter_builder | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/contacts_page.json
- contact360.io/app/app/(dashboard)/contacts/page.tsx
- contact360.io/app/src/hooks/contacts/useContactsFilters.ts

## Inventory

- **page_count:** 1
- **Source:** `get_contact_filters_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — Contact Foundation (Filters).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `filters` | READ | [filters.sql](../database/tables/filters.sql) |
| `filters_data` | READ | [filters_data.sql](../database/tables/filters_data.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Linked to `contact360.io/sync` for schema synchronization.

## Related endpoint graph

- **Inbound**: `Contacts Page` (Filter Sidebar).
- **Outbound**: `QueryContacts`.

<!-- AUTO:db-graph:end -->
---

*Generated from `get_contact_filters_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
