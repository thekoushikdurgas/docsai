---
title: "graphql/SearchLinkedIn"
source_json: mutation_search_linkedin_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/SearchLinkedIn

## Overview

Search LinkedIn profiles and extract contact data. Accepts SearchLinkedInInput with profileUrl (optional, String, valid LinkedIn URL) OR keywords (optional, String), firstName (optional, String), lastName (optional, String), companyName (optional, String), limit (optional, Int, default 10, max 100). Returns LinkedInSearchResponse with profiles (array of LinkedInProfile with profileUrl, firstName, lastName, headline, company, location, connectionDegree), total count. Credits: 1 credit per search. Activity logged (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_search_linkedin_graphql |
| _id | mutation_search_linkedin_graphql-001 |
| endpoint_path | graphql/SearchLinkedIn |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
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
mutation SearchLinkedIn($input: SearchLinkedInInput!) { linkedin { searchLinkedIn(input: $input) { profiles { profileUrl firstName lastName headline company } total } } }
```

## Data & infrastructure

### db_tables_read

- contacts
- companies
- contacts_index
- companies_index

### lambda_services

- backend(dev)/salesnavigator
- contact360.io/sync

## Service / repository methods

### service_methods

- searchLinkedIn

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
- **Source:** `mutation_search_linkedin_graphql.json`

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
- *None listed in JSON metadata*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)
- [Connectra (search / VQL)](../database/connectra_data_lineage.md)
- [Sales Navigator](../database/salesnavigator_data_lineage.md)

## Downstream services (cross-endpoint)

- Delegates to **`backend(dev)/salesnavigator`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.
- Delegates to **`contact360.io/sync`** — see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) and that service’s era matrix JSON / `*_endpoint_era_matrix.md`.

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_search_linkedin_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
