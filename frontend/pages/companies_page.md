---
title: "Companies"
page_id: companies_page
source_json: companies_page.json
generator: json_to_markdown.py
---

# Companies

> **Exports:** Company export modals mirror contacts. Planned central hub: [export_page.md](export_page.md); jobs: [jobs_page.md](jobs_page.md).

## Overview

- **page_id:** companies_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 3.x, 5.x, 8.x, 11.x
- **flow_id:** companies
- **_id:** companies_page-001

## Metadata

- **route:** /companies
- **file_path:** contact360.io/app/app/(dashboard)/companies/page.tsx
- **purpose:** Company listing and management page with VQL filtering, search, grid/list view modes, bulk export (Pro+), pagination, and AI-powered company summaries via Gemini.
- **s3_key:** data/pages/companies_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** BULK_EXPORT requires Pro+ via hasFeatureAccess(Feature.BULK_EXPORT)
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
### uses_endpoints (4)

- `graphql/CompanyQuery` — Query companies with VQL filtering, pagination, and sorting. Batched with filter definitions in companiesPageApi via useCompaniesPage hook.
- `graphql/CompanyFilters` — Get available filter definitions for companies. Batched with company data in companiesPageApi via useCompaniesPage hook.
- `graphql/GenerateCompanySummary` — AI-generated company summary via aiChats.generateCompanySummary. Called on-demand from CompaniesDataDisplay.
- `graphql/CreateCompanyExport` — Create a CSV export of selected companies. Requires BULK_EXPORT feature.

### UI components (metadata)

- **CompaniesPage** — `app/(dashboard)/companies/page.tsx`
- **DataPageLayout** — `components/layouts/DataPageLayout.tsx`
- **DataToolbar** — `components/patterns/DataToolbar.tsx`
- **Pagination** — `components/patterns/Pagination.tsx`
- **CompaniesFilterSidebar** — `components/companies/CompaniesFilterSidebar.tsx`
- **CompaniesDataDisplay** — `components/companies/CompaniesDataDisplay.tsx`
- **FloatingActionBar** — `components/shared/FloatingActionBar.tsx`
- **ExportModal** — `components/shared/ExportModal.tsx` (Dynamic)
- **DashboardAccessGate** — `components/shared/DashboardAccessGate.tsx`
- **FileDown** — `lucide-react` (icon)

- **versions:** []
- **endpoint_count:** 4
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Companies

### description

Company listing and management page with VQL filtering, search, grid/list view modes, bulk export (Pro+), pagination, and AI-powered company summaries via Gemini.


## Sections (UI structure)

### headings



### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| companies-grid | grid | Grid |
| companies-list | list | List |


### era

0.x, 1.x, 3.x, 5.x, 8.x


### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| open AddCompanyModal | DataToolbar | add-company | Add Company | primary |
| open ImportCompanyModal | DataToolbar | import-companies | Import CSV | secondary |
| companiesService.ExportCompanies (Pro+) | CompaniesFloatingActions | export-selected | Export Selected | primary |
| companiesService.BulkDeleteCompanies → ConfirmModal | CompaniesFloatingActions | delete-selected | Delete Selected | danger |
| useCompaniesFilters.applyFilters() | CompaniesFilterSidebar | apply-filters | Apply Filters | primary |
| useCompaniesFilters.clearFilters() | CompaniesFilterSidebar | clear-filters | Clear | ghost |
| useCompaniesView.setViewMode('list') | CompaniesDataDisplay | view-list | List | icon |
| useCompaniesView.setViewMode('grid') | CompaniesDataDisplay | view-grid | Grid | icon |


### input_boxes

| component | id | label | options | placeholder | required | type |
| --- | --- | --- | --- | --- | --- | --- |
| DataToolbar | companies-search | Search companies |  | Company name or domain... |  | search |
| CompaniesFilterSidebar | filter-industry | Industry | ['SaaS', 'Fintech', 'Healthcare', 'E-commerce', 'Manufacturing', 'Other'] |  |  | multi-select |
| CompaniesFilterSidebar | filter-location | HQ Location |  | Country or city |  | multi-select |
| CompaniesFilterSidebar | filter-size-min | Min employees |  | e.g. 10 |  | number |
| CompaniesFilterSidebar | filter-size-max | Max employees |  | e.g. 1000 |  | number |
| AddCompanyModal | company-name | Company name |  |  | True | text |
| AddCompanyModal | company-domain | Domain |  | company.com | True | text |


### radio_buttons

| component | id | label | options | purpose | era |
| --- | --- | --- | --- | --- | --- |
| CompaniesDataDisplay | view-mode | View mode | ['List', 'Grid'] | Toggle between list rows and card grid layout | 3.x |


### text_blocks

| component | content | id | type | era |
| --- | --- | --- | --- | --- |
| CompaniesDataDisplay | {total} companies · {filtered} matching | companies-count | stat | 3.x |
| CompaniesDataDisplay | No companies found. Add a company or import a CSV. | companies-empty | empty-state | 3.x |
| CompanySummaryCard | AI Summary: {summaryText} | ai-summary-v1 | info | 5.x |


### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| CompaniesPage | filter-export-flow | Filter and export companies | ['Apply filters (industry, location, size)', 'companiesService.CompanyQuery with filters', 'Switch view: list vs grid', 'Select rows → floating actions bar', 'Export Selected (Pro+) → ExportModal → jo |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/patterns/DataToolbar.tsx | DataToolbar | Search input + Add/Import/column toggle |
| components/companies/CompaniesFilterSidebar.tsx | CompaniesFilterSidebar | Industry, size, location filter groups |
| components/companies/CompaniesDataDisplay.tsx | CompaniesDataDisplay | View mode toggle + list/grid container |
| components/companies/CompaniesList.tsx | CompaniesList | List rows with checkbox and action menu |
| components/companies/CompaniesGrid.tsx | CompaniesGrid | Card grid layout (logo, name, industry, size) |
| components/companies/CompanyRow.tsx | CompanyRow | Single list row: logo, name, industry, actions |
| components/companies/CompanyContactsTab.tsx | CompanyContactsTab | Contacts sub-tab in company detail panel |
| components/companies/CompaniesModals.tsx | CompaniesModals | Modal registry: Add, Import, Export, Confirm |
| components/companies/AddCompanyModal.tsx | AddCompanyModal | Add/edit company form: name, domain, industry, size |
| components/companies/ImportCompanyModal.tsx | ImportCompanyModal | CSV import wizard: upload → map → confirm |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/companies/useCompaniesFilters.ts | useCompaniesFilters | attribute-based faceted filtering state | 3.x |
| hooks/companies/useCompaniesPage.ts | useCompaniesPage | Paginated GQL company retrieval | 3.x |
| hooks/companies/useCompaniesView.ts | useCompaniesView | Grid/List display mode persistence | 0.x |
| hooks/companies/useCompanyExport.ts | useCompanyExport | multi-format data extraction and generation | 8.x |
| context/RoleContext.ts | useRole | Bulk export feature gating | 1.x |
| context/RoleContext.tsx | useRole | Feature access gating (Bulk Export) | 1.x |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/companiesService.ts | companiesService | ['CompanyQuery', 'CompanyFilters', 'CreateCompany', 'UpdateCompany', 'DeleteCompany', 'ExportCompanies'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/RoleContext.tsx | RoleContext | Pro+ gate for bulk export |


### utilities



### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useCompaniesPage | QUERY | CompanyQuery | companiesService |
| useCompaniesPage | QUERY | CompanyFilters | companiesService |
| useCompanyExport | MUTATION | ExportCompanies | companiesService |


## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| add-company | Add Company | primary | open AddCompanyModal | DataToolbar |
| import-companies | Import CSV | secondary | open ImportCompanyModal | DataToolbar |
| export-selected | Export Selected | primary | companiesService.ExportCompanies (Pro+) | CompaniesFloatingActions |
| delete-selected | Delete Selected | danger | companiesService.BulkDeleteCompanies → ConfirmModal | CompaniesFloatingActions |
| apply-filters | Apply Filters | primary | useCompaniesFilters.applyFilters() | CompaniesFilterSidebar |
| clear-filters | Clear | ghost | useCompaniesFilters.clearFilters() | CompaniesFilterSidebar |
| view-list | List | icon | useCompaniesView.setViewMode('list') | CompaniesDataDisplay |
| view-grid | Grid | icon | useCompaniesView.setViewMode('grid') | CompaniesDataDisplay |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| companies-search | Search companies | search | Company name or domain... | DataToolbar |
| filter-industry | Industry | multi-select |  | CompaniesFilterSidebar |
| filter-location | HQ Location | multi-select | Country or city | CompaniesFilterSidebar |
| filter-size-min | Min employees | number | e.g. 10 | CompaniesFilterSidebar |
| filter-size-max | Max employees | number | e.g. 1000 | CompaniesFilterSidebar |
| company-name | Company name | text |  | AddCompanyModal |
| company-domain | Domain | text | company.com | AddCompanyModal |


### checkboxes

| id | label | component |
| --- | --- | --- |
| row-select-all | Select all companies | CompaniesList |
| row-select | Select company row | CompanyRow |


### radio_buttons

| id | label | options | purpose | component |
| --- | --- | --- | --- | --- |
| view-mode | View mode | ['List', 'Grid'] | Toggle between list rows and card grid layout | CompaniesDataDisplay |


### progress_bars

[]

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/companies/useCompaniesPage.ts | useCompaniesPage | Batched: CompanyQuery + CompanyFilters |
| hooks/companies/useCompaniesFilters.ts | useCompaniesFilters | Filter state: industry, size, location |
| hooks/companies/useCompaniesView.ts | useCompaniesView | List/grid view mode with localStorage persistence |
| hooks/companies/useCompanyExport.ts | useCompanyExport | Export job creation and tracking |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/companiesService.ts | companiesService | ['CompanyQuery', 'CompanyFilters', 'CreateCompany', 'UpdateCompany', 'DeleteCompany', 'ExportCompanies'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/CompanyQuery, graphql/CompanyFilters, graphql/GenerateCompanySummary, graphql/CreateCompanyExport | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: companiesService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useCompaniesPage, useCompaniesFilters, useCompaniesView, useCompanyExport -> companiesService -> GraphQL gateway -> backend modules -> rendered states


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

**Route (registry):** `/companies`

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
- [contacts_page](contacts_page.md)
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
| `CompanyQuery` | [get_company_graphql.md](../../backend/endpoints/get_company_graphql.md) | QUERY | 3.x.x |
| `CompanyFilters` | [get_company_filters_graphql.md](../../backend/endpoints/get_company_filters_graphql.md) | QUERY | 3.x |
| `GenerateCompanySummary` | [mutation_generate_company_summary_graphql.md](../../backend/endpoints/mutation_generate_company_summary_graphql.md) | MUTATION | 4.x |
| `CreateCompanyExport` | [mutation_create_company_export_graphql.md](../../backend/endpoints/mutation_create_company_export_graphql.md) | MUTATION | 3.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
