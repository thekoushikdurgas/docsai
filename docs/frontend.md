# Contact360 frontend map

> **Note:** This file is named `frontend.md` in the repository. It is the **frontend** (product UI) index — dashboard, marketing, email app, DocsAI, and extension.

For **backend** services, see **`docs/docs/backend.md`**. For the full monorepo and per-service code pointers, see **`docs/docs/codebase.md`**. For system boundaries, see **`docs/docs/architecture.md`**. **Language policy** (Python GraphQL gateway vs Go/Gin satellites): **`docs/docs/backend-language-strategy.md`**.

**Page inventory, component catalog, design system, and hooks/services docs** live under **`docs/frontend/`** (see **`docs/frontend/README.md`**). Canonical app code remains under **`contact360.io/`** below.

### Frontend stack policy

- **Next.js** is the default for **customer-facing web apps** in this monorepo: dashboard (`contact360.io/app/`), marketing (`contact360.io/root/`), mailbox (`contact360.io/email/`).
- **Exceptions (explicit):**
  - **Django DocsAI** (`contact360.io/admin/`) — internal documentation, governance mirrors, and operational admin; not a public product SPA.
  - **Chrome extension MV3** (`extension/contact360/`) — browser surface; not Next.js.
- **API split:** Dashboard and extension use **GraphQL** via `contact360.io/api`. The **email web app** uses **REST** mailbox/backend URLs (`NEXT_PUBLIC_BACKEND_URL`) for IMAP/mailbox operations in addition to GraphQL where wired — treat email as **mixed** (REST + GraphQL) per `contact360.io/email/README.md`.

---

## Version era → primary UI surfaces (`0.x`–`10.x`)

Themes are defined in **`docs/version-policy.md`**. UI surface coverage at a glance:

| Era | Theme | Primary UI surfaces | Key UI elements introduced |
| --- | --- | --- | --- |
| `0.x` | Foundation | App shell, routing, design tokens | Layout, sidebar, auth shell, global CSS |
| `1.x` | User, billing, credit | Auth, profile, settings, billing, usage, admin | Login/register forms, billing modals, credit display, UPI payment, usage charts |
| `2.x` | Email system | Finder, verifier, results, export, jobs, files | Email input forms, result cards, progress bars, bulk upload, job status indicators |
| `3.x` | Contact & company data | Contacts, companies, search/filter UX | VQL query builder, data tables, filter sidebar, saved searches, company drill-down |
| `4.x` | Extension & Sales Navigator | `extension/contact360/` (Chrome), LinkedIn flows | Extension popup, SN ingestion panels, sync status indicators |
| `5.x` | AI workflows | AI chat, AI-assisted email writer, live voice | Chat message streams, AI confidence badges, streaming progress, AI tool panels |
| `6.x` | Reliability & scaling | Client resilience patterns | Error boundaries, retry UI, loading skeletons, offline banners |
| `7.x` | Deployment | RBAC-sensitive admin surfaces, DocsAI governance | Role-gated UI, feature flags, admin governance screens |
| `8.x` | Public & private APIs | API docs, integrations, analytics/reporting | API key manager, analytics charts, integration cards, reporting tables |
| `9.x` | Ecosystem & productization | Integrations hub, workspace/tenant admin | Integration setup wizards, entitlement indicators, plan upgrade flows |
| `10.x` | Email campaign | Campaign builder, audience, templates, send review | Campaign form, audience picker, email template editor, send progress tracker |

---

## Product applications (`contact360.io/`)

| Path | Role | Stack | Key docs |
| --- | --- | --- | --- |
| `contact360.io/app/` | Authenticated product (GraphQL-only client) | Next.js 16, React 19, modular CSS under `app/css/*` | `contact360.io/app/README.md`, `docs/DESIGN_UX.md`, `docs/API_DASHBOARD_MAPPING.md` |
| `contact360.io/root/` | Public marketing and growth pages | Next.js 16, custom CSS (BEM-like) | `contact360.io/root/README.md`; env: `GRAPHQL_URL`, dashboard URL for auth CTAs |
| `contact360.io/email/` | Mailbox/email application surface | Next.js 16, React 19, Tailwind + Radix UI | `contact360.io/email/README.md`, `docs/codebases/email-codebase-analysis.md` |
| `contact360.io/admin/` | Internal docs/admin mirror (roadmap & architecture constants) | Django | `docs/docsai-sync.md`, `contact360.io/admin/deploy/README.md` |

**Gateway contract:** All dashboard API traffic goes through **`contact360.io/api/`** GraphQL (`NEXT_PUBLIC_API_URL` / GraphQL URL in dashboard config).
**Email app contract:** `contact360.io/email` uses REST endpoints via `NEXT_PUBLIC_BACKEND_URL`.

---

## Browser extension

| Path | Role | Notes |
| --- | --- | --- |
| `extension/contact360/` | Chrome extension logic layer (Sales Navigator workflows) | **Canonical** path. Auth/session (`graphqlSession.js`), Lambda client (`lambdaClient.js`), and profile dedup (`profileMerger.js`) are implemented. Popup/content/manifest shell remains planned 4.5-4.7 work. |

### Design-system split note

- `contact360.io/app` uses dashboard primitives and modular CSS.
- `contact360.io/root` uses a separate 3D component system (`Button3D`, `Card3D`, `Modal3D`, etc.).
- `contact360.io/email` uses Tailwind + Radix-based mailbox UI primitives.

Phase **4.x** Extension and Sales Navigator maturity (auth, telemetry, SN ingestion, sync) is tracked in **`docs/roadmap.md`** and **`docs/versions.md`**.

---

## App directory structure (`contact360.io/app/src/`)

| Path | Contents |
| --- | --- |
| `components/` | Feature and shared UI components (see component catalog below) |
| `hooks/` | React custom hooks (data fetching, UI state, form handling) |
| `services/graphql/` | GraphQL service modules per domain |
| `context/` | React context providers (`AuthContext`, `RoleContext`, `ThemeContext`) |
| `lib/` | Utilities, helpers, constants, page APIs, error handlers |
| `text/` | UI copy strings (`copy.ts`) |

---

## UI component catalog (by era and domain)

### Foundation (`0.x`) — Layout and shell

| Component | Path | Purpose |
| --- | --- | --- |
| `MainLayout` | `components/layout/MainLayout.tsx` | Root authenticated layout wrapper — sidebar, header, content slot |
| `Sidebar` | `components/layout/Sidebar.tsx` | Left nav with route links, credit indicator, user badge |
| `DataPageLayout` | `components/layouts/DataPageLayout.tsx` | Resizable two-panel layout for data-heavy pages |
| `DashboardAccessGate` | `components/shared/DashboardAccessGate.tsx` | Guards dashboard routes; redirects unauthenticated users |
| `AuthErrorBanner` | `components/auth/AuthErrorBanner.tsx` | Inline auth error display (login/register pages) |

### Foundation (`0.x`) — UI primitives

| Component | Path | Purpose |
| --- | --- | --- |
| `Modal` | `components/ui/Modal.tsx` | Base modal wrapper (backdrop, close, z-index) |
| `ConfirmModal` | `components/ui/ConfirmModal.tsx` | Generic destructive-action confirmation dialog |
| `Popover` | `components/ui/Popover.tsx` | Floating popover / tooltip (anchor-positioned) |
| `Alert` | `components/ui/Alert.tsx` | Inline alert banner (success, warning, error, info) |
| `ResizeHandle` | `components/shared/ResizeHandle.tsx` | Drag handle for resizable panel splits |
| `FloatingActionBar` | `components/shared/FloatingActionBar.tsx` | Sticky bottom action bar for bulk selection actions |
| `TablePagination` | `components/shared/TablePagination.tsx` | Page size and page index controls for data tables |
| `FilterSection` | `components/shared/FilterSection.tsx` | Collapsible labeled filter group (used in sidebars) |
| `ExportModal` | `components/shared/ExportModal.tsx` | Column selection and format picker for CSV exports |
| `TwoFactorModal` | `components/shared/TwoFactorModal.tsx` | TOTP/OTP entry modal (2FA challenge flow) |

### Foundation (`0.x`) — Pattern components

| Component | Path | Purpose |
| --- | --- | --- |
| `DataToolbar` | `components/patterns/DataToolbar.tsx` | Search input + action buttons row above data tables |
| `GenericToolbar` | `components/patterns/GenericToolbar.tsx` | Flexible toolbar wrapper for view-mode and sort controls |
| `Pagination` | `components/patterns/Pagination.tsx` | Page-number strip with ellipsis for large lists |

### User, billing, credit (`1.x`)

| Component | Path | Purpose | UI elements |
| --- | --- | --- | --- |
| `CreditBudgetAlerts` | `components/layout/CreditBudgetAlerts.tsx` | Sticky low-credit warning banner (threshold-driven) | Alert banner, progress bar |
| `UpiPaymentModal` | `components/billing/UpiPaymentModal.tsx` | UPI QR payment proof submission dialog | File input, text input, submit button, progress indicator |
| `ProfileOverview` | `components/profile/ProfileOverview.tsx` | User profile header (avatar, name, plan badge) | Read-only display fields, badge |
| `ProfileTabGeneral` | `components/profile/ProfileTabGeneral.tsx` | Editable profile fields tab (name, email, password) | Text inputs, save button, toggle |
| `FeatureOverviewPanel` | `components/usage/FeatureOverviewPanel.tsx` | Feature credit consumption summary per feature | Progress bars, credit counters |

### User, billing, credit (`1.x`) — Dashboard overview

| Component | Path | Purpose | UI elements |
| --- | --- | --- | --- |
| `DashboardOverview` | `components/dashboard/DashboardOverview.tsx` | Credit/usage stats summary cards | Stat cards, icon badges |
| `DashboardLineChart` | `components/dashboard/DashboardLineChart.tsx` | Line chart of daily activity/performance | SVG/Canvas line chart, legend |

