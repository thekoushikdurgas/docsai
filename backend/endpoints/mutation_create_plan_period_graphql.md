---
title: "graphql/CreatePlanPeriod"
source_json: mutation_create_plan_period_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreatePlanPeriod

## Overview

Create or update a plan period. Accepts CreatePlanPeriodInput with tier (required, String, existing plan tier), period (required, enum: monthly, quarterly, yearly), credits (required, Int), ratePerCredit (required, Float), price (required, Float), savingsAmount (optional, Float), savingsPercentage (optional, Int). Creates new period or updates existing. Returns CreatePlanPeriodResponse with message (String), tier (String), period (String). Raises NotFoundError (404) if plan tier not found. Raises ForbiddenError (403) if not SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_plan_period_graphql |
| _id | mutation_create_plan_period_graphql-001 |
| endpoint_path | graphql/CreatePlanPeriod |
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
| service_file | appointment360/app/graphql/modules/billing/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/billingService.ts |


## GraphQL operation

```graphql
mutation CreatePlanPeriod($input: CreatePlanPeriodInput!) { billing { createPlanPeriod(input: $input) { message tier period } } }
```

## Service / repository methods

### service_methods

- createPlanPeriod

### repository_methods

- create_plan_period

## Inventory

- **page_count:** 0
- **Source:** `mutation_create_plan_period_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation & Pre-Product Stabilization (Billing bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `subscription_plans` | READ | [subscription_plans.sql](../database/tables/subscription_plans.sql) |
| `subscription_plan_periods` | WRITE | [subscription_plan_periods.sql](../database/tables/subscription_plan_periods.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Direct insert/upsert into `subscription_plan_periods` via BillingRepository. No downstream service calls.

## Related endpoint graph

- **Inbound**: `Admin Billing Page` (Frontend SuperAdmin).
- **Outbound**: `GetPlans` (verify new period), `GetAdminPlans` (admin listing).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_plan_period_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
