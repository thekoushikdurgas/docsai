---
title: "Login"
page_id: login_page
source_json: login_page.json
generator: json_to_markdown.py
---

# Login

## Overview

- **page_id:** login_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** dashboard
- **era_tags:** 0.x, 1.x
- **flow_id:** login
- **_id:** login_page-001

## Metadata

- **route:** /login
- **file_path:** contact360.io/app/app/(auth)/login/page.tsx
- **purpose:** Authentication entry page for Contact360. Provides sign-in and register tabs with email/password forms and redirects authenticated users to /dashboard.
- **s3_key:** data/pages/login_page.json
- **status:** published
- **authentication:** Not required (public auth page); authenticated users are redirected away.
- **authorization:** None
- **page_state:** development
- **last_updated:** 2026-03-24T00:00:00.000000+00:00
### uses_endpoints (2)

- `graphql/Login` — Authenticate user with email and password. Returns JWT token and user object.
- `graphql/Register` — Register new user with name, email, password. Returns JWT token.

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
### api_versions

- graphql

- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Login

### description

Host both sign-in and registration flows in a single auth experience. Uses tabs to switch between login and register and redirects authenticated users to /dashboard.


## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| auth-header | 1 | Contact360 |
| auth-subheader | 2 | Sign in to your account |


### subheadings

| id | level | text |
| --- | --- | --- |
| register-subheader | 2 | Create your account |


### tabs

| content_ref | id | label |
| --- | --- | --- |
| auth-login-form | sign-in | Sign In |
| auth-register-form | register | Create Account |


### buttons

| action | component | id | label | loading_state | size | type |
| --- | --- | --- | --- | --- | --- | --- |
| submit login form | AuthSubmitButton | login-submit | Sign In | Signing in... | full-width | primary |
| submit register form | AuthSubmitButton | register-submit | Create Account | Creating account... | full-width | primary |
| navigate to /forgot-password | AuthFooter | forgot-password | Forgot password? |  |  | link |
| open terms page | AuthFooter | terms-link | Terms of Service |  |  | link |
| open privacy page | AuthFooter | privacy-link | Privacy Policy |  |  | link |


### input_boxes

- **[0]**
  - **id:** login-email
  - **label:** Email address
  - **type:** email
  - **placeholder:** you@company.com
  - **required:** True
  - **validation:** RFC 5322 email format via authValidation.validateEmail
  - **autocomplete:** email
  - **component:** EmailField
  - **tab:** sign-in

- **[1]**
  - **id:** login-password
  - **label:** Password
  - **type:** password
  - **placeholder:** Enter your password
  - **required:** True
  - **validation:** Non-empty via authValidation.validatePassword
  - **autocomplete:** current-password
  - **has_toggle:** True
  - **toggle_label:** Show/hide password
  - **component:** PasswordField
  - **tab:** sign-in

- **[2]**
  - **id:** register-name
  - **label:** Full name
  - **type:** text
  - **placeholder:** Your full name
  - **required:** True
  - **validation:** Non-empty, min 2 chars via authValidation.validateName
  - **autocomplete:** name
  - **component:** NameField
  - **tab:** register

- **[3]**
  - **id:** register-email
  - **label:** Email address
  - **type:** email
  - **placeholder:** you@company.com
  - **required:** True
  - **validation:** Email format, uniqueness checked server-side
  - **autocomplete:** email
  - **component:** EmailField
  - **tab:** register

- **[4]**
  - **id:** register-password
  - **label:** Password
  - **type:** password
  - **placeholder:** Create a strong password
  - **required:** True
  - **validation:** Min 8 chars, strength indicator
  - **autocomplete:** new-password
  - **has_toggle:** True
  - **component:** PasswordField
  - **tab:** register

- **[5]**
  - **id:** register-confirm-password
  - **label:** Confirm password
  - **type:** password
  - **placeholder:** Repeat your password
  - **required:** True
  - **validation:** Must match password field
  - **autocomplete:** new-password
  - **has_toggle:** True
  - **component:** PasswordField
  - **tab:** register



### text_blocks

| component | content | id | type |
| --- | --- | --- | --- |
| AuthErrorBanner | Dynamic error message from API (wrong password, account not found, etc.) | error-banner | error |
| AuthFooter | By creating an account, you agree to our Terms of Service and Privacy Policy. | terms-notice | caption |


### checkboxes

| component | default | id | label | required | tab |
| --- | --- | --- | --- | --- | --- |
| AuthFooter | False | terms-accept | I agree to the Terms of Service and Privacy Policy | True | register |


### radio_buttons



### progress_bars



### graphs



### flows

| component | id | label | steps |
| --- | --- | --- | --- |
| AuthCard | login-flow | Login flow | ['Enter email + password', 'Submit → authService.Login', 'Token stored via tokenManager', 'Redirect to /dashboard (or intended URL via useAuthRedirect)'] |
| AuthCard | register-flow | Register flow | ['Enter name + email + password + confirm', 'Accept terms checkbox', 'Submit → authService.Register', 'Token stored', 'Redirect to /dashboard'] |


