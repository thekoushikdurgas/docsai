---
title: "Files"
page_id: files_page
source_json: files_page.json
generator: json_to_markdown.py
---

# Files

> **Export listing:** A standalone **My Exports** hub is planned — [export_page.md](export_page.md). This page handles S3 file browser and creating jobs from stored files.

## Overview

- **page_id:** files_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 3.x, 6.x, 8.x, 11.x
- **flow_id:** files
- **_id:** files_page-001

## Metadata

- **route:** /files
- **file_path:** contact360.io/app/app/(dashboard)/files/page.tsx
- **purpose:** Cloud storage and dataset management page for S3-backed files. Supports browsing S3 tree, previewing CSV datasets, viewing schema and stats, and creating exports/import jobs from existing files.
- **s3_key:** data/pages/files_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate in the dashboard layout)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-12T00:00:00.000000+00:00
- `graphql/ListBucketObjects` — List S3 objects with prefix filtering. Supports tree-building logic. Via useFiles hook.
- `graphql/GetPresignedUploadUrl` — Request S3 presigned URL for multipart upload. Via useCsvUpload hook.
- `graphql/GetS3FileDownloadUrl` — Request S3 presigned URL for secure retrieval. Via s3Service.
- `graphql/DeleteS3File` — Delete object from storage. Via s3Service.
- `graphql/CreateEmailFinderExport` — Trigger email finder job on existing file.
- `graphql/CreateEmailVerifyExport` — Trigger email verification job on existing file.
- `graphql/CreateContact360Import` — Trigger platform import from CSV.
- `graphql/CreateAppointmentImport` — Trigger appointment system import.
### UI components (metadata)

