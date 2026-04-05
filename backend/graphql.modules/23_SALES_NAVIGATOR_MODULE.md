# Sales Navigator Module

Sales Navigator ingestion and synchronization endpoints for profile capture and Connectra upsert.

## Operations (GraphQL gateway)

Paths: `query { salesNavigator { salesNavigatorRecords(filters: { limit, offset }) { ... } } }`, `mutation { salesNavigator { saveSalesNavigatorProfiles(input: { profiles: [...] }) { ... } } }`.

| Operation | Type | Parameters | Description |
| --- | --- | --- | --- |
| `salesNavigatorRecords` | Query | `filters`: `SalesNavigatorFilterInput` (optional; **pagination** `limit` / `offset` via input base) | Paginated **user scraping metadata** rows (`UserScrapingConnection`), not arbitrary Connectra VQL |
| `saveSalesNavigatorProfiles` | Mutation | `input`: `SaveProfilesInput!` (`profiles`: `[JSON!]!`, max 1000) | Proxies to Sales Navigator / Connectra save flow; returns `SaveProfilesResponse` |

There are **no** gateway fields named `getSyncStatus` or `listSyncJobs` in `app/graphql/modules/sales_navigator/` — remove those from client code or treat any doc references as **planned/future**.

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

```graphql
type SalesNavigatorQuery {
  salesNavigatorRecords(filters: SalesNavigatorFilterInput = null): UserScrapingConnection!
}

type SalesNavigatorMutation {
  saveSalesNavigatorProfiles(input: SaveProfilesInput!): SaveProfilesResponse!
}

input SalesNavigatorFilterInput {
  limit: Int = 100
  offset: Int = 0
}

input SaveProfilesInput {
  profiles: [JSON!]!
}
```

### POST `/graphql` — example

```json
{
  "query": "query ($filters: SalesNavigatorFilterInput) { salesNavigator { salesNavigatorRecords(filters: $filters) { items { id source createdAt } pageInfo { total limit offset } } } }",
  "variables": { "filters": { "limit": 20, "offset": 0 } }
}
```

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>`.

---

## Direct Sales Navigator REST contract (source service)

The GraphQL module proxies profile save operations to `backend(dev)/salesnavigator` (FastAPI Lambda). The canonical REST endpoints are:

### Endpoints

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/` | None | Service info |
| `GET` | `/v1/health` | None | Liveness check |
| `POST` | `/v1/scrape` | `X-API-Key` | Parse SN HTML; extract profiles; optionally save to Connectra |
| `POST` | `/v1/save-profiles` | `X-API-Key` | Save profile array to Connectra (bulk upsert) |

> **Docs drift notice:** `docs/api.md` in the service repo documents `POST /v1/scrape-html-with-fetch` — this endpoint is **NOT implemented** in the current codebase. Remove from docs or implement before `4.x` release.

### `POST /v1/save-profiles` request schema

```json
{
  "profiles": [
    {
      "name": "Jane Smith",
      "title": "VP Engineering",
      "company": "Acme Corp",
      "location": "San Francisco, CA, United States",
      "profile_url": "https://www.linkedin.com/sales/lead/ACw...",
      "company_url": "https://www.linkedin.com/sales/company/123",
      "connection_degree": "2nd"
    }
  ]
}
```

- Max 1000 profiles per request.
- `profile_url` is used as the deduplication key.

### `POST /v1/save-profiles` response schema

```json
{
  "success": true,
  "saved_count": 18,
  "contacts_created": 12,
  "contacts_updated": 6,
  "companies_created": 5,
  "companies_updated": 3,
  "errors": []
}
```

### Partial success

`success: true` with non-empty `errors[]` is valid. The response represents the profiles that were saved; `errors[]` contains the profiles that failed with reason.

---

## Field mapping (SN profile → Connectra contact)

| SN field | Contact field | Notes |
| --- | --- | --- |
| `name` (parsed) | `first_name`, `last_name` | Split on first space |
| `title` | `title` | Normalized |
| `title`, `about` | `seniority` | executive/director/manager/senior_ic/entry |
| `title`, `about` | `departments` | Keyword extraction |
| `location` | `city`, `state`, `country` | Comma split |
| `email` | `email` | Optional |
| `mobile_phone` | `mobile_phone` | Optional |
| `profile_url` | `linkedin_sales_url` | SN URL |
| (converted) | `linkedin_url` | Standard LinkedIn URL; may be `PLACEHOLDER_VALUE` |
| (deterministic) | `uuid` | UUID5 from `linkedin_url + email` |
| — | `source` | Always `"sales_navigator"` |
| — | `data_quality_score` | Completeness score (0–100) |
| — | `lead_id`, `search_id` | Extracted from SN URL context |

---

## UUID generation (deterministic, idempotent)

```
contact_uuid = uuid5(NAMESPACE_URL, linkedin_url + email)
company_uuid = uuid5(NAMESPACE_URL, company_name_normalized + company_url)
```

This makes re-ingestion of the same profile idempotent at Connectra level.

---

## Deduplication

Profiles within a batch are deduplicated by normalized `profile_url` before sending to Connectra. The most-complete profile (highest field count) is retained; optional array fields (skills, etc.) are merged from duplicates.

---

## Connectra calls (downstream)

| Method | Connectra path | Purpose |
| --- | --- | --- |
| `POST` | `/companies/bulk` | Bulk upsert companies |
| `POST` | `/contacts/bulk` | Bulk upsert contacts |

---

## Known gaps

- `POST /v1/scrape-html-with-fetch` documented in `docs/api.md` but NOT implemented — fix before 4.x.
- `README.md` incorrectly states scraping feature is removed — clarify.
- Single global `API_KEY` is intentional in `0.x` foundation; per-tenant scoping is a `7.x` governance deliverable.
- Rate limiting exists at the dependency layer with `RATE_LIMIT_REQUESTS_PER_MINUTE`; tune policy in `6.x`.
- CORS is environment-configured through `ALLOWED_ORIGINS`; avoid wildcard origins outside local development.
- `employees_count`, `industries`, `annual_revenue` always `null` for SN companies.
- `linkedin_url` may be `PLACEHOLDER_VALUE` when SN URL cannot be converted — dedup quality risk.

---

## Era binding

- This module is operationally relevant from `3.x` through `10.x` (primary era: `4.x`).
- Scaffold and health endpoint available from `0.x`.
- AI field quality requirements active from `5.x`.

---

## Maintenance references

- Era index: `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
- Data lineage: `docs/backend/database/salesnavigator_data_lineage.md`
- UI bindings: `docs/frontend/salesnavigator-ui-bindings.md`
- Endpoint matrix: `docs/backend/endpoints/salesnavigator_endpoint_era_matrix.json`
- Codebase analysis: `docs/codebases/salesnavigator-codebase-analysis.md`

---

## Documentation metadata

- Era: `4.x` (primary)
- Introduced in: `4.0.x` (fill with exact minor)
- Frontend bindings: `docs/frontend/salesnavigator-ui-bindings.md`
- Data stores touched: Connectra PostgreSQL + Elasticsearch (`contacts`, `companies` indexes)

## Endpoint/version binding checklist

- Add `introduced_in` / `deprecated_in` tags per operation.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.
- Keep `salesnavigator_endpoint_era_matrix.json` aligned with deployed routes.
- Fix `docs/api.md` drift (scrape-html-with-fetch) before 4.x release.

## 2026 route-contract correction

- Canonical implemented routes are `/v1/scrape`, `/v1/save-profiles`, and `/v1/health`.
- Any documented-but-missing route must be marked planned/deprecated until implementation is shipped.