### Email system (`2.x`)

| Component | Path | Purpose | UI elements |
| --- | --- | --- | --- |
| `EmailVerifierSingle` | `components/email/EmailVerifierSingle.tsx` | Single email verification form + result | Text input, submit button, result badge |
| `EmailVerifierResult` | `components/email/EmailVerifierResult.tsx` | Verification result display card | Status badge, confidence bar, detail rows |
| `EmailVerifierBulkResults` | `components/email/EmailVerifierBulkResults.tsx` | Bulk verification summary table | Data table, filter tabs, export button |
| `EmailMappingModal` | `components/email/EmailMappingModal.tsx` | Column-to-field mapping for CSV uploads | Select dropdowns, preview table |
| `EmailAssistantPanel` | `components/email/EmailAssistantPanel.tsx` | AI-assisted email composition panel | Text area, AI suggestion chips, tone selector |
| `EmailExportColumnMappingFields` | `components/email/EmailExportColumnMappingFields.tsx` | Export column mapping form fields | Checkbox list, field drag-and-drop |

### Email system (`2.x`) — Jobs and files

| Component | Path | Purpose | UI elements |
| --- | --- | --- | --- |
| `JobsTable` | `components/jobs/JobsTable.tsx` | Tabular list of all bulk jobs | Sortable table, status badge, action menu |
| `JobsCard` | `components/jobs/JobsCard.tsx` | Single job card (compact view) | Progress bar, status icon, expand button |
| `JobsCardExpandPanel` | `components/jobs/JobsCardExpandPanel.tsx` | Expanded detail panel within job card | Detail rows, action buttons |
| `JobDetailsModal` | `components/jobs/JobDetailsModal.tsx` | Full job details dialog | Tab panes, result summary, download button |
| `ExecutionFlow` | `components/jobs/ExecutionFlow.tsx` | Step-by-step job execution flow visualization | Step nodes, progress connector, status icons |
| `ScheduleJobModal` | `components/jobs/ScheduleJobModal.tsx` | Cron/time picker for scheduling a job | Time picker, radio buttons, cron input |
| `JobsRetryModal` | `components/jobs/JobsRetryModal.tsx` | Confirmation and retry-scope selector for failed jobs | Radio buttons, confirm button |
| `JobsPipelineStats` | `components/jobs/JobsPipelineStats.tsx` | Pipeline stats bar (processed/failed/pending counts) | Mini bar chart, count labels |
| `DataInspector` | `components/jobs/DataInspector.tsx` | Inline JSON/data value inspector panel | Tree view, collapsible nodes |
| `DataValue` | `components/jobs/DataValue.tsx` | Renders a single typed data value | Type-aware formatted display |
| `FilesUploadModal` | `components/files/FilesUploadModal.tsx` | CSV file upload dialog | File drag-and-drop, progress bar, file list |
| `FilesUploadPanel` | `components/files/FilesUploadPanel.tsx` | In-page upload area (drag-and-drop zone) | Drop zone, upload progress, file preview |
| `FilesDetailView` | `components/files/FilesDetailView.tsx` | File metadata and schema detail panel | Info rows, schema table |
| `DataPreviewTable` | `components/files/DataPreviewTable.tsx` | Preview first N rows of uploaded CSV | Paginated table, column headers |
| `FilesCreateJobModal` | `components/files/FilesCreateJobModal.tsx` | Create finder/verifier job from file dialog | Radio buttons, column selectors, submit |
| `FilesSchemaPanel` | `components/files/FilesSchemaPanel.tsx` | CSV column schema display panel | Field-type badges, nullable indicator |
| `FilesColumnStatsPanel` | `components/files/FilesColumnStatsPanel.tsx` | Per-column statistics (null %, unique %, top values) | Mini bar charts, stat rows |
| `DatasetInfoPanel` | `components/files/DatasetInfoPanel.tsx` | File/dataset info summary (row count, size, created) | Info grid |
| `FilesPeekModal` | `components/files/FilesPeekModal.tsx` | Quick preview modal for a file | Modal table, row sample |
| `FilesDownloadModal` | `components/files/FilesDownloadModal.tsx` | Download format and range selector | Radio buttons, range input, download button |

### Contact and company data (`3.x`)

| Component | Path | Purpose | UI elements |
| --- | --- | --- | --- |
| `ContactsTable` | `components/contacts/ContactsTable.tsx` | Full contacts data table | Sortable table, row checkbox, status badge |
| `ContactsTableContainer` | `components/contacts/ContactsTableContainer.tsx` | State-managed wrapper for contacts table | Search input, column visibility toggle |
| `ContactRow` | `components/contacts/ContactRow.tsx` | Single contact table row | Avatar, name, email, action buttons |
| `ContactsFilters` | `components/contacts/ContactsFilters.tsx` | Advanced filter panel for contacts | Multi-select dropdowns, range inputs, apply button |
| `ContactsFloatingActions` | `components/contacts/ContactsFloatingActions.tsx` | Floating multi-select action bar (export, delete) | Floating action bar, selection count badge |
| `ContactsModals` | `components/contacts/ContactsModals.tsx` | Orchestrates all contact-related modals | Modal registry |
| `ContactsMetadata` | `components/contacts/ContactsMetadata.tsx` | Contact detail metadata panel | Info rows, tag list |
| `VQLQueryBuilder` | `components/contacts/VQLQueryBuilder.tsx` | Visual VQL filter builder (drag-and-drop conditions) | Condition rows, operator selects, add/remove buttons |
| `SaveSearchModal` | `components/contacts/SaveSearchModal.tsx` | Save current filter set as named search | Text input, confirm button |
| `SavedSearchesModal` | `components/contacts/SavedSearchesModal.tsx` | Browse and load saved searches | List with load/delete actions |
| `ImportContactModal` | `components/contacts/ImportContactModal.tsx` | CSV import wizard for contacts | File upload, column mapping, progress |
| `BulkInsertModal` | `components/contacts/BulkInsertModal.tsx` | Paste-and-insert bulk contact entry | Text area, preview table, submit |
| `CompaniesList` | `components/companies/CompaniesList.tsx` | List-mode companies display | List rows, sort header |
| `CompaniesGrid` | `components/companies/CompaniesGrid.tsx` | Card-grid mode companies display | Cards with logo, name, industry |
| `CompaniesDataDisplay` | `components/companies/CompaniesDataDisplay.tsx` | Toggleable list/grid container | View toggle button, results count |
| `CompaniesFilterSidebar` | `components/companies/CompaniesFilterSidebar.tsx` | Filter sidebar for companies (industry, size, location) | Checkbox groups, range sliders, clear button |
| `CompanyRow` | `components/companies/CompanyRow.tsx` | Single company list row | Logo, name, industry tag, action menu |
| `CompanyContactsTab` | `components/companies/CompanyContactsTab.tsx` | Contacts sub-tab within company detail | Contacts mini-table, add button |
| `CompaniesModals` | `components/companies/CompaniesModals.tsx` | Orchestrates all company-related modals | Modal registry |
| `AddCompanyModal` | `components/companies/AddCompanyModal.tsx` | Add/edit company form dialog | Text inputs, domain input, submit |
| `ImportCompanyModal` | `components/companies/ImportCompanyModal.tsx` | CSV import wizard for companies | File upload, column mapping, progress |

## Contacts and Companies pages (sync-powered)

This section captures the Connectra-facing UI contract for `contacts` and `companies` pages.

| Area | Contacts page (`/contacts`) | Companies page (`/companies`) |
| --- | --- | --- |
| Tabs | `Total`, `Net New`, `Saved`, `Do Not Contact` | `All`, `Saved`, `Do Not Contact` (project-dependent) |
| View mode | Table-first with column presets (`Simple`, `Full`) | `List` / `Grid` toggle via companies display controls |
| Search/filter | `DataToolbar` + `ContactsFilters` + `VQLQueryBuilder` modal | `DataToolbar` + `CompaniesFilterSidebar` |
| Saved search UX | `SaveSearchModal`, `SavedSearchesModal` | Shared saved-search pattern where enabled |
| Multi-select | Header/row checkboxes with floating bulk action bar | Row/card selection actions where enabled |
| Modals | Import, bulk insert, save search, export, details | Add company, import company, export, details |
| Progress bars | Import and export jobs, async status polling | Import and export job progress |
| Radio buttons | Export/download options, job mode/scope options | View mode and export mode options |
| Input boxes | Toolbar search, query-builder condition values, save-search name | Toolbar search, sidebar filters, add-company form fields |
| Backend bindings | `contactsService`, `useContactsPage`, `useContactsFilters` | `companiesService`, `useCompaniesPage`, `useCompaniesFilters` |

### Activities (`1.x` / shared)

| Component | Path | Purpose | UI elements |
| --- | --- | --- | --- |
| `ActivityDetailsModal` | `components/activities/ActivityDetailsModal.tsx` | Activity event detail dialog | Info rows, status badge, timestamp |

---

## UI form elements (by type)

### Input boxes

| Use case | Where used | Notes |
| --- | --- | --- |
| Email input (single finder) | `EmailVerifierSingle`, `EmailFinderSingle` pages | Validated on blur, enter-to-submit |
| Text search input | `DataToolbar`, contacts/companies pages | Debounced via `useDebouncedValue` |
| Name + domain fields (finder) | Email finder page | Three-field row (first, last, domain) |
| CSV column mapping selects | `EmailMappingModal`, `FilesCreateJobModal` | Dropdown per source column |
| Profile text fields | `ProfileTabGeneral` | Controlled inputs with inline validation |
| Payment proof input | `UpiPaymentModal` | File input + reference text field |
| Save-search name | `SaveSearchModal` | Single text input with validation |
| Bulk paste area | `BulkInsertModal` | Multi-line textarea |
| Cron / time input | `ScheduleJobModal` | Text + time picker |
| Company form fields | `AddCompanyModal` | Multi-field form with domain, URL, industry |

