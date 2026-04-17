# Contacts filters, VQL UI, and documentation sync

This note ties **product intent**, **implemented code** (`contact360.io/app`, `contact360.io/api`, Connectra client), and **where to extend docs** across Contact360 phases `0.x`–`11.x`.

## Deep summary (what the system does)

| Layer | Responsibility |
| ----- | ---------------- |
| **Connectra** | OpenSearch-backed VQL; `POST /common/{contact\|company}/filters/data` returns facet value pages; may include **`total`** for full result count. |
| **Gateway** | `ConnectraClient.get_filter_data` → `_parse_response` must **not** drop `total`. Strawberry `contacts.filterData` / `companies.filterData` expose `items` + **`total`**. |
| **App** | `useFilterOptions` + `useContactFilters`: paginated loads, debounced search, dedupe by `value`. `FilterCombobox` (Popover) replaces native `<select>`. Contacts page merges sidebar + advanced + column-derived `select_columns` / `company_config` into one list query. `VqlBuilderModal` can preview **full list** JSON. |

**Contract:** The dashboard speaks **GraphQL `VqlQueryInput`** (nested `filters` / `orderBy` / `selectColumns` / `companyConfig`), not raw Connectra `where` JSON. Parity with Connectra is enforced in **`vql_converter.py`** and Connectra docs under `EC2/sync.server/docs`.

## Smaller follow-up tasks (backlog)

Use these as checklist items in phase **3** (data/search), **0** (foundation), **6** (reliability), **8** (APIs), and **frontend** docs.

### Gateway and Connectra

- [ ] Confirm Connectra `filters/data` response schema in production (always sends `total` when paginated).
- [ ] If `total` is optional, document fallback: `hasMore` when last page length equals `limit`.
- [ ] Mirror **companies** list page: same `FilterCombobox` + `useFilterOptions` pattern as contacts (companies service already returns `{ items, total }`).

### App / UX

- [ ] Per-facet chip: remove **single** value without clearing entire facet (optional).
- [ ] Saved searches / URL serialization for `facetValues` + advanced draft (phase **10** campaigns overlap).
- [ ] AI filter row: wire to gateway when `NEXT_PUBLIC_CONTACTS_AI_SEARCH=1` (phase **5**).

### Docs hygiene (this repo)

- [ ] Regenerate or hand-update **`docs/codebases/app-codebase-analysis.md`** when that file exists in tree (path may differ); link `/contacts` to this note.
- [ ] **`docs/flowchart`:** add a small diagram node: “User filters → GraphQL VQL → gateway converter → Connectra”.
- [ ] **`docs/prd`:** avoid duplicate “Read all the above…” scratch files; consolidate pointers into `docs/docs/contacts-filter-vql-ui.md`.
- [ ] **Phases 1, 2, 4–11 `index.json`:** add optional `implementation_notes` pointer to `../docs/contacts-filter-vql-ui.md` only where contact/company search touches that phase (minimal edits — prefer single hub doc).

### Testing

- [ ] CI: `pytest` filter GraphQL tests + app `vitest` for `useFilterOptions` helpers.
- [ ] Golden `VqlQueryInput` payloads: single facet, multi facet `in_list`, advanced OR group + sidebar AND.

## Files to read in codebase

| Area | Path |
| ---- | ---- |
| Contacts page | `contact360.io/app/app/(dashboard)/contacts/page.tsx` |
| Sidebar | `contact360.io/app/src/components/feature/contacts/ContactsFilterSidebar.tsx` |
| Combobox | `contact360.io/app/src/components/ui/FilterCombobox.tsx` |
| Options hook | `contact360.io/app/src/hooks/useFilterOptions.ts`, `useContactFilters.ts` |
| VQL draft | `contact360.io/app/src/lib/vqlDraft.ts` |
| Gateway filterData | `contact360.io/api/app/graphql/modules/contacts/queries.py` |
| Connectra client | `contact360.io/api/app/clients/connectra_client.py` (`_parse_response`) |
