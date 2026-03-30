---
title: "graphql/ParseFilters"
source_json: mutation_parse_filters_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ParseFilters

## Overview

Parse natural language query into structured contact filters using AI. Accepts ParseFiltersInput with query (required, String, non-empty, max 1000 chars). Returns ParseFiltersResponse with jobTitles (array of String), companyNames (array of String), industry (array of String), location (array of String), employees (array of Int as [min, max] range), seniority (array of String). Example: 'Find CTOs at tech companies in San Francisco' -> {jobTitles: ['CTO'], industry: ['Technology'], location: ['San Francisco']}. Uses LambdaAIClient with Google Gemini AI.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_parse_filters_graphql |
| _id | mutation_parse_filters_graphql-001 |
| endpoint_path | graphql/ParseFilters |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/ai_chats/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/aiChatsService.ts |


## GraphQL operation

```graphql
mutation ParseFilters($input: ParseFiltersInput!) { aiChats { parseFilters(input: $input) { jobTitles companyNames industry location employees seniority } } }
```

## Service / repository methods

### service_methods

- parseFilters

## Inventory

- **page_count:** 0
- **Source:** `mutation_parse_filters_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

- *No `db_tables_read` / `db_tables_write` in this spec — gateway-only or metadata TBD; see lineage.*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_parse_filters_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