### Checkboxes

| Use case | Where used |
| --- | --- |
| Row selection (data tables) | `ContactsTable`, `JobsTable` (header + row checkboxes) |
| Export column selection | `EmailExportColumnMappingFields`, `ExportModal` |
| Feature/option toggles | `FilesCreateJobModal` (include/exclude options) |
| Bulk insert confirmation | `BulkInsertModal` |

### Radio buttons

| Use case | Where used |
| --- | --- |
| Job retry scope (all / failed only) | `JobsRetryModal` |
| Schedule frequency (once / daily / weekly) | `ScheduleJobModal` |
| Download range (all rows / filtered / first N) | `FilesDownloadModal` |
| Job type (finder / verifier) | `FilesCreateJobModal` |
| View mode (list / grid) | `CompaniesDataDisplay` |

### Progress bars

| Use case | Where used | Notes |
| --- | --- | --- |
| Credit balance bar | `CreditBudgetAlerts`, `FeatureOverviewPanel`, `Sidebar` | Color changes near zero |
| Bulk upload progress | `FilesUploadModal`, `FilesUploadPanel` | % complete from S3 multipart |
| Job processing progress | `JobsCard`, `JobsPipelineStats` | Polled from jobs API |
| Verification confidence score | `EmailVerifierResult` | 0–100% confidence bar |
| Bulk results summary | `EmailVerifierBulkResults` | Stacked bar (valid/invalid/unknown) |

### Tabs

| Page / component | Tab labels |
| --- | --- |
| Profile page | General · Security · Sessions · API Keys · Team |
| Company detail | Overview · Contacts · Activities |
| Jobs detail modal | Summary · Logs · Data |
| Files detail view | Preview · Schema · Stats · Info |
| Email results | All · Valid · Invalid · Unknown |
| Admin panel | Users · Payments · Settings |

### Buttons (pattern)

| Button type | Examples |
| --- | --- |
| Primary CTA | "Find Email", "Start Verification", "Upload File", "Save Search" |
| Secondary/outline | "Cancel", "Download Sample", "Clear Filters" |
| Danger/destructive | "Delete Contact", "Retry All Failed", confirm in `ConfirmModal` |
| Icon-only | Copy email, download CSV, expand row, refresh |
| Floating action | `ContactsFloatingActions` — "Export Selected", "Delete Selected" |
| Loading state | All submit buttons show spinner while request is in-flight |

### Graphs and charts

| Chart | Component | Type | Data |
| --- | --- | --- | --- |
| Dashboard performance | `DashboardLineChart` | Line chart | Daily activity events over time |
| Pipeline stats | `JobsPipelineStats` | Bar (horizontal) | Processed / failed / pending counts |
| Usage feature bar | `FeatureOverviewPanel` | Bar (vertical) | Credits used per feature |
| Verification results | `EmailVerifierBulkResults` | Stacked bar | Valid / invalid / catchall / unknown |
| Column stats | `FilesColumnStatsPanel` | Mini bar | Null %, unique % per CSV column |
| Credit balance | `CreditBudgetAlerts` | Progress bar | Remaining / total credits |

---

## Contexts

| Context | File | Provides | Consumed by |
| --- | --- | --- | --- |
| `AuthContext` | `context/AuthContext.tsx` | `user`, `token`, `login()`, `logout()`, `refreshToken()`, `isAuthenticated` | All authenticated components, hooks |
| `RoleContext` | `context/RoleContext.tsx` | `role`, `plan`, `isAdmin`, `isSuperAdmin`, `hasFeature()`, `featureAccess` | `DashboardAccessGate`, gated components, `featureAccess.ts` |
| `ThemeContext` | `context/ThemeContext.tsx` | `theme`, `toggleTheme()` (light/dark mode) | Layout, CSS variable root |

---

## Hooks catalog

### Auth and session hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useLoginForm` | `hooks/useLoginForm.ts` | Login form state, validation, submit |
| `useRegisterForm` | `hooks/useRegisterForm.ts` | Registration form state, validation, submit |
| `useAuthRedirect` | `hooks/useAuthRedirect.ts` | Post-auth redirect logic |
| `useSessionGuard` | `hooks/useSessionGuard.ts` | Enforces authenticated session; redirects on expiry |
| `useSessions` | `hooks/useSessions.ts` | Lists and revokes active sessions |

### Dashboard hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useDashboardPage` | `hooks/useDashboardPage.ts` | Batched data fetch: stats + activities + exports |
| `useDashboardPageAccess` | `hooks/dashboard/useDashboardPageAccess.ts` | Role-based dashboard access check |
| `useDashboardData` | `hooks/useDashboardData.ts` | Low-level dashboard data state |

### Email hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useEmailFinderSingle` | `hooks/useEmailFinderSingle.ts` | Single email finder form + submission |
| `useEmailVerifierSingle` | `hooks/useEmailVerifierSingle.ts` | Single email verifier form + submission |
| `useEmailVerifierBulk` | `hooks/useEmailVerifierBulk.ts` | Bulk verifier job state and polling |

### Contacts hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useContactsPage` | `hooks/contacts/useContactsPage.ts` | Contacts page data: list, pagination, filters |
| `useContactsFilters` | `hooks/contacts/useContactsFilters.ts` | Filter state management for contacts VQL |
| `useSavedSearches` | `hooks/contacts/useSavedSearches.ts` | Load, save, and delete saved searches |
| `useContactExport` | `hooks/contacts/useContactExport.ts` | Contact export job creation and status |
| `useContactColumns` | `hooks/contacts/useContactColumns.ts` | Column visibility and order state |

### Companies hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useCompaniesPage` | `hooks/companies/useCompaniesPage.ts` | Companies page data: list, pagination, filters |
| `useCompaniesFilters` | `hooks/companies/useCompaniesFilters.ts` | Filter state management for companies |
| `useCompaniesView` | `hooks/companies/useCompaniesView.ts` | List/grid view mode state |
| `useCompanyExport` | `hooks/companies/useCompanyExport.ts` | Company export job creation and status |

### Files and upload hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useNewExport` | `hooks/useNewExport.ts` | Multipart upload orchestration (CSV → job pipeline) |
| `useCsvUpload` | `hooks/useCsvUpload.ts` | CSV file selection, validation, and upload state |
| `useFilePreview` | `hooks/useFilePreview.ts` | Preview first N rows of an uploaded file |
| `useFiles` | `hooks/useFiles.ts` | File list, selection, and management state |
| `useBucketMetadata` | `hooks/useBucketMetadata.ts` | S3 bucket metadata (size, prefix tree) |
| `useFileStats` | `hooks/useFileStats.ts` | Per-file schema and column statistics |

### Jobs hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useJobs` | `hooks/useJobs.ts` | Job list, polling, status management |
| `useExpandedJobDetails` | `hooks/useExpandedJobDetails.ts` | Expanded job detail panel state |

### Billing and usage hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useBilling` | `hooks/useBilling.ts` | Credit packs, payment submission, plan state |
| `useUsage` | `hooks/useUsage.ts` | Credit usage, feature quota, usage history |
| `useFeatureOverview` | `hooks/useFeatureOverview.ts` | Feature-level usage summary |

### UI state hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useModal` | `hooks/useModal.ts` | Generic modal open/close/data state |
| `useViewMode` | `hooks/useViewMode.ts` | List / grid / table view mode toggle |
| `useResizablePanels` | `hooks/useResizablePanels.ts` | Two-panel resize with drag handle |
| `useSidebar` | `hooks/useSidebar.ts` | Sidebar collapsed / expanded state |
| `useDebouncedValue` | `hooks/useDebouncedValue.ts` | Debounce input value for search queries |

### Platform hooks

| Hook | File | Purpose |
| --- | --- | --- |
| `useAnalytics` | `hooks/useAnalytics.ts` | Analytics data fetch and chart state |
| `useAdmin` | `hooks/useAdmin.ts` | Admin user/payment management actions |
| `useTeam` | `hooks/useTeam.ts` | Team member listing and invite |
| `useLinkedIn` | `hooks/useLinkedIn.ts` | LinkedIn/Sales Navigator integration state |
| `useAPIKeys` | `hooks/useAPIKeys.ts` | API key creation, listing, and revocation |
| `useActivities` | `hooks/useActivities.ts` | Activity log fetch and filter state |
| `useCompanies` | `hooks/useCompanies.ts` | Company data top-level state |

---

## GraphQL services catalog

| Service | File | GraphQL operations |
| --- | --- | --- |
| `authService` | `services/graphql/authService.ts` | `Login`, `Register`, `Logout`, `RefreshToken`, `ValidateToken` |
| `billingService` | `services/graphql/billingService.ts` | `GetPlans`, `GetCreditPacks`, `CreatePayment`, `GetPaymentHistory`, `ApprovePayment` |
| `contactsService` | `services/graphql/contactsService.ts` | `ListContacts`, `GetContact`, `CreateContact`, `UpdateContact`, `DeleteContact`, `ExportContacts` |
| `companiesService` | `services/graphql/companiesService.ts` | `ListCompanies`, `GetCompany`, `CreateCompany`, `UpdateCompany`, `DeleteCompany`, `ExportCompanies` |
| `emailService` | `services/graphql/emailService.ts` | `FindEmail`, `VerifyEmail`, `BulkVerifyEmail`, `GetEmailHistory` |
| `jobsService` | `services/graphql/jobsService.ts` | `CreateJob`, `GetJob`, `ListJobs`, `RetryJob`, `CancelJob`, `ScheduleJob` |
| `usageService` | `services/graphql/usageService.ts` | `Usage`, `GetUsageHistory`, `GetFeatureUsage` |
| `profileService` | `services/graphql/profileService.ts` | `GetProfile`, `UpdateProfile`, `ChangePassword`, `UpdateAvatar` |
| `adminService` | `services/graphql/adminService.ts` | `UserStats`, `ListUsers`, `AdjustCredits`, `ListPaymentSubmissions` |
| `activitiesService` | `services/graphql/activitiesService.ts` | `GetActivities`, `GetActivityStats` |
| `analyticsService` | `services/graphql/analyticsService.ts` | `GetAnalytics`, `GetUserAnalytics`, `GetAdminAnalytics` |
| `savedSearchesService` | `services/graphql/savedSearchesService.ts` | `ListSavedSearches`, `CreateSavedSearch`, `DeleteSavedSearch` |
| `linkedinService` | `services/graphql/linkedinService.ts` | `GetLinkedInProfile`, `SyncSalesNavigator` |
| `salesNavigatorService` | `services/graphql/salesNavigatorService.ts` | `SaveSalesNavigatorProfiles`, `GetSyncStatus`, `ListSyncJobs` |
| `s3Service` | `services/graphql/s3Service.ts` | `GetPresignedUploadUrl`, `ListBucketObjects`, `GetPresignedDownloadUrl` |
| `twoFactorService` | `services/graphql/twoFactorService.ts` | `EnableTwoFactor`, `DisableTwoFactor`, `VerifyOTP` |
| `usersService` | `services/graphql/usersService.ts` | `ListUsers`, `GetUser`, `InviteUser`, `UpdateUserRole` |
| `healthService` | `services/graphql/healthService.ts` | `Health` (API connectivity check) |

