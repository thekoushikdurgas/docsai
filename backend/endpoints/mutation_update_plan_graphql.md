---
title: "graphql/UpdatePlan"
source_json: mutation_update_plan_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdatePlan

## Overview

Update an existing subscription plan. Accepts tier (String!, required) and UpdatePlanInput with optional fields: name (String), category (String - STARTER, PROFESSIONAL, BUSINESS, ENTERPRISE), isActive (Boolean). Returns object with message and tier. SuperAdmin only. Only provided fields are updated (partial update).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_plan_graphql |
| _id | mutation_update_plan_graphql-001 |
| endpoint_path | graphql/UpdatePlan |
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
| service_file | contact360.io/api/app/graphql/modules/billing/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/billingService.ts |


## Service / repository methods

### service_methods

- updatePlan

## Inventory

- **page_count:** 0
- **Source:** `mutation_update_plan_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing (Plan Management).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `plans` | WRITE | [plans.sql](../database/tables/plans.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Propagation**: Changes in plans affect `GetPlans` and `GetAdminPlans` immediately.

## Related endpoint graph

- **Inbound**: `Admin Plans Page`.
- **Outbound**: `GetAdminPlans` (refresh).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_plan_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
