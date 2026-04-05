# Contacts Module

The Contacts module is the core Contact360 GraphQL surface for querying and mutating contact data stored in Connectra.

## Overview

- Source of truth is Connectra (VQL), not Postgres
- Supports VQL filtering, pagination, sorting, and projection
- Handles single and bulk create/update flows
- Provides export/import orchestration through jobs module

## Query and mutation index

All operations are under the **`contacts`** namespace (`query { contacts { ... } }` / `mutation { contacts { ... } }`).

| Operation | Variable type | Return | Auth |
|---|---|---|---|
| `contact` | `uuid: ID!` | `Contact` | required |
| `contacts` | `query: VQLQueryInput` | `ContactConnection` | required |
| `contactCount` | `query: VQLQueryInput` | `Int` | required |
| `contactQuery` | `query: VQLQueryInput!` | `ContactConnection` | required |
| `filters` | — | `ContactFilterConnection` | required |
| `filterData` | `input: ContactFilterDataInput!` | `ContactFilterDataConnection` | required |
| `createContact` | `input: CreateContactInput!` | `Contact` | required |
| `updateContact` | `uuid: ID!, input: UpdateContactInput!` | `Contact` | required |
| `deleteContact` | `uuid: ID!` | `Boolean` | required |
| `batchCreateContacts` | `input: BatchCreateContactsInput!` | `[Contact!]!` | required |
| `exportContacts` | `input: CreateContact360ExportInput!` | `SchedulerJob` | required |
| `importContacts` | `input: CreateContact360ImportInput!` | `SchedulerJob` | SuperAdmin (enforced on delegated jobs mutation) |

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

**Contacts namespace (excerpt):**

```graphql
type ContactQuery {
  contact(uuid: ID!): Contact!
  contacts(query: VQLQueryInput = null): ContactConnection!
  contactCount(query: VQLQueryInput = null): Int!
  contactQuery(query: VQLQueryInput!): ContactConnection!
  filters: ContactFilterConnection!
  filterData(input: ContactFilterDataInput!): ContactFilterDataConnection!
}

type ContactMutation {
  createContact(input: CreateContactInput!): Contact!
  exportContacts(input: CreateContact360ExportInput!): SchedulerJob!
  importContacts(input: CreateContact360ImportInput!): SchedulerJob!
  updateContact(uuid: ID!, input: UpdateContactInput!): Contact!
  deleteContact(uuid: ID!): Boolean!
  batchCreateContacts(input: BatchCreateContactsInput!): [Contact!]!
}
```

**Shared VQL input (full field list):**

