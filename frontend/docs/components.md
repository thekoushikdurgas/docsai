# Contact360 Component Catalog

Comprehensive inventory of all UI components in `contact360.io/app/src/components/`, organized by product era and domain. Each entry includes the component file path, purpose, primary UI elements, key props/state, and which hooks/services it depends on.

**Canonical code root:** `contact360.io/app/src/`  
**Related:** `docs/frontend.md` (overview), `docs/frontend/design-system.md` (primitives), `docs/frontend/hooks-services-contexts.md` (hooks/services)

---

## Foundation (`0.x`) — Layout and shell

### `MainLayout`
- **File:** `components/layout/MainLayout.tsx`
- **Purpose:** Root wrapper for all authenticated dashboard pages. Renders `Sidebar`, top header bar, and the main content slot.
- **UI elements:** Fixed sidebar, top bar with user badge + credit indicator, scrollable content area, `CreditBudgetAlerts` at top.
- **Key children:** `Sidebar`, `CreditBudgetAlerts`
- **Contexts:** `AuthContext`, `RoleContext`, `ThemeContext`

### `Sidebar`
- **File:** `components/layout/Sidebar.tsx`
- **Purpose:** Left navigation panel with route links, credit balance progress bar, user avatar, and collapse toggle.
- **UI elements:** Nav links (icon + label), credit progress bar, user badge (avatar + name + plan), collapse toggle button.
- **Hook:** `useSidebar` (collapsed/expanded state)
- **Context:** `RoleContext` (gated nav items)

### `DataPageLayout`
- **File:** `components/layouts/DataPageLayout.tsx`
- **Purpose:** Resizable two-panel layout used on contacts, companies, and files pages. Left = list/table, right = detail.
- **UI elements:** Left panel (flex), `ResizeHandle` drag divider, right panel (collapsible).
- **Hook:** `useResizablePanels`

### `DashboardAccessGate`
- **File:** `components/shared/DashboardAccessGate.tsx`
- **Purpose:** Route guard that checks authentication and redirects unauthenticated users to `/login`.
- **UI elements:** Transparent wrapper (no visible UI) or loading spinner during token check.
- **Contexts:** `AuthContext`, `RoleContext`

### `AuthErrorBanner`
- **File:** `components/auth/AuthErrorBanner.tsx`
- **Purpose:** Inline error message display on login/register pages (wrong password, email taken, etc.).
- **UI elements:** Alert-style banner with error icon and message text.

---

## Foundation (`0.x`) — UI primitives

### `Modal`
- **File:** `components/ui/Modal.tsx`
- **Purpose:** Base modal container: backdrop overlay, centered card, close button (`×`), portal rendering.
- **UI elements:** Semi-transparent backdrop, white card (rounded corners, shadow), close icon button, slot for children.
- **Props:** `isOpen`, `onClose`, `title?`, `size?` (sm/md/lg/xl)
- **Used by:** All feature modals throughout the app.

### `ConfirmModal`
- **File:** `components/ui/ConfirmModal.tsx`
- **Purpose:** Destructive-action confirmation dialog. Shows message and "Confirm" + "Cancel" buttons.
- **UI elements:** Warning icon, message text, danger "Confirm" button (red), "Cancel" outline button.
- **Props:** `isOpen`, `onClose`, `onConfirm`, `message`, `confirmLabel?`

### `Popover`
- **File:** `components/ui/Popover.tsx`
- **Purpose:** Floating popover/tooltip anchored to a trigger element. Used for contextual menus and info overlays.
- **UI elements:** Trigger slot, floating panel (anchored with position logic), optional arrow.
- **Props:** `trigger`, `content`, `placement?` (top/bottom/left/right)

### `Alert`
- **File:** `components/ui/Alert.tsx`
- **Purpose:** Inline status alert (success ✓, warning ⚠, error ✕, info ℹ).
- **UI elements:** Icon, color-coded left border, message text, optional dismiss button.
- **Props:** `type` (`success`|`warning`|`error`|`info`), `message`, `dismissible?`

### `ResizeHandle`
- **File:** `components/shared/ResizeHandle.tsx`
- **Purpose:** Draggable divider between two panels in `DataPageLayout`.
- **UI elements:** Thin vertical bar, grab cursor on hover, visual drag indicator.
- **Hook:** Receives drag handlers from `useResizablePanels`.

### `FloatingActionBar`
- **File:** `components/shared/FloatingActionBar.tsx`
- **Purpose:** Sticky bottom action bar that appears when table rows are selected. Shows selection count and bulk action buttons.
- **UI elements:** Pill-shaped bar (fixed bottom center), selection count badge, action buttons (export, delete, etc.).
- **Props:** `selectedCount`, `actions[]` (label, onClick, variant)

### `TablePagination`
- **File:** `components/shared/TablePagination.tsx`
- **Purpose:** Page size selector and current-page / total-pages controls below data tables.
- **UI elements:** "Rows per page" select (10/25/50/100), `←` / `→` arrow buttons, "Page X of Y" text.
- **Props:** `page`, `pageSize`, `total`, `onPageChange`, `onPageSizeChange`

### `FilterSection`
- **File:** `components/shared/FilterSection.tsx`
- **Purpose:** Collapsible labeled filter group used in sidebars.
- **UI elements:** Section label with chevron toggle, animated collapse/expand, slot for filter controls.
- **Props:** `label`, `defaultOpen?`, `children`

### `ExportModal`
- **File:** `components/shared/ExportModal.tsx`
- **Purpose:** Generic export dialog: choose columns and output format (CSV/Excel/JSON).
- **UI elements:** Column checklist (with select-all), format radio buttons, "Export" button, record count preview.
- **Props:** `isOpen`, `onClose`, `columns[]`, `onExport`, `recordCount`

### `TwoFactorModal`
- **File:** `components/shared/TwoFactorModal.tsx`
- **Purpose:** TOTP OTP entry dialog for 2FA challenges (login or action confirmation).
- **UI elements:** 6-digit OTP input (auto-advance between cells), "Verify" button, timer countdown, "Resend" link.
- **Hook:** `twoFactorService`

---

## Foundation (`0.x`) — Pattern components