---

## Library utilities (`lib/`)

### Core runtime

| Module | File | Purpose |
| --- | --- | --- |
| `graphqlClient` | `lib/graphqlClient.ts` | GraphQL HTTP client (token injection, error parsing) |
| `config` | `lib/config.ts` | App env config (`NEXT_PUBLIC_API_URL`, feature flags) |
| `constants` | `lib/constants.ts` | App-wide constant values (limits, defaults) |
| `featureAccess` | `lib/featureAccess.ts` | Feature flag and plan-based access checks |
| `utils` | `lib/utils.ts` | General utilities (classnames, date format, debounce) |
| `toast` | `lib/toast.ts` | Toast notification helper (success, error, info) |
| `clipboard` | `lib/clipboard.ts` | Copy-to-clipboard with feedback |
| `animationsConfig` | `lib/animationsConfig.ts` | Framer Motion / CSS animation presets |

### Auth and session

| Module | File | Purpose |
| --- | --- | --- |
| `tokenManager` | `lib/tokenManager.ts` | Access/refresh token storage and retrieval |
| `sessionManager` | `lib/sessionManager.ts` | Session lifecycle management |
| `sessionUtils` | `lib/profile/sessionUtils.ts` | Session format helpers |
| `authValidation` | `lib/authValidation.ts` | Login/register form field validation rules |
| `authErrorHandler` | `lib/authErrorHandler.ts` | Auth error code to user message mapping |
| `apiErrorHandler` | `lib/apiErrorHandler.ts` | GraphQL/network error to toast mapping |
| `apiErrorTypes` | `lib/apiErrorTypes.ts` | TypeScript error type definitions |

### Domain utilities

| Module | File | Purpose |
| --- | --- | --- |
| `emailUtils` | `lib/email/emailUtils.ts` | Email format validation, pattern generation helpers |
| `emailValidation` | `lib/email/emailValidation.ts` | Email field validation rules |
| `jobsMapper` | `lib/jobs/jobsMapper.ts` | Job API response → UI model mapping |
| `jobsUtils` | `lib/jobs/jobsUtils.ts` | Job status color, label, and action helpers |
| `jobsValidation` | `lib/jobs/jobsValidation.ts` | Job form validation rules |
| `jobsConstants` | `lib/jobs/jobsConstants.ts` | Job status, type, and concurrency constants |
| `contactsUtils` | `lib/contacts/contactsUtils.ts` | Contact display formatters and helpers |
| `contactsConstants` | `lib/contacts/contactsConstants.ts` | Contact field names, filter options |
| `usageFormatters` | `lib/usageFormatters.ts` | Credit and usage number formatting |
| `dashboardMapper` | `lib/dashboardMapper.ts` | Dashboard API response → UI model mapping |
| `dashboardConstants` | `lib/dashboardConstants.ts` | Dashboard stat labels and chart config |
| `activitiesConstants` | `lib/activitiesConstants.ts` | Activity type labels and icon mapping |
| `s3TreeUtils` | `lib/s3/s3TreeUtils.ts` | S3 prefix tree builder for file browser |

### Page API layer

| Module | File | Purpose |
| --- | --- | --- |
| `pageApi` | `lib/api/pageApi.ts` | Base class for batched page data fetches |
| `queryBuilder` | `lib/api/queryBuilder.ts` | Dynamic GraphQL query composition |
| `dashboardPageApi` | `lib/api/pages/dashboardPageApi.ts` | Batched dashboard queries (stats + activities + exports) |
| `contactsPageApi` | `lib/api/pages/contactsPageApi.ts` | Batched contacts page queries (list + filters + metadata) |
| `companiesPageApi` | `lib/api/pages/companiesPageApi.ts` | Batched companies page queries |

---

## User-facing flows (where to look in code)

| Journey | Primary surface | Key components | Services / hooks |
| --- | --- | --- | --- |
| Sign up / sign in | `(auth)/login`, `(auth)/register` | `AuthErrorBanner`, form fields | `authService`, `useLoginForm`, `useRegisterForm` |
| Email finder (single) | `email/` page | Email input, result card | `emailService`, `useEmailFinderSingle` |
| Email verifier (single) | `email/` page | `EmailVerifierSingle`, `EmailVerifierResult` | `emailService`, `useEmailVerifierSingle` |
| Bulk CSV → jobs | `jobs/`, `files/` pages | `FilesUploadModal`, `FilesCreateJobModal`, `JobsCard` | `s3Service`, `jobsService`, `useNewExport` |
| Contacts search/filter | `contacts/` page | `ContactsTable`, `VQLQueryBuilder`, `ContactsFilters` | `contactsService`, `useContactsPage`, `useContactsFilters` |
| Companies search/filter | `companies/` page | `CompaniesList`/`CompaniesGrid`, `CompaniesFilterSidebar` | `companiesService`, `useCompaniesPage`, `useCompaniesFilters` |
| Billing, UPI proof | `billing/` page | `UpiPaymentModal`, plan cards | `billingService`, `useBilling` |
| Usage / analytics | `usage/`, `analytics/` | `FeatureOverviewPanel`, `DashboardLineChart` | `usageService`, `analyticsService`, `useUsage` |
| Admin control | `admin/` page | Stats grid, user table | `adminService`, `useAdmin` |
| Profile management | `profile/` page | `ProfileOverview`, `ProfileTabGeneral` | `profileService`, `useTeam`, `useAPIKeys` |
| AI chat | `ai-chat/` page | Chat message stream components | AI service, streaming client |
| Extension SN ingestion | `extension/contact360/` | Popup, ingestion status panel | `salesNavigatorService`, `useLinkedIn` |

---

## Design conventions and patterns

### Layout patterns

- **Two-panel (resizable):** `DataPageLayout` + `ResizeHandle` — used on contacts, companies, files pages. Left panel = list/table, right panel = detail view.
- **Toolbar + table:** `DataToolbar` / `GenericToolbar` above a sortable data table — standard pattern for all list pages.
- **Sidebar + content:** `MainLayout` wraps all authenticated pages. Sidebar collapses via `useSidebar`.
- **Floating actions:** `FloatingActionBar` appears when rows are selected (bulk actions).
- **Modal stack:** `Modal` base → feature modals (`UpiPaymentModal`, `FilesUploadModal`, etc.) — single z-index stack.
- **Paginated list:** `TablePagination` + `Pagination` component for large data sets.

### State management approach

- No global Redux/Zustand store — each page uses **React hooks + context**.
- **Auth state:** `AuthContext` + `RoleContext` (React Context API).
- **Page data:** Custom hooks (`useDashboardPage`, `useContactsPage`, etc.) wrapping `graphqlClient`.
- **Batched fetches:** Page API layer (`dashboardPageApi`, `contactsPageApi`) batches multiple GraphQL calls.
- **Optimistic UI:** Not applied globally — success/error state drives re-fetch.
- **Polling:** Jobs and export status use interval-based polling (60s default for dashboard exports).

### Error and loading states

- **Loading:** Components render skeleton states or spinner while data is fetching.
- **Error:** `Alert` component or `AuthErrorBanner` shows inline errors; `toast` for background operation errors.
- **Empty state:** Custom empty-state illustrations for no-results views (contacts, jobs).
- **Network error:** `apiErrorHandler` maps GraphQL errors to user-facing messages.

### Accessibility conventions

- All interactive elements have `aria-label` or visible label text.
- Modal focus trap via `Modal` component.
- Keyboard navigation: Tab order preserved in forms and tables.
- Color contrast: status badges use color + icon (not color alone).

---

## Related docs

| Doc | Use |
| --- | --- |
| `docs/frontend/README.md` | Page JSON inventory, CSV exports, era → surface mapping |
| `docs/frontend/components.md` | Detailed per-era component catalog |
| `docs/frontend/design-system.md` | Design tokens, primitives, form element patterns |
| `docs/frontend/hooks-services-contexts.md` | Full hook/service/context/lib catalog |
| `docs/flowchart.md` | User → UI → GraphQL → services flow diagrams |
| `docs/codebase.md` | `contact360.io/app/` implementation entry points |
| `docs/roadmap.md` / `docs/versions.md` | What ships when, by era |
| `docs/version-policy.md` | Major version themes (`0.x`–`10.x`) |


## GraphQL services catalog additions
- campaignService
- sequenceService
- templateService
- webhookService
- integrationService

## `s3storage` UI integration coverage

Primary UI-to-storage touchpoints in dashboard:

