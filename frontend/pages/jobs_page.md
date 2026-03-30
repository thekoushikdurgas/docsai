---
title: "Jobs"
page_id: jobs_page
source_json: jobs_page.json
generator: json_to_markdown.py
---

# Jobs

> **Export hub:** A dedicated `/export` management page is **planned** only — see [export_page.md](export_page.md). Live export job creation and status live on this route.

## Overview

- **page_id:** jobs_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 6.x, 8.x, 11.x
- **flow_id:** jobs
- **_id:** jobs_page-001

## Metadata

- **route:** /jobs
- **file_path:** contact360.io/app/app/(dashboard)/jobs/page.tsx
- **purpose:** Background jobs dashboard showing export/import and enrichment jobs. Includes cards/table views, filters, pagination, retry, download, and new export creation.
- **s3_key:** data/pages/jobs_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate in the dashboard layout)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
- `graphql/ListJobs` — List scheduler jobs via jobs.list. Support pagination (limit/offset) and filters (status, jobType). Via useJobs hook.
- `graphql/GetJob` — Get single job details via jobs.get. Used for expanded view and deep-dive metadata.
- `graphql/RetryJob` — Request job retry via jobs.retry mutation. Supports retry interval and run-after scheduling.
- `graphql/S3FileDownloadUrl` — Get presigned URL for S3 result files. Via s3Service.getS3FileDownloadUrl.
- `graphql/CreateJob` — Create new storage-backed job (export/import). Via useNewExport mutation loop.

### UI components (metadata)

- **JobsPage** — `app/(dashboard)/jobs/page.tsx`
- **JobsHeader** — `components/jobs/JobsHeader.tsx`
- **JobsPipelineStats** — `components/jobs/JobsPipelineStats.tsx`
- **JobsFilters** — `components/jobs/JobsFilters.tsx`
- **JobsCard** — `components/jobs/JobsCard.tsx`
- **JobsTable** — `components/jobs/JobsTable.tsx`
- **JobDetailsModal** — `components/jobs/JobDetailsModal.tsx`
- **ScheduleJobModal** — `components/jobs/ScheduleJobModal.tsx`
- **JobsRetryModal** — `components/jobs/JobsRetryModal.tsx`
- **JobsPagination** — `components/jobs/JobsPagination.tsx`
- **LottiePlayer** — `components/shared/LottiePlayer.tsx`
- **JobsCardExpandPanel** — `components/jobs/JobsCardExpandPanel.tsx`
- **JobDetailsModal** — `components/jobs/JobDetailsModal.tsx`
- **ScheduleJobModal** — `components/jobs/ScheduleJobModal.tsx`
- **JobsRetryModal** — `components/jobs/JobsRetryModal.tsx`
- **Modal** — `components/ui/Modal.tsx`
- **LottiePlayer** — `components/shared/LottiePlayer.tsx`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Jobs

### description

Background jobs dashboard showing export/import and enrichment jobs. Includes cards/table views, filters, pagination, retry, download, and new export creation.

## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| jobs-title | 1 | Jobs |
| pipeline-stats | 2 | Pipeline Overview |
| jobs-list | 2 | Job Queue |

### subheadings

| id | level | text |
| --- | --- | --- |
| jobs-active | 3 | Active Jobs |
| jobs-completed | 3 | Completed Jobs |

### tabs

| content_ref | id | label |
| --- | --- | --- |
| jobs-cards-view | cards | Cards |
| jobs-table-view | table | Table |

### buttons

| action | component | id | label | type | era |
| --- | --- | --- | --- | --- | --- |
| newExport.setModalOpen(true) | JobsHeader | initial-job-btn | New Export | primary | 6.x |
| setScheduleModalOpen(true) | JobsHeader | schedule-job-btn | Schedule | secondary | 6.x |
| refetch | JobsHeader | resync-btn | Refresh | icon | 0.x |
| openRetryModal | JobsCard | retry-btn | Retry | secondary | 6.x |
| handleDownload | JobsCard | download-btn | Download | secondary | 6.x |
| setDetailsModalJob | JobsCard | details-btn | View Details | ghost | 6.x |
| toggleExpand | JobsCard | expand-btn | Expand | icon | 6.x |
| handleRetryConfirm | JobsRetryModal | confirm-retry | Request Retry | primary | 6.x |
| newExport.onSubmit | Modal | submit-job | Create Job | primary | 6.x |

### input_boxes

| component | id | label | placeholder | type |
| --- | --- | --- | --- | --- |
| JobsHeader | jobs-search | Search jobs | Search by job name or ID | search |
| ScheduleJobModal | cron-expression | Cron expression | 0 0 * * * (daily midnight) | text |
| ScheduleJobModal | schedule-datetime | Run at |  | datetime-local |

### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| JobsEmptyState | No jobs yet. Create a new export from the Files page to get started. | jobs-empty | empty-state |
| JobsCard | {jobName} — {jobType} | job-name | label |
| JobsCard | Created {createdAt} · {elapsed} elapsed | job-created | caption |

### checkboxes

### radio_buttons

| component | id | label | options | purpose | era |
| --- | --- | --- | --- | --- | --- |
| JobsFilters | status-filter | Status | ['All', 'Processing', 'Completed', 'Failed'] | List filtering | 6.x |
| JobsFilters | type-filter | Type | ['All', 'Export', 'Import', 'Enrichment'] | List filtering | 6.x |
| JobsFilters | view-mode | View | ['Cards', 'Table'] | Layout toggle | 0.x |

### progress_bars

| component | id | label | polling_interval | purpose | era |
| --- | --- | --- | --- | --- | --- |
| JobsCard | job-progress | Job processing progress | 15s | Row-level progress | 6.x |
| JobsHeader | sync-progress | Synchronizing... |  | Background sync status | 6.x |
| JobsPipelineStats | throughput-bar | Pipeline throughput |  | Aggregate success rate | 6.x |

### graphs

| chart_type | component | data_source | id | label | metrics |
| --- | --- | --- | --- | --- | --- |
| horizontal_bar | JobsPipelineStats | jobsService.ListJobs aggregated | pipeline-stats | Jobs pipeline statistics | ['processed', 'failed', 'pending', 'total'] |

### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| ExecutionFlow | job-execution-flow | Job execution flow | ['Job created (from Files page or email bulk)', "JobsCard shows 'Processing' status + progress bar", 'useJobs polls every 15s', 'ExecutionFlow shows step nodes: upload → parse → process → output', "On |

### components

| file_path | name | purpose |
| --- | --- | --- |
| components/jobs/JobsHeader.tsx | JobsHeader | Title + New Export button + search + view toggle |
| components/jobs/JobsPipelineStats.tsx | JobsPipelineStats | Horizontal stacked bar: processed/failed/pending |
| components/jobs/JobsFilters.tsx | JobsFilters | Status and type filter radio/select controls |
| components/jobs/JobsCard.tsx | JobsCard | Compact card with status badge, progress bar, expand |
| components/jobs/JobsCardExpandPanel.tsx | JobsCardExpandPanel | Expanded detail with stats, download, retry |
| components/jobs/JobsTable.tsx | JobsTable | Tabular job list with sortable columns |
| components/jobs/JobDetailsModal.tsx | JobDetailsModal | Full modal: Summary / Logs / Data tabs |
| components/jobs/JobsRetryModal.tsx | JobsRetryModal | Retry scope radio (all / failed only) |
| components/jobs/ScheduleJobModal.tsx | ScheduleJobModal | Schedule frequency + datetime/cron input |
| components/jobs/ExecutionFlow.tsx | ExecutionFlow | Step pipeline diagram: upload→parse→process→output |
| components/jobs/JobsEmptyState.tsx | JobsEmptyState | Empty state illustration with CTA |
| components/jobs/JobsCardSkeleton.tsx | JobsCardSkeleton | Loading skeleton for job cards |

### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useJobs.ts | useJobs | Paginated GQL job polling and management | 6.x |
| hooks/useExpandedJobDetails.ts | useExpandedJobDetails | Individual job detail extraction for expanded view | 6.x |
| hooks/useNewExport.ts | useNewExport | Modal state for CSV-to-Job creation | 3.x |
| hooks/useAuth.ts | useAuth | SuperAdmin feature gating (Imports) | 1.x |

### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User context for job ownership |

### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/jobs/jobsMapper.ts | jobsMapper | Map API job responses to UI models |
| lib/jobs/jobsUtils.ts | jobsUtils | getStatusLabel, getStatusColor, canRetry, canCancel |
| lib/jobs/jobsConstants.ts | jobsConstants | JOB_STATUS enum, JOB_TYPE enum |

### ui_components

### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useJobs | QUERY | ListJobs | jobsService |
| useJobs | QUERY | GetJob | jobsService |
| useJobs | MUTATION | RetryJob | jobsService |
| useJobs | MUTATION | CancelJob | jobsService |
| useJobs | MUTATION | ScheduleJob | jobsService |

## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| new-export | New Export | primary | open FilesCreateJobModal or navigate to /files | JobsHeader |
| retry-job | Retry | secondary | open JobsRetryModal → jobsService.RetryJob | JobsCard |
| cancel-job | Cancel | danger | jobsService.CancelJob → ConfirmModal | JobsCard |
| download-result | Download | secondary | s3Service.GetPresignedDownloadUrl | JobsCardExpandPanel |
| view-job-details | View Details | ghost | open JobDetailsModal | JobsCard |
| schedule-job | Schedule | ghost | open ScheduleJobModal | JobsCard |
| refresh-jobs | Refresh | icon | useJobs.refetch() | JobsHeader |
| clear-filter | Clear Filters | ghost | reset JobsFilters state | JobsFilters |

### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| jobs-search | Search jobs | search | Search by job name or ID | JobsHeader |
| cron-expression | Cron expression | text | 0 0 * * * (daily midnight) | ScheduleJobModal |
| schedule-datetime | Run at | datetime-local |  | ScheduleJobModal |

### checkboxes

[]

### radio_buttons

| id | label | options | purpose | component |
| --- | --- | --- | --- | --- |
| retry-scope | Retry scope | ['Retry All', 'Retry Failed Only'] | Choose which rows to reprocess on retry | JobsRetryModal |
| schedule-frequency | Schedule frequency | ['Run Once', 'Daily', 'Weekly', 'Custom (cron)'] | Choose job recurrence | ScheduleJobModal |
| jobs-status-filter | Status filter | ['All', 'Processing', 'Completed', 'Failed', 'Scheduled'] | Filter job list by status | JobsFilters |
| jobs-type-filter | Job type filter | ['All', 'Email Finder', 'Email Verifier', 'Contact Export', 'Company Export'] | Filter job list by type | JobsFilters |

### progress_bars

| id | label | purpose | type | polling_interval | component |
| --- | --- | --- | --- | --- | --- |
| job-progress | Job processing progress | Shows processed rows / total rows for active jobs | determinate | 15s | JobsCard |
| pipeline-stats-bar | Pipeline throughput bar | Total processed / failed / pending across all recent jobs | stacked |  | JobsPipelineStats |

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useJobs.ts | useJobs | Job list with 15s polling, retry, cancel |
| hooks/useExpandedJobDetails.ts | useExpandedJobDetails | Fetch logs and data for expanded job |

## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/jobsService.ts | jobsService | ['ListJobs', 'GetJob', 'RetryJob', 'CancelJob', 'ScheduleJob', 'GetJobLogs', 'GetJobData'] |
| services/graphql/s3Service.ts | s3Service | ['GetPresignedDownloadUrl'] |

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql module operations (page-specific) | dashboard data and mutations via services/hooks |

## Data Sources

- Appointment360 GraphQL gateway
- Service modules: jobsService, s3Service
- Backend-owned data stores (via GraphQL modules)

## Flow summary

app page UI -> useJobs, useExpandedJobDetails -> jobsService, s3Service -> GraphQL gateway -> backend modules -> rendered states

<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, generic sidebar, skeleton loaders, layout toggles.
- **6.x** — Reliability & scaling — background jobs, polling, retry modals, pipeline throughput stats.
- **8.x** — Public & private APIs — export contracts, S3 presigned downloads, backend binding parity.
- **10.x** — Email campaign — campaign jobs, automated sequence processing hubs.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:Dashboard] > [H:Header] + [Q:JobSummary] + [T:JobTable] -> {useJobs}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/jobs`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [files_page.md](files_page.md) (after job creation).

**Typical outbound:** Sidebar peers; [files_page.md](files_page.md) (downloading result files).

**Cross-host:** Job result metadata synced to **root** (Marketing) for public-facing success metrics if public.
**Backend:** Appointment360 GraphQL gateway; background worker and S3 storage integrations.

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
- [files_page](files_page.md)
- [finder_page](finder_page.md)
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
| `ListJobs` | [query_list_jobs_graphql.md](../../backend/endpoints/query_list_jobs_graphql.md) | QUERY | 4.x |
| `GetJob` | [query_get_job_graphql.md](../../backend/endpoints/query_get_job_graphql.md) | QUERY | 4.x |
| `RetryJob` | *unresolved — add to endpoint index* | — | — |
| `S3FileDownloadUrl` | *unresolved — add to endpoint index* | — | — |
| `CreateJob` | [mutation_create_job_graphql.md](../../backend/endpoints/mutation_create_job_graphql.md) | MUTATION | 4.x |

**Unresolved operations** (not found in `index.md` / `endpoints_index.md`): 
`graphql/RetryJob`, `graphql/S3FileDownloadUrl`

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
