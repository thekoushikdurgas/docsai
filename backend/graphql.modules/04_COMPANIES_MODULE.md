# Companies Module

The Companies module exposes Connectra-backed company querying and mutation workflows.

## Operation matrix

- `company`
- `companies`
- `companyQuery`
- `companyCount`
- `companyContacts`
- `filters`
- `filterData`
- `createCompany`
- `updateCompany`
- `exportCompanies`
- `importCompanies`
- `deleteCompany` (`Boolean`; Connectra/gateway may reject unsupported deletes — check runtime errors)

GraphQL paths: `query { companies { ... } }`, `mutation { companies { ... } }`.

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

**Companies namespace (excerpt):**

```graphql
type CompanyQuery {
  company(uuid: ID!): Company!
  companies(query: VQLQueryInput = null): CompanyConnection!
  companyQuery(query: VQLQueryInput!): CompanyConnection!
  companyCount(query: VQLQueryInput = null): Int!
  companyContacts(companyUuid: ID!, query: VQLQueryInput = null, limit: Int = 100, offset: Int = 0): ContactConnection!
  filters: CompanyFilterConnection!
  filterData(input: CompanyFilterDataInput!): CompanyFilterDataConnection!
}

type CompanyMutation {
  createCompany(input: CreateCompanyInput!): Company!
  exportCompanies(input: CreateContact360ExportInput!): SchedulerJob!
  importCompanies(input: CreateContact360ImportInput!): SchedulerJob!
  updateCompany(uuid: ID!, input: UpdateCompanyInput!): Company!
  deleteCompany(uuid: ID!): Boolean!
}
```

**Inputs:** Reuse `VQLQueryInput` / `PopulateConfigInput` from [03_CONTACTS_MODULE.md](03_CONTACTS_MODULE.md). Company-specific inputs:

```graphql
input CompanyFilterDataInput {
  filterKey: String!
  searchText: String = null
  page: Int = 1
  limit: Int = 20
}

input CreateCompanyInput {
  name: String = null
  employeesCount: Int = null
  industries: [String!] = null
  keywords: [String!] = null
  address: String = null
  annualRevenue: Int = null
  totalFunding: Int = null
  technologies: [String!] = null
  textSearch: String = null
}

input UpdateCompanyInput {
  name: String = null
  employeesCount: Int = null
  industries: [String!] = null
  keywords: [String!] = null
  address: String = null
  annualRevenue: Int = null
  totalFunding: Int = null
  technologies: [String!] = null
  textSearch: String = null
}
```

`CreateContact360ImportInput.importTarget` should be `"company"` for company CSV imports.

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>`.

### `companies.company` (query)

```json
{
  "query": "query ($uuid: ID!) { companies { company(uuid: $uuid) { uuid name website country } } }",
  "variables": { "uuid": "550e8400-e29b-41d4-a716-446655440000" }
}
```

### `companies.companyContacts` (query)

```json
{
  "query": "query ($companyUuid: ID!, $query: VQLQueryInput, $limit: Int, $offset: Int) { companies { companyContacts(companyUuid: $companyUuid, query: $query, limit: $limit, offset: $offset) { total items { uuid email } } } }",
  "variables": {
    "companyUuid": "550e8400-e29b-41d4-a716-446655440000",
    "query": null,
    "limit": 100,
    "offset": 0
  }
}
```

## Connectra REST mapping (`EC2/sync.server`)

Gateway env: **`CONNECTRA_BASE_URL`**, **`CONNECTRA_API_KEY`** on **`X-API-Key`**. Full HTTP contract: **[connectra.api.md](../micro.services.apis/connectra.api.md)** · Postman: **[EC2_sync.server.postman_collection.json](../postman/EC2_sync.server.postman_collection.json)**.

| REST endpoint | Method | GraphQL binding | Notes |
| --- | --- | --- | --- |
| `/companies/` | `POST` | `companies`, `companyQuery` | Body: Connectra `VQLQuery` JSON |
| `/companies/count` | `POST` | `companyCount` | Same `where` as list |
| `/companies/batch-upsert` | `POST` | company batch create/update | Body: JSON array (max 100) |
| `/common/company/filters` | `GET` | `filters` | Path segment **`company`** (singular) |
| `/common/company/filters/data` | `POST` | `filterData` | Body: `filter_key`, `search_text`, `page`, `limit` |
| `/common/jobs` | `POST` | (orchestration as implemented) | List native Connectra jobs |
| `/common/jobs/create` | `POST` | `exportCompanies`, `importCompanies` | Gateway + scheduler |

## VQL input schema

- Same VQL envelope as contacts (`where`, `order_by`, `cursor`, `select_columns`, `company_config`, `page`, `limit`)
- Company search supports keyword, range, and text filters including denormalized dimensions
- `companyContacts` resolver uses company UUID to retrieve linked contact rows in contact query path

## Documentation metadata

- Era: `3.x`
- Introduced in: `3.0.0`
- Frontend bindings:
  - `docs/frontend/pages/companies_page.json`
  - `contact360.io/app/app/(dashboard)/companies/page.tsx`
  - `contact360.io/app/src/hooks/companies/useCompaniesPage.ts`
- Data stores touched:
  - Read: `companies` (PG), `companies_index` (ES), `contacts` (PG for `companyContacts`), `filters`, `filters_data`
  - Write: `companies` (PG), `companies_index` (ES), `filters_data` (PG), `jobs` (export/import orchestration)

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