- `FilesUploadModal` and `FilesUploadPanel` for CSV and artifact upload workflows.
- `FilesCreateJobModal` and `useNewExport` for multipart upload orchestration.
- `FilesSchemaPanel`, `FilesColumnStatsPanel`, and `DataPreviewTable` for storage-backed analysis endpoints.
- Billing/profile paths for proof/avatar/photo uploads routed through gateway contracts.

Era-focused UI task packs for storage:

- `1.x`: billing proof and avatar/photo path validation UX.
- `2.x`: multipart retry/resume progress UX and clearer error states.
- `3.x`: ingestion-ready metadata display and lineage indicators.
- `4.x`: extension-origin upload status and provenance tagging.
- `6.x`: resilient retry UX and reliability diagnostics in files/jobs surfaces.
- `10.x`: campaign artifact upload/review/provenance UI consistency.

Deep backend mapping reference: `docs/codebases/s3storage-codebase-analysis.md`.

## Era-tagging requirement for UI inventory

Every documented page/component entry in frontend docs must include:

- `era`
- `introduced_in`
- `tabs` (if present)
- `ui_elements` coverage (buttons, inputs, checkboxes, radios, progress, toasts)
- `graphql_bindings` and owning hook/service references

## `logs.api` UI integration coverage

| Era | UI surfaces | Components/elements | Hooks/services/contexts |
| --- | --- | --- | --- |
| `1.x` | Billing/auth activity indicators | Alert badges, status text, timeline rows | activity hooks + auth context wiring |
| `2.x` | Job progress and result diagnostics | `JobsCard`, `ExecutionFlow`, status chips | jobs hooks and polling services |
| `6.x` | Reliability dashboards | charts, filters, search inputs, checkbox toggles | observability services + workspace context |
| `7.x` | Admin audit views | tabs, table filters, radio/select controls, export buttons | admin services + role context |
| `8.x` | API access logs | endpoint filters, key selectors, response detail panels | API analytics hooks |
| `10.x` | Campaign compliance trails | read-only timeline panels, compliance checklists | campaign services and audit contexts |

Reference: `docs/frontend/logsapi-ui-bindings.md`.

## `jobs` UI integration coverage

| Era | UI surfaces | Components/elements | Hooks/services/contexts |
| --- | --- | --- | --- |
| `0.x` | dashboard jobs shell | `JobsCard`, basic status labels | auth contexts + initial jobs service wiring |
| `1.x` | billing/usage + job ownership views | retry buttons, warning banners | role context + usage/billing hooks + jobs queries |
| `2.x` | email bulk and jobs pages | `JobsTable`, `JobsCardExpandPanel`, `ScheduleJobModal`, progress bars, mapping checkboxes/radios | `useJobs`, `useNewExport`, `useCsvUpload`, `jobsService` |
| `3.x` | contacts/companies import-export flows | `ExecutionFlow`, `JobDetailsModal`, `DataInspector`, VQL inputs | contacts/companies hooks + GraphQL jobs module |
| `4.x` | extension/SN sync visibility | sync status cards and retry controls | extension hooks/services + job polling |
| `5.x` | AI workflow batch views | AI run cards, confidence/cost displays | AI hooks + jobs orchestration services |
| `6.x` | reliability dashboards | queue/failure cards, retry and health controls | observability hooks and metrics services |
| `7.x` | admin governance views | audit timeline panels, retention filters | role-gated admin contexts + timeline API |
| `8.x` | API/integration controls | webhook callback controls, API key selectors | integration services + callback handling |
| `9.x` | tenant productization surfaces | tenant quota cards, entitlement controls | tenant contexts + quota services |
| `10.x` | campaign operations | campaign execution/timeline, compliance checklists | campaign services + jobs timeline/status hooks |

Reference: `docs/frontend/jobs-ui-bindings.md`.

## Marketing app directory structure (`contact360.io/root/src/`)

| Path | Contents |
| --- | --- |
| `components/ui/` | 3D UI primitives and composites (`Button3D`, `Input3D`, `Checkbox3D`, `Modal3D`, `Tabs3D`, `Table3D`, selectors) |
| `components/landing/` | Landing and growth sections (`Hero`, pricing sections, features, CTA blocks) |
| `hooks/` | Marketing data and UX hooks (`useMarketingPage`, `useDocumentation`, `useLandingContent`, `usePricing`, `useForceLightTheme`) |
| `services/graphql/` | GraphQL service modules for marketing/auth/billing/usage/docs |
| `context/` | `AuthContext`, `RoleContext`, `ThemeContext` |
| `lib/` | GraphQL client, auth/token utilities, helpers |

## Marketing 3D UI component catalog (root)

| Era | Components |
| --- | --- |
| `0.x` | `Button3D`, `Input3D`, `Checkbox3D`, `TabGroup`, `Tabs3D`, `Modal3D`, `Tooltip3D`, `Card3D`, `Badge3D`, `Icon3D` |
| `1.x` | pricing and billing CTA/forms using `Input3D`, `Button3D`, `Card3D` |
| `2.x` | email-system storytelling controls with `Table3D`, `RangeSlider3D`, selector components |
| `3.x` | contact/company and data UX storytelling with tabs/cards/tables |
| `5.x` | AI workflow storytelling with badges/cards/tabs |
| `8.x` | API/platform messaging surfaces with tabs/cards/tooltips |
| `10.x` | campaign storytelling modules using cards/selectors/CTA buttons |

## DocsAI admin surfaces (`contact360.io/admin`)

| Surface | Implementation path | UI controls/elements |
| --- | --- | --- |
| Authenticated shell | `templates/base.html`, `apps/core/navigation.py` | sidebar groups, nav links, header controls |
| Documentation dashboard | `apps/documentation/views/dashboard.py` | tabs, filters, list/grid views, graph viewport |
| Roadmap dashboard | `templates/roadmap/dashboard.html` | preview/edit tabs, progress bar, radio status filters |
| Architecture blueprint | `templates/architecture/blueprint.html` | preview/edit tabs, readiness progress, radio filters |
| Relationship graphs | `static/js/components/relationship-graph-viewer.js`, `graph.js` | D3 force graph, Cytoscape graph, zoom/pan/highlight |

## Email Studio wiring (`emailapis` / `emailapigo`)

- Primary route: `contact360.io/app/app/(dashboard)/email/page.tsx`
- Main tabs: `finder`, `verifier`, `assistant`
- Single finder UX: first/last/domain inputs + submit button + result cards
- Single verifier UX: email input + verify button + status badge/confidence display
- Bulk UX: drop zone + mapping modal + progress bars + results table
- Controls: mapping checkboxes, row-selection checkboxes, retry-scope radio buttons
- Hook chain: `useEmailFinderSingle`, `useEmailVerifierSingle`, `useEmailVerifierBulk`, `useCsvUpload`
- Service chain: `src/services/graphql/emailService.ts` -> GraphQL `email` module -> `LambdaEmailClient` -> `lambda/emailapis` / `lambda/emailapigo`
- Contexts: `AuthContext` (session/token), `RoleContext` (credit/role gating)

See also: `docs/frontend/emailapis-ui-bindings.md`.

## Email Campaign UI wiring (`backend(dev)/email campaign`)

The email campaign UI spans four primary pages in the dashboard (`contact360.io/app/app/(dashboard)/`). All campaign API calls route through Appointment360 GraphQL; the gateway proxies to the campaign service REST API.

### Campaigns list page (`/campaigns`)

- **Route:** `app/(dashboard)/campaigns/page.tsx`
- **Primary component:** `CampaignsList` — sortable data table of all campaigns.
- **Columns:** Campaign name, status badge, audience count, sent, failed, open rate (era `10.x`), created date.
- **Status badges:** Colour-coded pill — `pending` (grey), `sending` (blue/animated), `completed` (green), `completed_with_errors` (amber), `failed` (red), `paused` (yellow).
- **Actions:** "New Campaign" primary CTA button (opens wizard); row-level "View" link; bulk-select checkboxes for delete/export.
- **Progress bar:** For `sending` campaigns, inline mini progress bar showing sent/total percentage.
- **Hook chain:** `useCampaignsPage` → GraphQL `listCampaigns` → campaign service.

### Campaign detail page (`/campaigns/:id`)

- **Route:** `app/(dashboard)/campaigns/[id]/page.tsx`
- **Stats bar:** Four metric tiles — Sent (count + %), Failed (count + %), Opens (rate, era `10.x`), Unsubscribes (count).
- **Progress bar:** Campaign send progress bar (animated while `status=sending`).
- **Recipient table:** Paginated table — name, email, status badge, sent_at timestamp; row-level retry action (era `6.x`+).
- **Analytics tab:** Open-rate line chart, click-rate line chart, unsubscribe trend chart (era `10.x`).
- **A/B test panel:** Variant A/B split display with winner badge (era `10.x`).

### Campaign wizard (`/campaigns/new`)

- **Route:** `app/(dashboard)/campaigns/new/page.tsx`
- **Step 1 — Audience:** Three radio buttons: "Use Saved Segment", "Run VQL Query", "Upload CSV". Audience count preview text below radio selection. "Next" button disabled until source selected.
- **Step 2 — Template:** Template grid with thumbnail previews. "Create New Template" shortcut link. Preview modal on hover.
- **Step 3 — Schedule:** Date/time picker with timezone selector. "Send Now" checkbox (overrides schedule). "AI-suggested time" option badge (era `5.x`).
- **Step 4 — Confirm:** Summary card showing audience size, template name, scheduled time, estimated credits. Editable via "Back" links. "Launch Campaign" primary button.
- **Checkboxes:** "Send Now" checkbox, "Enable A/B test" checkbox, "AI-optimized time" checkbox.
- **Progress bar:** Step indicator (1–4) at top of wizard.

### Template builder page (`/campaigns/templates`)

