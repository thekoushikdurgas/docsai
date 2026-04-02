---
title: "Admin"
page_id: admin_page
source_json: admin_page.json
generator: json_to_markdown.py
---

# Admin

## Overview

- **page_id:** admin_page
- **page_type:** dashboard
- **codebase:** app
- **surface:** dashboard
- **era_tags:** 1.x, 7.x, 9.x
- **flow_id:** admin
- **_id:** admin_page-001

## Metadata

- **route:** /admin
- **file_path:** contact360.io/app/app/(dashboard)/admin/page.tsx
- **purpose:** Admin Console: System-wide oversight for organizations, users, and global configuration.
- **status:** shipped
- **authentication:** Required (protected by useSessionGuard and DashboardAccessGate)
- **authorization:** SuperAdmin only; non-SuperAdmin users are redirected to /dashboard
- **page_state:** development
- **last_updated:** 2026-03-29T00:00:00Z
- **uses_endpoints:** []

### UI components (metadata)

- **AdminPage** — `app/(dashboard)/admin/page.tsx`
- **Shield** — `lucide-react`
- **RefreshCw** — `lucide-react`
- **Trash2** — `lucide-react`
- **PenSquare** — `lucide-react`
- **Button** — `components/ui/Button.tsx`
- **Badge** — `components/ui/Badge.tsx`
- **LoadingSpinner** — `components/shared/LoadingSpinner.tsx`
- **ErrorState** — `components/shared/ErrorState.tsx`
- **EmptyState** — `components/shared/EmptyState.tsx`

- **versions:** []
- **endpoint_count:** 0
- **api_versions:** []
- **codebase:** app
- **canonical_repo:** contact360.io/app

## Content sections (summary)

### title

Admin

### description

SuperAdmin control panel to inspect user stats (total/active) and manage users (view, delete). Non-SuperAdmin users see an access denied message or are redirected.

## Sections (UI structure)

### headings

| id | level | text |
| --- | --- | --- |
| admin-title | 1 | Admin Console |
| platform-stats | 2 | Platform Statistics |
| user-management | 2 | User Management |

### subheadings

| id | level | text |
| --- | --- | --- |
| total-users | 3 | Total Users |
| active-users | 3 | Active Users |

### tabs

| content_ref | id | label |
| --- | --- | --- |
| admin-users | users | Users |
| admin-payments | payments | Payments |
| admin-platform | platform | Platform |

### buttons

| action | component | id | label | type |
| --- | --- | --- | --- | --- |
| adminService → ConfirmModal → delete user | AdminUserTable | delete-user | Delete User | danger |
| adminService.AdjustCredits → credits input modal | AdminUserTable | adjust-credits | Adjust Credits | secondary |
| adminService.ApprovePaymentSubmission | AdminPaymentsTable | approve-payment | Approve | primary |
| adminService.DeclinePaymentSubmission | AdminPaymentsTable | decline-payment | Decline | danger |
| refetch UserStats | PageHeader | refresh-stats | Refresh | icon |

### input_boxes

| component | id | label | placeholder | required | type |
| --- | --- | --- | --- | --- | --- |
| AdminUserTable | search-users | Search users | Search by name or email |  | search |
| AdjustCreditsModal | credit-amount | Credit amount | e.g. 500 | True | number |
| AdjustCreditsModal | credit-reason | Reason | e.g. Bonus credits | False | text |

### text_blocks

| component | content | id | type | visibility |
| --- | --- | --- | --- | --- |
| StatsGrid | {totalUsers} total users | stats-total-users | stat |  |
| StatsGrid | {activeUsers} active (last 30 days) | stats-active-users | stat |  |
| AdminPage | Access denied. SuperAdmin only. | no-access | error | non-superAdmin |

### checkboxes

### radio_buttons

### progress_bars

### graphs

| chart_type | component | data_source | id | label | metrics | visibility |
| --- | --- | --- | --- | --- | --- | --- |
| stat_cards | StatsGrid | adminService.UserStats | user-stats-cards | Platform user statistics | ['total users', 'active users', 'by role', 'by plan'] | superAdmin only |

### flows

