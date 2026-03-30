---
title: "graphql/CreatePlan"
source_json: mutation_create_plan_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreatePlan

## Overview

Create a new subscription plan. Accepts CreatePlanInput with tier (required, String, unique identifier), name (required, String), category (required, enum: STARTER, PROFESSIONAL, BUSINESS, ENTERPRISE), periods (required, array of PlanPeriodInput with periodType: monthly/yearly, price, credits), isActive (optional, Boolean, default true). Returns CreatePlanResponse with message (String), tier (String). Raises ConflictError (409) if tier already exists. Raises ForbiddenError (403) if not SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_plan_graphql |
| _id | mutation_create_plan_graphql-001 |
| endpoint_path | graphql/CreatePlan |
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


## GraphQL operation

```graphql
mutation CreatePlan($input: CreatePlanInput!) { billing { createPlan(input: $input) { message tier } } }
```

## Service / repository methods

### service_methods

- createPlan

### repository_methods

- create_plan

## Inventory

- **page_count:** 0
- **Source:** `mutation_create_plan_graphql.json`

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

*Generated from `mutation_create_plan_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
