---
title: "graphql/GetContact"
source_json: get_contact_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetContact

## Overview

Get a single contact by UUID. Accepts uuid (ID!, required, valid UUID format). Returns Contact object with full details including id, firstName, lastName, email, phone, jobTitle, company information (id, name, domain, industry), contact metadata (linkedin_url, twitter_url), and social links. Uses Connectra service for data retrieval. Raises NotFoundError (404) if contact doesn't exist.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_contact_graphql |
| _id | get_contact_graphql-001 |
| endpoint_path | graphql/GetContact |
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
query GetContact($uuid: ID!) { contacts { contact(uuid: $uuid) { id firstName lastName email phone jobTitle company { id name domain } } } }
```

## Data & infrastructure

### db_tables_read

- contacts
- companies
- contacts_index

### lambda_services

- contact360.io/sync

## Service / repository methods

### service_methods

- contact

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | contactsService | useContactDetail | secondary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


### frontend_page_bindings

- docs/frontend/pages/contacts_page.json
- contact360.io/app/app/(dashboard)/contacts/page.tsx
- contact360.io/app/src/services/graphql/contactsService.ts

## Inventory

- **page_count:** 1
- **Source:** `get_contact_graphql.json`

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

- **Sync**: Real-time retrieval from `contact360.io/sync` endpoint.

## Related endpoint graph

- **Inbound**: `Contacts Page` (Search Result).
- **Outbound**: `UpdateContact`.

<!-- AUTO:db-graph:end -->
---

*Generated from `get_contact_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