```graphql
input VQLQueryInput {
  filters: VQLFilterInput = null
  selectColumns: [String!] = null
  companyConfig: PopulateConfigInput = null
  limit: Int = null
  offset: Int! = 0
  page: Int = null
  orderBy: [VQLOrderByInput!] = null
  searchAfter: [String!] = null
  sortBy: String = null
  sortDirection: String = "asc"
}

input VQLFilterInput {
  allOf: [VQLFilterInput!] = null
  anyOf: [VQLFilterInput!] = null
  conditions: [VQLConditionInput!] = null
}

input VQLConditionInput {
  field: String!
  operator: String!
  value: JSON!
}

input VQLOrderByInput {
  orderBy: String!
  orderDirection: String!
}

input PopulateConfigInput {
  populate: Boolean! = false
  selectColumns: [String!] = null
}

input ContactFilterDataInput {
  filterKey: String!
  searchText: String = null
  page: Int = 1
  limit: Int = 20
}

input CreateContactInput {
  firstName: String = null
  lastName: String = null
  companyUuid: ID = null
  email: String = null
  title: String = null
  departments: [String!] = null
  mobilePhone: String = null
  emailStatus: String = null
  seniority: String = null
  status: String = null
  textSearch: String = null
}

input UpdateContactInput {
  firstName: String = null
  lastName: String = null
  companyUuid: ID = null
  email: String = null
  title: String = null
  departments: [String!] = null
  mobilePhone: String = null
  emailStatus: String = null
  seniority: String = null
  status: String = null
  textSearch: String = null
}

input BatchCreateContactsInput {
  contacts: [CreateContactInput!]!
}

input CreateContact360ExportInput {
  outputPrefix: String!
  service: String!
  vql: JSON!
  workflowId: String = null
  s3Bucket: String = null
  sliceCount: Int! = 4
  pageSize: Int! = 1000
  retryCount: Int! = 2
  retryInterval: Int! = 5
  savedSearchId: ID = null
}

input CreateContact360ImportInput {
  s3Bucket: String!
  s3Key: String!
  outputPrefix: String! = "imports/"
  workflowId: String = null
  csvColumns: JSON = null
  chunkCount: Int! = 8
  retryCount: Int! = 3
  retryInterval: Int! = 5
  importTarget: String! = "contact"
}
```

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>`.

### `contacts.contact` (query)

```json
{
  "query": "query ($uuid: ID!) { contacts { contact(uuid: $uuid) { uuid firstName lastName email company { uuid name } } } }",
  "variables": { "uuid": "550e8400-e29b-41d4-a716-446655440000" }
}
```

**Success:**

```json
{
  "data": {
    "contacts": {
      "contact": {
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane@example.com",
        "company": null
      }
    }
  }
}
```

### `contacts.contacts` (query with VQL variables)

```json
{
  "query": "query ($query: VQLQueryInput) { contacts { contacts(query: $query) { total limit offset items { uuid email } } } }",
  "variables": {
    "query": {
      "limit": 50,
      "offset": 0,
      "filters": null,
      "sortBy": null,
      "sortDirection": "asc"
    }
  }
}
```

## Connectra REST mapping (`EC2/sync.server`)

Gateway env: **`CONNECTRA_BASE_URL`**, **`CONNECTRA_API_KEY`** on **`X-API-Key`**. Full request/response bodies, VQL JSON, pagination limits (`limit` ≤ 100, `page` ≤ 10), filter paths (`service` = **`contact`**, not `contacts`), jobs, and errors: **[connectra.api.md](../micro.services.apis/connectra.api.md)** · Postman: **[EC2_sync.server.postman_collection.json](../postman/EC2_sync.server.postman_collection.json)**.

| REST endpoint | Method | GraphQL binding | Notes |
| --- | --- | --- | --- |
| `/contacts/` | `POST` | `contacts`, `contactQuery` | Body: Connectra `VQLQuery` JSON |
| `/contacts/count` | `POST` | `contactCount` | Same `where` as list |
| `/contacts/batch-upsert` | `POST` | `batchCreateContacts` | Body: JSON array of contacts (max 100) |
| `/common/contact/filters` | `GET` | `filters` | Path segment **`contact`** (singular) |
| `/common/contact/filters/data` | `POST` | `filterData` | Body: `filter_key`, `search_text`, `page`, `limit` |
| `/common/jobs` | `POST` | (orchestration / polling as implemented) | List native Connectra jobs |
| `/common/jobs/create` | `POST` | `exportContacts`, `importContacts` | Gateway wraps scheduler + Connectra |

## VQL input schema

- `where.text_matches.must/must_not`
- `where.keyword_match.must/must_not`
- `where.range_query.must/must_not`
- `order_by`, `cursor`, `select_columns`, `company_config`, `page`, `limit`
- GraphQL-to-VQL conversion happens in gateway (`vql_converter.py`) before Connectra call

## Error handling

- Validation errors for invalid filters/pagination
- Service unavailable for Connectra failures
- Forbidden for cross-tenant access attempts

## Documentation metadata

- Era: `3.x`
- Introduced in: `3.0.0`
- Frontend bindings:
  - `docs/frontend/pages/contacts_page.json`
  - `contact360.io/app/app/(dashboard)/contacts/page.tsx`
  - `contact360.io/app/src/hooks/contacts/useContactsPage.ts`
- Data stores touched:
  - Read: `contacts` (PG), `companies` (PG when populate), `contacts_index` (ES), `filters`, `filters_data`
  - Write: `contacts` (PG), `contacts_index` (ES), `filters_data` (PG), `jobs` (for export/import orchestration)

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

