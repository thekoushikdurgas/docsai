---
title: "graphql/Verify2FA"
source_json: mutation_verify_2fa_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/Verify2FA

## Overview

Verify and enable 2FA for user account. Accepts Verify2FAInput with code (required, 6-digit TOTP code) and optional backupCode (String). Returns Boolean (true on success). Validates the provided code against the TOTP secret generated during Setup2FA. Once verified, 2FA is marked as enabled for the user. Raises ValidationError (422) if code is invalid or expired.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_verify_2fa_graphql |
| _id | mutation_verify_2fa_graphql-001 |
| endpoint_path | graphql/Verify2FA |
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
mutation Verify2FA($input: Verify2FAInput!) { twoFactor { verify2FA(input: $input) } }
```

## Service / repository methods

### service_methods

- verify2FA

## Inventory

- **page_count:** 1
- **Source:** `mutation_verify_2fa_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Security).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `two_factor` | READ / WRITE | [two_factor.sql](../database/tables/two_factor.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Security Auditing**: Logs 2FA verification success/failure.

## Related endpoint graph

- **Inbound**: `Setup2FA` (pre-requisite).
- **Outbound**: `AuthContext` (refresh).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_verify_2fa_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
