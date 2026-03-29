---
title: "graphql/RegenerateBackupCodes"
source_json: mutation_regenerate_backup_codes_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/RegenerateBackupCodes

## Overview

Regenerate backup codes for current user. No input required (uses current user from context). Invalidates all previous backup codes. Returns RegenerateBackupCodesResponse with backupCodes (array of 10 new single-use recovery codes). Codes are hashed before storage. Raises NotFoundError (404) if 2FA is not enabled. Important: New backup codes shown only once - user must store securely.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_regenerate_backup_codes_graphql |
| _id | mutation_regenerate_backup_codes_graphql-001 |
| endpoint_path | graphql/RegenerateBackupCodes |
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
mutation RegenerateBackupCodes { twoFactor { regenerateBackupCodes { backupCodes } } }
```

## Service / repository methods

### service_methods

- regenerateBackupCodes

## Inventory

- **page_count:** 0
- **Source:** `mutation_regenerate_backup_codes_graphql.json`

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

- **Security Auditing**: Logs backup code regeneration event.

## Related endpoint graph

- **Inbound**: `Profile Page` (Frontend), `TwoFactor Setup`.
- **Outbound**: `Verify2FA` (to confirm persistence).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_regenerate_backup_codes_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
