# Contact360 frontend documentation (`docs/frontend/`)

This folder holds **supplementary frontend inventory** for Contact360: per-page JSON metadata (routes, GraphQL usage, file paths) and **CSV exports** for spreadsheets or DocsAI ingestion, plus comprehensive design and engineering reference docs.

**Canonical product code** lives under **`contact360.io/`** (dashboard `app/`, marketing `root/`, DocsAI `admin/`). See **`docs/frontend.md`** for the live frontend map.

---

## Folder reality snapshot

- Includes component catalog, design-system guide, hooks/services/contexts catalog, and multiple service UI-binding docs.
- Acts as the frontend-side contract bridge to backend modules and endpoint metadata.
- Should be updated together with `docs/frontend/pages/` when UX behaviors change.

---

## Version era → frontend surfaces (Contact360 `0.x`–`10.x`)

| Era | Theme | Primary UI surfaces (typical) | Key UI elements introduced |
| --- | --- | --- | --- |
| `0.x` | Foundation | Repo layout, design tokens, shared components, layout shell | `MainLayout`, `Sidebar`, `Modal`, `Alert`, `DataToolbar` primitives |
| `1.x` | User, billing, credit | `login`, `register`, `profile`, `settings`, `billing`, `usage`, `admin` | Login/register forms, credit progress bars, UPI payment modal, usage charts |
| `2.x` | Email system | `email` (finder/verifier), `jobs`, `files`, bulk upload | Email inputs, progress bars, job execution flow, CSV drag-and-drop |
| `3.x` | Contact & company data | `contacts`, `companies`, search/filter UX | VQL query builder, data tables, filter sidebars, saved searches |
| `4.x` | Extension & Sales Navigator | Chrome extension `extension/contact360/`; LinkedIn/SN flows | Extension popup, SN ingestion panels, sync status indicators |
| `5.x` | AI workflows | `ai_chat`, AI-assisted email/writer pages | Chat stream display, AI confidence badges, `EmailAssistantPanel` |
| `6.x` | Reliability & scaling | **`status_page`** (`/status`, planned) + cross-cutting patterns on all routes | Public status/incidents UI; skeletons, retry, offline banners app-wide |
| `7.x` | Deployment | **`deployment_page`** (`/admin/deployments`, planned); DocsAI admin; RBAC admin | Deploy metadata for superAdmin; role-gated UI, feature flags, 2FA |
| `8.x` | Public & private APIs | `api_docs`, integrations, analytics/reporting UI | API key manager, analytics charts, integration cards |
| `9.x` | Ecosystem & productization | `integrations`, workspace/tenant admin, entitlement UX | Integration wizards, plan upgrade flows, entitlement indicators |
| `10.x` | Email campaign | **`campaigns_page`**, **`campaign_builder_page`**, **`sequences_page`**, **`campaign_templates_page`** (all planned) | Campaign list/wizard, sequences, templates, schedule/review, send progress |

Canonical policy text: **`docs/version-policy.md`**. Stages and releases: **`docs/roadmap.md`**, **`docs/versions.md`**.

## Tri-surface coverage contract (`root` + `app` + `admin`)

Frontend documentation in this folder must treat all three UI surfaces as first-class:

- `contact360.io/root/` (marketing/public UX)
- `contact360.io/app/` (authenticated dashboard UX)
- `contact360.io/admin/` (DocsAI/admin Django UX)

For each era and page inventory update, include coverage for:

- pages/routes and tabs
- buttons and text CTAs
- input boxes/selects/textareas
- checkboxes and radio controls
- progress indicators and loading states
- components/utilities/services/hooks/contexts
- graph and flow interactions
- backend API/endpoint bindings and data-source notes

---

## Contents

| Path | Purpose |
| --- | --- |
| [`components.md`](components.md) | Per-era component catalog — all UI components with file paths, UI elements, hooks/service dependencies |
| [`design-system.md`](design-system.md) | Design tokens, colors, typography, form elements (inputs, checkboxes, radio buttons, progress bars), button variants, accessibility |
| [`hooks-services-contexts.md`](hooks-services-contexts.md) | Full catalog of React hooks, GraphQL services, contexts, and lib utilities by domain and era |
| [`s3storage-ui-bindings.md`](s3storage-ui-bindings.md) | Storage-linked UI bindings and era task packs for file, upload, and artifact surfaces |
| [`emailapis-ui-bindings.md`](emailapis-ui-bindings.md) | Finder/verifier UI bindings across marketing, dashboard, and admin governance surfaces |
| [`logsapi-ui-bindings.md`](logsapi-ui-bindings.md) | Audit/observability UI bindings across dashboard and admin audit surfaces |
| [`pages/`](pages/) | One JSON file per logical page (`*_page.json`), plus `pages_index.json` aggregate |
| [`excel/`](excel/) | CSV exports derived from page inventories (e.g. for spreadsheets) |

---

## JSON page specs (`pages/`)

- **`pages_index.json`** — index of all pages with metadata (routes, endpoints, component paths). Paths inside JSON may reference historical aliases (`contact360/dashboard/`); treat **`contact360.io/app/`** as the canonical dashboard root unless a note says otherwise.
- **Per-page files** — e.g. `dashboard_page.json`, `billing_page.json`: route, GraphQL operations, auth notes.

See **[`pages/README.md`](pages/README.md)** for naming, era tagging, and page-to-component mapping guidance.

---

## Excel / CSV (`excel/`)

CSV files are **exports** of page metadata (titles, products, dashboard vs marketing vs docs classification). They are **not** source of truth; regenerate from tooling when inventory changes.

