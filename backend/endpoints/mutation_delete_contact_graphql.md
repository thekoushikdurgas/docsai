---
title: "graphql/DeleteContact"
source_json: mutation_delete_contact_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteContact

## Overview

Delete a contact by UUID. Accepts uuid (ID!, required, valid UUID format). Uses ConnectraClient; note Connectra may not support hard delete (implementation may return not supported). Returns Boolean indicating success. Requires authentication. Raises NotFoundError (404) if contact not found. Activity logged (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_contact_graphql |
| _id | mutation_delete_contact_graphql-001 |
| endpoint_path | graphql/DeleteContact |
| method | MUTATION |
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
| service_file | contact360.io/api/app/graphql/modules/contacts/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/contactsService.ts |


## GraphQL operation

```graphql
mutation DeleteContact($uuid: ID!) { contacts { deleteContact(uuid: $uuid) } }
```

## Data & infrastructure

### db_tables_read

- contacts
- contacts_index

### db_tables_write

- contacts
- contacts_index
- filters_data

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- deleteContact

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | contactsService | useContactsModals | secondary | data_mutation | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/contacts_page.json
- contact360.io/app/app/(dashboard)/contacts/page.tsx
- contact360.io/app/src/services/graphql/contactsService.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_delete_contact_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x – 10.x)

- **Lifecycle `era` (metadata):** `3.x.x` — Contact & Company Data System.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `contacts` | WRITE | [contacts.sql](../database/tables/contacts.sql) |
| `contact_tags` | WRITE | [contact_tags.sql](../database/tables/contact_tags.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Triggers record removal in Connectra search index via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Contact Detail` (Delete Action).
- **Outbound**: `QueryContacts`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_contact_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