### `DataToolbar`
- **File:** `components/patterns/DataToolbar.tsx`
- **Purpose:** Standard toolbar row above data tables: search text input on left, action buttons on right.
- **UI elements:** Search text input (with magnifier icon), "Add" / "Import" / "Filter" action buttons, view-mode toggle.
- **Props:** `searchValue`, `onSearchChange`, `actions[]`, `viewMode?`

### `GenericToolbar`
- **File:** `components/patterns/GenericToolbar.tsx`
- **Purpose:** Flexible toolbar for custom sort controls, bulk mode toggles, and secondary actions.
- **UI elements:** Left slot (title/count), center slot (sort/filter controls), right slot (action buttons).

### `Pagination`
- **File:** `components/patterns/Pagination.tsx`
- **Purpose:** Page-number navigation strip with ellipsis for large data sets (standalone, not table-inline).
- **UI elements:** `←` prev, numbered page buttons (with `…` ellipsis), `→` next, current page highlighted.
- **Props:** `currentPage`, `totalPages`, `onPageChange`

---

## Era 1 (`1.x`) — User, billing, credit

### `CreditBudgetAlerts`
- **File:** `components/layout/CreditBudgetAlerts.tsx`
- **Purpose:** Sticky banner shown at top of all authenticated pages when credits fall below threshold.
- **UI elements:** Amber/red `Alert` banner with credit count, "Buy Credits" CTA button, progress bar (remaining/total).
- **Threshold logic:** Shown when credits < 20% of plan allocation.
- **Context:** `RoleContext` (reads credit balance)

### `UpiPaymentModal`
- **File:** `components/billing/UpiPaymentModal.tsx`
- **Purpose:** Manual UPI payment proof submission dialog. User scans QR, pays, uploads screenshot as proof.
- **UI elements:**
  - Step 1: UPI QR code display + amount
  - Step 2: File input (image upload), transaction reference text input
  - Submit button with loading state
  - Progress indicator (step 1 / step 2)
- **Hook:** `useBilling`
- **Service:** `billingService`

### `ProfileOverview`
- **File:** `components/profile/ProfileOverview.tsx`
- **Purpose:** User profile header showing avatar, full name, plan badge, and account summary.
- **UI elements:** Avatar circle (initials fallback), name + email, plan badge (color-coded by tier), member-since date.
- **Service:** `profileService`

### `ProfileTabGeneral`
- **File:** `components/profile/ProfileTabGeneral.tsx`
- **Purpose:** Editable general profile tab (name, email, password change).
- **UI elements:** Text inputs (first name, last name, email), password change sub-section (current + new + confirm), "Save Changes" button.
- **Validation:** `authValidation`
- **Service:** `profileService`

### `FeatureOverviewPanel`
- **File:** `components/usage/FeatureOverviewPanel.tsx`
- **Purpose:** Summary of credit consumption per feature (finder, verifier, AI, etc.).
- **UI elements:** Feature rows (icon + name + usage count + credit cost), vertical bar chart per feature, "Upgrade" CTA for capped features.
- **Hook:** `useFeatureOverview`
- **Service:** `usageService`

### `DashboardOverview`
- **File:** `components/dashboard/DashboardOverview.tsx`
- **Purpose:** Quick stats cards row (total lookups, credits remaining, exports, active jobs).
- **UI elements:** Stat cards (number + label + trend arrow), icon badges per stat type.
- **Hook:** `useDashboardData`

### `DashboardLineChart`
- **File:** `components/dashboard/DashboardLineChart.tsx`
- **Purpose:** Line chart showing daily/weekly activity or performance trend.
- **UI elements:** Responsive SVG line chart, X-axis (dates), Y-axis (count), hover tooltip, legend.
- **Library:** Recharts or similar charting library.
- **Hook:** `useDashboardData`

### `ActivityDetailsModal`
- **File:** `components/activities/ActivityDetailsModal.tsx`
- **Purpose:** Full detail view of a single activity event (action, status, timestamp, metadata).
- **UI elements:** Info rows (field + value), status badge (success/fail), timestamp, raw data expandable JSON.
- **Service:** `activitiesService`

---

## Era 2 (`2.x`) — Email system

### `EmailVerifierSingle`
- **File:** `components/email/EmailVerifierSingle.tsx`
- **Purpose:** Single email verification form. Accepts one email address and triggers verification.
- **UI elements:** Email text input (with validation), "Verify" submit button (loading state), error alert.
- **Hook:** `useEmailVerifierSingle`
- **Service:** `emailService`

### `EmailVerifierResult`
- **File:** `components/email/EmailVerifierResult.tsx`
- **Purpose:** Displays verification result for a single email: status badge, confidence progress bar, and check details.
- **UI elements:**
  - Status badge: Valid (green) / Catchall (yellow) / Invalid (red) / Unknown (grey)
  - Confidence bar (0–100%, color-coded)
  - Detail rows: DNS, SMTP, SPF, DMARC check results (✓/✗)
  - Copy email button
- **Props:** `result` (email, status, confidence, checks)

### `EmailVerifierBulkResults`
- **File:** `components/email/EmailVerifierBulkResults.tsx`
- **Purpose:** Summary and table for bulk verification results.
- **UI elements:**
  - Summary stacked bar (valid / invalid / catchall / unknown proportions)
  - Filter tabs (All / Valid / Invalid / Unknown)
  - Sortable table with email, status badge, confidence, verified-at
  - "Download CSV" button
  - `TablePagination`
- **Hook:** `useEmailVerifierBulk`

### `EmailMappingModal`
- **File:** `components/email/EmailMappingModal.tsx`
- **Purpose:** Maps CSV column headers to required finder fields (first name, last name, domain).
- **UI elements:** Column mapping rows (source column label → select dropdown), preview of first row values, "Confirm Mapping" button.
- **Props:** `isOpen`, `onClose`, `csvHeaders[]`, `onConfirm(mapping)`

### `EmailAssistantPanel`
- **File:** `components/email/EmailAssistantPanel.tsx`
- **Purpose:** AI-assisted email composition sidebar panel. Suggests subject lines, body content, and tone.
- **UI elements:** Tone selector (radio: professional / casual / friendly), prompt text area, AI suggestion output, "Copy" button, "Regenerate" button.

