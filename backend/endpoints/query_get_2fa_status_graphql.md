---
title: "graphql/Get2FAStatus"
source_json: query_get_2fa_status_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/Get2FAStatus

## Overview

Get 2FA status for the current user. Returns whether 2FA is enabled and setup completion status. This is used by the frontend to determine if the user should be prompted to set up 2FA or if they can manage their existing settings.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_2fa_status_graphql |
| _id | query_get_2fa_status_graphql-001 |
| endpoint_path | graphql/Get2FAStatus |
| method | QUERY |
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
| service_file | contact360.io/api/app/graphql/modules/two_factor/queries.py |
| router_file | contact360/dashboard/src/services/graphql/twoFactorService.ts |

## Service / repository methods

### service_methods

- get2FAStatus

## Inventory

- **page_count:** 1
- **Source:** `query_get_2fa_status_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Security).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `two_factor` | READ | [two_factor.sql](../database/tables/two_factor.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Security Auditing**: None (read-only status).

## Related endpoint graph

- **Inbound**: `Profile Page` (Frontend), `Settings Page`.
- **Outbound**: `Setup2FA` (if disabled).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_2fa_status_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
