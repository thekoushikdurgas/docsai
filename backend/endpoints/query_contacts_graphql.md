---
title: "graphql/QueryContacts"
source_json: query_contacts_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/QueryContacts

## Overview

Query contacts using VQL (Vivek Query Language) with filtering, pagination, and sorting. Supports complex nested AND/OR filter logic and field selection.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_contacts_graphql |
| _id | query_contacts_graphql-001 |
| endpoint_path | graphql/QueryContacts |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 3.x.x |
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
| service_file | contact360.io/api/app/graphql/modules/contacts/queries.py |
| router_file | contact360/dashboard/src/services/graphql/contactsService.ts |


## GraphQL operation

```graphql
query QueryContacts($input: VQLQueryInput) { contacts { contacts(input: $input) { items { id uuid firstName lastName email companyId } total limit offset hasNext } } }
```

## Data & infrastructure

### db_tables_read

- contacts
- companies
- filters
- filters_data
- contacts_index

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- queryContacts

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | contactsService | useContactsPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/contacts_page.json
- contact360.io/app/app/(dashboard)/contacts/page.tsx
- contact360.io/app/src/hooks/contacts/useContactsPage.ts

## Inventory

- **page_count:** 1
- **Source:** `query_contacts_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x – 10.x)

- **Lifecycle `era` (metadata):** `3.x.x` — Contact & Company Data System.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `contacts` | READ | [contacts.sql](../database/tables/contacts.sql) |
| `companies` | READ | [companies.sql](../database/tables/companies.sql) |
| `tags` | READ | [tags.sql](../database/tables/tags.sql) |
| `contact_tags` | READ | [contact_tags.sql](../database/tables/contact_tags.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Linked to `contact360.io/sync` for real-time indexing.

## Related endpoint graph

- **Inbound**: `Contacts Page`.
- **Outbound**: `GetContact`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_contacts_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