### components

| file_path | name | purpose |
| --- | --- | --- |
| components/auth/AuthPageLayout.tsx | AuthPageLayout | Full-page centered card layout for auth pages |
| components/auth/AuthCard.tsx | AuthCard | White card container with logo, tabs, form |
| components/auth/AuthTabs.tsx | AuthTabs | Sign In / Create Account tab switcher |
| components/auth/AuthErrorBanner.tsx | AuthErrorBanner | Inline error alert for failed auth attempts |
| components/auth/EmailField.tsx | EmailField | Email input with format validation |
| components/auth/PasswordField.tsx | PasswordField | Password input with show/hide toggle |
| components/auth/AuthSubmitButton.tsx | AuthSubmitButton | Primary CTA button with loading state |
| components/auth/AuthFooter.tsx | AuthFooter | Links (forgot password, terms, privacy) + terms checkbox |


### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| hooks/useLoginForm.ts | useLoginForm | Login form state and submission logic | 0.x |
| hooks/useAuthRedirect.ts | useAuthRedirect | Redirect authenticated users to dashboard | 0.x |


### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/authService.ts | authService | ['Login', 'Register'] |


### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/AuthContext.tsx | AuthContext | Receives login result; sets user + token; redirects if already authenticated |


### utilities

| file_path | name | purpose |
| --- | --- | --- |
| lib/authValidation.ts | authValidation | Field validation: email format, password strength, name length, password match |
| lib/tokenManager.ts | tokenManager | Stores JWT token after successful login/register |


### ui_components



### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useLoginForm | MUTATION | Login | authService |
| useRegisterForm | MUTATION | Register | authService |


## UI elements (top-level)

### buttons

| id | label | type | size | action | loading_state | component |
| --- | --- | --- | --- | --- | --- | --- |
| login-submit | Sign In | primary | full-width | submit login form | Signing in... | AuthSubmitButton |
| register-submit | Create Account | primary | full-width | submit register form | Creating account... | AuthSubmitButton |
| forgot-password | Forgot password? | link |  | navigate to /forgot-password |  | AuthFooter |
| terms-link | Terms of Service | link |  | open terms page |  | AuthFooter |
| privacy-link | Privacy Policy | link |  | open privacy page |  | AuthFooter |


### inputs

| id | label | type | placeholder | required | validation | autocomplete | component | tab |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| login-email | Email address | email | you@company.com | True | RFC 5322 email format via authValidation.validateEmail | email | EmailField | sign-in |
| login-password | Password | password | Enter your password | True | Non-empty via authValidation.validatePassword | current-password | PasswordField | sign-in |
| register-name | Full name | text | Your full name | True | Non-empty, min 2 chars via authValidation.validateName | name | NameField | register |
| register-email | Email address | email | you@company.com | True | Email format, uniqueness checked server-side | email | EmailField | register |
| register-password | Password | password | Create a strong password | True | Min 8 chars, strength indicator | new-password | PasswordField | register |
| register-confirm-password | Confirm password | password | Repeat your password | True | Must match password field | new-password | PasswordField | register |


### checkboxes

| id | label | required | default | component | tab |
| --- | --- | --- | --- | --- | --- |
| terms-accept | I agree to the Terms of Service and Privacy Policy | True | False | AuthFooter | register |


### radio_buttons

[]

### progress_bars

[]

### toasts

[]

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useLoginForm.ts | useLoginForm | Login form state, validation, submit handler |
| hooks/useRegisterForm.ts | useRegisterForm | Register form state, validation, submit handler |
| hooks/useAuthRedirect.ts | useAuthRedirect | Post-login redirect to intended URL or /dashboard |


## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/authService.ts | authService | ['Login', 'Register'] |


## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql/Login, graphql/Register | dashboard data and mutations via services/hooks |


## Data Sources

- Appointment360 GraphQL gateway
- Service modules: authService
- Backend-owned data stores (via GraphQL modules)


## Flow summary

app page UI -> useLoginForm, useRegisterForm, useAuthRedirect -> authService -> GraphQL gateway -> backend modules -> rendered states


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

**Route (registry):** `/login`

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
| `Login` | [mutation_login_graphql.md](../../backend/endpoints/mutation_login_graphql.md) | MUTATION | 0.x |
| `Register` | [mutation_register_graphql.md](../../backend/endpoints/mutation_register_graphql.md) | MUTATION | 0.x |

*Regenerate this table with* `python docs/frontend/pages/link_endpoint_specs.py`*. Naming rules: [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).*

<!-- AUTO:endpoint-links:end -->
---

*Generated from JSON. Edit `*_page.json` and re-run `python json_to_markdown.py`.*