### `EmailExportColumnMappingFields`
- **File:** `components/email/EmailExportColumnMappingFields.tsx`
- **Purpose:** Column selection checklist for email result export.
- **UI elements:** Checkbox list of exportable fields (email, first name, domain, status, confidence, …), "Select All" toggle.
- **Props:** `fields[]`, `selected[]`, `onChange`

---

## Era 2 (`2.x`) — Jobs and execution

### `JobsTable`
- **File:** `components/jobs/JobsTable.tsx`
- **Purpose:** Full tabular view of all bulk jobs with sort, status, and actions.
- **UI elements:** Sortable columns (name, type, status, created, progress), status badge, action menu (view/retry/cancel/download), `TablePagination`.
- **Hook:** `useJobs`
- **Service:** `jobsService`

### `JobsCard`
- **File:** `components/jobs/JobsCard.tsx`
- **Purpose:** Compact card view of a single job for dashboard or summary lists.
- **UI elements:** Job name + type icon, status badge, progress bar (% processed), "Expand" chevron, elapsed time.
- **Hook:** `useExpandedJobDetails`

### `JobsCardExpandPanel`
- **File:** `components/jobs/JobsCardExpandPanel.tsx`
- **Purpose:** Expanded detail panel within `JobsCard`. Shows stats, actions, and mini log.
- **UI elements:** Stat rows (total / processed / failed / pending), "Retry Failed" button, "Download Result" button, progress counts.

### `JobDetailsModal`
- **File:** `components/jobs/JobDetailsModal.tsx`
- **Purpose:** Full job details dialog with tabbed sections.
- **Tabs:** Summary · Logs · Data
- **UI elements:** Summary tab (stats grid, status timeline), Logs tab (scrollable log entries), Data tab (`DataInspector`).
- **Props:** `isOpen`, `onClose`, `jobId`

### `ExecutionFlow`
- **File:** `components/jobs/ExecutionFlow.tsx`
- **Purpose:** Visual step-by-step job execution pipeline diagram.
- **UI elements:** Step nodes (upload → parse → process → output), connector lines with status icons (pending/running/done/failed), step labels.
- **Props:** `steps[]` (name, status, count)

### `ScheduleJobModal`
- **File:** `components/jobs/ScheduleJobModal.tsx`
- **Purpose:** Job scheduling dialog (run once / recurring).
- **UI elements:** Radio buttons (run once / daily / weekly), date-time picker, cron expression input (advanced), "Schedule" button.
- **Props:** `isOpen`, `onClose`, `onSchedule`, `jobId`

### `JobsRetryModal`
- **File:** `components/jobs/JobsRetryModal.tsx`
- **Purpose:** Retry scope selector for failed jobs.
- **UI elements:** Radio buttons (retry all / retry failed only), confirmation message, "Retry" button.
- **Props:** `isOpen`, `onClose`, `onRetry`, `failedCount`

### `JobsPipelineStats`
- **File:** `components/jobs/JobsPipelineStats.tsx`
- **Purpose:** Horizontal stats bar for a job pipeline: processed / failed / pending counts.
- **UI elements:** Three colored segment bars (green/red/grey) with count labels, percentage display.
- **Props:** `processed`, `failed`, `pending`, `total`

### `DataInspector`
- **File:** `components/jobs/DataInspector.tsx`
- **Purpose:** Collapsible tree view for inspecting JSON/object data from job outputs.
- **UI elements:** Tree nodes (key: value), expand/collapse toggle per node, type-colored values (string/number/boolean/null/array/object).
- **Props:** `data` (any JSON-serializable value)

### `DataValue`
- **File:** `components/jobs/DataValue.tsx`
- **Purpose:** Renders a single typed data value with appropriate formatting.
- **UI elements:** Type-specific display: string (plain text), number (formatted), boolean (badge), null (grey "null"), URL (clickable link).
- **Props:** `value`, `type?`

---

## Era 2 (`2.x`) — Files

### `FilesUploadModal`
- **File:** `components/files/FilesUploadModal.tsx`
- **Purpose:** CSV file upload dialog with drag-and-drop zone.
- **UI elements:** Drag-and-drop area (dashed border, upload icon), file list (name + size), upload progress bar (per file), "Upload" button, error messages.
- **Hook:** `useCsvUpload`
- **Service:** `s3Service`

### `FilesUploadPanel`
- **File:** `components/files/FilesUploadPanel.tsx`
- **Purpose:** In-page upload area (not a modal) with drag-and-drop and progress.
- **UI elements:** Drop zone (full-width), progress bar, uploaded files list, "Choose File" button fallback.

### `FilesDetailView`
- **File:** `components/files/FilesDetailView.tsx`
- **Purpose:** Right-panel detail view for a selected file: metadata, schema, stats, and preview tabs.
- **Tabs:** Preview · Schema · Stats · Info
- **UI elements:** `DataPreviewTable` (Preview tab), `FilesSchemaPanel` (Schema tab), `FilesColumnStatsPanel` (Stats tab), `DatasetInfoPanel` (Info tab).

### `DataPreviewTable`
- **File:** `components/files/DataPreviewTable.tsx`
- **Purpose:** Paginated preview of first N rows of an uploaded CSV.
- **UI elements:** Scrollable table (columns from CSV headers), row index, page controls (prev/next N rows), "Show more" button.
- **Props:** `rows[]`, `headers[]`, `pageSize?`

### `FilesCreateJobModal`
- **File:** `components/files/FilesCreateJobModal.tsx`
- **Purpose:** Create a finder or verifier job from an uploaded file.
- **UI elements:** Radio buttons (Email Finder / Email Verifier), column mapping section (for finder: first name, last name, domain), "Create Job" button.
- **Hook:** `useNewExport`
- **Service:** `jobsService`

### `FilesSchemaPanel`
- **File:** `components/files/FilesSchemaPanel.tsx`
- **Purpose:** CSV column schema display showing inferred data types.
- **UI elements:** Table of column names with type badge (string/email/numeric/boolean/date), nullable indicator.
- **Props:** `schema[]` (column name, type, nullable)

