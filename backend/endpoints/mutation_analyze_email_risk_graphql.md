---
title: "graphql/AnalyzeEmailRisk"
source_json: mutation_analyze_email_risk_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/AnalyzeEmailRisk

## Overview

Analyze email address for risk factors using AI. Accepts AnalyzeEmailRiskInput with email (required, valid email format, max 255 chars). Returns EmailRiskAnalysisResponse with riskScore (Int, 0-100, higher = higher risk), analysis (String, detailed explanation), isRoleBased (Boolean, true if role-based like info@, support@), isDisposable (Boolean, true if from disposable email service), domain (String), createdAt (DateTime). Uses LambdaAIClient with Google Gemini AI for analysis. Activity logged (non-blocking). Raises ValidationError (422) if email format invalid.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_analyze_email_risk_graphql |
| _id | mutation_analyze_email_risk_graphql-001 |
| endpoint_path | graphql/AnalyzeEmailRisk |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 2.x |
| introduced_in | 2.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/ai_chats/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/aiChatsService.ts |


## GraphQL operation

```graphql
mutation AnalyzeEmailRisk($input: AnalyzeEmailRiskInput!) { aiChats { analyzeEmailRisk(input: $input) { riskScore analysis isRoleBased isDisposable } } }
```

## Service / repository methods

### service_methods

- analyzeEmailRisk

## Inventory

- **page_count:** 0
- **Source:** `mutation_analyze_email_risk_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `2.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

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

*Generated from `mutation_analyze_email_risk_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
