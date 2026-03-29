# Contacts Module

The Contacts module is the core Contact360 GraphQL surface for querying and mutating contact data stored in Connectra.

## Overview

- Source of truth is Connectra (VQL), not Postgres
- Supports VQL filtering, pagination, sorting, and projection
- Handles single and bulk create/update flows
- Provides export/import orchestration through jobs module

## Query and mutation index

| Operation | Variable type | Return | Auth |
|---|---|---|---|
| `contact` | `uuid: ID!` | `Contact` | required |
| `contacts` | `query: VQLQueryInput` | `ContactConnection` | required |
| `contactCount` | `query: VQLQueryInput` | `Int` | required |
| `contactQuery` | `query: VQLQueryInput!` | `ContactConnection` | required |
| `filters` | none | `ContactFilterConnection` | required |
| `filterData` | `input: ContactFilterDataInput!` | `ContactFilterDataConnection` | required |
| `createContact` | `input: CreateContactInput!` | `Contact` | required |
| `updateContact` | `uuid: ID!, input: UpdateContactInput!` | `Contact` | required |
| `batchCreateContacts` | `input: BatchCreateContactsInput!` | `BatchCreateContactsResult` | required |
| `exportContacts` | `input: CreateContact360ExportInput!` | `SchedulerJob` | required |
| `importContacts` | `input: CreateContact360ImportInput!` | `SchedulerJob` | superadmin |

## Connectra REST mapping

| REST endpoint | Method | GraphQL binding | Introduced in | Auth/rate-limit |
| --- | --- | --- | --- | --- |
| `/contacts/` | `POST` | `contacts`, `contactQuery` | `3.0.0` | API key, Connectra token-bucket limiter |
| `/contacts/count` | `POST` | `contactCount` | `3.0.0` | API key, Connectra token-bucket limiter |
| `/contacts/batch-upsert` | `POST` | `batchCreateContacts` | `3.0.0` | API key, protected write path |
| `/common/:service/filters` (`service=contacts`) | `GET/POST` | `filters` | `3.0.0` | API key |
| `/common/:service/filters/data` (`service=contacts`) | `GET/POST` | `filterData` | `3.0.0` | API key |
| `/common/jobs` | `POST` | export/import job polling paths | `3.0.0` | API key |
| `/common/jobs/create` | `POST` | `exportContacts`, `importContacts` | `3.0.0` | API key + role guard from gateway |

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

