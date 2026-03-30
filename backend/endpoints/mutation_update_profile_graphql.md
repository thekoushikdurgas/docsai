---
title: "graphql/UpdateProfile"
source_json: mutation_update_profile_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdateProfile

## Overview

Update current user's profile. Accepts UpdateProfileInput with jobTitle (optional, max 255 characters), bio (optional, max 1000 characters), timezone (optional, max 100 characters), and notifications (optional, valid JSON object). Returns updated UserProfile with userId, jobTitle, bio, timezone, role, credits, subscriptionPlan, subscriptionStatus, avatarUrl, createdAt, updatedAt. Profile updates are atomic with transaction rollback on failure. Raises ValidationError (422) if field validation fails.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_profile_graphql |
| _id | mutation_update_profile_graphql-001 |
| endpoint_path | graphql/UpdateProfile |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 1.x |
| introduced_in | 1.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/profile/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/usersService.ts |


## GraphQL operation

```graphql
mutation UpdateProfile($input: UpdateProfileInput!) { users { updateProfile(input: $input) { userId jobTitle bio timezone role credits } } }
```

## Service / repository methods

### service_methods

- updateProfile

### repository_methods

- update_profile

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | usersService | useUserProfile | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_update_profile_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — User / Identity system.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | WRITE | [users.sql](../database/tables/users.sql) |
| `user_profiles` | WRITE | [user_profiles.sql](../database/tables/user_profiles.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Avatar Storage**: Updates `avatarUrl` via `s3storage` Lambda integration.

## Related endpoint graph

- **Inbound**: `Profile Page` (Frontend), `Settings Page`.
- **Outbound**: `GetMe` (refresh).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_profile_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
