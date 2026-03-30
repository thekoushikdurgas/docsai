---
title: "graphql/GenerateCompanySummary"
source_json: mutation_generate_company_summary_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GenerateCompanySummary

## Overview

Generate an AI-powered company summary. Accepts GenerateCompanySummaryInput with companyName (required, String, max 255 chars) and industry (required, String, max 255 chars). Returns CompanySummaryResponse with summary (String, comprehensive AI-generated company overview including business description, market position, key products/services, and industry context). Uses LambdaAIClient with Google Gemini AI. Activity logged (non-blocking). Raises ValidationError (422) if inputs exceed max length.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_generate_company_summary_graphql |
| _id | mutation_generate_company_summary_graphql-001 |
| endpoint_path | graphql/GenerateCompanySummary |
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
| service_file | contact360.io/api/app/graphql/modules/ai_chats/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/aiChatsService.ts |


## GraphQL operation

```graphql
mutation GenerateCompanySummary($input: GenerateCompanySummaryInput!) { aiChats { generateCompanySummary(input: $input) { summary } } }
```

## Service / repository methods

### service_methods

- generateCompanySummary

## Inventory

- **page_count:** 0
- **Source:** `mutation_generate_company_summary_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `4.x` — Contact AI (Enrichment).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `companies` | READ | [companies.sql](../database/tables/companies.sql) |
| `company_summaries` | WRITE | [company_summaries.sql](../database/tables/company_summaries.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Contact AI Service](../database/contact_ai_data_lineage.md)

## Downstream services (cross-endpoint)

- **Contact AI**: AI generation via `backend(dev)/contact.ai` (Gemini).

## Related endpoint graph

- **Inbound**: `Company Detail` (AI Summary Action).
- **Outbound**: `GetCompany`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_generate_company_summary_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