### `FilesColumnStatsPanel`
- **File:** `components/files/FilesColumnStatsPanel.tsx`
- **Purpose:** Per-column statistics (null rate, unique rate, top values, type distribution).
- **UI elements:** Column accordion rows, null-% mini bar (red), unique-% mini bar (blue), top-10 values list.
- **Hook:** `useFileStats`

### `DatasetInfoPanel`
- **File:** `components/files/DatasetInfoPanel.tsx`
- **Purpose:** File/dataset meta info panel (row count, file size, upload date, S3 key).
- **UI elements:** Grid of info rows (label + value), formatted size and date.

### `FilesPeekModal`
- **File:** `components/files/FilesPeekModal.tsx`
- **Purpose:** Quick inline preview of a file's first rows as a modal.
- **UI elements:** `DataPreviewTable` inside a modal, file name title, "Close" button.

### `FilesDownloadModal`
- **File:** `components/files/FilesDownloadModal.tsx`
- **Purpose:** Download options dialog for a file: all rows / filtered / first N.
- **UI elements:** Radio buttons (download scope), row count input (for "first N"), format select (CSV/Excel), "Download" button.
- **Service:** `s3Service` (presigned download URL)

---

## Era 3 (`3.x`) — Contacts

### `ContactsTable`
- **File:** `components/contacts/ContactsTable.tsx`
- **Purpose:** Full contacts data table with sorting, selection, and inline actions.
- **UI elements:** Header row (sortable column labels), `ContactRow` per row, header checkbox (select all), `TablePagination`.
- **Hook:** `useContactColumns` (column visibility)
- **Service:** `contactsService`

### `ContactsTableContainer`
- **File:** `components/contacts/ContactsTableContainer.tsx`
- **Purpose:** State-managed container for `ContactsTable` + toolbar + column toggles.
- **UI elements:** `DataToolbar`, column visibility toggle dropdown, `ContactsTable`.
- **Hook:** `useContactsPage`

### `ContactRow`
- **File:** `components/contacts/ContactRow.tsx`
- **Purpose:** Single row in the contacts table.
- **UI elements:** Checkbox, avatar (initials), name, company, email, title, actions menu (view/edit/delete/find email).
- **Props:** `contact`, `selected`, `onSelect`, `onAction`

### `ContactsFilters`
- **File:** `components/contacts/ContactsFilters.tsx`
- **Purpose:** Collapsible advanced filter sidebar for contacts.
- **UI elements:** `FilterSection` groups: Company (text input), Title (text input), Location (multi-select), Industry (multi-select), Seniority (checkbox group), Active/Inactive toggle.
- **Hook:** `useContactsFilters`

### `ContactsFloatingActions`
- **File:** `components/contacts/ContactsFloatingActions.tsx`
- **Purpose:** `FloatingActionBar` customized for contact bulk operations.
- **UI elements:** Selected count badge, "Export Selected" button, "Delete Selected" danger button.

### `ContactsModals`
- **File:** `components/contacts/ContactsModals.tsx`
- **Purpose:** Modal registry — renders all contact-related modals controlled by parent modal state.
- **Children:** `ImportContactModal`, `BulkInsertModal`, `SaveSearchModal`, `SavedSearchesModal`, `ExportModal`, `ConfirmModal` (delete).

### `ContactsMetadata`
- **File:** `components/contacts/ContactsMetadata.tsx`
- **Purpose:** Contact detail panel shown in right slot of `DataPageLayout`.
- **UI elements:** Avatar, full name, job title, company, email (with copy button), phone, LinkedIn link, tags, activity feed (mini).

### `VQLQueryBuilder`
- **File:** `components/contacts/VQLQueryBuilder.tsx`
- **Purpose:** Visual filter builder generating VQL queries for Connectra.
- **UI elements:** Condition rows (field selector dropdown → operator selector → value input), AND/OR toggle between conditions, "Add Condition" button, "Remove" × per row, "Apply Filters" button.
- **Hook:** `useContactsFilters`

### `SaveSearchModal`
- **File:** `components/contacts/SaveSearchModal.tsx`
- **Purpose:** Save current VQL filter set as a named saved search.
- **UI elements:** Text input (search name), optional description textarea, "Save" button.

### `SavedSearchesModal`
- **File:** `components/contacts/SavedSearchesModal.tsx`
- **Purpose:** Browse and load previously saved searches.
- **UI elements:** List of saved searches (name + created date + filter summary), "Load" button per row, "Delete" (× button), search filter input at top.
- **Hook:** `useSavedSearches`
- **Service:** `savedSearchesService`

### `ImportContactModal`
- **File:** `components/contacts/ImportContactModal.tsx`
- **Purpose:** Multi-step CSV import wizard for contacts.
- **Steps:** Upload CSV → Map columns → Confirm import
- **UI elements:** File upload (step 1), column mapping dropdowns (step 2), preview table + count (step 3), progress bar during import.

### `BulkInsertModal`
- **File:** `components/contacts/BulkInsertModal.tsx`
- **Purpose:** Paste-based bulk contact entry (one per line, formatted).
- **UI elements:** Multi-line textarea (paste instructions), "Parse" button, preview table of parsed rows, "Insert" confirm button.

---

## Era 3 (`3.x`) — Companies

### `CompaniesList`
- **File:** `components/companies/CompaniesList.tsx`
- **Purpose:** List-view companies display with sortable rows.
- **UI elements:** Row list (logo + name + industry + size + location + actions).

### `CompaniesGrid`
- **File:** `components/companies/CompaniesGrid.tsx`
- **Purpose:** Card-grid view for companies (2–4 columns).
- **UI elements:** Company cards (logo, name, industry tag, employee count), hover action overlay.

### `CompaniesDataDisplay`
- **File:** `components/companies/CompaniesDataDisplay.tsx`
- **Purpose:** Container that switches between list and grid view of companies.
- **UI elements:** View toggle buttons (list icon / grid icon), results count label, `CompaniesList` or `CompaniesGrid`.
- **Hook:** `useCompaniesView`