See **[`excel/README.md`](excel/README.md)**.

---

## Component catalog (`components.md`)

The **[`components.md`](components.md)** file is the definitive component reference, organized by era:

- **Foundation (`0.x`):** Layout (`MainLayout`, `Sidebar`, `DataPageLayout`), UI primitives (`Modal`, `Alert`, `Popover`, `ConfirmModal`), patterns (`DataToolbar`, `Pagination`)
- **Era 1 (`1.x`):** Billing (`UpiPaymentModal`), profile (`ProfileOverview`, `ProfileTabGeneral`), usage (`FeatureOverviewPanel`), credit alerts (`CreditBudgetAlerts`)
- **Era 2 (`2.x`):** Email (`EmailVerifierSingle`, `EmailVerifierResult`, `EmailVerifierBulkResults`), jobs (`JobsTable`, `JobsCard`, `ExecutionFlow`), files (`FilesUploadModal`, `DataPreviewTable`)
- **Era 3 (`3.x`):** Contacts (`ContactsTable`, `VQLQueryBuilder`, `SavedSearchesModal`), companies (`CompaniesGrid`, `CompaniesFilterSidebar`)
- **Era 5 (`5.x`):** AI (`EmailAssistantPanel`)
- **Shared/cross-era:** `ExportModal`, `TablePagination`, `FloatingActionBar`, `FilterSection`

---

## Design system (`design-system.md`)

The **[`design-system.md`](design-system.md)** file covers:

- **Colors:** Brand palette, semantic colors (success/warning/danger/info), status badge colors, credit balance color progression
- **Typography:** Page titles, body text, stat numbers, monospace for emails/API keys
- **Spacing:** CSS variable tokens (`--space-1` through `--space-12`)
- **Form elements:** Text inputs, textareas, selects, checkboxes, radio buttons, toggle switches, file drag-and-drop
- **Progress bars:** Credit balance, upload progress, job processing, confidence scores, stacked bars
- **Buttons:** Variants (primary, secondary, danger, ghost), sizes, states (loading, disabled)
- **Tabs, tables, badges, icons, animations**
- **Accessibility checklist and dark mode**

---

## Hooks, services, and contexts (`hooks-services-contexts.md`)

The **[`hooks-services-contexts.md`](hooks-services-contexts.md)** file covers:

- **Contexts:** `AuthContext`, `RoleContext`, `ThemeContext`
- **Auth hooks:** `useLoginForm`, `useRegisterForm`, `useSessionGuard`, `useSessions`
- **Dashboard hooks:** `useDashboardPage`, `useDashboardPageAccess`
- **Email hooks:** `useEmailFinderSingle`, `useEmailVerifierSingle`, `useEmailVerifierBulk`
- **Contacts/companies hooks:** `useContactsPage`, `useContactsFilters`, `useSavedSearches`, `useCompaniesPage`
- **Files/upload hooks:** `useNewExport`, `useCsvUpload`, `useFilePreview`, `useFiles`
- **Jobs hooks:** `useJobs`, `useExpandedJobDetails`
- **Billing/usage hooks:** `useBilling`, `useUsage`, `useFeatureOverview`
- **UI hooks:** `useModal`, `useViewMode`, `useResizablePanels`, `useSidebar`, `useDebouncedValue`
- **Platform hooks:** `useAnalytics`, `useAdmin`, `useTeam`, `useLinkedIn`, `useAPIKeys`
- **All 17 GraphQL service modules** with operations listed
- **All `lib/` utilities** (graphqlClient, tokenManager, authValidation, emailUtils, jobsMapper, contactsUtils, toast, clipboard, and more)
- **Page API layer** (dashboardPageApi, contactsPageApi, companiesPageApi)

---

## Related docs

| Doc | Use |
| --- | --- |
| `docs/frontend.md` | Dashboard, marketing, DocsAI, extension — canonical frontend map |
| `docs/flowchart.md` | User journey flowcharts, component interaction diagrams |
| `docs/codebase.md` | `contact360.io/app/` implementation entry points |
| `docs/backend.md` | Backend services that the frontend talks to |
| `docs/version-policy.md` | Major version themes (`0.x`–`10.x`) |
| `docs/roadmap.md` | What ships per stage |

## Manual update checklist (for this folder)

When a UI behavior changes in `root`, `app`, or `admin`, update these docs in one pass:

1. `components.md`
2. `design-system.md`
3. `hooks-services-contexts.md`
4. one or more binding docs (`emailapis-ui-bindings.md`, `logsapi-ui-bindings.md`, `s3storage-ui-bindings.md`)
5. `pages/` metadata docs
6. `excel/` export contract docs

---

## Email app docs pack — `contact360.io/email`

### Component highlights
- `components/email-list.tsx` — mailbox fetch orchestration, loading/error/empty state.
- `components/data-table.tsx` — tabs, checkbox selection, pagination, row action dropdown.
- `components/app-sidebar.tsx` — folder navigation and user bootstrap.
- `components/nav-user.tsx` — account menu + logout.
- `app/account/[userId]/page.tsx` — profile and IMAP account management.

### Hooks/services/contexts
- `context/imap-context.tsx` — active account context + persistence.
- `hooks/use-mobile.ts` — responsive helper.
- Service access is direct `fetch` using `BACKEND_URL` in `lib/utils.ts`.

### Design system and UX profile
- Dark-theme-first mailbox shell.
- Emphasis on compact table workflows for high-volume email triage.
- Uses shadcn/Radix primitives for consistent tabs/buttons/inputs/checkbox/dropdowns.
