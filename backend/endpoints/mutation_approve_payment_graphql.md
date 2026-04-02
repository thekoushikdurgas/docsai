---
title: "graphql/ApprovePayment"
source_json: mutation_approve_payment_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ApprovePayment

## Overview

Approve a pending payment submission and credit the user account.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_approve_payment_graphql |
| _id | mutation_approve_payment_graphql-001 |
| endpoint_path | graphql/ApprovePayment |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |

## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-04-01T00:00:00.000000+00:00 |
| updated_at | 2026-04-01T00:00:00.000000+00:00 |
| era | 1.x |
| introduced_in | 1.0.0 |

## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | admin, superadmin |
| rate_limited | False |

## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/billing/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |

## Service / repository methods

### service_methods

- approvePayment
- approve_submission

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — User & Billing & Credit System.

---

*Runtime parity anchor for high-risk operation `approvePayment`.*
