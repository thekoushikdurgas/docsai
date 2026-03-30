---
title: "graphql/GetHealth"
source_json: query_get_health_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetHealth

## Overview

Get API health status. No input required. Returns HealthStatus with status (String: 'healthy', 'degraded', 'unhealthy'), timestamp (DateTime), uptime (Float, seconds), version (String), services (array of ServiceHealth with name, status, latency, lastChecked). Checks database connectivity, S3 availability, and external service health. Public endpoint - no authentication required. Also available as REST endpoint at /health.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_health_graphql |
| _id | query_get_health_graphql-001 |
| endpoint_path | graphql/GetHealth |
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
| service_file | contact360.io/api/app/graphql/modules/health/queries.py |
| router_file | contact360/dashboard/src/services/graphql/healthService.ts |


## GraphQL operation

```graphql
query GetHealth { health { apiHealth { status timestamp uptime version services { name status latency } } } }
```

## Service / repository methods

### service_methods

- apiHealth

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/system-status | Admin System Status Page | healthService | useSystemStatus | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_health_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `6.x` — Observability (Ops).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `system_health` | READ | [system_health.sql](../database/tables/system_health.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Infrastructure Connectivity](../database/service_topology.md)

## Downstream services (cross-endpoint)

- **S3Storage**: Health check via `lambda/s3storage`.
- **Logs API**: Health check via `lambda/logs.api`.

## Related endpoint graph

- **Inbound**: `Admin System Status Page`.
- **Outbound**: `GetAPIMetadata`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_health_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
