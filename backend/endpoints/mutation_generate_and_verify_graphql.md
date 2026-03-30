---
title: "graphql/GenerateAndVerify"
source_json: mutation_generate_and_verify_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GenerateAndVerify

## Overview

Generate email combinations and verify them. Accepts GenerateAndVerifyInput with firstName (required, String), lastName (required, String), domain (optional, String) OR website (optional, String) - at least one required, emailCount (optional, Int, 1-50, default 10), provider (optional, String). Generates email patterns (john.doe@, jdoe@, john_doe@, etc.) then verifies via Lambda Email service. Returns GenerateAndVerifyResponse with emails (array of {email, isValid, confidence}), total (Int), validCount (Int). Credits: 1 credit per search (FreeUser/ProUser only). Activity logged (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_generate_and_verify_graphql |
| _id | mutation_generate_and_verify_graphql-001 |
| endpoint_path | graphql/GenerateAndVerify |
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
| service_file | appointment360/app/graphql/modules/email/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/emailService.ts |


## GraphQL operation

```graphql
mutation GenerateAndVerify($input: GenerateAndVerifyInput!) { email { generateAndVerify(input: $input) { emails { email isValid confidence } total validCount } } }
```

## Service / repository methods

### service_methods

- generateAndVerify

## Inventory

- **page_count:** 0
- **Source:** `mutation_generate_and_verify_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

- *No `db_tables_read` / `db_tables_write` in this spec — gateway-only or metadata TBD; see lineage.*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_generate_and_verify_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
