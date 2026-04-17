# App — Contacts list: filters, VQL, and Connectra `filterData`

**Scope:** `contact360.io/app` contacts page (`/contacts`), gateway `contact360.io/api`, Connectra `POST /common/contact/filters/data`.

## Implemented behavior (baseline)

1. **Sidebar + advanced merge** — Tab, email search, status, dynamic facets, and optional advanced `DraftQuery` merge into one `VqlQueryInput` for `contacts.contacts(query)`.
2. **Multi-value facets** — `facetValues` is `Record<string, string[]>`. One value → `eq`; multiple → `in_list` (mapped to `in` for the API).
3. **Paginated facet options** — `contacts.filterData(input)` with `page`, `limit`, `searchText`; UI uses infinite scroll + typeahead in `FilterCombobox`.
4. **GraphQL `filterData.total`** — Gateway reads Connectra `total` when present; `ConnectraClient._parse_response` preserves upstream `total` instead of overwriting with page length only.
5. **VQL preview** — Advanced modal Preview tab can show **Full list query** (merged filters + columns + `limit`/`offset`) vs **Advanced only**.

## Cross-references

- Architecture decisions: [`../DECISIONS.md`](../DECISIONS.md) (dashboard contacts / filterData section).
- Deeper narrative + backlog tasks: [`../docs/contacts-filter-vql-ui.md`](../docs/contacts-filter-vql-ui.md).
- Gateway GraphQL notes: [`../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md`](../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md).

## Phase 3 roadmap alignment

- Stub **`3.6.1.2`** *Faceted navigation* — product doc; app now ships a first slice (dynamic keys from `filters` + VQL merge). Remaining doc work: formalize OR semantics, saved views, and company page parity.