### `CompaniesFilterSidebar`
- **File:** `components/companies/CompaniesFilterSidebar.tsx`
- **Purpose:** Filter panel for companies (industry, size, location, founded year).
- **UI elements:** `FilterSection` groups: Industry (checkbox list), Company Size (range slider), HQ Location (multi-select), Founded (year range input).
- **Hook:** `useCompaniesFilters`

### `CompanyRow`
- **File:** `components/companies/CompanyRow.tsx`
- **Purpose:** Single company row in list view.
- **UI elements:** Company logo (favicon fallback), name (link), industry badge, size label, location, action menu.

### `CompanyContactsTab`
- **File:** `components/companies/CompanyContactsTab.tsx`
- **Purpose:** "Contacts" sub-tab within the company detail panel. Shows contacts at that company.
- **UI elements:** Mini contact table (avatar, name, title, email), "Add Contact" button, `TablePagination`.

### `CompaniesModals`
- **File:** `components/companies/CompaniesModals.tsx`
- **Purpose:** Modal registry for company-related modals.
- **Children:** `AddCompanyModal`, `ImportCompanyModal`, `ExportModal`, `ConfirmModal` (delete).

### `AddCompanyModal`
- **File:** `components/companies/AddCompanyModal.tsx`
- **Purpose:** Add or edit a company record.
- **UI elements:** Text inputs (name, domain, website), industry select, size select, location text input, "Save" button.

### `ImportCompanyModal`
- **File:** `components/companies/ImportCompanyModal.tsx`
- **Purpose:** CSV import wizard for companies (same UX pattern as `ImportContactModal`).
- **Steps:** Upload → Map columns → Confirm import
- **UI elements:** File upload, column mapping dropdowns, preview table, import progress bar.

---

## Era 5 (`5.x`) — AI workflows

### `EmailAssistantPanel`
*(Also listed under Email system — dual-era component)*
- **File:** `components/email/EmailAssistantPanel.tsx`
- **Purpose:** AI-powered email drafting assistant in a slide-in panel.
- **UI elements:** Tone radio buttons (professional/casual/friendly), context textarea (recipient, goal), AI-generated draft output area, "Regenerate" icon button, "Copy" icon button, word-count indicator.

---

## Era 6 (`6.x`) — Reliability patterns

### Error boundaries and loading states (pattern)
- All data-heavy components render a **loading skeleton** while hooks are in loading state.
- **Error state:** `Alert` component (type=`error`) with retry button on data-fetch failure.
- **Empty state:** Illustrated empty-state card (specific per page: no contacts, no jobs, no results).
- **Retry pattern:** `useJobs`, `useContactsPage` etc. expose a `refetch()` function wired to retry buttons.

---

## Era 7 (`7.x`) — Deployment / RBAC-gated components

### Role-gated component pattern
```tsx
// Role-gated render (via RoleContext + featureAccess)
const { isAdmin, hasFeature } = useContext(RoleContext)
if (!isAdmin) return null
return <AdminOnlyComponent />
```

Components that are role-gated:
- `DashboardOverview` (StatsGrid): admin/superAdmin only
- `DashboardLineChart`: role-gated via `DashboardComponentGuard`
- Admin page sections: user table, payment submissions

---

## Shared / cross-era components

| Component | Primary era | Also used in |
| --- | --- | --- |
| `Modal` | Foundation | All eras (modals throughout) |
| `ConfirmModal` | Foundation | 1.x billing, 3.x contacts/companies, 10.x campaign |
| `ExportModal` | 2.x email | 3.x contacts/companies |
| `TablePagination` | 2.x jobs | 3.x contacts/companies |
| `FilterSection` | 3.x contacts | 9.x integrations filter UI |
| `FloatingActionBar` | 3.x contacts | 10.x campaign audience |
| `DataToolbar` | 3.x contacts | 2.x jobs, 8.x analytics |
| `DataPageLayout` | 3.x contacts | 2.x files, 5.x AI chat |
| `Alert` | Foundation | All eras |
| `Pagination` | 2.x jobs | 3.x contacts/companies |

---

## Component quick-reference (alphabetical)

