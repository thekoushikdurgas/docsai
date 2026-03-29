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

## Connectra REST mapping

| REST endpoint | Method | GraphQL binding | Introduced in | Auth/rate-limit |
| --- | --- | --- | --- | --- |
| `/companies/` | `POST` | `companies`, `companyQuery` | `3.0.0` | API key, Connectra token-bucket limiter |
| `/companies/count` | `POST` | `companyCount` | `3.0.0` | API key, Connectra token-bucket limiter |
| `/companies/batch-upsert` | `POST` | batch company create/update paths | `3.0.0` | API key, protected write path |
| `/common/:service/filters` (`service=companies`) | `GET/POST` | `filters` | `3.0.0` | API key |
| `/common/:service/filters/data` (`service=companies`) | `GET/POST` | `filterData` | `3.0.0` | API key |
| `/common/jobs` | `POST` | export/import job polling paths | `3.0.0` | API key |
| `/common/jobs/create` | `POST` | `exportCompanies`, `importCompanies` | `3.0.0` | API key + role guard from gateway |

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

