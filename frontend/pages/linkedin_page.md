---
title: "LinkedIn"
page_id: linkedin_page
source_json: linkedin_page.json
generator: json_to_markdown.py
---

# LinkedIn

## Overview

- **page_id:** linkedin_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 4.x, 8.x, 11.x
- **flow_id:** linkedin
- **_id:** linkedin_page-001

## Metadata

- **route:** /linkedin
- **file_path:** contact360.io/app/app/(dashboard)/linkedin/page.tsx
- **purpose:** LinkedIn Studio for professional networking enrichment, data extraction (single/bulk), and CSV batch processing.
- **status:** shipped
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** Access gated for ProEngine v4; Free users have monthly extraction limits (5 per month).
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00Z

### uses_endpoints (4)

- `graphql/SearchByLinkedInUrl` — Search contacts and companies by single LinkedIn URL. Used in Search tab. linkedin.search mutation.
- `graphql/ExportByLinkedInUrls` — Export contacts/companies from LinkedIn URLs. Used in Paste tab and Upload tab (after CSV mapping). Creates export job.
- `graphql/UpsertByLinkedInUrl` — Upsert single contact/company from LinkedIn URL. Used for add-to-Connectra flow.
- `graphql/GetExport` — Get export status and download URL. Used for polling and download after exportByLinkedInUrls.

### UI components (metadata)

- **LinkedInPage** — `app/(dashboard)/linkedin/page.tsx`
- **Button** — `components/ui/Button.tsx`
- **Input** — `components/ui/Input.tsx`
- **Badge** — `components/ui/Badge.tsx`
- **Modal** — `components/ui/Modal.tsx`
- **Tabs** — `components/ui/Tabs.tsx`
- **InfoCard** — (Internal detail card)
- **MappingModal** — (Internal CSV mapping)

- **versions:** []
- **endpoint_count:** 4

### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

LinkedIn

### description

LinkedIn tools page with Search, Upload, and Paste tabs. Search by single URL; upload CSV with column mapping; paste URLs for bulk export. UsageCounter for free users. Sections gated via DashboardComponentGuard.

## Sections (UI structure)

### headings

### subheadings

### tabs

| content_ref | id | label |
| --- | --- | --- |
| linkedin-search | search | Search |
| linkedin-upload | upload | Upload |
| linkedin-paste | paste | Paste |

### era

4.x

### buttons

| action | component | id | label | loading_state | tab | type |
| --- | --- | --- | --- | --- | --- | --- |
| linkedinService.SearchByLinkedInUrl | LinkedInSearchTab | search-linkedin | Search | Searching... | search | primary |
| linkedinService.UpsertByLinkedInUrl | LinkedInSearchTab | add-to-contacts | Add to Contacts |  | search | secondary |
| open file input → LinkedInCsvMappingModal | LinkedInUploadTab | upload-csv | Upload CSV |  | upload | primary |
| linkedinService.ExportByLinkedInUrls → job created | LinkedInUploadTab | export-urls | Export |  | upload | primary |
| linkedinService.ExportByLinkedInUrls (pasted URLs) | LinkedInPasteTab | paste-submit | Export All |  | paste | primary |
| exportService.GetExport → download URL | LinkedInPage | download-result | Download |  |  | secondary |

### input_boxes

- **[0]**
  - **id:** linkedin-url-single
  - **label:** LinkedIn URL
  - **type:** url
  - **placeholder:** https://linkedin.com/in/username
  - **required:** True
  - **validation:** LinkedIn URL format
  - **component:** LinkedInSearchTab
  - **tab:** search

- **[1]**
  - **id:** linkedin-csv-upload
  - **label:** CSV with LinkedIn URLs
  - **type:** file
  - **accept:** .csv
  - **required:** True
  - **component:** LinkedInUploadTab
  - **tab:** upload

- **[2]**
  - **id:** linkedin-url-column
  - **label:** LinkedIn URL column
  - **type:** select
  - **placeholder:** Select column
  - **component:** LinkedInCsvMappingModal

- **[3]**
  - **id:** linkedin-paste-input
  - **label:** LinkedIn URLs (one per line)
  - **type:** textarea
  - **placeholder:** https://linkedin.com/in/name1
https://linkedin.com/in/name2
  - **rows:** 8
  - **component:** LinkedInPasteTab
  - **tab:** paste

### text_blocks

| component | content | id | type | visibility |
| --- | --- | --- | --- | --- |
| UsageCounter | {used}/{limit} LinkedIn lookups | usage-counter | stat | free users |
| LinkedInSearchTab | Found: {contactName} at {company} | search-result | result |  |
| LinkedInPage | Processing {count} URLs... | export-job-status | status |  |

### checkboxes

### radio_buttons

### progress_bars

| component | id | label | polling_interval | purpose | type |
| --- | --- | --- | --- | --- | --- |
| LinkedInPage | export-progress | LinkedIn export progress | 10s | Tracks export job status while URLs are being enriched | determinate |

### graphs

### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| LinkedInUploadTab | bulk-linkedin-flow | Bulk LinkedIn URL enrichment | ['Upload CSV or paste URLs in bulk', 'Map LinkedIn URL column in CSV', 'linkedinService.ExportByLinkedInUrls → job created', 'Poll exportService.GetExport for job status', 'On completion: Download res |

### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/linkedin/LinkedInHeader.tsx | LinkedInHeader | Page title and usage counter |
| components/features/linkedin/LinkedInTabNavigation.tsx | LinkedInTabNavigation | Search / Upload / Paste tab switcher |
| components/features/linkedin/LinkedInSearchTab.tsx | LinkedInSearchTab | Single URL input + search + result display |
| components/features/linkedin/LinkedInUploadTab.tsx | LinkedInUploadTab | CSV file upload + column mapping + export |
| components/features/linkedin/LinkedInPasteTab.tsx | LinkedInPasteTab | Multi-line URL textarea + bulk export |
| components/features/linkedin/LinkedInCsvMappingModal.tsx | LinkedInCsvMappingModal | Column mapping for CSV upload |
| components/shared/UsageCounter.tsx | UsageCounter | Remaining LinkedIn lookups (free users) |

### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| context/AuthContext.ts | useAuth | User role and usage limit tracking | 0.x |
| hooks/useLinkedIn.ts | useLinkedIn | LinkedIn data extraction and job management | 4.x |

### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/linkedinService.ts | linkedinService | ['SearchByLinkedInUrl', 'ExportByLinkedInUrls', 'UpsertByLinkedInUrl', 'GetExport'] |

### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/RoleContext.tsx | RoleContext | DashboardComponentGuard gating of tabs; UsageCounter for free users |

### utilities

### ui_components

### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useLinkedIn | MUTATION | SearchByLinkedInUrl | linkedinService |
| useLinkedIn | MUTATION | ExportByLinkedInUrls | linkedinService |
| useLinkedIn | MUTATION | UpsertByLinkedInUrl | linkedinService |
| useLinkedIn | QUERY | GetExport | exportService |

## UI elements (top-level)

### buttons

| id | label | type | action | loading_state | component | tab |
| --- | --- | --- | --- | --- | --- | --- |
| search-linkedin | Search | primary | linkedinService.SearchByLinkedInUrl | Searching... | LinkedInSearchTab | search |
| add-to-contacts | Add to Contacts | secondary | linkedinService.UpsertByLinkedInUrl |  | LinkedInSearchTab | search |
| upload-csv | Upload CSV | primary | open file input → LinkedInCsvMappingModal |  | LinkedInUploadTab | upload |
| export-urls | Export | primary | linkedinService.ExportByLinkedInUrls → job created |  | LinkedInUploadTab | upload |
| paste-submit | Export All | primary | linkedinService.ExportByLinkedInUrls (pasted URLs) |  | LinkedInPasteTab | paste |
| download-result | Download | secondary | exportService.GetExport → download URL |  | LinkedInPage |  |

### inputs

| id | label | type | placeholder | required | validation | component | tab |
| --- | --- | --- | --- | --- | --- | --- | --- |
| linkedin-url-single | LinkedIn URL | url | https://linkedin.com/in/username | True | LinkedIn URL format | LinkedInSearchTab | search |
| linkedin-csv-upload | CSV with LinkedIn URLs | file |  | True |  | LinkedInUploadTab | upload |
| linkedin-url-column | LinkedIn URL column | select | Select column |  |  | LinkedInCsvMappingModal |  |
| linkedin-paste-input | LinkedIn URLs (one per line) | textarea | https://linkedin.com/in/name1
https://linkedin.com/in/name2 |  |  | LinkedInPasteTab | paste |

### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | polling_interval | component |
| --- | --- | --- | --- | --- | --- |
| export-progress | LinkedIn export progress | Tracks export job status while URLs are being enriched | determinate | 10s | LinkedInPage |

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useLinkedIn.ts | useLinkedIn | LinkedIn search, export, upsert mutations; export status polling |

## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/linkedinService.ts | linkedinService | ['SearchByLinkedInUrl', 'ExportByLinkedInUrls', 'UpsertByLinkedInUrl', 'GetExport'] |

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/SearchByLinkedInUrl, graphql/ExportByLinkedInUrls, graphql/UpsertByLinkedInUrl, graphql/GetExport | dashboard data and mutations via services/hooks |

## Data Sources

- Appointment360 GraphQL gateway
- Service modules: linkedinService
- Backend-owned data stores (via GraphQL modules)

## Flow summary

app page UI -> useLinkedIn -> linkedinService -> GraphQL gateway -> backend modules -> rendered states

<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **4.x** — Extension & Sales Navigator — LinkedIn dashboard page, Chrome extension marketing, SN workflows.
- **8.x** — Public & private APIs — API docs, integrations story, export contracts, developer surfaces.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H:Header] + [B:Banner] + [K:Card] + [G:InfoGrid] -> {useAuth, useLinkedIn}

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/linkedin`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions.

**Typical outbound:** Sidebar peers; [contacts_page.md](contacts_page.md) (Search -> Add to Contacts); [export_page.md](export_page.md) (Bulk CSV status).

**Cross-host:** Prospect data extracted via LinkedIn is enriched by **email** (Mailhub) for corporate email identification.
**Backend:** Appointment360 GraphQL gateway; proEngine v4 for headless browser orchestration and SN sync.

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
- [jobs_page](jobs_page.md)
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
| `SearchByLinkedInUrl` | [mutation_search_linkedin_graphql.md](../../backend/endpoints/mutation_search_linkedin_graphql.md) | MUTATION | 4.x |
| `ExportByLinkedInUrls` | [mutation_export_linkedin_results_graphql.md](../../backend/endpoints/mutation_export_linkedin_results_graphql.md) | MUTATION | 4.x |
| `UpsertByLinkedInUrl` | [mutation_upsert_by_linkedin_url_graphql.md](../../backend/endpoints/mutation_upsert_by_linkedin_url_graphql.md) | MUTATION | 4.x |
| `GetExport` | [query_get_export_graphql.md](../../backend/endpoints/query_get_export_graphql.md) | QUERY | 3.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