| Component | File | Era |
| --- | --- | --- |
| `ActivityDetailsModal` | `components/activities/ActivityDetailsModal.tsx` | 1.x |
| `AddCompanyModal` | `components/companies/AddCompanyModal.tsx` | 3.x |
| `Alert` | `components/ui/Alert.tsx` | 0.x |
| `AuthErrorBanner` | `components/auth/AuthErrorBanner.tsx` | 0.x |
| `BulkInsertModal` | `components/contacts/BulkInsertModal.tsx` | 3.x |
| `CompaniesDataDisplay` | `components/companies/CompaniesDataDisplay.tsx` | 3.x |
| `CompaniesFilterSidebar` | `components/companies/CompaniesFilterSidebar.tsx` | 3.x |
| `CompaniesGrid` | `components/companies/CompaniesGrid.tsx` | 3.x |
| `CompaniesList` | `components/companies/CompaniesList.tsx` | 3.x |
| `CompaniesModals` | `components/companies/CompaniesModals.tsx` | 3.x |
| `CompanyContactsTab` | `components/companies/CompanyContactsTab.tsx` | 3.x |
| `CompanyRow` | `components/companies/CompanyRow.tsx` | 3.x |
| `ConfirmModal` | `components/ui/ConfirmModal.tsx` | 0.x |
| `ContactRow` | `components/contacts/ContactRow.tsx` | 3.x |
| `ContactsFilters` | `components/contacts/ContactsFilters.tsx` | 3.x |
| `ContactsFloatingActions` | `components/contacts/ContactsFloatingActions.tsx` | 3.x |
| `ContactsMetadata` | `components/contacts/ContactsMetadata.tsx` | 3.x |
| `ContactsModals` | `components/contacts/ContactsModals.tsx` | 3.x |
| `ContactsTable` | `components/contacts/ContactsTable.tsx` | 3.x |
| `ContactsTableContainer` | `components/contacts/ContactsTableContainer.tsx` | 3.x |
| `CreditBudgetAlerts` | `components/layout/CreditBudgetAlerts.tsx` | 1.x |
| `DashboardAccessGate` | `components/shared/DashboardAccessGate.tsx` | 0.x |
| `DashboardLineChart` | `components/dashboard/DashboardLineChart.tsx` | 1.x |
| `DashboardOverview` | `components/dashboard/DashboardOverview.tsx` | 1.x |
| `DataInspector` | `components/jobs/DataInspector.tsx` | 2.x |
| `DataPageLayout` | `components/layouts/DataPageLayout.tsx` | 0.x |
| `DataPreviewTable` | `components/files/DataPreviewTable.tsx` | 2.x |
| `DatasetInfoPanel` | `components/files/DatasetInfoPanel.tsx` | 2.x |
| `DataToolbar` | `components/patterns/DataToolbar.tsx` | 0.x |
| `DataValue` | `components/jobs/DataValue.tsx` | 2.x |
| `EmailAssistantPanel` | `components/email/EmailAssistantPanel.tsx` | 2.x/5.x |
| `EmailExportColumnMappingFields` | `components/email/EmailExportColumnMappingFields.tsx` | 2.x |
| `EmailMappingModal` | `components/email/EmailMappingModal.tsx` | 2.x |
| `EmailVerifierBulkResults` | `components/email/EmailVerifierBulkResults.tsx` | 2.x |
| `EmailVerifierResult` | `components/email/EmailVerifierResult.tsx` | 2.x |
| `EmailVerifierSingle` | `components/email/EmailVerifierSingle.tsx` | 2.x |
| `ExecutionFlow` | `components/jobs/ExecutionFlow.tsx` | 2.x |
| `ExportModal` | `components/shared/ExportModal.tsx` | 0.x/2.x |
| `FeatureOverviewPanel` | `components/usage/FeatureOverviewPanel.tsx` | 1.x |
| `FilesColumnStatsPanel` | `components/files/FilesColumnStatsPanel.tsx` | 2.x |
| `FilesCreateJobModal` | `components/files/FilesCreateJobModal.tsx` | 2.x |
| `FilesDetailView` | `components/files/FilesDetailView.tsx` | 2.x |
| `FilesDownloadModal` | `components/files/FilesDownloadModal.tsx` | 2.x |
| `FilesPeekModal` | `components/files/FilesPeekModal.tsx` | 2.x |
| `FilesSchemaPanel` | `components/files/FilesSchemaPanel.tsx` | 2.x |
| `FilesUploadModal` | `components/files/FilesUploadModal.tsx` | 2.x |
| `FilesUploadPanel` | `components/files/FilesUploadPanel.tsx` | 2.x |
| `FilterSection` | `components/shared/FilterSection.tsx` | 0.x/3.x |
| `FloatingActionBar` | `components/shared/FloatingActionBar.tsx` | 0.x |
| `GenericToolbar` | `components/patterns/GenericToolbar.tsx` | 0.x |
| `ImportCompanyModal` | `components/companies/ImportCompanyModal.tsx` | 3.x |
| `ImportContactModal` | `components/contacts/ImportContactModal.tsx` | 3.x |
| `JobDetailsModal` | `components/jobs/JobDetailsModal.tsx` | 2.x |
| `JobsCard` | `components/jobs/JobsCard.tsx` | 2.x |
| `JobsCardExpandPanel` | `components/jobs/JobsCardExpandPanel.tsx` | 2.x |
| `JobsPipelineStats` | `components/jobs/JobsPipelineStats.tsx` | 2.x |
| `JobsRetryModal` | `components/jobs/JobsRetryModal.tsx` | 2.x |
| `JobsTable` | `components/jobs/JobsTable.tsx` | 2.x |
| `MainLayout` | `components/layout/MainLayout.tsx` | 0.x |
| `Modal` | `components/ui/Modal.tsx` | 0.x |
| `Pagination` | `components/patterns/Pagination.tsx` | 0.x |
| `Popover` | `components/ui/Popover.tsx` | 0.x |
| `ProfileOverview` | `components/profile/ProfileOverview.tsx` | 1.x |
| `ProfileTabGeneral` | `components/profile/ProfileTabGeneral.tsx` | 1.x |
| `ResizeHandle` | `components/shared/ResizeHandle.tsx` | 0.x |
| `SavedSearchesModal` | `components/contacts/SavedSearchesModal.tsx` | 3.x |
| `SaveSearchModal` | `components/contacts/SaveSearchModal.tsx` | 3.x |
| `ScheduleJobModal` | `components/jobs/ScheduleJobModal.tsx` | 2.x |
| `Sidebar` | `components/layout/Sidebar.tsx` | 0.x |
| `TablePagination` | `components/shared/TablePagination.tsx` | 0.x |
| `TwoFactorModal` | `components/shared/TwoFactorModal.tsx` | 1.x/7.x |
| `UpiPaymentModal` | `components/billing/UpiPaymentModal.tsx` | 1.x |
| `VQLQueryBuilder` | `components/contacts/VQLQueryBuilder.tsx` | 3.x |

---

## Related docs

- `docs/frontend.md` — canonical frontend map and overview
- `docs/frontend/design-system.md` — design tokens, colors, typography, form elements
- `docs/frontend/hooks-services-contexts.md` — hooks, services, contexts, lib utilities
- `docs/flowchart.md` — component interaction and user journey flowcharts

## Component metadata normalization

Each component entry should expose `era`, `introduced_in`, and `ui_elements` keys to keep component inventory aligned with page and version docs.

## `contact360.io/root` marketing 3D component catalog

