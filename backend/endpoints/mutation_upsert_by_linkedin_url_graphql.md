---
title: "graphql/UpsertByLinkedInUrl"
source_json: mutation_upsert_by_linkedin_url_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpsertByLinkedInUrl

## Overview

Create or update a contact and/or company by LinkedIn URL. Accepts LinkedInUpsertInput with url (required), and optional contactData, contactMetadata, companyData, companyMetadata. Supports partial data for both contact and company. Returns LinkedInUpsertResponse with success, created flag, contact (ContactWithRelations), company (CompanyWithRelations), and errors array. Credits: 1 credit per upsert operation (FreeUser/ProUser only).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_upsert_by_linkedin_url_graphql |
| _id | mutation_upsert_by_linkedin_url_graphql-001 |
| endpoint_path | graphql/UpsertByLinkedInUrl |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
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
| service_file | contact360.io/api/app/graphql/modules/linkedin/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/linkedinService.ts |


## GraphQL operation

```graphql
mutation UpsertByLinkedInUrl($input: LinkedInUpsertInput!) { linkedin { upsertByLinkedInUrl(input: $input) { success created contact { id firstName lastName email } company { id name } errors } } }
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

- backend(dev)/salesnavigator
- contact360.io/sync

## Service / repository methods

### service_methods

- upsertByLinkedInUrl

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /linkedin | Linkedin Page | linkedinService | useLinkedIn | primary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


### frontend_page_bindings

- contact360.io/app/app/(dashboard)/linkedin/page.tsx
- contact360.io/app/src/services/graphql/linkedinService.ts
- contact360.io/app/src/hooks/useLinkedIn.ts

## Inventory

- **page_count:** 1
- **Source:** `mutation_upsert_by_linkedin_url_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Contact AI (LinkedIn Sync).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `contacts` | READ/WRITE | [contacts.sql](../database/tables/contacts.sql) |
| `companies` | READ/WRITE | [companies.sql](../database/tables/companies.sql) |
| `contacts_index` | WRITE | [contacts_index.sql](../database/tables/contacts_index.sql) |
| `companies_index` | WRITE | [companies_index.sql](../database/tables/companies_index.sql) |
| `filters_data` | WRITE | [filters_data.sql](../database/tables/filters_data.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Connectra (Search/VQL)](../database/connectra_data_lineage.md)
- [Sales Navigator Service](../database/salesnavigator_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sales Navigator**: Data enrichment via `backend(dev)/salesnavigator`.
- **Sync**: Elastic/Search indexing via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Linkedin Page` (Upsert Action).
- **Outbound**: `GetContact`, `GetCompany`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_upsert_by_linkedin_url_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