- **Route:** `app/(dashboard)/campaigns/templates/page.tsx`
- **Template list:** Searchable grid with thumbnail, name, subject preview, AI badge (for AI-generated), action buttons (Edit, Duplicate, Delete).
- **Template editor modal:** Split view — HTML source editor (left) + rendered preview (right). Variable insertion buttons (`{{FirstName}}`, `{{LastName}}`, `{{Company}}`, `{{UnsubscribeURL}}`). Subject line input. Save / Preview / Delete actions.
- **AI generation:** "Generate with AI" button → prompt textarea drawer → streams AI output into editor. AI confidence badge after generation.
- **Preview mode:** Renders template with sample `TemplateData` via `POST /templates/:id/preview`.
- **Input boxes:** Template name, subject line, HTML body editor, AI prompt textarea.

### Sequence builder page (`/campaigns/sequences`)

- **Route:** `app/(dashboard)/campaigns/sequences/page.tsx`
- **Step canvas:** Drag-and-drop vertical canvas with step cards.
- **Step types:** Email step card (template picker + delay input), Wait step card (days/hours input), Branch step card (condition radio: "if opened", "if clicked", "if not opened").
- **Sequence list sidebar:** Existing sequences with status, step count, active recipient count.
- **Sequence actions:** Start, Pause, Archive buttons; status badge per sequence.

### Component inventory (campaign UI)

| Component | Type | Used in pages |
| --- | --- | --- |
| `CampaignsList` | Table | Campaigns list |
| `CampaignStatusBadge` | Badge/pill | All campaign pages |
| `CampaignSendProgress` | Progress bar | List + detail |
| `CampaignWizard` | Multi-step form | New campaign |
| `AudienceSourcePicker` | Radio button group | Wizard step 1 |
| `AudienceCountPreview` | Text/number display | Wizard step 1 |
| `TemplatePicker` | Grid selector | Wizard step 2 |
| `TemplateThumbnail` | Card + preview modal | Templates list + wizard |
| `TemplateEditor` | Split HTML editor + preview | Template builder |
| `AITemplateGenerator` | Textarea + streaming output | Template builder |
| `SchedulePicker` | Date/time picker + checkbox | Wizard step 3 |
| `CampaignSummaryCard` | Summary + edit links | Wizard step 4 |
| `RecipientTable` | Paginated table | Campaign detail |
| `CampaignStatsBar` | Metric tiles | Campaign detail |
| `AnalyticsCharts` | Line charts | Campaign detail analytics tab |
| `SequenceCanvas` | Drag-drop step builder | Sequence builder |
| `SequenceStepCard` | Step type card | Sequence builder |

### Hook and service chain

```
useCampaignsPage → GraphQL listCampaigns → campaign service GET /campaigns
useCampaignDetail → GraphQL getCampaign + listRecipients → campaign service
useCampaignWizard → GraphQL createCampaign → POST /campaign
useTemplates → GraphQL listTemplates / createTemplate / deleteTemplate → /templates
useSequence → GraphQL createSequence / triggerSequence → /sequences
```

### Context and RBAC

- `AuthContext`: session token forwarded to GraphQL calls.
- `RoleContext`: `campaign-manager` role required for create/delete; `viewer` role is read-only.
- Feature flag: `email_campaigns_enabled` gate on all campaign routes (era `0.x`–`2.x` will be false by default).

See also: `docs/frontend/pages/campaign_builder_page.json`, `docs/frontend/pages/campaigns_page.json`, `docs/frontend/pages/campaign_templates_page.json`, `docs/frontend/pages/sequences_page.json`.

---

## Contact AI UI integration coverage (`backend(dev)/contact.ai`)

### Era coverage table

| Era | Dashboard page/route | Contact AI features active |
| --- | --- | --- |
| `0.x`–`1.x` | None | Health CI probe only |
| `2.x` | Contact detail page | `EmailRiskBadge` on email field |
| `3.x` | Contact search + company detail | `AIFilterInput` on search, `CompanySummaryTab` on company detail |
| `4.x` | Extension popup (optional) | AI chat context action (optional) |
| `5.x` | `/app/ai-chat` (new page) | Full chat list, thread, streaming, model selector, all utility components |
| `6.x` | `/app/ai-chat` | Error state, retry button, SSE reconnect, reliability wrappers |
| `7.x` | `/app/ai-chat` + admin | Role-gated AI features, admin usage view |
| `8.x` | `/app/settings/api-keys` | AI API quota display |
| `9.x` | `/app/integrations` | AI-powered connector config panel |
| `10.x` | `/app/campaigns/editor` | `CampaignAIAssistant` panel (subject/body generation) |

### Component inventory (Contact AI)

| Component | Type | Page/surface | Contact AI endpoint |
| --- | --- | --- | --- |
| `AIChatPage` | Page layout | `/app/ai-chat` | All `/api/v1/ai-chats/` |
| `ChatList` | Paginated list | AI chat page | `GET /api/v1/ai-chats/` |
| `ChatListItem` | List item card | AI chat page | — |
| `NewChatButton` | Button | AI chat page | `POST /api/v1/ai-chats/` |
| `ChatThread` | Message thread | AI chat page | `GET /api/v1/ai-chats/{id}/` |
| `ChatMessage` | Message bubble | AI chat page | — |
| `ContactsInMessage` | Inline contact cards | AI chat page | — (from AI reply JSONB) |
| `ChatInput` | Textarea + send | AI chat page | `POST /api/v1/ai-chats/{id}/message` |
| `StreamingText` | Token-by-token display | AI chat page | `POST /message/stream` (SSE) |
| `ModelSelector` | Dropdown / radio | AI chat page | `model` field in send payload |
| `ChatContextMenu` | Rename/delete actions | AI chat page | `PUT` / `DELETE /api/v1/ai-chats/{id}/` |
| `AILoadingSpinner` | Spinner | AI chat page | Streaming / loading state |
| `AIErrorState` | Error + retry CTA | AI chat page | `503` / `429` / timeout |
| `EmailRiskBadge` | Inline badge | Contact detail | `POST /api/v1/ai/email/analyze` |
| `CompanySummaryTab` | Tab panel | Company detail | `POST /api/v1/ai/company/summary` |
| `AIFilterInput` | NL text + chips | Contact search | `POST /api/v1/ai/parse-filters` |
| `CampaignAIAssistant` | Side panel | Campaign editor | `POST /api/v1/ai/email/generate` (`10.x`) |

### Input box and control bindings

| Control | Type | Component | Validation |
| --- | --- | --- | --- |
| Chat message | `<textarea>` | `ChatInput` | Min 1, max 10 000 chars |
| Model picker | `<select>` / radio | `ModelSelector` | FLASH, PRO, FLASH_2_0, PRO_2_5 |
| Chat title rename | `<input type="text">` | `ChatContextMenu` | Max 255 chars |
| Email risk input | `<input type="email">` | `EmailRiskBadge` | Valid email, max 255 chars |
| Company name | `<input type="text">` | `CompanySummaryTab` | Max 255 chars |
| Industry | `<input type="text">` | `CompanySummaryTab` | Max 255 chars |
| NL filter query | `<input type="text">` | `AIFilterInput` | Max 1000 chars |

### Progress bars and loading states

| State | Component | Visual |
| --- | --- | --- |
| Chat list loading | `ChatList` skeleton | Skeleton rows |
| Message sending (sync) | `AILoadingSpinner` | Spinner + disabled input |
| SSE stream active | `StreamingText` | Token append + cursor blink |
| Email risk loading | `EmailRiskBadge` | Inline spinner |
| Company summary loading | `CompanySummaryTab` | Shimmer placeholder |
| Filter parse loading | `AIFilterInput` | Input disabled + spinner |
| Rate limit error | `AIErrorState` | Retry countdown (`Retry-After`) |

### Hooks and contexts

| Hook / Context | Purpose | GraphQL operation |
| --- | --- | --- |
| `useChatList` | Paginated chat list | `aiChats` query |
| `useChat` | Single chat with messages | `aiChat` query |
| `useSendMessage` | Send message (sync) | `sendMessage` mutation |
| `useStreamMessage` | SSE token stream | Direct SSE to `LambdaAIClient` |
| `useCreateChat` | Create new chat | `createAIChat` mutation |
| `useDeleteChat` | Delete chat | `deleteAIChat` mutation |
| `useRenameChat` | Update title | `updateAIChat` mutation |
| `useEmailRisk` | Email risk analysis | `analyzeEmailRisk` mutation |
| `useCompanySummary` | Company summary | `generateCompanySummary` mutation |
| `useParseFilters` | NL → filter chips | `parseContactFilters` mutation |
| `AIChatContext` | Selected chat, stream state | Global |
| `AIModelContext` | Selected model (localStorage) | Global |

**Deep reference:** `docs/frontend/contact-ai-ui-bindings.md`

---

## Appointment360 GraphQL gateway — UI wiring per page

`contact360.io/api` is the sole API surface consumed by every dashboard page and the browser extension. All hooks and services below route through the single `/graphql` endpoint. Auth is managed by Bearer JWT stored by `AuthContext`.

### Auth pages (`/login`, `/register`, `/forgot-password`)

| UI element | Bound operation | Module |
| --- | --- | --- |
| Login form (email + password fields) | `mutation login(email, password)` | `auth` |
| Register form (name + email + password) | `mutation register(...)` | `auth` |
| Logout button (header) | `mutation logout` | `auth` |
| Token refresh (silent, on 401) | `mutation refresh_token(refresh_token)` | `auth` |
| "Me" on app load | `query me` | `auth` |

**Hooks/context:** `useAuth` (login, logout, auto-refresh), `AuthContext` (user object, isAuthenticated, credits)

---

### `/contacts` page

