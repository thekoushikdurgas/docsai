# Dashboard GraphQL and VQL

The primary CRM dashboard (`contact360.io/app`) uses **GraphQL** against **`api.contact360.io`**, not direct Connectra HTTP from the browser.

- **List / count:** `contacts.contacts(query: VqlQueryInput)`, `contactCount`, exports use the same `VqlQueryInput` fragments.
- **Facet values:** `contacts.filterData(input)` — pagination fields `page`, `limit`, `searchText`; response includes **`total`** when Connectra supplies it (see `ConnectraClient._parse_response` and `docs/DECISIONS.md`).
- **Triple sync (keep aligned):**
  1. Gateway **only** produces Connectra `where` JSON via [`contact360.io/api/app/utils/vql_converter.py`](../../contact360.io/api/app/utils/vql_converter.py).
  2. This doc (dashboard field names, `filterData`, `total` semantics).
  3. Phase 3 UI doc [`3.Contact360 contact and company data system/52-app-contacts-vql-filters.md`](../3.Contact360%20contact%20and%20company%20data%20system/52-app-contacts-vql-filters.md) + [`docs/docs/contacts-filter-vql-ui.md`](../docs/contacts-filter-vql-ui.md).

**Task backlog and file map:** [`../docs/contacts-filter-vql-ui.md`](../docs/contacts-filter-vql-ui.md).
