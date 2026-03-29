---
title: "Email"
page_id: email_page
source_json: email_page.json
generator: json_to_markdown.py
---

# Email

## Overview

- **page_id:** email_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App (Dashboard)
- **era_tags:** 0.x, 2.x, 5.x, 8.x, 11.x
- **flow_id:** email
- **_id:** email_page-001

## Metadata

- **route:** /email
- **file_path:** contact360.io/app/app/(dashboard)/email/page.tsx
- **purpose:** Email Finder and Verifier page with Finder | Verifier tabs. Finder: single and bulk email search by name/domain. Verifier: single and bulk email verification with risk analysis.
- **s3_key:** data/pages/email_page.json
- **status:** published
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T10:30:00Z
### uses_endpoints (6)

- `graphql/FindEmails` — Find single email by first name, last name, domain.
- `graphql/FindEmailsBulk` — Bulk email finder export job creation.
- `graphql/VerifySingleEmail` — Verify a single email address for validity and risk.
- `graphql/VerifyEmailsBulk` — Bulk email verification export job creation.
- `graphql/AnalyzeEmailRisk` — AI-powered email risk analysis (Gemini).
- `graphql/GetActivities` — Get finder/verifier activity history.
- `graphql/GetEmailAssistantSuggestions` — AI suggestions for follow-ups (era 5.x).

### UI components (metadata)

- **EmailPage** — `app/(dashboard)/email/page.tsx`
- **EmailFinderSingle** — `components/email/EmailFinderSingle.tsx`
- **EmailVerifierSingle** — `components/email/EmailVerifierSingle.tsx`
- **EmailBulkDropZone** — `components/email/EmailBulkDropZone.tsx`
- **EmailAssistantPanel** — `components/email/EmailAssistantPanel.tsx`
- **EmailCreditsBanner** — `components/email/EmailCreditsBanner.tsx`
- **EmailMappingModal** — `components/email/EmailMappingModal.tsx`
- **EmailVerifierBulkResults** — `components/email/EmailVerifierBulkResults.tsx`
- **EmailExportColumnMappingFields** — `components/email/EmailExportFields.tsx`
- **LottiePlayer** — `components/shared/LottiePlayer.tsx`
- **Modal** — `components/ui/Modal.tsx`
- **Button** — `components/ui/Button.tsx`

- **versions:** []
- **endpoint_count:** 6
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Email

### description

Email Finder and Verifier page with Finder | Verifier tabs. Finder: single and bulk email search by name/domain. Verifier: single and bulk email verification with risk analysis.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| email-title | 1 | Email Tools |
| finder-single | 2 | Find Email |
| verifier-single | 2 | Verify Email |
| bulk-section | 2 | Bulk Operations |
| history | 2 | Recent History |


### subheadings

| id | level | text |
| --- | --- | --- |
| finder-bulk-header | 3 | Upload CSV for bulk email finding |
| verifier-bulk-header | 3 | Upload CSV for bulk verification |
| risk-analysis | 3 | AI Risk Analysis |


### tabs

| content_ref | id | label |
| --- | --- | --- |
| email-finder-tab | finder | Finder |
| email-verifier-tab | verifier | Verifier |
| email-assistant-tab | assistant | Assistant |


### buttons

| action | component | id | label | loading_state | tab | type |
| --- | --- | --- | --- | --- | --- | --- |
| handleFinderSubmit | EmailFinderSingle | find-email-submit | Find Email | Searching... | finder | primary |
| finderBulkUpload.selectFile | EmailBulkDropZone | finder-bulk-upload | Upload CSV |  | finder | secondary |
| handleStartEnrichment | EmailMappingModal | finder-bulk-submit | Start Enrichment |  | finder | primary |
| handleVerifierSubmit | EmailVerifierSingle | verify-email-submit | Verify Email | Verifying... | verifier | primary |
| verifierBulkUpload.selectFile | EmailBulkDropZone | verifier-bulk-upload | Upload CSV |  | verifier | secondary |
| handleStartVerifierBulk | Modal | verifier-bulk-submit | Start Verification |  | verifier | primary |
| handleCopyFinderResult | EmailFinderSingle | copy-email | Copy |  |  | icon |
| handleGenerateSuggestions | EmailAssistantPanel | generate-draft | Generate Draft | Generating... | assistant | primary |
| handleCopySuggestion | EmailAssistantPanel | copy-draft | Copy Draft |  | assistant | secondary |


