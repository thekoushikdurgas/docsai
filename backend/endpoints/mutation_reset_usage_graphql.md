---
title: "graphql/ResetUsage"
source_json: mutation_reset_usage_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ResetUsage

## Overview

Reset usage counter for a specific feature to zero. Accepts ResetUsageInput with featureKey (required, String, max 100 chars, valid feature: email_finder, email_verifier, ai_chat, export, linkedin_search). Returns ResetUsageResponse with featureKey (String), used (Int, 0 after reset), limit (Int), success (Boolean). Auto-creates usage record if doesn't exist. Raises ForbiddenError (403) if not Admin. Raises ValidationError (422) if invalid feature key.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_reset_usage_graphql |
| _id | mutation_reset_usage_graphql-001 |
| endpoint_path | graphql/ResetUsage |
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


## GraphQL operation

```graphql
mutation ResetUsage($input: ResetUsageInput!) { usage { resetUsage(input: $input) { featureKey used limit success } } }
```

## Service / repository methods

### service_methods

- resetUsage

### repository_methods

- reset_feature_usage

## Inventory

- **page_count:** 0
- **Source:** `mutation_reset_usage_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing (Usage Caps).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_usage` | WRITE | [user_usage.sql](../database/tables/user_usage.sql) |
| `users` | READ | [users.sql](../database/tables/users.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Enforcement**: Blocks feature access in `Contact Search`, `Email Finder`, etc.

## Related endpoint graph

- **Inbound**: `Admin Dashboard`.
- **Outbound**: `GetUsage` (UI refresh).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_reset_usage_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
