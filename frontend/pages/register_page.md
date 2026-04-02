---
title: "Create Account"
page_id: register_page
source_json: register_page.json
generator: json_to_markdown.py
---

# Create Account

## Overview

- **page_id:** register_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** App Auth
- **era_tags:** 0.x, 1.x, 11.x
- **flow_id:** register
- **_id:** register_page-001

## Metadata

- **route:** /register
- **file_path:** contact360.io/app/app/(auth)/register/page.tsx
- **purpose:** Standalone registration page for Contact360. Collects name, email, password, confirm password with terms acceptance. On success redirects to /dashboard.
- **s3_key:** data/pages/register_page.json
- **status:** published
- **authentication:** Not required; authenticated users redirected to /dashboard.
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00.000000+00:00
### uses_endpoints (1)

- `graphql/Register` — Register new user with name, email, password. Returns JWT token and user.

### UI components (metadata)

- **RegisterPage** — `app/(auth)/register/page.tsx` (Redirects to `/login?tab=register`)
- **AuthPageLayout** — `components/auth/AuthPageLayout.tsx`
- **AuthCard** — `components/auth/AuthCard.tsx`
- **AuthTabs** — `components/auth/AuthTabs.tsx`
- **AuthErrorBanner** — `components/auth/AuthErrorBanner.tsx`
- **NameField** — `components/auth/NameField.tsx`
- **EmailField** — `components/auth/EmailField.tsx`
- **PasswordField** — `components/auth/PasswordField.tsx`
- **AuthSubmitButton** — `components/auth/AuthSubmitButton.tsx`
- **AuthFooter** — `components/auth/AuthFooter.tsx`

- **versions:** []
- **endpoint_count:** 1
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Create Account

### description

New user registration with name, email, password fields and terms acceptance.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| register-title | 1 | Create your account |
| register-subtitle | 2 | Start finding verified B2B contacts for free |


### subheadings



### tabs



### buttons

| action | component | id | label | loading_state | size | type |
| --- | --- | --- | --- | --- | --- | --- |
| submit register form → authService.Register | AuthSubmitButton | register-submit | Create Account | Creating account... | full-width | primary |
| navigate to /login | AuthFooter | sign-in-link | Already have an account? Sign in |  |  | link |


### input_boxes

- **[0]**
  - **id:** name
  - **label:** Full name
  - **type:** text
  - **placeholder:** Your full name
  - **required:** True
  - **validation:** Non-empty, min 2 chars
  - **autocomplete:** name
  - **component:** NameField

- **[1]**
  - **id:** email
  - **label:** Work email
  - **type:** email
  - **placeholder:** you@company.com
  - **required:** True
  - **validation:** RFC 5322 email format; uniqueness server-side
  - **autocomplete:** email
  - **component:** EmailField

- **[2]**
  - **id:** password
  - **label:** Password
  - **type:** password
  - **placeholder:** Min 8 characters
  - **required:** True
  - **validation:** Min 8 chars, at least one uppercase, one number
  - **autocomplete:** new-password
  - **has_toggle:** True
  - **component:** PasswordField

- **[3]**
  - **id:** confirm-password
  - **label:** Confirm password
  - **type:** password
  - **placeholder:** Repeat password
  - **required:** True
  - **validation:** Must match password
  - **autocomplete:** new-password
  - **has_toggle:** True
  - **component:** PasswordField



### checkboxes

| component | default | id | label | required |
| --- | --- | --- | --- | --- |
| AuthFooter | False | terms-accept | I agree to the Terms of Service and Privacy Policy | True |


### radio_buttons



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| AuthErrorBanner | Dynamic API error (email already in use, invalid input, etc.) | error-message | error |
| PasswordField | At least 8 characters with a number and uppercase letter | password-hint | hint |


### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| AuthCard | registration-flow | Registration flow | ['Fill name, email, password, confirm password', 'Check terms checkbox', 'Submit → authService.Register mutation', 'On success: token stored, redirect to /dashboard', 'On error: AuthErrorBanner shows  |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/auth/index.tsx | AuthPageLayout | Centered full-page layout for auth |
| components/auth/index.tsx | AuthCard | White card wrapper with logo and form |
| components/auth/AuthErrorBanner.tsx | AuthErrorBanner | Inline error banner for failed registration |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useRegisterForm.ts | useRegisterForm | Register form state and submission logic | 0.x |
| hooks/useAuthRedirect.ts | useAuthRedirect | Redirect authenticated users to dashboard | 0.x |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/authService.ts | authService | ['Register'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | Receives token and user after registration; provides to all child components |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/authValidation.ts | authValidation | Validates name, email, password, password match |
| lib/tokenManager.ts | tokenManager | Stores JWT after registration |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useRegisterForm | MUTATION | Register | authService |


## UI elements (top-level)

### buttons

| id | label | type | size | action | loading_state | component |
| --- | --- | --- | --- | --- | --- | --- |
| register-submit | Create Account | primary | full-width | submit register form → authService.Register | Creating account... | AuthSubmitButton |
| sign-in-link | Already have an account? Sign in | link |  | navigate to /login |  | AuthFooter |


### inputs

| id | label | type | placeholder | required | validation | autocomplete | component |
| --- | --- | --- | --- | --- | --- | --- | --- |
| name | Full name | text | Your full name | True | Non-empty, min 2 chars | name | NameField |
| email | Work email | email | you@company.com | True | RFC 5322 email format; uniqueness server-side | email | EmailField |
| password | Password | password | Min 8 characters | True | Min 8 chars, at least one uppercase, one number | new-password | PasswordField |
| confirm-password | Confirm password | password | Repeat password | True | Must match password | new-password | PasswordField |


### checkboxes

| id | label | required | default | component |
| --- | --- | --- | --- | --- |
| terms-accept | I agree to the Terms of Service and Privacy Policy | True | False | AuthFooter |


### radio_buttons

[]

### progress_bars

[]

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useRegisterForm.ts | useRegisterForm | Controlled form state, field validation, submit handler |
| hooks/useAuthRedirect.ts | useAuthRedirect | Redirect to /dashboard after successful registration |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/authService.ts | authService | ['Register'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/Register | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: authService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useRegisterForm, useAuthRedirect -> authService -> GraphQL gateway -> backend modules -> rendered states


<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **0.x** — Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.
- **1.x** — User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/register`

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
- [export_page](export_page.md)
- [files_page](files_page.md)
- [finder_page](finder_page.md)
- [jobs_page](jobs_page.md)
- [linkedin_page](linkedin_page.md)
- [live_voice_page](live_voice_page.md)
- [login_page](login_page.md)
- [profile_page](profile_page.md)
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
| `Register` | [mutation_register_graphql.md](../../backend/endpoints/mutation_register_graphql.md) | MUTATION | 0.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