- **FilesPage** — `app/(dashboard)/files/page.tsx`
- **FilesToolbar** — `components/files/FilesToolbar.tsx`
- **FilesSidebar** — `components/files/FilesSidebar.tsx`
- **FilesDetailView** — `components/files/FilesDetailView.tsx`
- **FilesUploadModal** — `components/files/FilesUploadModal.tsx` (Dynamic)
- **FilesCreateJobModal** — `components/files/FilesCreateJobModal.tsx` (Dynamic)
- **FilesPeekModal** — `components/files/FilesPeekModal.tsx` (Dynamic)
- **FilesDownloadModal** — `components/files/FilesDownloadModal.tsx` (Dynamic)
- **FilesEmptyState** — `components/files/FilesEmptyState.tsx`
- **LoadingSpinner** — `components/shared/LoadingSpinner.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **ConfirmModal** — `components/ui/ConfirmModal.tsx`
- **FilesDownloadModal** — `components/files/FilesDownloadModal.tsx`
- **ConfirmModal** — `components/ui/ConfirmModal.tsx`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Files

### description

Cloud storage and dataset management page for S3-backed files. Supports browsing S3 tree, previewing CSV datasets, viewing schema and stats, and creating exports/import jobs from existing files.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| files-title | 1 | Files |
| storage-overview | 2 | Storage |
| dataset-detail | 2 | Dataset Details |


### subheadings

| id | level | text |
| --- | --- | --- |
| file-preview | 3 | Preview |
| file-schema | 3 | Schema |
| file-stats | 3 | Column Statistics |


### tabs

| content_ref | id | label | location |
| --- | --- | --- | --- |
| file-data-preview | preview | Preview | FilesDetailView |
| file-schema-panel | schema | Schema | FilesDetailView |
| file-column-stats | stats | Stats | FilesDetailView |
| file-dataset-info | info | Info | FilesDetailView |


### buttons

| action | component | id | label | type | era |
| --- | --- | --- | --- | --- | --- |
| setUploadModalOpen(true) | FilesToolbar | upload-btn | Upload File | primary | 3.x |
| handleRefresh | FilesToolbar | refresh-btn | Refresh | icon | 0.x |
| onFileSelect | FilesSidebar | select-file | [File Name] | text | 0.x |
| setPeekRow | FilesSidebar | peek-btn | Peek | ghost | 8.x |
| setDownloadRow | FilesSidebar | download-btn | Download | ghost | 8.x |
| setDeleteConfirmNode | FilesSidebar | delete-btn | Delete | ghost/danger | 8.x |
| handleDownload | FilesDownloadModal | confirm-download | Download | primary | 8.x |
| handleCreateJobFromFile | FilesCreateJobModal | confirm-job | Create Job | primary | 3.x |
| csvUpload.start | FilesUploadModal | start-upload | Upload | primary | 6.x |


### input_boxes

| accept | component | id | label | placeholder | required | type |
| --- | --- | --- | --- | --- | --- | --- |
|  | FilesToolbar | file-search | Search files | Search by filename |  | search |
| .csv | FilesUploadModal | file-upload-input | CSV file |  | True | file |
|  | FilesDownloadModal | download-rows | Number of rows | e.g. 100 |  | number |
|  | FilesCreateJobModal | column-map-first-name | First Name column |  |  | select |
|  | FilesCreateJobModal | column-map-last-name | Last Name column |  |  | select |
|  | FilesCreateJobModal | column-map-domain | Domain column |  |  | select |
|  | FilesCreateJobModal | column-map-email | Email column |  |  | select |


### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| FilesEmptyState | No files uploaded yet. Upload a CSV to get started. | files-empty | empty-state |
| DatasetInfoPanel | {rowCount} rows · {fileSize} | file-row-count | stat |
| DatasetInfoPanel | Uploaded {uploadDate} | file-upload-date | caption |


### checkboxes



### radio_buttons

| component | id | label | options | purpose | era |
| --- | --- | --- | --- | --- | --- |
| FilesCreateJobModal | job-type-toggle | Job Type | ['Email Finder', 'Email Verifier', 'Import'] | Job configuration | 3.x |
| FilesDownloadModal | download-scope | Range | ['All', 'Filtered', 'Selection'] | Partial retrieval | 8.x |


### progress_bars

| component | id | label | purpose | type |
| --- | --- | --- | --- | --- |
| FilesUploadModal | upload-progress | Upload progress | Multipart S3 upload progress per file | determinate |


### graphs

| chart_type | component | data_source | id | label | x_axis | y_axis |
| --- | --- | --- | --- | --- | --- | --- |
| horizontal_mini_bar | FilesColumnStatsPanel | useFileStats | column-null-rate | Null rate per column | Column name | Null % |
| horizontal_mini_bar | FilesColumnStatsPanel | useFileStats | column-unique-rate | Unique value rate per column |  |  |


### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| FilesPage | upload-to-job-flow | Upload CSV → create job | ["Click 'Upload File' → FilesUploadModal", 'Drag-and-drop or click CSV', 's3Service.GetPresignedUploadUrl → multipart upload', 'Upload progress bar', 'File appears in FilesSidebar tree', 'Select file  |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/files/FilesToolbar.tsx | FilesToolbar | Upload button + search + view controls |
| components/files/FilesSidebar.tsx | FilesSidebar | S3 tree browser (prefix folders + files) |
| components/files/FilesDetailView.tsx | FilesDetailView | Right panel: Preview/Schema/Stats/Info tabs |
| components/files/FilesUploadModal.tsx | FilesUploadModal | Drag-and-drop CSV upload with progress bar |
| components/files/FilesCreateJobModal.tsx | FilesCreateJobModal | Job type radio + column mapping selects |
| components/files/FilesPeekModal.tsx | FilesPeekModal | Quick preview of first rows |
| components/files/FilesDownloadModal.tsx | FilesDownloadModal | Download scope radio + format radio + rows input |
| components/files/DataPreviewTable.tsx | DataPreviewTable | Paginated first-N rows table |
| components/files/FilesSchemaPanel.tsx | FilesSchemaPanel | Column name + inferred type badges |
| components/files/FilesColumnStatsPanel.tsx | FilesColumnStatsPanel | Per-column null% and unique% mini bars |
| components/files/DatasetInfoPanel.tsx | DatasetInfoPanel | File metadata: rows, size, S3 key, upload date |
| components/files/FilesEmptyState.tsx | FilesEmptyState | Empty state with upload CTA |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useFiles.ts | useFiles | S3 tree construction and prefix filtering | 3.x |
| hooks/useFilePreview.ts | useFilePreview | Partial row retrieval and schema extraction | 3.x |
| hooks/useFileStats.ts | useFileStats | Backend metrics (row counts, size) | 6.x |
| hooks/useCsvUpload.ts | useCsvUpload | Multipart upload management | 3.x |
| hooks/useBucketMetadata.ts | useBucketMetadata | Syncing `metadata.json` for rich dataset info | 8.x |
| context/AuthContext.ts | useAuth | Authenticated user identity for S3 key naming | 0.x |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/s3Service.ts | s3Service | ['GetPresignedUploadUrl', 'ListBucketObjects', 'GetPresignedDownloadUrl', 'DeleteObject'] |
| services/graphql/jobsService.ts | jobsService | ['CreateJob'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User scoped S3 prefix |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/s3/s3TreeUtils.ts | s3TreeUtils | Build tree structure from S3 prefix keys for sidebar |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useCsvUpload | QUERY | GetPresignedUploadUrl | s3Service |
| useFiles | QUERY | ListBucketObjects | s3Service |
| useFiles | QUERY | GetPresignedDownloadUrl | s3Service |
| useNewExport | MUTATION | CreateJob | jobsService |


## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| upload-file | Upload File | primary | open FilesUploadModal | FilesToolbar |
| create-job | Create Job | secondary | open FilesCreateJobModal | FilesDetailView |
| peek-file | Peek | ghost | open FilesPeekModal | FilesSidebar |
| download-file | Download | secondary | open FilesDownloadModal | FilesDetailView |
| delete-file | Delete | danger | open ConfirmModal → s3Service.DeleteObject | FilesDetailView |
| confirm-upload | Upload | primary | s3Service.GetPresignedUploadUrl → multipart upload | FilesUploadModal |
| confirm-download | Download | primary | s3Service.GetPresignedDownloadUrl | FilesDownloadModal |
| confirm-job-create | Create Job | primary | jobsService.CreateJob | FilesCreateJobModal |


### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| file-search | Search files | search | Search by filename | FilesToolbar |
| file-upload-input | CSV file | file |  | FilesUploadModal |
| download-rows | Number of rows | number | e.g. 100 | FilesDownloadModal |
| column-map-first-name | First Name column | select |  | FilesCreateJobModal |
| column-map-last-name | Last Name column | select |  | FilesCreateJobModal |
| column-map-domain | Domain column | select |  | FilesCreateJobModal |
| column-map-email | Email column | select |  | FilesCreateJobModal |


### checkboxes

[]

### radio_buttons

| id | label | options | purpose | component |
| --- | --- | --- | --- | --- |
| job-type | Job type | ['Email Finder', 'Email Verifier'] | Choose what operation to run on the CSV file | FilesCreateJobModal |
| download-scope | Download scope | ['All rows', 'Filtered rows', 'First N rows'] | Choose which rows to download | FilesDownloadModal |
| download-format | Format | ['CSV', 'Excel (XLSX)'] | Choose output file format for download | FilesDownloadModal |


### progress_bars

| id | label | purpose | type | component |
| --- | --- | --- | --- | --- |
| upload-progress | Upload progress | Multipart S3 upload progress per file | determinate | FilesUploadModal |


### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useFiles.ts | useFiles | File list, selection, delete |
| hooks/useCsvUpload.ts | useCsvUpload | File select, validate, S3 multipart upload |
| hooks/useFilePreview.ts | useFilePreview | Fetch first N rows for preview |
| hooks/useFileStats.ts | useFileStats | Per-column statistics (null %, unique %) |
| hooks/useBucketMetadata.ts | useBucketMetadata | S3 bucket tree structure |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/s3Service.ts | s3Service | ['GetPresignedUploadUrl', 'ListBucketObjects', 'GetPresignedDownloadUrl', 'DeleteObject'] |
| services/graphql/jobsService.ts | jobsService | ['CreateJob'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql module operations (page-specific) | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: s3Service, jobsService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useFiles, useCsvUpload, useFilePreview, useFileStats -> s3Service, jobsService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app layout, sidebar navigation, breadcrumb logic, toast system.
- **3.x** — Contact & company data — CSV-to-job loop, column mapping, multipart uploads.
- **6.x** — Reliability & scaling — background sync, progress bars, error handling, ConfirmModal patterns.
- **8.x** — Public & private APIs — S3 secure retrieval, presigned link generation, object intelligence (Peek).

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:CloudStorage] > [H:Header] + [T:Toolbar] + [S:Sidebar] + [Q:MainContent] > [V:DetailView] + [M:Modals] -> {useFiles, useFilePreview, useCsvUpload}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/files`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions.

