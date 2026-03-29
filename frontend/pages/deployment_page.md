---
title: "Deployments"
page_id: deployment_page
source_json: deployment_page.json
generator: json_to_markdown.py
---

# Deployments

## Overview

- **page_id:** deployment_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** dashboard
- **era_tags:** 7.x
- **flow_id:** deployment
- **_id:** deployment_page-001

## Metadata

- **route:** /admin/deployments
- **file_path:** contact360.io/app/app/(dashboard)/admin/deployments/page.tsx
- **purpose:** Planned admin-only deployment and release visibility: environment, build SHA, last deploy time, rollback affordance (superAdmin). Complements 7.x deployment pipeline (CI/CD) without exposing secrets to end users.
- **s3_key:** data/pages/deployment_page.json
- **status:** planned
- **authentication:** Required (useSessionGuard + DashboardAccessGate)
- **authorization:** superAdmin only; non-superAdmin redirected to /dashboard
- **page_state:** planned
- **last_updated:** 2026-03-24T00:00:00.000000+00:00
- **uses_endpoints:** []
- **ui_components:** []
- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Deployments

### description

Planned: view current deployment metadata and release history for ops.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| deploy-title | 1 | Deployments |
| current | 2 | Current release |
| history | 2 | Release history |


### subheadings



### tabs

| content_ref | id | label |
| --- | --- | --- |
| deploy-overview | overview | Overview |
| deploy-history | history | History |


### buttons

| action | component | id | label | type | visibility |
| --- | --- | --- | --- | --- | --- |
| refetch deployment metadata | DeploymentPage | refresh-deploy | Refresh | icon |  |
| external link to CI (e.g. GitHub Actions) | DeploymentPage | open-pipeline | Open pipeline | secondary | superAdmin |


### input_boxes



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| DeploymentPage | Build: {shaShort} | build-sha | stat |
| DeploymentPage | Environment: {production\|staging} | env-label | badge |
| DeploymentPage | Deployed at {isoTimestamp} | deployed-at | caption |


### checkboxes



### radio_buttons



### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| DeploymentPage | deploy-visibility-flow | Deployment visibility (admin) | ['superAdmin navigates to /admin/deployments', 'deploymentService.GetCurrentDeployment', 'Table of recent releases with actor/commit message', 'Optional: link to external CI run'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/features/admin/DeploymentPage.tsx | DeploymentPage | Planned: current build card + release history table |


### hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useDeployments.ts | useDeployments | Planned: list deployments + current |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/deploymentService.ts | deploymentService | ['GetCurrentDeployment', 'ListDeployments'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/RoleContext.tsx | RoleContext | superAdmin gate |


### utilities



### ui_components



### endpoints



## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| refresh-deploy | Refresh | icon | refetch deployment metadata | DeploymentPage |
| open-pipeline | Open pipeline | secondary | external link to CI (e.g. GitHub Actions) | DeploymentPage |


### inputs

[]

### checkboxes

[]

### radio_buttons

[]

### progress_bars

[]

### toasts

[]

## Graphql Bindings

| hook | operation | service | type |
| --- | --- | --- | --- |
| useDeploymentPage (planned) | GetCurrentDeployment, ListDeployments | deploymentService (planned) | query |


## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useDeployments.ts | useDeployments | Planned: list deployments + current |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/deploymentService.ts | deploymentService | ['GetCurrentDeployment', 'ListDeployments'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| admin/deployment governance | deployment metadata endpoints (planned) | superAdmin deployment visibility |


## Data Sources

- Deployment metadata services (planned)
- CI/CD pipeline integration references


## Flow summary

superAdmin deployment page -> planned deployment hooks/services -> deployment metadata endpoints -> release overview/history UI


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **7.x** — Deployment — governance, deployments surface, RBAC-sensitive admin views.
- **Status** — Planned or spec-only; confirm `page.tsx` exists before treating as shipped.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L:Admin] > [H:Header] + [Q:DeployStatus] + [T:LogViewer] -> {useAdmin}
/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/admin/deployments`

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
| — | *No `graphql/...` references in this page spec* | — | — |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
