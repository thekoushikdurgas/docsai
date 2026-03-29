---
title: "graphql/VerifyAndFind"
source_json: mutation_verify_and_find_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/VerifyAndFind

## Overview

Verify and find the first valid email for a contact. Accepts VerifyAndFindInput with firstName, lastName, domain/website (either required), emailCount (1-50, default: 10), and optional provider. Generates email combinations, verifies them, and returns the first valid email. Returns VerifyAndFindResponse with email, status, and source. Credits: 1 credit per search (FreeUser/ProUser only).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_verify_and_find_graphql |
| _id | mutation_verify_and_find_graphql-001 |
| endpoint_path | graphql/VerifyAndFind |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 4.x |
| introduced_in | 4.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/email/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/emailService.ts |


## Service / repository methods

### service_methods

- verifyAndFind
- verifyexportEmail

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /app | Finder Page | emailService |  | secondary | data_mutation | 2025-01-27T12:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_verify_and_find_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Data Integrity (Verification).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `contacts` | READ/WRITE | [contacts.sql](../database/tables/contacts.sql) |
| `verification_logs` | WRITE | [verification_logs.sql](../database/tables/verification_logs.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [MailVetter Service](../database/mailvetter_data_lineage.md)

## Downstream services (cross-endpoint)

- **MailVetter**: Real-time SMTP/MX verification via `backend(dev)/mailvetter`.

## Related endpoint graph

- **Inbound**: `Finder Page` (Verification Action).
- **Outbound**: `UpdateContact` (save results).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_verify_and_find_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