**Typical outbound:** Sidebar peers; [jobs_page.md](jobs_page.md) (after job creation from file).

**Cross-host:** S3-backed assets shared with **email** (Mailhub) for attachment handling.
**Backend:** Appointment360 GraphQL gateway; S3 storage management and job creation services.

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
- [export_page](export_page.md)
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
| `ListBucketObjects` | *unresolved — add to endpoint index* | — | — |
| `GetPresignedUploadUrl` | *unresolved — add to endpoint index* | — | — |
| `GetS3FileDownloadUrl` | [query_get_s3_file_presigned_url_graphql.md](../../backend/endpoints/query_get_s3_file_presigned_url_graphql.md) | QUERY | 2.x |
| `DeleteS3File` | *unresolved — add to endpoint index* | — | — |
| `CreateEmailFinderExport` | *unresolved — add to endpoint index* | — | — |
| `CreateEmailVerifyExport` | *unresolved — add to endpoint index* | — | — |
| `CreateContact360Import` | *unresolved — add to endpoint index* | — | — |
| `CreateAppointmentImport` | *unresolved — add to endpoint index* | — | — |

**Unresolved operations** (not found in `index.md` / `endpoints_index.md`):
`graphql/ListBucketObjects`, `graphql/GetPresignedUploadUrl`, `graphql/DeleteS3File`, `graphql/CreateEmailFinderExport`, `graphql/CreateEmailVerifyExport`, `graphql/CreateContact360Import`, `graphql/CreateAppointmentImport`

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
