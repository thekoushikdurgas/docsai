---
title: "graphql/AggregateMetrics"
source_json: query_aggregate_metrics_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/AggregateMetrics

## Overview

Get aggregated statistics for a performance metric (avg, min, max, p50, p75, p95, count) for a given metric name and date range.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_aggregate_metrics_graphql |
| _id | query_aggregate_metrics_graphql-001 |
| endpoint_path | graphql/AggregateMetrics |
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
| service_file | contact360.io/api/app/graphql/modules/analytics/queries.py |
| router_file | contact360/dashboard/src/services/graphql/analyticsService.ts |


## Service / repository methods

### service_methods

- aggregateMetrics

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /analytics | Analytics Page | analyticsService | useAnalyticsPage | secondary | analytics | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_aggregate_metrics_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `6.x` — Observability (Aggregate Metrics).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `performance_metrics` | READ | [performance_metrics.sql](../database/tables/performance_metrics.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Logs API Service](../database/logsapi_data_lineage.md)

## Downstream services (cross-endpoint)

- **Logs API**: Performance data aggregation via `lambda/logs.api`.

## Related endpoint graph

- **Inbound**: `Analytics Page`.
- **Outbound**: `GetPerformanceMetrics`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_aggregate_metrics_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