| Component | Path | Purpose | Era |
| --- | --- | --- | --- |
| `Button3D` | `contact360.io/root/src/components/ui/Button3D.tsx` | primary/secondary CTA actions | `0.x` |
| `Input3D` | `contact360.io/root/src/components/ui/Input3D.tsx` | text inputs in marketing forms | `0.x` |
| `Checkbox3D` | `contact360.io/root/src/components/ui/Checkbox3D.tsx` | preference/option toggles | `0.x` |
| `TabGroup` / `Tabs3D` | `contact360.io/root/src/components/ui/TabGroup.tsx`, `Tabs3D.tsx` | tab navigation and segmented views | `0.x` |
| `Modal3D` / `Drawer3D` | `contact360.io/root/src/components/ui/Modal3D.tsx`, `Drawer3D.tsx` | overlays and side panels | `0.x` |
| `Tooltip3D` | `contact360.io/root/src/components/ui/Tooltip3D.tsx` | hover help and hints | `0.x` |
| `Card3D` / `CardSelect3D` | `contact360.io/root/src/components/ui/Card3D.tsx`, `CardSelect3D.tsx` | feature and option cards | `0.x` |
| `Badge3D` / `Icon3D` | `contact360.io/root/src/components/ui/Badge3D.tsx`, `Icon3D.tsx` | status and icon primitives | `0.x` |
| `Table3D` / `ColumnSelector3D` | `contact360.io/root/src/components/ui/Table3D.tsx`, `ColumnSelector3D.tsx` | data preview and column controls | `2.x` |
| `RangeSlider3D` | `contact360.io/root/src/components/ui/RangeSlider3D.tsx` | range-based filtering/pricing interactions | `2.x` |
| `RichSelect3D` / `Select3D` / `MultiSelect3D` / `FilterMultiSelect3D` | `contact360.io/root/src/components/ui/*.tsx` | single/multi-select controls | `2.x` |
| `ResizeHandle` | `contact360.io/root/src/components/ui/ResizeHandle.tsx` | resizable split panels | `3.x` |
| `TiltRow` / `Accordion3D` | `contact360.io/root/src/components/ui/TiltRow.tsx`, `Accordion3D.tsx` | interaction accents and progressive reveal content | `3.x` |
| `Toast3D` / `ComingSoonToast` | `contact360.io/root/src/components/ui/Toast3D.tsx`, `ComingSoonToast.tsx` | feedback notifications | `1.x` |

## `contact360.io/admin` DocsAI template component catalog

| Component category | Primary paths | Notes |
| --- | --- | --- |
| Buttons | `contact360.io/admin/static/css/components/button.css` | variant, size, and loading-state styles |
| Form inputs | `contact360.io/admin/static/css/components/form-inputs.css` | input/select/textarea plus `.form-radio-group` |
| Tabs | `contact360.io/admin/static/css/components/tabs.css` | default/pills/underline/detail tab variants |
| Progress UI | `contact360.io/admin/static/css/components/progress.css`, `templates/components/progress.html` | reusable progress bar markup + styling |
| Graph viewers | `static/js/components/relationship-graph-viewer.js`, `static/js/components/graph.js` | D3 force graph and Cytoscape graph rendering |
| Base shell | `templates/base.html` | sidebar/header authenticated shell |
| Roadmap controls | `templates/roadmap/dashboard.html` | preview/edit tabs + progress + radio filters |
| Architecture controls | `templates/architecture/blueprint.html` | preview/edit tabs + progress + radio filters |

## Cross-surface component coverage matrix

| UI concern | `contact360.io/root` | `contact360.io/app` | `contact360.io/admin` |
| --- | --- | --- | --- |
| Tabs | `TabGroup`, `Tabs3D` | `Tabs`, domain tab components | `tabs.css` + dashboard tab JS controllers |
| Buttons | `Button3D` | `Button`, domain action buttons | `button.css` + template action buttons |
| Input boxes | `Input3D`, selector family | `Input`, form fields, filter inputs | `form-inputs.css` (`form-input`, `form-select`, `form-textarea`) |
| Checkboxes | `Checkbox3D` | table/select and settings checkboxes | checkbox patterns in forms/filter templates |
| Radio buttons | shared config radios | domain radios in workflow forms | `.form-radio-group` in admin forms |
| Progress bars | marketing/progress visuals | upload, usage, job progress bars | `progress.css` + `templates/components/progress.html` |
| Graph/flow | chart wrappers in marketing demos | Recharts analytics and workflow visuals | D3 `relationship-graph-viewer.js` + Cytoscape `graph.js` |


---

## Extension surface — `extension/contact360`

> **Surface type:** Logic + transport utilities consumed by extension popup/content scripts. No React components — pure JavaScript ES6+ modules.

### `auth/graphqlSession.js` — Auth utility

| Export | Type | Purpose | Era |
| --- | --- | --- | --- |
| `getValidAccessToken()` | async fn | Returns a valid Bearer token; refreshes proactively if within 5 min of expiry | 1.x–4.x |
| `refreshAccessToken(refreshToken)` | async fn | Calls `auth.refreshToken` mutation on Appointment360; stores result | 1.x |
| `storeTokens(tokens)` | async fn | Persists `{ accessToken, refreshToken }` to `chrome.storage.local` | 1.x |
| `getStoredTokens()` | async fn | Reads both tokens from `chrome.storage.local` | 1.x |
| `isTokenExpired(token, bufferSeconds?)` | fn | Returns `true` if token `exp` is within buffer; default buffer = 300 s | 1.x |
| `decodeJWT(token)` | fn | Base64url-decodes JWT payload; no external library | 0.x |

### `utils/lambdaClient.js` — REST transport

| Export | Type | Purpose | Era |
| --- | --- | --- | --- |
| `saveProfiles(profiles[])` | async fn | Splits into batches of 10, submits to `POST /v1/save-profiles`, retries on failure | 3.x–4.x |
| `BATCH_SIZE` | const | Default 10 profiles per request | 3.x |
| `MAX_RETRIES` | const | Default 3 retries with exponential back-off + jitter | 6.x |
| `buildRequestOptions(token)` | fn | Constructs fetch options: `Authorization`, `Content-Type`, adaptive timeout | 4.x |
| `pruneProfile(profile)` | fn | Strips `null`/`undefined` fields before serialization | 3.x |

### `utils/profileMerger.js` — Data utilities

| Export | Type | Purpose | Era |
| --- | --- | --- | --- |
| `deduplicateProfiles(profiles[])` | fn | Groups by `profile_url`; merges each group; returns clean array | 3.x |
| `mergeProfiles(a, b)` | fn | Field-level merge; higher completeness record wins per field | 3.x |
| `scoreProfile(profile)` | fn | Completeness score 0–1 based on non-empty field count | 3.x |

