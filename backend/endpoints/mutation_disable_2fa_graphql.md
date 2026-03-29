---
title: "graphql/Disable2FA"
source_json: mutation_disable_2fa_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/Disable2FA

## Overview

Disable 2FA for the current user. Returns success status. Once disabled, the user will no longer be prompted for a TOTP code during login. This action requires the user to be authenticated.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_disable_2fa_graphql |
| _id | mutation_disable_2fa_graphql-001 |
| endpoint_path | graphql/Disable2FA |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |

## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.4.0 |

## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | True |

## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/two_factor/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/twoFactorService.ts |

## GraphQL operation

```graphql
mutation Disable2FA { twoFactor { disable2FA } }
```

## Service / repository methods

### service_methods

- disable2FA

## Inventory

- **page_count:** 1
- **Source:** `mutation_disable_2fa_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Security).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `two_factor` | WRITE | [two_factor.sql](../database/tables/two_factor.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Security Auditing**: Logs 2FA disable event with user metadata.

## Related endpoint graph

- **Inbound**: `Profile Page` (Frontend), `Settings Page`.
- **Outbound**: `AuthContext` (refresh).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_disable_2fa_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
