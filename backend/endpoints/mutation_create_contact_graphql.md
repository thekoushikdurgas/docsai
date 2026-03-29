---
title: "graphql/CreateContact"
source_json: mutation_create_contact_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateContact

## Overview

Create a new contact. Accepts CreateContactInput with first_name, last_name, company_uuid, email, title, departments, mobile_phone, email_status, seniority, status, text_search (all optional). Uses ConnectraClient to create contact via Connectra service. Returns Contact with id, firstName, lastName, email, jobTitle, company. Requires authentication. Activity logged (non-blocking). Raises BadRequestError/ValidationError on invalid input.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_contact_graphql |
| _id | mutation_create_contact_graphql-001 |
| endpoint_path | graphql/CreateContact |
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
mutation CreateContact($input: CreateContactInput!) { contacts { createContact(input: $input) { id firstName lastName email jobTitle company { id name } } } }
```

## Data & infrastructure

### db_tables_read

- companies
- filters

### db_tables_write

- contacts
- contacts_index
- filters_data

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- createContact

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
- **Source:** `mutation_create_contact_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x – 10.x)

- **Lifecycle `era` (metadata):** `3.x.x` — Contact & Company Data System.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `contacts` | WRITE | [contacts.sql](../database/tables/contacts.sql) |
| `companies` | READ | [companies.sql](../database/tables/companies.sql) |
| `tags` | READ | [tags.sql](../database/tables/tags.sql) |
| `contact_tags` | WRITE | [contact_tags.sql](../database/tables/contact_tags.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Triggers re-indexing in `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Contacts Page` (Add Contact Modal).
- **Outbound**: `GetContact`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_contact_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
