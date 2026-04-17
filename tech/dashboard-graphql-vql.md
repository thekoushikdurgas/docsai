# Dashboard GraphQL and VQL

The primary CRM dashboard (`contact360.io/app`) uses **GraphQL** against **`api.contact360.io`**, not direct Connectra HTTP from the browser.

- **List / count:** `contacts.contacts(query: VqlQueryInput)`, `contactCount`, exports use the same `VqlQueryInput` fragments.
- **Facet values:** `contacts.filterData(input)` — pagination fields `page`, `limit`, `searchText`; response includes **`total`** when Connectra supplies it (see `ConnectraClient._parse_response` and `docs/DECISIONS.md`).

**Task backlog and file map:** [`../docs/contacts-filter-vql-ui.md`](../docs/contacts-filter-vql-ui.md).