### Expected popup UI elements (contract)

| UI element | Implementation location | Backed by | Era |
| --- | --- | --- | --- |
| Profile count badge | Extension popup HTML | `deduplicateProfiles()` | 4.x |
| Upload progress bar | Extension popup HTML | `saveProfiles()` batch counter | 4.x |
| Error toast | Extension popup HTML | `saveProfiles()` error array | 4.x |
| Token status indicator | Extension popup HTML | `isTokenExpired()` | 1.x |
| Sync status panel | Extension popup HTML | `saveProfiles()` `{ saved, errors }` | 4.x |
| Company capture checkbox | Extension popup HTML | Toggle company extraction flag | 3.x |
| Dedup strategy radio group | Extension popup HTML | Merge strategy: strict / loose | 4.x |

### Cross-surface component coverage note

| Surface | Component type | Pattern |
| --- | --- | --- |
| `contact360.io/app` | React TSX components | Import `hooks/` and `services/` |
| `contact360.io/root` | React TSX 3D components | BEM CSS + `context/` |
| `contact360.io/admin` | Django Jinja2 templates | Static CSS + D3/Cytoscape JS |
| `contact360.extension` | Vanilla HTML/CSS/JS | `auth/` + `utils/` imported by popup/content scripts |

---

## Extension surface — `contact360.extension`

### Popup UI (`popup.html` / `popup.css` / `popup.js`)

Two-tab layout (Status | Settings). All visual styles come from `popup.css` design tokens (`--c360-*` prefix, kit-aligned dark palette).

#### Status tab components

| Component | Class | Purpose |
|---|---|---|
| Token status badge | `.c360-status` + `--ok / --warn / --bad / --unknown` | Auth state machine display |
| Gateway status badge | `.c360-status` + variants | Health check result |
| Batch feedback row | `.c360-batch-feedback` + `__dot--saved/retry/failed` | Capture result counters |
| Progress bar | `.c360-progress` + `--indeterminate` | Capture in-progress indicator |
| Capture button | `.c360-popup__button` | Triggers `C360_CAPTURE_AND_SAVE` message to background |
| Recheck button | `.c360-popup__button--ghost` | Re-runs `refreshTokenStatus` + `checkGateway` |

#### Settings tab components

| Component | Class | Purpose |
|---|---|---|
| Gateway URL input | `.c360-popup__input` (type url) | `chrome.storage.local` → `c360_gateway_base_url` |
| Gateway API Key input | `.c360-popup__input` (type password) | `c360_gateway_api_key` |
| Logs URL input | `.c360-popup__input` (type url) | `c360_logs_api_base_url` |
| Logs API Key input | `.c360-popup__input` (type password) | `c360_logs_api_key` |
| Telemetry checkbox | `.c360-checkbox` + `.c360-checkbox-group` | `c360_telemetry_enabled` |
| Save Settings button | `.c360-popup__button` | Persists all settings + re-checks gateway |

#### Shared components

| Component | Class | Description |
|---|---|---|
| Tab nav | `.c360-tabs` + `.c360-tabs__tab[aria-selected]` | Keyboard-navigable tab bar (ArrowLeft/ArrowRight) |
| Tab panels | `.c360-tab-panel` | Toggled via `hidden` attribute |
| Toast | `.c360-toast` + `--show / --success / --warn` | `aria-live="polite"` notification |
| Header | `.c360-popup__header` | App title + "Ext" badge |

### JS utility modules

#### `auth/graphqlSession.js`
- `ensureAccessToken(opts)` — proactive refresh, buffer = 60 s before exp
- `createChromeStorageAdapter()` — `chrome.storage.local` adapter for popup + background
- `decodeJwtPayload(token)` — base64url decode
- **Global:** `globalThis.Contact360GraphQLSession`
- **Full contract:** [extension-graphql-session.md](../../backend/micro.services.apis/extension-graphql-session.md)

#### `utils/telemetryClient.js`
- `window.Contact360Telemetry.emit(eventType, payload?)` — best-effort POST to Logs API
- Log body: `{ logs: [{ level, service_type: "extension", action_type, metadata }] }`
- **Full schema:** [extension-telemetry-schema.md](../../backend/micro.services.apis/extension-telemetry-schema.md)

### Design system and UX profile
- **Dark palette** (Slate-950 base) — designed for compact overlay popup (~320 px wide)
- **8-pt grid** (`--c360-space-*` tokens: 4/8/12/16/24 px)
- **Kit-aligned radius:** `--c360-radius-lg: 8px` (matches kit `0.75 rem` at 16-px base)
- **Font:** `system-ui, -apple-system, "Segoe UI", Roboto` — Roboto is the kit font fallback
- **Transitions:** 150 ms `cubic-bezier(0.4, 0, 0.2, 1)`
---

## Email app docs pack — `contact360.io/email`

### Component highlights
- `components/email-list.tsx` — mailbox fetch orchestration, loading/error/empty state.
- `components/data-table.tsx` — tabs, checkbox selection, pagination, row action dropdown.
- `components/app-sidebar.tsx` — folder navigation and user bootstrap.
- `components/nav-secondary.tsx` — secondary sidebar rail (folder/account shortcuts).
- `components/nav-user.tsx` — account menu + logout.
- `app/account/[userId]/page.tsx` — profile and IMAP account management.

### Email surface component set (canonical)
- `DataTable` (`components/data-table.tsx`)
- `email-list` (`components/email-list.tsx`)
- `app-sidebar` (`components/app-sidebar.tsx`)
- `LoginForm` (`components/login-form.tsx`)
- `ImapConnect` (`app/account/[userId]/page.tsx` IMAP connect flow controls)

### Hooks/services/contexts
- `context/imap-context.tsx` — active account context + persistence.
- `hooks/use-mobile.ts` — responsive helper.
- Service access is direct `fetch` using `BACKEND_URL` in `lib/utils.ts`.

### Design system and UX profile
- Dark-theme-first mailbox shell.
- Emphasis on compact table workflows for high-volume email triage.
- Uses shadcn/Radix primitives for consistent tabs/buttons/inputs/checkbox/dropdowns.
