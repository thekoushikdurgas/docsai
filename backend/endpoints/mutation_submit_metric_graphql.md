---
title: "graphql/SubmitMetric"
source_json: mutation_submit_metric_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/SubmitMetric

## Overview

Submit a single performance metric. Accepts SubmitMetricInput with metricType (required, enum: page_load, api_call, render_time, memory_usage), name (required, String), value (required, Float), unit (optional, String: ms, bytes, etc.), metadata (optional, JSON). Returns SubmitMetricResponse with success (Boolean), message (String). Typically called automatically by frontend performance monitor. Stored via Lambda Logs API for analytics dashboards.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_submit_metric_graphql |
| _id | mutation_submit_metric_graphql-001 |
| endpoint_path | graphql/SubmitMetric |
| method | MUTATION |
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
| service_file | contact360.io/api/app/graphql/modules/analytics/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/analyticsService.ts |


## GraphQL operation

```graphql
mutation SubmitMetric($input: SubmitMetricInput!) { analytics { submitMetric(input: $input) { success message } } }
```

## Service / repository methods

### service_methods

- submitMetric

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /analytics | Analytics Page | analyticsService | useAnalyticsPage | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_submit_metric_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `6.x` — Observability (Metrics Submission).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `performance_metrics` | WRITE | [performance_metrics.sql](../database/tables/performance_metrics.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Logs API Service](../database/logs_api_data_lineage.md)

## Downstream services (cross-endpoint)

- **LogsAPI**: Metric persistence via `lambda/logs.api`.

## Related endpoint graph

- **Inbound**: `Frontend Performance Monitor`.
- **Outbound**: `GetPerformanceMetrics`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_submit_metric_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
