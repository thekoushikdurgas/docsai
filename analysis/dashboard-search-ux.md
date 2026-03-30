# Dashboard search UX — contacts & companies (era `3.x`)

**Intent:** Contacts and companies **discovery** with VQL-backed filters, **saved searches**, **natural-language filter parsing** (Contact AI / Gemini), **import/export**, and **company drill-down**. This doc aligns with [`docs/frontend/pages/contacts_page.json`](../frontend/pages/contacts_page.json), [`docs/frontend/pages/companies_page.json`](../frontend/pages/companies_page.json), and [`docs/frontend/hooks-services-contexts.md`](../frontend/hooks-services-contexts.md).

**Era:** `3.x` — Contact360 contact and company data system (not limited to legacy roadmap stage labels).

---

## Routes (Next.js app)

| Area | Path | Notes |
| --- | --- | --- |
| Contacts | `contact360.io/app/app/(dashboard)/contacts/page.tsx` | Main search + filter surface; batched queries via `contactsPageApi` |
| Companies list | `app/(dashboard)/companies/page.tsx` | Company browse; `companiesPageApi` batching |
| Company detail | `app/(dashboard)/companies/[id]/page.tsx` | Drill-down by id |

Full endpoint graphs live in the page JSON files under [`docs/frontend/pages/`](../frontend/pages/).

---

## Hooks and services

| Hook | File | Role |
| --- | --- | --- |
| `useContactsPage` | `hooks/contacts/useContactsPage.ts` | List, count, pagination, sort; uses `contactsPageApi` |
| `useContactsFilters` | `hooks/contacts/useContactsFilters.ts` | Filter state; NL parse via `ParseFilters` / Contact AI path |
| `useSavedSearches` | (see hooks doc) | CRUD for saved searches; `savedSearchesService` |
| `useCompaniesPage` | `hooks/companies/useCompaniesPage.ts` | Companies list + filters batch |
| `useCompaniesFilters` | `hooks/companies/useCompaniesFilters.ts` | Company filter UI state |
| `useCompaniesView` | `hooks/companies/useCompaniesView.ts` | View mode helpers |
| `useNewExport` | `src/hooks/useNewExport.ts` | Export from current VQL / saved search → jobs |

| Service | File |
| --- | --- |
| `contactsService` | `services/graphql` — list, count, filters |
| `companiesService` | `services/graphql` |
| `savedSearchesService` | `services/graphql/savedSearchesService.ts` |
| `contactsPageApi` | `lib/api/pages/contactsPageApi.ts` |
| companies batch | `lib/api/pages/companiesPageApi.ts` (see hooks doc) |

See **Hook ↔ service matrix** in [`docs/frontend/hooks-services-contexts.md`](../frontend/hooks-services-contexts.md).

---

## Key UI components (contacts)

Representative bindings (see [`contacts_page.json`](../frontend/pages/contacts_page.json) for full tree):

- Natural language search / AI filter suggestions
- Query builder and filter sidebar
- `SaveSearchModal`, `SavedSearchesModal`
- Bulk export (Pro+), import entry points
- Simple vs full view modes

Companies page adds **AI company summary** (`GenerateCompanySummary` / `useCompanySummary` per `companies_page.json`).

---

## Saved searches and export

- **UI:** `src/components/contacts/SaveSearchModal.tsx`, `SavedSearchesModal.tsx`
- **API:** `src/services/graphql/savedSearchesService.ts`
- **Export:** `src/hooks/useNewExport.ts`; jobs surface `app/(dashboard)/jobs/page.tsx` — bind [`docs/frontend/jobs-ui-bindings.md`](../frontend/jobs-ui-bindings.md)

---

## Filter ↔ VQL

- GraphQL resolvers use **`vql_converter.py`** (Appointment360) per **[`vql-filter-taxonomy.md`](vql-filter-taxonomy.md)**.
- AI-assisted parsing: **Service task slices** in `3.3.P` / `3.4.P` patch files (ex-`contact-ai-contact-company-task-pack.md`), [`docs/frontend/contact-ai-ui-bindings.md`](../frontend/contact-ai-ui-bindings.md).

---

## Feature gating

- Advanced filters / saved searches may be constrained via `src/lib/featureAccess.ts` (`ADVANCED_FILTERS`, `SAVE_SEARCHES`).

---

## Related planning docs

- **Appointment360 (gateway):** **Service task slices** in `3.0.P`–`3.4.P` patches (ex-`appointment360-contact-company-task-pack.md`) — GraphQL module binding
- [`3.4 — Dashboard UX.md`](3.4 — Dashboard UX.md) — Dashboard UX minor
