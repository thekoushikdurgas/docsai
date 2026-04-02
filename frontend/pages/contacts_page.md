---
title: "Contacts"
page_id: contacts_page
source_json: contacts_page.json
generator: json_to_markdown.py
---

# Contacts

> **Exports:** In-app export modals and bulk actions live here. A dedicated **My Exports** hub is still [planned](export_page.md); track job status on [jobs_page.md](jobs_page.md).

## Overview

- **page_id:** contacts_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 3.x, 8.x, 11.x
- **flow_id:** contacts
- **_id:** contacts_page-001

## Metadata

- **route:** /contacts
- **file_path:** contact360.io/app/app/(dashboard)/contacts/page.tsx
- **purpose:** Contact listing and management with VQL filtering, natural language AI search, Query Builder, saved searches, Simple/Full view modes, bulk export (Pro), import, and pagination.
- **s3_key:** data/pages/contacts_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** Export requires Pro+ (gated via getContactsFloatingActions isPro check)
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00

### uses_endpoints (8)

- `graphql/ContactQuery` — Query contacts with VQL filtering, pagination, and sorting. Batched with contactCount and savedSearches in contactsPageApi via useContactsPage hook.
- `graphql/ContactCount` — Get total contact count with filters applied. Batched with contact data and saved searches in contactsPageApi via useContactsPage hook.
- `graphql/ListSavedSearches` — List saved searches for contacts. Batched with contact data in contactsPageApi via useContactsPage hook.
- `graphql/ParseFilters` — Parse natural language to VQL filters via aiChats.parseFilters. Used in NaturalLanguageSearch for AI-powered filter suggestions.
- `graphql/CreateSavedSearch` — Create a new saved search for contacts
- `graphql/UpdateSavedSearch` — Update an existing saved search
- `graphql/DeleteSavedSearch` — Delete a saved search
- `graphql/CreateContactExport` — Create a CSV export of selected contacts. Pro

### UI components (metadata)

- **ContactsPage** — `app/(dashboard)/contacts/page.tsx`
- **DataPageLayout** — `components/layouts/DataPageLayout.tsx`
- **DataToolbar** — `components/patterns/DataToolbar.tsx`
- **Pagination** — `components/patterns/Pagination.tsx`
- **ContactsFilters** — `components/contacts/ContactsFilters.tsx`
- **ContactsTableContainer** — `components/contacts/ContactsTableContainer.tsx`
- **ContactsMetadata** — `components/contacts/ContactsMetadata.tsx`
- **VQLQueryBuilder** — `components/contacts/VQLQueryBuilder.tsx` (Dynamic)
- **ExportConfirmModal** — `components/shared/ExportModal.tsx` (Dynamic)
- **ExportModal** — `components/shared/ExportModal.tsx` (Dynamic)
- **SaveSearchModal** — `components/contacts/SaveSearchModal.tsx` (Dynamic)
- **SavedSearchesModal** — `components/contacts/SavedSearchesModal.tsx` (Dynamic)
- **DataToolbar** — `components/patterns/DataToolbar.tsx`
- **Pagination** — `components/patterns/Pagination.tsx`

- **versions:** []
- **endpoint_count:** 8

### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Contacts

### description

Contact listing and management with VQL filtering, natural language AI search, Query Builder, saved searches, Simple/Full view modes, bulk export (Pro), import, and pagination.

## Sections (UI structure)

### headings

### subheadings

### tabs

| content_ref | id | label |
| --- | --- | --- |
| contacts-total | total | Total |
| contacts-net-new | net-new | Net New |
| contacts-saved | saved | Saved |
| contacts-dnc | do-not-contact | Do Not Contact |

### era

0.x, 1.x, 3.x, 5.x, 8.x

### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| open AddContactModal | DataToolbar | add-contact | Add Contact | primary |
| open ImportContactModal | DataToolbar | import-contacts | Import CSV | secondary |
| open BulkInsertModal | DataToolbar | bulk-insert | Bulk Paste | ghost |
| contactsService.ExportContacts → ExportConfirmModal (Pro+) | ContactsFloatingActions | export-selected | Export Selected | primary |
| contactsService.BulkDeleteContacts → ConfirmModal | ContactsFloatingActions | delete-selected | Delete Selected | danger |
| open SaveSearchModal | ContactsFilters | save-search | Save Search | ghost |
| open SavedSearchesModal | ContactsFilters | load-saved-search | Saved Searches | ghost |
| useContactsFilters.applyFilters() | VQLQueryBuilder | apply-filters | Apply Filters | primary |
| useContactsFilters.clearFilters() | ContactsFilters | clear-filters | Clear All | ghost |
| useContactColumns.toggleColumn() | ContactsTableContainer | toggle-column-visibility | Columns | secondary |

