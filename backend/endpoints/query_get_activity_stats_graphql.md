---
title: "graphql/GetActivityStats"
source_json: query_get_activity_stats_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetActivityStats

## Overview

Get activity statistics for a time range. Returns counts by service type, action type, and status.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_activity_stats_graphql |
| _id | query_get_activity_stats_graphql-001 |
| endpoint_path | graphql/GetActivityStats |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 6.x |
| introduced_in | 6.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/activities/queries.py |
| router_file | contact360/dashboard/src/services/graphql/activitiesService.ts |


## Service / repository methods

### service_methods

- getActivityStats
- activityStats

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /activities | Activities Page | activitiesService | useActivitiesPage | primary | analytics | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_activity_stats_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `6.x` — Observability (Activity Stats).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `activity_logs` | READ | [activity_logs.sql](../database/tables/activity_logs.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Logs API Service](../database/logsapi_data_lineage.md)

## Downstream services (cross-endpoint)

- **Logs API**: Activity data aggregation via `lambda/logs.api`.

## Related endpoint graph

- **Inbound**: `Activities Page`.
- **Outbound**: `GetActivities`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_activity_stats_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
