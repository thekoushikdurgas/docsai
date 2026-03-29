---
title: "graphql/Setup2FA"
source_json: mutation_setup_2fa_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/Setup2FA

## Overview

Setup 2FA for user account. No input required. Generates TOTP secret and backup codes. Returns Setup2FAResponse with qrCodeDataUrl (String, base64 data URL for QR code), secret (String, TOTP secret for manual entry), backupCodes (array of String, 10 single-use recovery codes). QR code is for authenticator apps (Google Authenticator, Authy). User must verify 2FA with mutation Verify2FA to complete setup. Raises ConflictError (409) if 2FA already enabled.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_setup_2fa_graphql |
| _id | mutation_setup_2fa_graphql-001 |
| endpoint_path | graphql/Setup2FA |
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
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/two_factor/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/twoFactorService.ts |


## GraphQL operation

```graphql
mutation Setup2FA { twoFactor { setup2FA { qrCodeDataUrl secret backupCodes } } }
```

## Service / repository methods

### service_methods

- setup2FA

### repository_methods

- update_user_2fa

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | twoFactorService | use2FA | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_setup_2fa_graphql.json`

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

- **Security Auditing**: Logs 2FA configuration events.

## Related endpoint graph

- **Inbound**: `Profile Page` (Frontend), `Settings Page`.
- **Outbound**: `Verify2FA` (to complete flow).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_setup_2fa_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
