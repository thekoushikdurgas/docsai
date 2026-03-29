---
title: "graphql/TrackUsage"
source_json: mutation_track_usage_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/TrackUsage

## Overview

Track feature usage for the current user. Accepts TrackUsageInput with feature (required, non-empty string, max 100 characters, must be valid feature name) and amount (non-negative integer, min: 1, max: 1,000,000, default: 1). Returns TrackUsageResponse with feature, used, limit, and success. Increments usage count for the specified feature. Usage records are auto-created if they don't exist. Limits are updated if user role changed. Usage is capped at the limit (won't exceed limit). Unlimited features (limit is None or 0) keep used count at 0. Role-based limits: Limits are determined by user role (FREE_USER vs PRO_USER). Silently fails for analytics (no toast shown).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_track_usage_graphql |
| _id | mutation_track_usage_graphql-001 |
| endpoint_path | graphql/TrackUsage |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 1.x |
| introduced_in | 1.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/usage/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/usageService.ts |


## Service / repository methods

### service_methods

- trackUsage

## Inventory

- **page_count:** 0
- **Source:** `mutation_track_usage_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing (Usage Tracking).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_usage` | WRITE | [user_usage.sql](../database/tables/user_usage.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Enforcement**: Increments counters that are read by `GetUsage`.

## Related endpoint graph

- **Inbound**: `Core App (automated)`.
- **Outbound**: `GetUsage` (state check).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_track_usage_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