| UI element | Bound operation | Module |
| --- | --- | --- |
| Contact list table | `query contacts(query: VQLQueryInput)` | `contacts` |
| Contacts count badge | `query contactCount(query)` | `contacts` |
| Filter sidebar (field selectors) | `query contacts.filters()` | `contacts` |
| Filter value typeahead | `query contacts.filterData(input)` | `contacts` |
| Search / query builder input | VQL `where` field builder → `contacts(query)` | `contacts` |
| Pagination controls (page/per_page) | `page`/`per_page` in VQLQueryInput | `contacts` |
| Sort column headers | `sort` field in VQLQueryInput | `contacts` |
| Contact row click → detail modal | `query contact(uuid)` | `contacts` |
| Export button | `mutation exportContacts(query)` → job dispatch | `contacts` + `jobs` |
| Import CSV modal | `mutation createContact360Import(...)` | `jobs` |
| Add contact button | `mutation createContact(input)` | `contacts` |
| Save search button | `mutation savedSearches.createSavedSearch(...)` | `savedSearches` |
| Saved searches sidebar | `query savedSearches(type: "contact")` | `savedSearches` |
| LinkedIn import button | `mutation upsertByLinkedinUrl(url)` | `linkedin` / `contacts` |

**Hooks:** `useContactsPage`, `useContactsFilters`, `useContactColumns`, `useContactExport`, `useSavedSearches`
**Services:** `contactsService.ts` → `listContacts`, `getContact`, `contactCount`, `getContactFilters`, `getContactFilterData`

---

### `/companies` page

| UI element | Bound operation | Module |
| --- | --- | --- |
| Company grid / list view | `query companies(query: VQLQueryInput)` | `companies` |
| Companies count | `query companyCount(query)` | `companies` |
| Filter sidebar | `query companies.filters()` + `filterData()` | `companies` |
| Company card → detail modal | `query company(uuid)` | `companies` |
| Company contacts tab | `query companyContacts(company_uuid)` | `companies` |
| Export button | `mutation exportCompanies(query)` | `companies` + `jobs` |
| View toggle (grid / list) | Local state only | — |
| Add company button | `mutation createCompany(input)` | `companies` |

**Hooks:** `useCompaniesPage`, `useCompaniesFilters`, `useCompaniesView`, `useCompanyExport`
**Services:** `companiesService.ts` → `listCompanies`, `getCompany`, `companyContacts`

---

### `/email` page (Finder, Verifier, Assistant tabs)

| UI element | Bound operation | Module |
| --- | --- | --- |
| Finder tab, single email input | `query findEmails(input)` | `email` |
| Finder tab, bulk CSV upload | `mutation createEmailFinderExport(...)` → poll `query job(jobId)` | `email` + `jobs` |
| Verifier tab, single email input | `query verifySingleEmail(input)` | `email` |
| Verifier tab, bulk CSV upload | `mutation createEmailVerifyExport(...)` → poll `query job(jobId)` | `email` + `jobs` |
| Job progress bar (bulk) | `query job(jobId)` polling every 2s | `jobs` |
| Download result button | `mutation s3.getDownloadUrl(key)` after job completes | `s3` |
| Add email pattern modal | `mutation addEmailPattern(input)` | `email` |
| Pattern import CSV | `mutation createEmailPatternImport(...)` | `jobs` |
| Jobs history list | `query jobs(limit, offset, jobType: "email_export")` | `jobs` |
| Retry failed job button | `mutation retryJob(jobId)` | `jobs` |

**Hooks:** `useEmailFinderSingle`, `useEmailFinderBulk`, `useEmailVerifierSingle`, `useEmailVerifierBulk`, `useCsvUpload`, `useJobStatus`
**Services:** `emailService.ts`, `jobsService.ts`

---

### `/campaigns` page and sub-pages

| UI element | Bound operation | Module |
| --- | --- | --- |
| Campaigns list table | `query campaigns(limit, offset, status)` | `campaigns` (10.x) |
| Campaign status badge + progress bar | `sent / total` ratio from `CampaignType` | `campaigns` |
| Campaign detail modal | `query campaign(uuid)` | `campaigns` |
| New campaign button → `/campaigns/new` | local navigation | — |
| Delete campaign | `mutation deleteCampaign(uuid)` | `campaigns` |
| Pause / resume buttons | `mutation pauseCampaign` / `mutation resumeCampaign` | `campaigns` |
| `/campaigns/new` wizard step 1 — audience | VQL contacts filter → `contactCount(query)` preview | `contacts` |
| `/campaigns/new` wizard step 2 — template | `query campaignTemplates()` | `campaignTemplates` |
| `/campaigns/new` wizard step 3 — schedule | date/time picker → schedule fields on `CreateCampaignInput` | `campaigns` |
| `/campaigns/new` wizard step 4 — confirm + send | `mutation createCampaign(input)` | `campaigns` |
| `/campaigns/templates` list | `query campaignTemplates()` | `campaignTemplates` |
| Template create/edit modal (WYSIWYG) | `mutation createCampaignTemplate` / `updateCampaignTemplate` | `campaignTemplates` |
| Template variable `{{Name}}` highlight | local rich-text component | — |
| `/campaigns/sequences` list | `query sequences(campaignUuid)` | `sequences` (10.x) |
| Add sequence step button | `mutation createSequence(input)` | `sequences` |
| Sequence step drag-and-drop reorder | `mutation reorderSequenceSteps(...)` | `sequences` |

**Hooks:** `useCampaignList`, `useCampaignWizard`, `useCampaignTemplates`, `useSequenceBuilder`
**Services:** `campaignsService.ts` → binds to 10.x GraphQL modules

---

### Profile, billing, admin pages

| UI element | Bound operation | Module |
| --- | --- | --- |
| Credits counter (header) | `query usage(feature)` | `usage` |
| Profile page → update profile | `mutation updateProfile(input)` | `profile` |
| API keys list | `query apiKeys()` | `profile` |
| Create API key button | `mutation createApiKey(name)` | `profile` |
| Revoke API key | `mutation deleteApiKey(id)` | `profile` |
| Sessions list | `query sessions()` | `profile` |
| 2FA enable flow | `mutation enableTwoFactor` → QR code → `mutation verifyTwoFactor(otp)` | `twoFactor` |
| Billing page → plans | `query plans` | `billing` |
| Subscribe button | `mutation subscribe(planId)` → idempotency key required | `billing` |
| Purchase add-on | `mutation purchaseAddon(...)` | `billing` |
| Submit payment proof | `mutation submitPaymentProof(amount, proofUrl)` | `billing` |
| Admin panel (SuperAdmin) → user list | `query admin.users()` | `admin` |
| Admin credit user | `mutation admin.creditUser(user_uuid, feature, amount)` | `admin` |
| Notification bell | `query notifications()` (poll 30s) | `notifications` |
| Notification drop-down | `mutation markNotificationRead(id)` | `notifications` |

**Hooks:** `useCredits`, `useApiKeys`, `useTwoFactor`, `useBilling`, `useNotifications`
**Context:** `AuthContext`, `CreditContext`, `NotificationContext`

---

### Appointment360 gateway — component and context inventory

| Component / Context / Hook | Role | GraphQL binding |
| --- | --- | --- |
| `AuthContext` | Global user state, JWT tokens | `query me`, `mutation login/logout/refresh` |
| `CreditContext` | Credit balance per feature | `query usage(feature)` |
| `NotificationContext` | Unread count, notification list | `query notifications()` |
| `useGraphQLClient` | Authenticated httpx GraphQL transport | All mutations/queries |
| `useContactsPage` | Contacts list, filters, pagination | `contacts`, `contactCount`, `filters`, `filterData` |
| `useCompaniesPage` | Companies list, filters, pagination | `companies`, `companyCount`, `filters`, `filterData` |
| `useEmailFinderSingle` | Single email find | `findEmails` |
| `useEmailVerifierSingle` | Single email verify | `verifySingleEmail` |
| `useJobStatus` | Job polling wrapper | `query job(jobId)` |
| `useSavedSearches` | Load, save, apply, delete searches | `savedSearches` module |
| `useCampaignList` | Campaign listing, status | `campaigns` (10.x) |
| `useCampaignWizard` | Multi-step campaign creation flow | `campaigns` + `contacts` + `campaignTemplates` |
| `useNotifications` | Polling, mark-read, badge count | `notifications` |
| `useAdminPanel` | Admin stats, credit, payment approval | `admin` |
| `useAuth` | Login, logout, refresh token | `auth` |

---

## Extension surface — `extension/contact360`

> **Surface type:** Logic + transport layer (not a standalone UI app). Provides auth, API client, and data hygiene utilities consumed by extension popup/content scripts.

### Directory structure

```
extension/contact360/
├── auth/
│   └── graphqlSession.js      # JWT decode, expiry check, proactive refresh, chrome.storage.local
├── utils/
│   ├── lambdaClient.js        # Batched REST client → POST /v1/save-profiles (retry, jitter, adaptive timeout)
│   └── profileMerger.js       # Profile dedup and merge by completeness score
├── tests/                     # Jest unit + integration tests
└── docs/                      # Sales Navigator API service docs
```

### UI elements (expected in extension popup / content scripts)

| UI element | Role | Era |
| --- | --- | --- |
| Profile count badge | Shows deduplicated vs raw profile count | 4.x |
| Upload progress bar | % complete while batch save runs | 4.x |
| Error toast | Failed batch error with retry CTA | 4.x |
| Token status indicator | Active / Expired badge | 1.x |
| Sync status panel | Batch upload results (saved / errored) | 4.x |
| Company capture checkbox | Toggle company profile capture | 3.x |
| Dedup settings radio group | Merge strategy: strict / loose | 4.x |

### Utilities and services

| File | Type | Key export | Era |
| --- | --- | --- | --- |
| `auth/graphqlSession.js` | Auth utility | `getValidAccessToken()`, `storeTokens()`, `refreshAccessToken()` | 1.x–4.x |
| `utils/lambdaClient.js` | REST client | `saveProfiles(profiles[])` with batching, retry, compression | 3.x–6.x |
| `utils/profileMerger.js` | Data utility | `deduplicateProfiles(profiles[])`, `mergeProfiles(a,b)`, `scoreProfile(p)` | 3.x–4.x |

### Backend API bindings

