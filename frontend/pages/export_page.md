---
title: "Export"
page_id: export_page
source_json: export_page.json
generator: json_to_markdown.py
---

# Export

## Implementation status (repository)

**Not implemented as a dedicated route.** There is no `contact360.io/app/app/(dashboard)/export/page.tsx` and no `components/features/export/*` in this workspace. Export-related UX today lives elsewhere:

- **Jobs** — `contact360.io/app/app/(dashboard)/jobs/page.tsx` (create export jobs, file upload, status).
- **Files** — `contact360.io/app/app/(dashboard)/files/page.tsx` (artifacts, export-from-file flows).
- **Contacts / Companies** — export modals and bulk actions on those pages.

The sections below describe the **target** dedicated export hub (for planning and GraphQL contract alignment). Treat as **spec / backlog**, not current UI.

## Overview

- **page_id:** export_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 3.x, 6.x, 11.x
- **flow_id:** export
- **_id:** export_page-001

## Metadata

- **route:** `/export` *(planned — not present in App Router)*
- **file_path:** *N/A* — implement at `contact360.io/app/app/(dashboard)/export/page.tsx` when built
- **purpose:** Export management hub for tracking, downloading, and canceling bulk data exports (Contacts, Companies, Results).
- **status:** planned
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** S3 Files tab and Delete All button visible only to admin/superAdmin.
- **page_state:** spec/backlog
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
### uses_endpoints (4)

- `graphql/Exports` — List exports with pagination and status/type filters. Via exportPageApi. Auto-refreshes every 3 seconds for pending/processing exports.
- `graphql/GetExport` — Get export details for download URL and status polling. Used by useExportManager.
- `graphql/CancelExport` — Cancel a pending or processing export.
- `graphql/S3ListFiles` — List S3 export files. Used by S3FileBrowser. Only when S3 tab is active (admin/superAdmin).

### UI components (metadata)

- **ToolPageLayout** — `components/layouts/ToolPageLayout.tsx`
- **DashboardAccessGate** — `components/shared/DashboardAccessGate.tsx`
- **PageHeader** — `components/patterns/PageHeader.tsx`
- **ExportFilters** — `components/features/export/ExportFilters.tsx`
- **ExportListTable** — `components/features/export/ExportListTable.tsx`
- **ExportTableRow** — `components/features/export/ExportTableRow.tsx`
- **ExportDeleteModal** — `components/features/export/ExportDeleteModal.tsx`
- **ExportMessages** — `components/features/export/ExportMessages.tsx`
- **S3FileBrowser** — `components/features/export/S3FileBrowser.tsx`

- **versions:** []
- **endpoint_count:** 4
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Export

### description

Export management page with My Exports and S3 Files (admin-only) tabs. List, filter, download, cancel exports. Create Export redirects to contacts. Delete All and S3 tab for admin/superAdmin.


## Sections (UI structure)

### headings



### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| export-list | exports | My Exports |
| s3-browser | s3 | S3 Files |


### era

2.x


### buttons

| action | component | id | label | type | visibility |
| --- | --- | --- | --- | --- | --- |
| navigate to /contacts (Pro+) | PageHeader | create-export | Create Export | primary |  |
| exportsService.GetExport → presigned URL | ExportTableRow | download-export | Download | secondary |  |
| exportsService.CancelExport → ConfirmModal | ExportTableRow | cancel-export | Cancel | danger |  |
| open ExportDeleteModal | ExportTableRow | delete-export | Delete | danger |  |
| bulk delete all exports → ConfirmModal | PageHeader | delete-all | Delete All | danger | admin/superAdmin only |
| useExportPage.applyFilters() | ExportFilters | apply-filter | Apply | primary |  |


### input_boxes

| component | id | label | options | type |
| --- | --- | --- | --- | --- |
| ExportFilters | filter-status | Status | ['All', 'Pending', 'Processing', 'Completed', 'Failed', 'Cancelled'] | select |
| ExportFilters | filter-type | Type | ['All', 'Contacts', 'Companies', 'Email Finder', 'Email Verifier'] | select |
| ExportFilters | filter-date-from | From date |  | date |
| ExportFilters | filter-date-to | To date |  | date |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| ExportListTable | No exports yet. Create a new export from the Contacts page. | export-empty | empty-state |
| ExportTableRow | Pending — waiting to start | export-status-pending | status |
| ExportTableRow | Processing — {row}% | export-status-processing | status |
| ExportTableRow | Completed — {rowCount} rows exported | export-status-complete | success |


### checkboxes



### radio_buttons



### progress_bars

| component | id | label | polling_interval | purpose | type |
| --- | --- | --- | --- | --- | --- |
| ExportTableRow | export-row-progress | Export row progress | 3s | Shows rows processed vs total for active exports | determinate |


### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| ExportListTable | export-download-flow | Export download flow | ['Export created from Contacts or Companies page', "ExportListTable shows 'Processing' + progress bar", 'Auto-polls every 3s (useExportPage)', "On completion: 'Download' button appears", 'exportsServi |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/export/ExportFilters.tsx | ExportFilters | Status and type filter dropdowns + date range |
| components/features/export/ExportListTable.tsx | ExportListTable | Paginated table of exports with status and actions |
| components/features/export/ExportTableRow.tsx | ExportTableRow | Single row: status badge, progress bar, download/cancel |
| components/features/export/ExportDeleteModal.tsx | ExportDeleteModal | Confirm deletion of export record |
| components/features/export/ExportMessages.tsx | ExportMessages | Toast messages for export actions |
| components/features/export/S3FileBrowser.tsx | S3FileBrowser | Admin-only S3 file tree browser (S3 tab) |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useExport.ts | useExportPage | Export list with 3s polling for active exports; filter state |
| hooks/useExport.ts | useExportManager | Download, cancel, delete individual exports |
| hooks/useS3Files.ts | useS3Files | S3 file listing for admin S3 tab |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/exportsService.ts | exportsService | ['Exports', 'GetExport', 'CancelExport', 'DeleteExport'] |
| services/graphql/s3Service.ts | s3Service | ['S3ListFiles'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/RoleContext.tsx | RoleContext | S3 tab + Delete All visibility (admin/superAdmin) |


### utilities



### ui_components



### endpoints

| condition | hook | method | operation | service |
| --- | --- | --- | --- | --- |
|  | useExportPage | QUERY | Exports | exportsService |
|  | useExportManager | QUERY | GetExport | exportsService |
|  | useExportManager | MUTATION | CancelExport | exportsService |
| admin/superAdmin only | useS3Files | QUERY | S3ListFiles | s3Service |


## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| create-export | Create Export | primary | navigate to /contacts (Pro+) | PageHeader |
| download-export | Download | secondary | exportsService.GetExport → presigned URL | ExportTableRow |
| cancel-export | Cancel | danger | exportsService.CancelExport → ConfirmModal | ExportTableRow |
| delete-export | Delete | danger | open ExportDeleteModal | ExportTableRow |
| delete-all | Delete All | danger | bulk delete all exports → ConfirmModal | PageHeader |
| apply-filter | Apply | primary | useExportPage.applyFilters() | ExportFilters |


### inputs

| id | label | type | options | component |
| --- | --- | --- | --- | --- |
| filter-status | Status | select | ['All', 'Pending', 'Processing', 'Completed', 'Failed', 'Cancelled'] | ExportFilters |
| filter-type | Type | select | ['All', 'Contacts', 'Companies', 'Email Finder', 'Email Verifier'] | ExportFilters |
| filter-date-from | From date | date |  | ExportFilters |
| filter-date-to | To date | date |  | ExportFilters |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | polling_interval | component |
| --- | --- | --- | --- | --- | --- |
| export-row-progress | Export row progress | Shows rows processed vs total for active exports | determinate | 3s | ExportTableRow |


### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useExport.ts | useExportPage | Export list with 3s polling for active exports; filter state |
| hooks/useExport.ts | useExportManager | Download, cancel, delete individual exports |
| hooks/useS3Files.ts | useS3Files | S3 file listing for admin S3 tab |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/exportsService.ts | exportsService | ['Exports', 'GetExport', 'CancelExport', 'DeleteExport'] |
| services/graphql/s3Service.ts | s3Service | ['S3ListFiles'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/Exports, graphql/GetExport, graphql/CancelExport, graphql/S3ListFiles | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: exportsService, s3Service
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useExportPage, useExportManager, useS3Files -> exportsService, s3Service -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **3.x** — Contact & company data — VQL tables, export modals, files, prospect finder narrative.
- **6.x** — Reliability & scaling — analytics, activities, jobs, status, error/retry/skeleton patterns.
- **Status** — Planned or spec-only; confirm `page.tsx` exists before treating as shipped.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/export *(planned)*`

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
- [contacts_page](contacts_page.md)
- [dashboard_page](dashboard_page.md)
- [dashboard_pageid_page](dashboard_pageid_page.md)
- [deployment_page](deployment_page.md)
- [email_page](email_page.md)
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
| `Exports` | [list_exports_graphql.md](../../backend/endpoints/list_exports_graphql.md) | QUERY | 3.x |
| `GetExport` | [query_get_export_graphql.md](../../backend/endpoints/query_get_export_graphql.md) | QUERY | 3.x |
| `CancelExport` | [mutation_cancel_export_graphql.md](../../backend/endpoints/mutation_cancel_export_graphql.md) | MUTATION | 4.x |
| `S3ListFiles` | [query_list_s3_files_graphql.md](../../backend/endpoints/query_list_s3_files_graphql.md) | QUERY | 2.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
