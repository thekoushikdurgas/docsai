---
title: "graphql/GetActivities"
source_json: get_activities_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetActivities

## Overview

Get user activities with filtering, pagination, and sorting. Accepts optional ActivityFilterInput with serviceType (enum: export, import, auth, email, contact, company, search, ai), actionType (enum: create, update, delete, export, import, login, logout, search, find), status (enum: success, failure, pending), startDate/endDate (DateTime range), limit (Int, default 100), offset (Int, default 0). Returns ActivityConnection with items (array of Activity with id, serviceType, actionType, status, metadata, createdAt), total, limit, offset, hasNext, hasPrevious. User isolation enforced.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_activities_graphql |
| _id | get_activities_graphql-001 |
| endpoint_path | graphql/GetActivities |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-19T12:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limit | 100 requests/minute |
| rate_limited | True |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/activities/queries.py |
| router_file | contact360/dashboard/src/services/graphql/activitiesService.ts |


## GraphQL operation

```graphql
query GetActivities($input: ActivityFilterInput) { activities { activities(input: $input) { items { id serviceType actionType status metadata createdAt } total hasNext } } }
```

## Service / repository methods

### service_methods

- activities

### repository_methods

- get_activities_by_user

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /activities | Activities Page | activitiesService | useActivitiesPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /dashboard | Dashboard Page | activitiesService | useDashboardPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /verifier | Verifier Page | activitiesService | useVerifier | secondary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 3
- **Source:** `get_activities_graphql.json`

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

*Generated from `get_activities_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