| Function call | Endpoint | Era |
| --- | --- | --- |
| `refreshAccessToken()` | `POST /graphql` → `mutation auth.refreshToken` | 1.x |
| `saveProfiles()` | `POST /v1/save-profiles` (Lambda SN API) | 3.x |
| Lambda SN API relay | `POST /contacts/bulk` + `POST /companies/bulk` (Connectra) | 3.x |

### Data sources

| Source | Access | Era |
| --- | --- | --- |
| `chrome.storage.local` | `accessToken`, `refreshToken` | 1.x |
| LinkedIn / SN DOM | Profile HTML scrape (content script) | 3.x–4.x |
| Appointment360 GraphQL | Token refresh, session validation | 1.x |
| Lambda SN API | Profile submission and relay to Connectra | 3.x |

### Era contributions

| Era | Extension contribution |
| --- | --- |
| `0.x` | Extension folder scaffolded; no active logic |
| `1.x` | Auth/token lifecycle: `graphqlSession.js` with `chrome.storage.local` pattern |
| `3.x` | Profile capture: `profileMerger.js` dedup; `lambdaClient.js` core save flow |
| `4.x` | SN maturity: retry/back-off, adaptive timeout, proactive token refresh, batch chunking |
| `6.x` | Reliability: exponential back-off + jitter, request queueing, adaptive timeout |
| `8.x` | `/v1/save-profiles` documented as private API; `auth.refreshToken` as public GraphQL surface |
| `9.x` | SN as primary external ingestion channel for ecosystem data |
| `10.x` | SN profile bulk ingestion feeds email campaign contact lists |

---

## Sales Navigator service — UI/UX integration coverage

**Service:** `backend(dev)/salesnavigator`
**Primary era:** `4.x`
**Deep reference:** `docs/frontend/salesnavigator-ui-bindings.md`

### Extension popup surface (4.x primary delivery)

| UI element | Component | Bound to | Era |
| --- | --- | --- | --- |
| "Save to Contact360" button | `SNSaveButton` | `POST /v1/save-profiles` (via GraphQL) | 4.x |
| "Sync Page" CTA | `SNSyncCTA` | `POST /v1/scrape` (`save:true`) | 4.x |
| Profile count badge | `SNProfileCountBadge` | Extraction result count | 4.x |
| Save progress bar (indeterminate → determinate) | `SNSaveProgress` | Save session state | 4.x |
| Saved count display | `SNSaveSummaryCard` | `saved_count` from response | 4.x |
| Created/updated split | `SNSaveSummaryCard` | `contacts_created` / `contacts_updated` | 4.x |
| Error toast | `SNErrorToast` | `errors[]` in response | 4.x |
| Error drawer | `SNErrorDrawer` | Failed profiles list | 4.x |
| Retry button | `SNRetryButton` | Re-call save after error | 4.x |
| Data quality badge | `DataQualityBadge` | `data_quality_score` per profile | 4.x |
| Already-saved indicator | `AlreadySavedBadge` | UUID match returned | 4.x |
| Profile checkbox / Select-all | `ProfileCheckbox` / `ProfileSelectAll` | Client-side selection | 4.x |
| Connection degree badge | `ConnectionDegreeBadge` | `connection_degree` | 4.x |

### Dashboard — Contacts / SN ingestion panel (3.x–4.x)

| UI element | Component | Bound to | Era |
| --- | --- | --- | --- |
| SN ingestion panel | `SNIngestionPanel` | `/contacts/import` SN tab | 3.x–4.x |
| Sync history table | `SNSyncHistoryTable` | Past sessions via Connectra | 4.x |
| Ingestion stats card | `SNIngestionStatsCard` | `saved_count`, error rate | 4.x |
| Source filter chip | `SNSourceFilterChip` | `source=sales_navigator` VQL filter | 3.x |
| "Source: Sales Navigator" badge | `ContactSourceBadge` | `contact.source` field | 3.x |
| Seniority chip | `SeniorityChip` | `contact.seniority` | 3.x |
| Department chip(s) | `DepartmentChips` | `contact.departments[]` | 3.x |
| Data quality progress bar (thin) | `DataQualityBar` | `contact.data_quality_score` | 4.x |
| SN profile URL link | `SNProfileLink` | `contact.linkedin_sales_url` | 3.x |

### Hooks

| Hook | Purpose | Era |
| --- | --- | --- |
| `useSaveProfiles` | Save profile array → `saveSalesNavigatorProfiles` mutation | 4.x |
| `useScrapeAndSave` | Parse HTML + save → `POST /v1/scrape` | 4.x |
| `useSNSyncStatus` | Poll sync result + loading/error state | 4.x |
| `useSNHistory` | Load SN ingestion history from Connectra | 4.x |
| `useContactSourceFilter` | Apply `source=sales_navigator` filter | 3.x |

### Progress bar state machine

| Phase | Value | Message |
| --- | --- | --- |
| Idle | 0% | — |
| Extracting profiles | 20% | "Extracting profiles…" |
| Deduplicating | 40% | "Deduplicating…" |
| Saving to Contact360 | 60–90% | "Saving profiles…" |
| Complete (success) | 100% | "X profiles saved" |
| Partial error | 100% (amber) | "X saved, Y failed" |
---

## Email app surface — `contact360.io/email`

### Route map

| Route | Purpose | UI elements |
| --- | --- | --- |
| `/auth/login` | User login | Email/password inputs, submit button, error text |
| `/auth/signup` | User registration | Username/email/password inputs, submit button |
| `/inbox` | Inbox folder | Folder tabs, table, checkboxes, row actions, pagination |
| `/sent` | Sent folder | Table view reused from inbox |
| `/spam` | Spam folder | Table view reused from inbox |
| `/draft` | Draft folder | Table view reused from inbox |
| `/email/[mailId]` | Email detail | Sanitized HTML body render, loading spinner |
| `/account/[userId]` | Profile + IMAP accounts | Avatar, inputs, provider grid, connect form, switch buttons |

### UI control inventory
- **Tabs:** all/unread/flagged in `DataTable`.
- **Buttons:** compose, account actions, connect/switch, row actions.
- **Inputs:** auth and account forms, table filter input.
- **Checkbox:** row selection and select-all.
- **Progress/loader:** spinner and loading states (no numeric progress bar yet).
- **Radio:** no active radio control in current mailbox flow.
- **Graph:** `ui/chart.tsx` available but not wired to mailbox pages.

### Backend bindings
- `POST /auth/login`, `POST /auth/signup`, `POST /logout`
- `GET /auth/user/{id}`
- `GET /api/emails/{folder}`
- `GET /api/emails/{mailId}?folder=...`
- `GET /api/user/{id}`, `PUT /api/user/update/{id}`, `POST /api/user/imap/{id}`

### Data/security notes
- `mailhub_active_account` is persisted in localStorage by `ImapContext`.
- Email details HTML is sanitized with DOMPurify before render.
- Current `X-Email` / `X-Password` header transport is documented as legacy and must migrate to a mailbox session token model.

---

## Mailvetter verifier UI wiring

Mailvetter is backend-first; product UI consumes it through gateway email verification contracts.

### Dashboard `/email` verifier mapping

| UI element | Bound operation | Backend chain |
| --- | --- | --- |
| Single email input + verify button | `verifySingleEmail` | App -> Appointment360 `email` module -> verifier backend |
| Bulk CSV upload + start | `verifyEmailsBulk` / jobs | App -> Appointment360 `jobs` + `email` -> verifier backend |
| Job progress bar | `job(jobId)` polling | App -> Appointment360 `jobs` |
| Result status chips | `valid/risky/invalid/catch_all/unknown` | mapped from verifier result |
| Confidence score | `confidence_score` | mapped from verifier score |
| Detail drawer/modal | `score_details` and `analysis` | explainability payload |

### Legacy operator UI (`backend(dev)/mailvetter/.../static/index.html`)

| UI element | Behavior |
| --- | --- |
| API key input | Saves Bearer token in localStorage |
| CSV input + Start button | Uploads CSV to legacy `/upload` |
| Progress bar + counts | Polls legacy `/status` endpoint |
| Results table + pagination | Pulls paged rows from legacy `/results` |
| Row detail modal | Renders raw per-email analysis JSON |
| Download CSV button | Client-side export of loaded rows |

### UX governance

- Dashboard verifier UI is canonical product surface.
- Legacy static UI is operational fallback only.
- New product work must align to `/v1` semantics and gateway contracts.

## Admin frontend surface (`contact360.io/admin`)

- Rendering model: Django templates + Tailwind asset pipeline for admin/operator workflows.
- Primary operational views: billing, users, logs, jobs, storage, settings.
- Role controls: `require_super_admin` and `require_admin_or_super_admin` guards on privileged pages.
- Scope note: `contact360.io/admin` is an **internal control plane only**, not a customer-facing product UI. No new product UX should be implemented using Django templates; all new customer surfaces belong in the Next.js apps (`contact360.io/app`, `contact360.io/root`, `contact360.io/email`).

### Admin view bindings

| Admin UI surface | Bound view/service |
| --- | --- |
| Billing payment review | `billing_payments_view` + `admin_client` mutations |
| Billing QR/settings | `billing_qr_upload_view`, `billing_settings_view` |
| Logs console | `logs_view` + `logs_api_client.py` |
| Jobs console | `jobs_view` + job scheduler client |
| Storage console | `storage_files_view` + `s3storage_client.py` |

### Integration clients (admin)

- `apps/admin/services/admin_client.py` -> Appointment360 GraphQL.
- `apps/admin/services/logs_api_client.py` -> `lambda/logs.api`.
- `apps/admin/services/s3storage_client.py` -> `lambda/s3storage`.

Known gap: `s3storage_client.py` auth-header behavior requires parity with storage auth contract hardening (`S3S-0.1`).


## Assets & Exports
- [Pages Export Excel](frontend/excel/pages_export_2026-03-16.xlsx)