### input_boxes

- **[0]**
  - **id:** first-name
  - **label:** First Name
  - **type:** text
  - **placeholder:** John
  - **required:** True
  - **validation:** Non-empty
  - **component:** FinderSingleSearch
  - **tab:** finder

- **[1]**
  - **id:** last-name
  - **label:** Last Name
  - **type:** text
  - **placeholder:** Doe
  - **required:** True
  - **validation:** Non-empty
  - **component:** FinderSingleSearch
  - **tab:** finder

- **[2]**
  - **id:** company-domain
  - **label:** Company Domain
  - **type:** text
  - **placeholder:** company.com
  - **required:** True
  - **validation:** Domain format via emailUtils.validateDomain
  - **component:** FinderSingleSearch
  - **tab:** finder

- **[3]**
  - **id:** verify-email-input
  - **label:** Email Address
  - **type:** email
  - **placeholder:** email@company.com
  - **required:** True
  - **validation:** RFC 5322 email format
  - **component:** VerifierEmailTab
  - **tab:** verifier

- **[4]**
  - **id:** bulk-csv-upload-finder
  - **label:** CSV file
  - **type:** file
  - **accept:** .csv
  - **required:** True
  - **component:** FinderBulkUpload
  - **tab:** finder

- **[5]**
  - **id:** bulk-csv-upload-verifier
  - **label:** CSV file
  - **type:** file
  - **accept:** .csv
  - **required:** True
  - **component:** VerifierBulkTab
  - **tab:** verifier



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| UsageCounter | {credits} finder credits remaining | credits-counter | stat |
| MetricsBanner | Processed {total} · Found {found} · Failed {failed} | metrics-banner | info |
| FinderSingleSearch | Enter first name, last name, and company domain to find an email. | empty-finder | empty-state |
| FinderSingleSearch | Found: {email} ({confidence}% confidence) | result-email | result |
| VerifierEmailTab | Valid — this email exists and is deliverable | result-status-valid | success |
| VerifierEmailTab | Invalid — this email does not exist | result-status-invalid | error |
| VerifierEmailTab | Catchall — domain accepts all emails, cannot confirm deliverability | result-status-catchall | warning |


### checkboxes



### radio_buttons



### progress_bars

| color_logic | component | id | label | purpose | type |
| --- | --- | --- | --- | --- | --- |
| green > 70%, amber 40-70%, red < 40% | FinderSingleSearch | confidence-score | Email confidence score | 0–100% confidence that the found email is correct | determinate |
| green for valid, amber for catchall, red for invalid | VerifierEmailTab | verifier-confidence | Deliverability confidence | 0–100% confidence in email deliverability | determinate |
|  | VerifierBulkTab | bulk-processing-progress | Bulk processing progress | Tracks CSV processing: rows done / total | determinate |


### graphs

| chart_type | component | data_source | id | label | segments |
| --- | --- | --- | --- | --- | --- |
| stacked_bar | VerifierBulkTab | emailService.VerifyEmailsBulk result | bulk-results-stacked-bar | Bulk verification results breakdown | ['valid', 'invalid', 'catchall', 'unknown'] |


### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| EmailFinderSingle | single-finder-flow | Single email finder flow | ['Enter first name + last name + domain', 'Submit → useEmailFinderSingle → emailService.FindEmails', 'Result: email + confidence bar + copy button'] |
| EmailMappingModal | bulk-finder-flow | Bulk email finder flow | ['Upload CSV', 'Map columns (name, domain)', 'Submit → createEmailFinderExport job', 'Track in Jobs page'] |
| EmailAssistantPanel | ai-assistant-flow | AI email assistant flow | ['Paste recipient response', 'Submit → generate follow-up drafts', 'Copy chosen draft to clipboard'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
- **EmailMainTabs** — `components/features/email/EmailMainTabs.tsx`
- **EmailFinderSingle** — `components/email/EmailFinderSingle.tsx`
- **EmailVerifierSingle** — `components/email/EmailVerifierSingle.tsx`
- **EmailBulkDropZone** — `components/email/EmailBulkDropZone.tsx`
- **EmailMappingModal** — `components/email/EmailMappingModal.tsx`
- **EmailAssistantPanel** — `components/email/EmailAssistantPanel.tsx`
- **EmailCreditsBanner** — `components/email/EmailCreditsBanner.tsx`
- **EmailVerifierBulkResults** — `components/email/EmailVerifierBulkResults.tsx`
- **EmailExportColumnMappingFields** — `components/email/EmailExportColumnMappingFields.tsx`


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/index.ts | useEmailFinderSingle | Single-enrichment GQL resolver | 2.x |
| hooks/index.ts | useEmailVerifierSingle | Multi-provider SMTP verification | 2.x |
| hooks/index.ts | useEmailVerifierBulk | Batch verification and stats aggregation | 2.x |
| hooks/index.ts | useCsvUpload | S3 multipart upload with progress tracking | 6.x |
| context/AuthContext.ts | useAuth | User role/credits context for banners | 1.x |


### services

| file_path | name | operations |
| --- | --- | --- |
- **emailService** — `FindEmails`, `VerifySingleEmail`, `GetActivities`.
- **jobsService** — `createEmailFinderExport`, `createEmailVerifyExport`.
- **aiChatsService** — `AnalyzeEmailRisk`, `GetEmailAssistantSuggestions`.


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | User session for API calls |
| context/RoleContext.tsx | RoleContext | Credit check before submit; gated bulk features |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/email/emailUtils.ts | emailUtils | formatEmail, extractDomain, generatePatterns |
| lib/email/emailValidation.ts | emailValidation | validateEmailInput, validateDomain, validateEmailFinderInputs |
| lib/clipboard.ts | clipboard | Copy email result to clipboard |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useFinder | QUERY | FindEmails | emailService |
| useFinder | QUERY | FindEmailsBulk | emailService |
| useVerifier | QUERY | VerifySingleEmail | emailService |
| useEmailVerifierBulk | QUERY | VerifyEmailsBulk | emailService |
| useVerifier | MUTATION | AnalyzeEmailRisk | geminiService |


## UI elements (top-level)

### buttons

| id | label | type | action | loading_state | component | tab |
| --- | --- | --- | --- | --- | --- | --- |
| find-email-submit | Find Email | primary | emailService.FindEmails | Searching... | FinderSingleSearch | finder |
| finder-bulk-upload | Upload CSV | secondary | open file picker → FinderBulkUpload |  | FinderBulkUpload | finder |
| finder-bulk-submit | Find Emails in Bulk | primary | emailService.FindEmailsBulk (up to 50) |  | FinderBulkUpload | finder |
| verify-email-submit | Verify Email | primary | emailService.VerifySingleEmail | Verifying... | VerifierEmailTab | verifier |
| verifier-bulk-upload | Upload CSV | secondary | open file picker → VerifierBulkTab |  | VerifierBulkTab | verifier |
| verifier-bulk-submit | Verify in Bulk | primary | emailService.VerifyEmailsBulk (up to 1000) |  | VerifierBulkTab | verifier |
| copy-email | Copy | icon | clipboard.copyToClipboard(email) |  | FinderSingleSearch |  |
| analyze-risk | Analyze Risk | secondary | geminiService.AnalyzeEmailRisk (AI) |  | EmailRiskAnalyzer | verifier |
| export-results | Export Results | secondary | download CSV of results |  | VerifierBulkTab |  |
| clear-results | Clear | ghost | reset finder/verifier state |  | FinderSingleSearch |  |


### inputs

| id | label | type | placeholder | required | validation | component | tab |
| --- | --- | --- | --- | --- | --- | --- | --- |
| first-name | First Name | text | John | True | Non-empty | FinderSingleSearch | finder |
| last-name | Last Name | text | Doe | True | Non-empty | FinderSingleSearch | finder |
| company-domain | Company Domain | text | company.com | True | Domain format via emailUtils.validateDomain | FinderSingleSearch | finder |
| verify-email-input | Email Address | email | email@company.com | True | RFC 5322 email format | VerifierEmailTab | verifier |
| bulk-csv-upload-finder | CSV file | file |  | True |  | FinderBulkUpload | finder |
| bulk-csv-upload-verifier | CSV file | file |  | True |  | VerifierBulkTab | verifier |


### checkboxes

[]

### radio_buttons

[]

### progress_bars

| id | label | purpose | type | color_logic | component |
| --- | --- | --- | --- | --- | --- |
| confidence-score | Email confidence score | 0–100% confidence that the found email is correct | determinate | green > 70%, amber 40-70%, red < 40% | FinderSingleSearch |
| verifier-confidence | Deliverability confidence | 0–100% confidence in email deliverability | determinate | green for valid, amber for catchall, red for invalid | VerifierEmailTab |
| bulk-processing-progress | Bulk processing progress | Tracks CSV processing: rows done / total | determinate |  | VerifierBulkTab |


### toasts

[]

## Graphql Bindings

| hook | operation | service | type |
| --- | --- | --- | --- |
| useFinder | FindEmails, FindEmailsBulk | emailService | query |
| useVerifier | VerifySingleEmail, VerifyEmailsBulk | emailService | query |
| useVerifier | AnalyzeEmailRisk | geminiService | mutation |


## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useEmailFinderSingle.ts | useFinder | Finder form state, submit, result, credit check |
| hooks/useEmailVerifierSingle.ts | useVerifier | Verifier form state, submit, result |
| hooks/useEmailVerifierBulk.ts | useEmailVerifierBulk | Bulk verifier job state and progress polling |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/emailService.ts | emailService | ['FindEmails', 'FindEmailsBulk', 'VerifySingleEmail', 'VerifyEmailsBulk', 'GetActivities'] |
| services/graphql/aiChatsService.ts | geminiService | ['AnalyzeEmailRisk'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql email module resolvers | finder/verifier/read and bulk operations |
| downstream services | emailapis/emailapigo/mailvetter (via gateway orchestration) | email lookup and verification execution |


## Data Sources

- Appointment360 GraphQL gateway
- emailapis/emailapigo runtime stores and provider integrations via backend


## Flow summary

email UI tabs -> finder/verifier hooks -> GraphQL gateway -> email services pipeline -> results/progress/exports rendered in app


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — baseline email search and verification primitives.
- **2.x** — Email system — finder & verifier flows, bulk/jobs, Mailhub folders, product marketing pages.
- **5.x** — AI workflows — AI Email Assistant for follow-up drafting and intent analysis.
- **8.x** — Public & private APIs — API docs, integrations story, export contracts, developer surfaces.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:Dashboard] > [H:Header] + [S:Tabs] + [Q:CreditsBanner] + [C:Card] > [St:SubTabs] + [U:PanelContent] + [M:Modals] -> {useEmailFinder, useEmailVerifier}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/email`

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
| `FindEmails` | [query_find_emails_graphql.md](../../backend/endpoints/query_find_emails_graphql.md) | QUERY | 2.x |
| `VerifySingleEmail` | [mutation_verify_single_email_graphql.md](../../backend/endpoints/mutation_verify_single_email_graphql.md) | MUTATION | 2.x |
| `VerifyEmailsBulk` | [mutation_verify_bulk_emails_graphql.md](../../backend/endpoints/mutation_verify_bulk_emails_graphql.md) | MUTATION | 2.x |
| `AnalyzeEmailRisk` | [mutation_analyze_email_risk_graphql.md](../../backend/endpoints/mutation_analyze_email_risk_graphql.md) | MUTATION | 2.x |
| `GetActivities` | [get_activities_graphql.md](../../backend/endpoints/get_activities_graphql.md) | QUERY | 0.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
