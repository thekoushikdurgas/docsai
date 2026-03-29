# Appointment360 (contact360.io/api) — Era 3.x Contact & Company Data Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Define `ContactQuery { contact(uuid), contacts(query), contactCount(query), contactQuery(query), filters(), filterData(input) }` | P0 |
| Define `ContactMutation { createContact, batchCreateContacts, updateContact, deleteContact, exportContacts, batchUpsertContacts, upsertByLinkedinUrl, searchLinkedin, syncIntegration }` | P0 |
| Define `CompanyQuery { company(uuid), companies(query), companyCount(query), companyQuery(query), companyContacts(company_uuid), filters(), filterData(input) }` | P0 |
| Define `CompanyMutation { createCompany, batchCreateCompanies, updateCompany, deleteCompany, exportCompanies }` | P0 |
| Define `VQLQueryInput` type: `where`, `sort`, `page`, `per_page` fields | P0 |
| Define `ContactType`, `CompanyType`, `FilterType`, `FilterDataType` GraphQL output types | P0 |
| Document contacts module in `docs/backend/apis/03_CONTACTS_MODULE.md` | P1 |
| Document companies module in `docs/backend/apis/04_COMPANIES_MODULE.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement `ConnectraClient` in `app/clients/connectra_client.py` | P0 |
| Wire `contacts(query)` → `ConnectraClient.query_contacts(vql_input)` | P0 |
| Wire `contactCount(query)` → `ConnectraClient.count_contacts(vql_input)` | P0 |
| Wire `contact(uuid)` → `ConnectraClient.query_contacts` with uuid filter | P0 |
| Wire `contacts.filters()` → `ConnectraClient.get_filters()` | P0 |
| Wire `contacts.filterData(input)` → `ConnectraClient.get_filter_data(input)` | P0 |
| Wire `batchUpsertContacts` → `ConnectraClient.batch_upsert_contacts(...)` | P0 |
| Wire `exportContacts` → `TkdjobClient.create_contact360_export(...)` | P0 |
| Wire `companies(query)` → `ConnectraClient.query_companies(vql_input)` | P0 |
| Wire `companyContacts(company_uuid)` → `ConnectraClient.query_contacts` with company filter | P0 |
| Implement `vql_converter.py`: translate GraphQL `VQLQueryInput` → Connectra REST format | P0 |
| Implement `connectra_mappers.py`: map Connectra JSON responses → GraphQL types | P0 |
| Add DataLoader for contact batch loading by uuid | P1 |
| Add DataLoader for company batch loading by uuid | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| `/contacts` page, list tab → `query contacts(query: VQLQueryInput)` binding | P0 |
| Contacts filter sidebar → `query filters()` + `query filterData(input)` binding | P0 |
| Contacts search bar → VQL `where` input builder | P0 |
| Contacts export button → `mutation exportContacts` → job polling | P0 |
| Contact detail modal → `query contact(uuid)` binding | P0 |
| Import contacts modal (CSV) → `mutation createContact360Import` via jobs module | P0 |
| `/companies` page grid/list → `query companies(query)` binding | P0 |
| Company detail view, contacts tab → `query companyContacts(company_uuid)` | P0 |
| Pagination controls → `per_page`/`page` in `VQLQueryInput` | P0 |
| Table sort headers → `sort` field in `VQLQueryInput` | P0 |
| `useContactsPage` hook: state for query, pagination, sort, loading | P0 |
| `useContactsFilters` hook: load filters, apply filter selections | P0 |
| `useCompaniesPage` hook: mirror of contacts page hook | P0 |
| `contactsService.ts`: `listContacts`, `getContact`, `contactCount`, `getContactFilters` | P0 |
| `companiesService.ts`: `listCompanies`, `getCompany`, `companyContacts` | P0 |

---

## Data track

| Task | Priority |
| --- | --- |
| Contacts and companies data stored in Connectra (PostgreSQL + Elasticsearch) — not appointment360 DB | P0 |
| Track `exportContacts` job uuid in `activities` table (appointment360 DB) | P0 |
| Track `batchUpsertContacts` usage for credit deduction | P0 |
| Saved searches persist in appointment360 DB: `saved_searches` table with `type=contact\|company`, `vql_json`, `name` | P1 |
| DataLoader batch keys logged for debugging N+1 issues | P1 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure `CONNECTRA_BASE_URL`, `CONNECTRA_API_KEY`, `CONNECTRA_TIMEOUT` in `.env.example` | P0 |
| Test `query contacts` round-trip with Connectra dev instance | P0 |
| Write contract test: `contacts(query)` input → Connectra REST `/contacts/query` | P1 |
| Write contract test: `companies(query)` input → Connectra REST `/companies/query` | P1 |
| Add `/contacts` + `/companies` Postman collection to `docs/backend/postman/` | P1 |

---

## Email app surface contributions (era sync)

- Added preparatory hooks for contact/company linkage from mailbox context (roadmap-level).
- Data table selection model is aligned for future extraction workflows.