### input_boxes

| component | id | label | options | placeholder | required | type |
| --- | --- | --- | --- | --- | --- | --- |
| DataToolbar | contacts-search | Search contacts |  | Name, email, company... |  | search |
| NaturalLanguageSearch | nl-search | Natural language search |  | e.g. CTOs at Series B startups in New York |  | text |
| VQLQueryBuilder | vql-field | Field | ['name', 'company', 'title', 'location', 'email', 'industry', 'seniority'] |  |  | select |
| VQLQueryBuilder | vql-operator | Operator | ['contains', 'is', 'is not', 'starts with', 'ends with'] |  |  | select |
| VQLQueryBuilder | vql-value | Value |  | Enter value |  | text |
| SaveSearchModal | save-search-name | Search name |  | e.g. NYC CTOs | True | text |
| ContactsFilters | invite-email | Company domain filter |  | e.g. company.com |  | text |

### text_blocks

| component | content | id | type | visibility |
| --- | --- | --- | --- | --- |
| ContactsTableContainer | {total} contacts · {filtered} matching filters | contacts-count | stat |  |
| ContactsFloatingActions | {selectedCount} selected | selected-count | badge |  |
| ContactsTable | No contacts found. Import a CSV or add contacts manually. | contacts-empty | empty-state |  |
| ContactsFloatingActions | Export requires Pro plan. Upgrade to export contacts. | export-pro-gate | warning | free users |

### checkboxes

| component | id | label | purpose |
| --- | --- | --- | --- |
| ContactsTable | row-select-all | Select all contacts | Header checkbox to select/deselect all rows |
| ContactRow | row-select | Select contact row | Per-row checkbox for multi-select |

### radio_buttons

### progress_bars

### graphs

### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| ContactsPage | vql-filter-flow | VQL filter + export flow | ['Open VQLQueryBuilder', 'Add conditions (field + operator + value) + AND/OR logic', 'Apply Filters → useContactsFilters builds VQL query', 'contactsService.ListContacts with VQL filters', 'Table re-r |

### components

| file_path | name | purpose |
| --- | --- | --- |
| components/layouts/DataPageLayout.tsx | DataPageLayout | Resizable two-panel: table left, detail right |
| components/patterns/DataToolbar.tsx | DataToolbar | Search input + Add/Import/Bulk paste buttons + column toggle |
| components/features/contacts/NaturalLanguageSearch.tsx | NaturalLanguageSearch | AI natural language → VQL filter parsing (Gemini) |
| components/contacts/VQLQueryBuilder.tsx | VQLQueryBuilder | Visual condition builder (field/operator/value rows) |
| components/contacts/ContactsFilters.tsx | ContactsFilters | Filter sidebar with collapsible FilterSection groups |
| components/contacts/ContactsTableContainer.tsx | ContactsTableContainer | State wrapper: table + column visibility toggle |
| components/contacts/ContactsTable.tsx | ContactsTable | Sortable table: avatar, name, email, company, checkbox |
| components/contacts/ContactRow.tsx | ContactRow | Single row: checkbox, avatar, fields, action menu |
| components/contacts/ContactsMetadata.tsx | ContactsMetadata | Right-panel: full contact detail and tags |
| components/contacts/ContactsFloatingActions.tsx | ContactsFloatingActions | Floating bar on selection: Export / Delete buttons |
| components/contacts/ContactsModals.tsx | ContactsModals | Registry: Import, BulkInsert, SaveSearch, Saved, Export, Confirm |
| components/contacts/SaveSearchModal.tsx | SaveSearchModal | Name input for saving current filter set |
| components/contacts/SavedSearchesModal.tsx | SavedSearchesModal | List of saved searches with load/delete |
| components/shared/TablePagination.tsx | TablePagination | Page size selector + prev/next controls |

### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/contacts/useContactsFilters.ts | useContactsFilters | Multi-stage filter state (VQL, AI, quick) | 3.x |
| hooks/contacts/useContactsPage.ts | useContactsPage | Paginated GQL contact retrieval | 3.x |
| hooks/contacts/useContactExport.ts | useContactExport | Background task triggering for data sets | 6.x |
| hooks/contacts/useSavedSearches.ts | useSavedSearches | CRUD for persistent discovery queries | 1.x |
| context/RoleContext.ts | useRole | Pro-feature gating (Saved searches) | 1.x |
| hooks/contacts/useSavedSearches.ts | useSavedSearches | CRUD for filtered search presets | 3.x |
| hooks/useModal.ts | useModal | Generic open/close state for dialogs | 0.x |
| context/RoleContext.tsx | useRole | Checks for Pro/Premium features (AI search, exports) | 1.x |

### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/contactsService.ts | contactsService | ['ContactQuery', 'ContactCount', 'CreateContactExport'] |
| services/graphql/savedSearchesService.ts | savedSearchesService | ['ListSavedSearches', 'CreateSavedSearch', 'UpdateSavedSearch', 'DeleteSavedSearch'] |
| services/graphql/aiChatsService.ts | geminiService | ['ParseFilters'] |

### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User ID for contact ownership |
| context/RoleContext.tsx | RoleContext | Export gate (Pro+), feature access |

### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/contacts/contactsUtils.ts | contactsUtils | formatContactName, getContactInitials, contactToCSVRow |
| lib/contacts/contactsConstants.ts | contactsConstants | CONTACT_FIELDS, SENIORITY_OPTIONS, INDUSTRY_OPTIONS |

### ui_components

### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useContactsPage | QUERY | ContactQuery | contactsService |
| useContactsPage | QUERY | ContactCount | contactsService |
| useContactsPage | QUERY | ListSavedSearches | savedSearchesService |
| useContactsFilters | MUTATION | ParseFilters | geminiService |
| useContactExport | MUTATION | CreateContactExport | contactsService |

## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| add-contact | Add Contact | primary | open AddContactModal | DataToolbar |
| import-contacts | Import CSV | secondary | open ImportContactModal | DataToolbar |
| bulk-insert | Bulk Paste | ghost | open BulkInsertModal | DataToolbar |
| export-selected | Export Selected | primary | contactsService.ExportContacts → ExportConfirmModal (Pro+) | ContactsFloatingActions |
| delete-selected | Delete Selected | danger | contactsService.BulkDeleteContacts → ConfirmModal | ContactsFloatingActions |
| save-search | Save Search | ghost | open SaveSearchModal | ContactsFilters |
| load-saved-search | Saved Searches | ghost | open SavedSearchesModal | ContactsFilters |
| apply-filters | Apply Filters | primary | useContactsFilters.applyFilters() | VQLQueryBuilder |
| clear-filters | Clear All | ghost | useContactsFilters.clearFilters() | ContactsFilters |
| toggle-column-visibility | Columns | secondary | useContactColumns.toggleColumn() | ContactsTableContainer |

### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| contacts-search | Search contacts | search | Name, email, company... | DataToolbar |
| nl-search | Natural language search | text | e.g. CTOs at Series B startups in New York | NaturalLanguageSearch |
| vql-field | Field | select |  | VQLQueryBuilder |
| vql-operator | Operator | select |  | VQLQueryBuilder |
| vql-value | Value | text | Enter value | VQLQueryBuilder |
| save-search-name | Search name | text | e.g. NYC CTOs | SaveSearchModal |
| invite-email | Company domain filter | text | e.g. company.com | ContactsFilters |

### checkboxes

| id | label | purpose | component |
| --- | --- | --- | --- |
| row-select-all | Select all contacts | Header checkbox to select/deselect all rows | ContactsTable |
| row-select | Select contact row | Per-row checkbox for multi-select | ContactRow |

### radio_buttons

[]

### progress_bars

[]

### toasts

[]

## Graphql Bindings

| hook | operation | service | type |
| --- | --- | --- | --- |
| useContactsPage | ContactQuery, ContactCount | contactsService | query |
| useContactsPage | ListSavedSearches | savedSearchesService | query |
| useContactsFilters | ParseFilters | geminiService | mutation |

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/contacts/useContactsPage.ts | useContactsPage | Batched: ContactQuery + ContactCount + ListSavedSearches |
| hooks/contacts/useContactsFilters.ts | useContactsFilters | VQL filter state, NL parse, apply/clear |
| hooks/contacts/useSavedSearches.ts | useSavedSearches | Save, load, delete saved filter sets |
| hooks/contacts/useContactExport.ts | useContactExport | Export job creation and tracking |
| hooks/contacts/useContactColumns.ts | useContactColumns | Column visibility and order (localStorage) |

## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/contactsService.ts | contactsService | ['ContactQuery', 'ContactCount', 'CreateContactExport'] |
| services/graphql/savedSearchesService.ts | savedSearchesService | ['ListSavedSearches', 'CreateSavedSearch', 'UpdateSavedSearch', 'DeleteSavedSearch'] |
| services/graphql/aiChatsService.ts | geminiService | ['ParseFilters'] |

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql contacts, savedSearches, aiChats modules | contact listing/filtering/saved-search operations |
| downstream services | connectra + data enrichment paths via backend modules | filtered contact/company retrieval |

## Data Sources

- Appointment360 GraphQL gateway
- Connectra-backed contact/company data stores via backend

## Flow summary

contacts page filters/VQL -> hooks/page APIs -> GraphQL queries/mutations -> connectra-backed result sets -> table/detail/export workflows

<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **3.x** — Contact & company data — VQL tables, export modals, files, prospect finder narrative.
- **8.x** — Public & private APIs — API docs, integrations story, export contracts, developer surfaces.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/contacts`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions, bookmarks to route. **Typical outbound:** sidebar peers (see **Peer pages**), `router.push` / `<Link>` from **### buttons** table above.

**Cross-host:** marketing [landing_page.md](landing_page.md) → [login_page.md](login_page.md) / [register_page.md](register_page.md); product pages on **root** deep-link to app auth.

## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [activities_page](activities_page.md)
- [admin_page](admin_page.md)
- [ai_chat_page](ai_chat_page.md)
- [analytics_page](analytics_page.md)
- [billing_page](billing_page.md)
- [campaign_builder_page](campaign_builder_page.md)
- [campaign_templates_page](campaign_templates_page.md)
- [campaigns_page](campaigns_page.md)
- [companies_page](companies_page.md)
- [dashboard_page](dashboard_page.md)
- [dashboard_pageid_page](dashboard_pageid_page.md)
- [deployment_page](deployment_page.md)
- [email_page](email_page.md)
- [export_page](export_page.md)
- [files_page](files_page.md)
- [finder_page](finder_page.md)
- [jobs_page](jobs_page.md)
- [linkedin_page](linkedin_page.md)
- [live_voice_page](live_voice_page.md)
- [login_page](login_page.md)
- [profile_page](profile_page.md)
- [register_page](register_page.md)
- [root_page](root_page.md)
- [sequences_page](sequences_page.md)
- [settings_page](settings_page.md)
- [status_page](status_page.md)
- [usage_page](usage_page.md)
- [verifier_page](verifier_page.md)

<!-- AUTO:design-nav:end -->

<!-- AUTO:endpoint-links:start -->

## Backend endpoint specs (GraphQL)

| GraphQL operation | Endpoint spec | Method | Era |
| --- | --- | --- | --- |
| `ContactQuery` | *unresolved — add to endpoint index* | — | — |
| `ContactCount` | [count_contacts_graphql.md](../../backend/endpoints/count_contacts_graphql.md) | QUERY | 2.x |
| `ListSavedSearches` | [query_list_saved_searches_graphql.md](../../backend/endpoints/query_list_saved_searches_graphql.md) | QUERY | 9.x |
| `ParseFilters` | [mutation_parse_filters_graphql.md](../../backend/endpoints/mutation_parse_filters_graphql.md) | MUTATION | 0.x |
| `CreateSavedSearch` | [mutation_create_saved_search_graphql.md](../../backend/endpoints/mutation_create_saved_search_graphql.md) | MUTATION | 9.x |
| `UpdateSavedSearch` | [mutation_update_saved_search_graphql.md](../../backend/endpoints/mutation_update_saved_search_graphql.md) | MUTATION | 9.x |
| `DeleteSavedSearch` | [mutation_delete_saved_search_graphql.md](../../backend/endpoints/mutation_delete_saved_search_graphql.md) | MUTATION | 9.x |
| `CreateContactExport` | [mutation_create_contact_export_graphql.md](../../backend/endpoints/mutation_create_contact_export_graphql.md) | MUTATION | 3.x |

**Unresolved operations** (not found in `index.md` / `endpoints_index.md`): 
`graphql/ContactQuery`

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