| component | id | label | steps |
| --- | --- | --- |
| AdminPaymentsTable | approve-payment-flow | Payment approval flow | ['View pending payment submissions in Payments tab', "Click 'Approve' on a submission", 'adminService.ApprovePaymentSubmission', 'Credits automatically added to user account', "Toast: 'Payment approve |

### components

| file_path | name | purpose |
| --- | --- | --- |
| components/shared/StatsGrid.tsx | StatsGrid | Total/active user stats cards |
| components/features/admin/AdminUserTable.tsx | AdminUserTable | User list with search, adjust credits, delete |
| components/features/admin/AdminPaymentsTable.tsx | AdminPaymentsTable | Payment submissions with approve/decline |

### hooks

| file_path | name | purpose | era |
| --- | --- | --- | --- |
| context/AuthContext.ts | useAuth | User role verification (SuperAdmin check) | 0.x |
| hooks/useAdmin.ts | useAdmin | Platform-wide user management and stats | 1.x, 7.x |

### services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/adminService.ts | adminService | ['UserStats', 'ListUsers', 'AdjustCredits', 'ListPaymentSubmissions', 'ApprovePaymentSubmission', 'DeclinePaymentSubmission'] |

### contexts

| file_path | name | purpose |
| --- | --- | --- |
| context/RoleContext.tsx | RoleContext | isSuperAdmin gate — redirects non-superAdmin to /dashboard |

### utilities

### ui_components

### endpoints

| hook | method | operation | service |
| --- | --- | --- | --- |
| useAdmin | QUERY | UserStats | adminService |
| useAdmin | QUERY | ListUsers | adminService |
| useAdmin | MUTATION | AdjustCredits | adminService |
| useAdmin | MUTATION | ApprovePaymentSubmission | adminService |

## UI elements (top-level)

### buttons

| id | label | type | action | component |
| --- | --- | --- | --- | --- |
| delete-user | Delete User | danger | adminService → ConfirmModal → delete user | AdminUserTable |
| adjust-credits | Adjust Credits | secondary | adminService.AdjustCredits → credits input modal | AdminUserTable |
| approve-payment | Approve | primary | adminService.ApprovePaymentSubmission | AdminPaymentsTable |
| decline-payment | Decline | danger | adminService.DeclinePaymentSubmission | AdminPaymentsTable |
| refresh-stats | Refresh | icon | refetch UserStats | PageHeader |

### inputs

| id | label | type | placeholder | component |
| --- | --- | --- | --- | --- |
| search-users | Search users | search | Search by name or email | AdminUserTable |
| credit-amount | Credit amount | number | e.g. 500 | AdjustCreditsModal |
| credit-reason | Reason | text | e.g. Bonus credits | AdjustCreditsModal |

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
| useAdmin | UserStats, ListUsers, ListPaymentSubmissions | adminService | query |
| useAdmin | AdjustCredits, ApprovePaymentSubmission, DeclinePaymentSubmission | adminService | mutation |

## Hooks

| file_path | name | purpose |
| --- | --- | --- |
| hooks/useAdmin.ts | useAdmin | UserStats, ListUsers, AdjustCredits, payment approval |

## Services

| file_path | name | operations |
| --- | --- | --- |
| services/graphql/adminService.ts | adminService | ['UserStats', 'ListUsers', 'AdjustCredits', 'ListPaymentSubmissions', 'ApprovePaymentSubmission', 'DeclinePaymentSubmission'] |

## Backend Bindings

| layer | path | usage |
| --- | --- | --- |
| gateway | graphql admin module operations | admin control plane actions in app dashboard |
| docsai admin linkage | contact360.io/admin governance surfaces | complementary operational governance outside app dashboard |

## Data Sources

- Appointment360 GraphQL gateway
- admin module data stores and logs
- DocsAI governance context references

## Flow summary

app admin dashboard -> useAdmin/adminService -> GraphQL admin operations -> user/payment/admin state updates with superAdmin gating

<!-- AUTO:design-nav:start -->

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

- **1.x** — User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.
- **7.x** — Deployment — governance, deployments surface, RBAC-sensitive admin views.
- **9.x** — Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** [L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `/admin`

**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).

**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions, bookmarks to route. **Typical outbound:** sidebar peers (see **Peer pages**), `router.push` / `<Link>` from **### buttons** table above.

**Cross-host:** marketing [landing_page.md](landing_page.md) → [login_page.md](login_page.md) / [register_page.md](register_page.md); product pages on **root** deep-link to app auth.

## Backend API documentation

- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` to refresh the `AUTO:endpoint-links` table in this file.
- **Endpoint ↔ database naming & Connectra scope:** [ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).
- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).

### Peer pages (same codebase)

- [activities_page](activities_page.md)
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
