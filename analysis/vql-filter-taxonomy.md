# VQL filter taxonomy (frozen reference)

**Status:** Contract mirror — keep in sync with code when adding fields.

**Canonical implementation**

- GraphQL → VQL conversion: `contact360.io/api/app/utils/vql_converter.py`
- Connectra query shape: `contact360.io/sync/utilities/structures.go` (`VQLQuery`, `WhereStruct`, …)
- Read APIs: `ContactService.ListByFilters` / `CountByFilters`, `CompanyService` equivalents under `contact360.io/sync/modules/*/service/`

## `VQLQuery` contract (Connectra)

```json
{
  "where": {
    "text_matches": { "must": [], "must_not": [] },
    "keyword_match": { "must": {}, "must_not": {} },
    "range_query": { "must": {}, "must_not": {} }
  },
  "order_by": [{ "order_by": "string", "order_direction": "asc|desc" }],
  "cursor": [],
  "select_columns": [],
  "company_config": { "populate": false, "select_columns": [] },
  "page": 0,
  "limit": 0
}
```

`text_matches` entries use `TextMatchStruct`: `text_value`, `filter_key`, `search_type`, optional `slop`, `operator`, `fuzzy`.

## Field type taxonomy (Appointment360 GraphQL filters)

Field types determine how filters map to `text_matches` vs `keyword_match` vs `range_query`. **Unknown fields default to keyword** in `get_field_type()`.

### Contacts — text fields

`first_name`, `last_name`, `title`, `city`, `state`, `country`, `linkedin_url`

### Contacts — keyword fields

`id`, `company_id`, `email`, `departments`, `mobile_phone`, `email_status`, `seniority`, `status`, `uuid`

### Contacts — range fields

`created_at`, `updated_at`

### Companies — text fields

`name`, `address`, `city`, `state`, `country`, `linkedin_url`, `website`, `normalized_domain`

### Companies — keyword fields

`id`, `industries`, `keywords`, `technologies`, `uuid`

### Companies — range fields

`employees_count`, `annual_revenue`, `total_funding`, `created_at`, `updated_at`

### Denormalized company fields on contact index (`company_*`)

Used when filtering contacts by company attributes without separate company populate. **Changing these without ES/pg mapping updates can break queries** (see comments in `vql_converter.py`).

**Text:** `company_name`, `company_address`, `company_city`, `company_state`, `company_country`, `company_linkedin_url`, `company_website`, `company_normalized_domain`

**Keyword:** `company_industries`, `company_keywords`, `company_technologies`

**Range:** `company_employees_count`, `company_annual_revenue`, `company_total_funding`

## Operator mapping (GraphQL → VQL text `search_type`)

| GraphQL operator | VQL `search_type` | Notes |
|------------------|-------------------|--------|
| `contains`       | `shuffle`         | fuzzy + operator `and` where applicable |
| `exact`          | `exact`           | fuzzy, `slop` 1 |
| `starts_with`    | `substring`       | |
| `ends_with`      | `substring`       | |

## Search type to Elasticsearch mapping (runtime)

| VQL `search_type` | ES query strategy | Runtime note |
| --- | --- | --- |
| `exact` | `match_phrase` (+ `slop`) | Best for precise phrase matching |
| `shuffle` | `match` (+ optional fuzzy/operator) | Order-insensitive token matching |
| `substring` | ngram-backed field matching | Supports prefix/suffix/contains-like behavior |

## Pagination contract

- Cursor-first pagination is preferred for deep/large result traversal.
- Page/limit fields remain supported for straightforward UI pagination.
- Recommended limits: default 50; UI hard guard <= 1000 per request.
- Large exports should route through job/stream flows, not oversized page pulls.

## Change process (freeze discipline)

1. Add fields to Elasticsearch / PostgreSQL mappings and Connectra parsers as needed.
2. Update `vql_converter.py` sets and `DENORMALIZED_TO_COMPANY_COLUMN` if applicable.
3. Update **this file** in the same change set.
4. Run Connectra + gateway integration tests for `ListByFilters` / `CountByFilters`.

## Related GraphQL inputs

- `VQLQueryInput`, `VQLFilterInput` — `contact360.io/api/app/graphql/modules/contacts/inputs.py` (and companies module).
