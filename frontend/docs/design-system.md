# Contact360 Design System

This document defines the design language, UI patterns, form elements, and component conventions for the Contact360 dashboard (`contact360.io/app/`) and marketing site (`contact360.io/root/`).

**Code root:** `contact360.io/app/src/`  
**Styles:** Modular CSS under `contact360.io/app/app/css/`  
**Related:** `docs/frontend/components.md` (component catalog), `docs/frontend.md` (frontend map)

---

## Design principles

| Principle | Description |
| --- | --- |
| **Clarity** | Data-dense pages must remain scannable — use visual hierarchy (size, weight, color) to guide attention. |
| **Speed** | Immediate feedback for all user actions. Loading skeletons replace blank screens; progress bars replace waiting. |
| **Role-aware** | UI surfaces adapt to user role (Free / Pro / Admin / SuperAdmin) — upgrade CTAs, gated features, admin sections. |
| **Consistency** | Reuse base primitives (`Modal`, `Alert`, `DataToolbar`, `TablePagination`) across all feature areas. |
| **Accessibility** | WCAG 2.1 AA target: sufficient color contrast, keyboard navigation, focus traps in modals, `aria-label` on icons. |

---

## Color palette

### Brand colors

| Token name | Usage | Value (approx) |
| --- | --- | --- |
| `--color-primary` | Primary buttons, active nav, progress bars | Brand blue (e.g. `#2563eb`) |
| `--color-primary-hover` | Button hover state | Darker blue |
| `--color-primary-light` | Input focus ring, subtle highlights | Light blue tint |
| `--color-accent` | CTAs, upgrade banners | Brand accent (e.g. violet or teal) |

### Semantic colors

| Token | Meaning | Used on |
| --- | --- | --- |
| `--color-success` | Valid, completed, positive | Status badge, `Alert` success, ✓ icons |
| `--color-warning` | Catchall, low credits, caution | Low-credit banner, catchall badge |
| `--color-danger` | Invalid, error, destructive | Error alert, danger button, invalid badge |
| `--color-info` | Informational | Info `Alert`, tooltip |
| `--color-neutral` | Unknown, pending, disabled | Unknown badge, disabled inputs |

### Credit balance color progression

| Threshold | Color | Component |
| --- | --- | --- |
| > 50% credits remaining | Green `--color-success` | Sidebar credit bar, `CreditBudgetAlerts` |
| 20%–50% remaining | Amber `--color-warning` | Banner switches to amber |
| < 20% remaining | Red `--color-danger` | Banner turns red, sticky alert appears |

### Status badge colors

| Status | Color | Component |
| --- | --- | --- |
| Valid / Success / Active | Green | `EmailVerifierResult`, job status |
| Catchall / Warning | Yellow/amber | Verifier result |
| Invalid / Error / Failed | Red | Verifier result, job failed badge |
| Unknown / Pending | Grey | Default/neutral |
| Processing / Running | Blue | Job in-progress |
| Scheduled | Purple | Scheduled job |
| Cancelled | Grey/strikethrough | Cancelled job |

---

## Typography

| Level | Usage | Approx size + weight |
| --- | --- | --- |
| Page title | Page `<h1>` (e.g. "Contacts", "Dashboard") | 24px, semibold |
| Section heading | Card titles, modal titles | 18px, semibold |
| Sub-heading | Tab labels, panel section titles | 14–16px, medium |
| Body text | Data rows, descriptions, labels | 14px, regular |
| Small / caption | Metadata, timestamps, hints | 12px, regular |
| Monospace | Email addresses, API keys, code snippets | 13px, monospace |
| Stat number | Dashboard stat cards | 28–36px, bold |

**Font stack:** System font stack (Inter, system-ui, -apple-system, sans-serif).

---

## Spacing and layout

| Token | Value | Usage |
| --- | --- | --- |
| `--space-1` | 4px | Micro gaps (icon to text) |
| `--space-2` | 8px | Compact padding, badge inner |
| `--space-3` | 12px | Input padding, small card gap |
| `--space-4` | 16px | Standard padding, row height |
| `--space-6` | 24px | Section gaps, card padding |
| `--space-8` | 32px | Page-level margins |
| `--space-12` | 48px | Large section gaps |

**Grid:** CSS Grid for page-level layouts. Flexbox for component-level layouts.  
**Sidebar width:** 240px expanded, 64px collapsed.  
**Content max-width:** 1280px (centered, with 24px padding on each side).  
**Modal widths:** sm=400px, md=540px, lg=720px, xl=960px.

---

## Elevation and shadows

| Level | CSS shadow | Usage |
| --- | --- | --- |
| Level 1 | `0 1px 3px rgba(0,0,0,0.08)` | Cards, tables |
| Level 2 | `0 4px 12px rgba(0,0,0,0.12)` | Dropdowns, popovers |
| Level 3 | `0 8px 24px rgba(0,0,0,0.16)` | Modals, dialogs |
| Level 4 | `0 16px 40px rgba(0,0,0,0.2)` | Full-screen overlays |

---

## Border radius

| Token | Value | Usage |
| --- | --- | --- |
| `--radius-sm` | 4px | Badges, tags |
| `--radius-md` | 8px | Cards, inputs, buttons |
| `--radius-lg` | 12px | Modals |
| `--radius-full` | 9999px | Pills, avatars, progress bars |

---

## Form elements

### Text inputs

| Variant | Usage | State |
| --- | --- | --- |
| Default text input | Name, email, domain, reference fields | Default (grey border) |
| Focus state | On tab/click | Primary color border + ring |
| Error state | Failed validation | Red border + error message below |
| Disabled state | Read-only fields | Light grey background, no cursor |
| With icon (left) | Search input (magnifier), email (envelope) | 36px left padding for icon |
| With icon (right) | Password (eye toggle), clear (×) | 36px right padding |

**Pattern:**
```
[Label]
[Input field]                  ← 36-40px height, full-width by default
[Error message text] (if any)  ← 12px red text below input
```

### Textarea

| Usage | Rows | Resize |
| --- | --- | --- |
| Bulk paste (`BulkInsertModal`) | 6–10 | Vertical only |
| AI context / prompt | 4–6 | Vertical only |
| Description fields | 3–4 | Vertical only |

### Select / Dropdown

| Variant | Usage |
| --- | --- |
| Native `<select>` | Simple single-value (page size, format selector) |
| Custom dropdown | Column mapping, filter values (with search) |
| Multi-select | Filter fields (industry, location), column export |

**Custom dropdown features:** search-as-you-type, "Select All" option, count badge when N items selected.

### Checkbox

| Pattern | Usage |
| --- | --- |
| Standalone checkbox | Feature toggles, option selection |
| Header checkbox (tables) | "Select all rows" in `ContactsTable`, `JobsTable` |
| Row checkbox | Individual row selection (appears on hover or click) |
| Checkbox list | Export column selection, filter option groups |

**Visual:** 16×16px square, primary color when checked, indeterminate state (dash) for partial selection.

### Radio buttons

| Usage | Component |
| --- | --- |
| Job type (finder / verifier) | `FilesCreateJobModal` |
| Download scope (all / filtered / first N) | `FilesDownloadModal` |
| Retry scope (all / failed only) | `JobsRetryModal` |
| Schedule frequency (once / daily / weekly) | `ScheduleJobModal` |
| View mode (list / grid) | `CompaniesDataDisplay` |
| AI tone (professional / casual / friendly) | `EmailAssistantPanel` |
| Export format (CSV / Excel / JSON) | `ExportModal` |

**Visual:** 16×16px circle, primary color when selected. Always grouped with a visible label per option.

### Toggle switch

| Usage | Component |
| --- | --- |
| Theme (light/dark) | Profile settings, `ThemeContext` |
| 2FA enable/disable | Profile security tab, `TwoFactorModal` |
| Active/inactive filter | Contacts filter, company filter |
| Feature flag toggle | Admin settings panel |

**Visual:** 36×20px pill, primary color when ON, grey when OFF. Slides with 150ms transition.

### File input / drag-and-drop

| Variant | Usage |
| --- | --- |
| Drag-and-drop zone | `FilesUploadModal`, `FilesUploadPanel` — dashed border, upload icon, instruction text |
| Click-to-browse fallback | Hidden `<input type="file">` triggered by zone click |
| Image upload | `UpiPaymentModal` — accepts image/*, shows preview thumbnail |

**States:** Default (dashed border), drag-over (solid primary border + background tint), uploading (progress bar replaces zone).

---

## Progress bars

| Type | Component | Visual spec |
| --- | --- | --- |
| Credit balance | `CreditBudgetAlerts`, `Sidebar`, `FeatureOverviewPanel` | Full-width thin bar (6px height), color changes by threshold |
| File upload | `FilesUploadModal`, `FilesUploadPanel` | Animated fill bar with % label, per-file or overall |
| Job progress | `JobsCard`, `JobsPipelineStats` | Horizontal fill bar with processed/total label |
| Confidence score | `EmailVerifierResult` | 0–100% fill bar, color = status color |
| Stacked bar | `EmailVerifierBulkResults` | Full-width divided into valid/invalid/catchall/unknown segments |
| Column stats | `FilesColumnStatsPanel` | Mini horizontal bars per column (null %, unique %) |
| Payment step | `UpiPaymentModal` | Step indicator (1 → 2 → done) |

---

## Badges and tags

| Variant | Usage | Visual |
| --- | --- | --- |
| Status badge | Job status, verification status | Colored pill (background + text) |
| Plan badge | User plan in profile header | Pill with tier color (Free=grey, Pro=blue, Enterprise=purple) |
| Count badge | Selection count, notification count | Small filled circle with number |
| Industry tag | Company cards | Outlined small pill, neutral color |
| Type badge | CSV column type (string/email/numeric) | Mono font, type-specific color |

---

## Icons

- **Library:** Lucide Icons (or equivalent).
- **Sizes:** 16px (inline text), 20px (action buttons), 24px (nav icons), 32px (feature icons).
- **Usage conventions:**
  - Always paired with text in buttons (`<icon> Label`).
  - Icon-only buttons always have `aria-label`.
  - Nav sidebar: 20px icon + 14px label (hidden when collapsed).
  - Status icons: check circle (valid), × circle (invalid), `~` circle (catchall/unknown), clock (pending).

---

## Buttons

### Variants

| Variant | CSS class pattern | Usage |
| --- | --- | --- |
| Primary | `.btn-primary` | Main CTA ("Find Email", "Upload", "Save") |
| Secondary / outline | `.btn-outline` | Secondary actions ("Cancel", "Clear", "Back") |
| Danger | `.btn-danger` | Destructive ("Delete", "Retry All Failed") |
| Ghost | `.btn-ghost` | Low-priority ("Learn More", icon-only actions) |
| Link | `.btn-link` | In-text navigation or secondary links |
| Icon only | `.btn-icon` | Copy, download, expand, close — always `aria-label` |

### States

| State | Visual |
| --- | --- |
| Default | Solid fill (primary) or bordered (outline) |
| Hover | Darker shade, slight lift (shadow) |
| Active / pressed | Darker shade, inset shadow |
| Loading | Spinner replaces or overlays text, disabled interaction |
| Disabled | 50% opacity, no cursor, `disabled` attribute |
| Focus | Primary color outline ring (keyboard nav) |

### Sizes

| Size | Height | Font size | Padding |
| --- | --- | --- | --- |
| Small | 28px | 12px | 8px 12px |
| Medium (default) | 36px | 14px | 10px 16px |
| Large | 44px | 16px | 12px 24px |
| Full-width | — | 14px | — |

---

## Tabs

| Pattern | Usage | Components |
| --- | --- | --- |
| Underline tabs | Page-level navigation (Profile, Admin, Company detail) | `<TabBar>` + active underline |
| Contained tabs | Within panels (`FilesDetailView`, `JobDetailsModal`) | Background pill on active |
| Filter tabs | Result filtering (All/Valid/Invalid) | `EmailVerifierBulkResults` |

**Keyboard:** Arrow keys to navigate between tabs; Enter/Space to select.

---

## Tables

| Element | Visual / behavior |
| --- | --- |
| Header row | Bold column labels, sort icon (up/down/neutral), sticky on scroll |
| Data rows | Alternating subtle row background (optional), hover highlight |
| Row selection | Checkbox on left (header = select all), selected rows get highlight |
| Row actions | Hidden until hover → action icon buttons appear (or `⋮` menu) |
| Empty state | Centered illustration + message + optional CTA |
| Loading | Skeleton rows (animated shimmer) |
| Error | `Alert` type=error with "Try again" button |
| Pagination | `TablePagination` below table |

---

## Loading states

| Pattern | Usage |
| --- | --- |
| Skeleton loader | Content placeholders (same shape as content, shimmer animation) |
| Inline spinner | Button loading state, small inline data fetch |
| Full-page spinner | Initial session check (`DashboardAccessGate`) |
| Progress bar | File upload, job processing |
| Streaming text | AI chat token streaming |

---

## Toast notifications

- **Library:** Custom `toast` utility (`lib/toast.ts`).
- **Position:** Top-right corner, stacked.
- **Types:** success (green), error (red), info (blue), warning (amber).
- **Duration:** 4s auto-dismiss (error: 6s, no auto-dismiss for critical).
- **Usage pattern:** Called after async operations from hooks (billing, export, import, profile save).

---

## Animations

| Animation | Config (from `animationsConfig.ts`) | Usage |
| --- | --- | --- |
| Page transitions | Fade-in (150ms ease) | Route change |
| Modal open/close | Scale + fade (200ms) | All modals |
| Sidebar collapse/expand | Width transition (250ms ease) | `Sidebar` |
| Alert appear | Slide-down + fade (200ms) | `CreditBudgetAlerts` |
| Skeleton shimmer | Linear gradient loop | Loading states |
| Progress bar fill | Width transition (smooth) | All progress bars |
| AI token streaming | Character-by-character appear | AI chat output |
| Floating bar appear | Slide-up from bottom (200ms) | `FloatingActionBar` |

---

## Responsive behavior

| Breakpoint | Behavior |
| --- | --- |
| ≥ 1280px (xl) | Full two-panel layout, sidebar expanded |
| 1024px–1280px (lg) | Sidebar collapsed by default, panels stack |
| 768px–1024px (md) | Mobile-friendly table (horizontal scroll), sidebar hidden with toggle |
| < 768px (sm) | Single column, modals full-screen, tables scrollable |

**Note:** Dashboard is primarily a desktop product. Mobile support is degraded-but-functional (important actions accessible via scroll/swipe).

---

## Accessibility checklist

- 📌 Planned: All form inputs have `<label>` (or `aria-label` / `aria-labelledby`).
- 📌 Planned: All icon-only buttons have `aria-label`.
- 📌 Planned: Modal has `role="dialog"`, `aria-modal="true"`, focus trap on open, returns focus to trigger on close.
- 📌 Planned: Status badges use color + text (never color alone).
- 📌 Planned: Progress bars have `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`.
- 📌 Planned: Data tables have `<th scope="col">` headers.
- 📌 Planned: Interactive elements reachable by keyboard (Tab + Enter/Space).
- 📌 Planned: Error messages are associated with inputs via `aria-describedby`.
- 📌 Planned: Color contrast meets WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text).
- 📌 Planned: Skip-to-content link at top of authenticated layout.

---

## Dark mode

- **Context:** `ThemeContext` (`context/ThemeContext.tsx`) provides `theme` + `toggleTheme()`.
- **Implementation:** CSS custom properties on `:root` switch values. No class swapping needed.
- **Toggle location:** Profile settings page, sidebar footer icon button.
- **Persistence:** Stored in `localStorage`.

---

## Marketing site design conventions (`contact360.io/root/`)

| Convention | Detail |
| --- | --- |
| Styling | Custom CSS, BEM-like naming (not Tailwind, not modular CSS) |
| Typography | Larger hero type (48–72px), lighter weight in hero |
| CTA buttons | Extra-large primary buttons ("Get Started Free", "Start Finding Emails") |
| Color usage | Brand primary, accent gradient for hero sections |
| Responsiveness | Mobile-first, all sections stack on < 768px |
| Animation | Intersection Observer-based reveal animations on scroll |

---

## Related docs

- `docs/frontend.md` — frontend overview and component summary
- `docs/frontend/components.md` — per-era component catalog
- `docs/frontend/hooks-services-contexts.md` — hooks, services, contexts, utilities
- `docs/flowchart.md` — user journey and component interaction flowcharts

## Era usage annotation requirement

Design-system primitives and composites should annotate when they became standard (`introduced_in`) and which era(s) rely on them most heavily.

## Marketing 3D design system (`contact360.io/root`)

| Area | Pattern |
| --- | --- |
| Naming | BEM-like CSS naming with semantic blocks/modifiers |
| Theme behavior | `useForceLightTheme` in marketing layout to keep public pages in light mode |
| Buttons | `Button3D` supports large CTA emphasis and elevated 3D styling |
| Inputs | `Input3D` and related selects/multi-selects provide consistent border, focus, and depth affordances |
| Checkbox/radio | `Checkbox3D` for checkbox flows; radio controls used in shared config forms |
| Tabs/cards | `TabGroup`, `Tabs3D`, `Card3D`, `CardSelect3D` for product storytelling and comparison sections |
| Feedback | `Toast3D`, `ComingSoonToast`, badges, tooltips for lightweight interaction feedback |
| Data visuals | `Table3D`, range controls, and chart wrappers for preview-oriented presentation |

### System split note

- `contact360.io/root` maintains a dedicated 3D system (`Button3D`, `Card3D`, `Modal3D`, selector family) separate from dashboard primitives.
- `contact360.io/email` standardizes on Radix/shadcn-style primitives with Tailwind utility styling for mailbox workflows.

## DocsAI admin static CSS system (`contact360.io/admin/static/css/components`)

| File | Design responsibility |
| --- | --- |
| `button.css` | button variants, sizes, disabled/loading states |
| `form-inputs.css` | text inputs, select, textarea, validation states, `.form-radio-group` |
| `tabs.css` | tab layouts (default/pills/underline/detail) |
| `progress.css` | progress bars and state styling |
| `graph.css` | graph viewport and graph interaction styling |
| `modal.css` | modal shell and overlay behavior |

Related template + JS pairings:

- Progress markup: `contact360.io/admin/templates/components/progress.html`
- D3 graph: `contact360.io/admin/static/js/components/relationship-graph-viewer.js`
- Cytoscape graph: `contact360.io/admin/static/js/components/graph.js`

## Cross-surface token contract (Dashboard UI Kit alignment)

This section is the **single reference table** mapping the Dashboard UI Kit's design tokens to every codebase's native token prefix. All UI work across eras should use these values, not ad-hoc hex literals.

### Kit source tokens (`docs/frontend/ideas/Dashboard ui kit/scss/abstracts/`)

| Kit SCSS variable | Kit value | Role |
| --- | --- | --- |
| `$font-family-base` | `'Roboto', sans-serif` | Base font |
| `$body-bg` | `#f9f9f9` | Page background (light) |
| `$body-color` | `#7e7e7e` | Default body text |
| `$border-radius` | `0.75rem` (12px) | Default card/button radius |
| `$blue` (primary) | `#5e72e4` | Primary brand blue |
| `$green` (success) | `#297F00` | Success semantic color |
| `$red` (danger) | `#EE3232` | Danger/error semantic color |
| `$orange` (warning) | `#ff9900` | Warning semantic color |
| `$shadow` | `0px 0px 40px 0px rgba(82,63,105,0.1)` | Card shadow |
| `$border` | `#f0f1f5` | Border color |
| `$d-bg` | `#181f39` | Dark mode background |
| `$dark-card` | `#1e2746` | Dark mode card surface |

### Per-codebase token mapping

| Design token role | Kit reference | `app` — `--c360-*` | `root` — `--color-*` | `admin` — `--color-*` | `extension` — `--c360-color-*` |
| --- | --- | --- | --- | --- | --- |
| **Primary** | `#5e72e4` | `--c360-primary` = `--c360-indigo-600` (`#4f46e5`) | `--color-primary` = `#7c3aed` (marketing purple) | `--color-primary-600` = `#2563eb` | `--c360-color-primary` = `#2563eb` |
| **Primary hover** | darker blue | `--c360-primary-hover` = `--c360-indigo-700` | `--color-primary-hover` = `#6d28d9` | `--color-primary-700` = `#1d4ed8` | `--c360-color-primary-hover` = `#1d4ed8` |
| **Success** | `#297F00` | `--c360-success` = `#16a34a` | `--color-emerald-500` = `#10b981` | `--color-success-600` = `#16a34a` | `--c360-color-success-fg` = `#86efac` |
| **Warning** | `#ff9900` | `--c360-warning` = `#ca8a04` | `--color-amber-500` = `#f59e0b` | `--color-warning-600` = `#d97706` | `--c360-color-warn-fg` = `#fcd34d` |
| **Danger** | `#EE3232` | `--c360-danger` = `#dc2626` | `--color-rose-500` = `#f43f5e` | `--color-error-600` = `#dc2626` | `--c360-color-danger-fg` = `#fca5a5` |
| **Page background** | `#f9f9f9` | `--c360-bg` = `--c360-slate-50` (`#f8fafc`) | `--color-surface` = `#0f172a` (dark/glass) | `--color-gray-50` = `#f9fafb` | `--c360-color-bg` = `#0f172a` |
| **Surface / card** | `#ffffff` | `--c360-bg-elevated` = `#ffffff` | glass `rgba(255,255,255,0.1)` | `--color-gray-100` = `#f3f4f6` | `--c360-color-surface` = `#1e293b` |
| **Border** | `#f0f1f5` | `--c360-border` = `--c360-slate-200` (`#e2e8f0`) | `--color-glass-border` = `rgba(255,255,255,0.2)` | `--color-gray-200` = `#e5e7eb` | `--c360-color-border` = `#334155` |
| **Body text** | `#7e7e7e` | `--c360-text` = `--c360-slate-900` | `--color-slate-100` = `#f1f5f9` | `--color-gray-900` = `#111827` | `--c360-color-text` = `#f1f5f9` |
| **Muted text** | — | `--c360-text-muted` = `--c360-slate-500` | `--color-slate-400` = `#94a3b8` | `--color-gray-500` = `#6b7280` | `--c360-color-text-secondary` = `#94a3b8` |
| **Card radius** | `0.75rem` (12px) | `--c360-radius-lg` = `1rem` → **align to `0.75rem`** | `--radius-lg` varies | `--radius-lg` = `12px` | `--c360-radius-lg` = `8px` → target `12px` |
| **Card shadow** | `0px 0px 40px 0px rgba(82,63,105,0.1)` | Level 1: `0 1px 3px rgba(0,0,0,0.08)` | glass shadow | `box-shadow` in `cards.css` | `box-shadow: 0 2px 8px rgba(0,0,0,0.4)` |
| **Font stack** | Roboto / system | `system-ui, -apple-system, sans-serif` | `system-ui, sans-serif` | `system-ui, sans-serif` | `system-ui, Roboto, sans-serif` |

### Alignment decisions (locked)

| Codebase | Decision |
| --- | --- |
| `contact360.io/app` | Keep indigo-600 primary. Adjust `--c360-radius-lg` from `1rem` → `0.75rem` to match kit card radius. Adopt kit body-bg feel via `--c360-slate-50`. |
| `contact360.io/root` | Keeps purple `#7c3aed` primary for brand identity. For `/docs` and `/api-docs` subpages only: inherit kit neutral palette (slate-50 bg, gray text, `0.75rem` radius). |
| `contact360.io/admin` | `--color-primary-600: #2563eb` already closest to kit. Verify body bg `#f9f9f9` equivalent is applied via Tailwind `bg-gray-50` / `design-tokens.css`. |
| `contact360.extension` | Blue-600 primary matches admin. `popup.css` already documents 8pt grid kit alignment. Increase `--c360-radius-lg` from `8px` → `12px` for toasts/popup card. |

### Component parity matrix

| UI control | Kit demo page | `app` primitive | `root` primitive | `admin` CSS + template | `extension` CSS |
| --- | --- | --- | --- | --- | --- |
| Button | `ui-button.html` | `Button.tsx` → `c360-btn--*` | `Button3D.tsx` | `static/css/components/button.css` | `.c360-popup__button` |
| Input | `form-element.html` | `Input.tsx` → `c360-input` | `Input3D.tsx` | `static/css/components/form-inputs.css` | `.c360-popup__input` |
| Checkbox | `form-element.html` | `Checkbox.tsx` → `c360-checkbox` | `Checkbox3D.tsx` | `form-inputs.css` `.form-checkbox` | `.c360-checkbox` |
| Radio | `form-element.html` | `Radio.tsx` → `c360-radio` | `Radio3D.tsx` | `form-inputs.css` `.form-radio-group` | — (planned `c360-radio`) |
| Progress | `ui-progressbar.html` | `Progress.tsx` → `c360-progress--*` | `Progress3D.tsx` | `static/css/components/progress.css` | `.c360-progress` |
| Tabs | `ui-tab.html` | `Tabs.tsx` / `tabs/Tabs.tsx` | `TabGroup.tsx` / `Tabs3D.tsx` | `static/css/components/tabs.css` + `dashboard-tabs.js` | planned two-tab layout |
| Badge | `ui-badge.html` | `Badge.tsx` → `c360-badge--*` | `Badge3D.tsx` | `static/css/components/badges.css` | `.c360-status--*` |
| Alert / Toast | `ui-alert.html`, `uc-toastr.html` | `Alert.tsx`, `sonner` | `Toast3D.tsx` | flash messages in `base.html` + `app-flash--*` | `.c360-toast` |
| Modal | `ui-modal.html` | `Modal.tsx`, `ConfirmModal.tsx` | `Modal3D.tsx` | `static/css/components/modal.css` + `modal.js` | — (planned confirm) |
| Pagination | `ui-pagination.html` | `Pagination.tsx`, `TablePagination.tsx` | — | `static/css/components/pagination.css` | — |
| Wizard / steps | `form-wizard.html` | multi-step React state | — | `templates/partials/stepper.html` | — |
| Chart (line) | `chart-chartjs.html` | `DashboardLineChart.tsx` (Recharts) | `RechartsChart.tsx` | D3 `graph.js` | — |

### Spacing system (8pt grid — shared across all surfaces)

| Step | Value | Kit equiv (`$spacer * N`) | `--c360-spacing-*` | `--space-*` (docs convention) |
| --- | --- | --- | --- | --- |
| 1 | 4px | — | `--c360-spacing-1` | `--space-1` |
| 2 | 8px | `$spacer * 0.5` | `--c360-spacing-2` | `--space-2` |
| 3 | 12px | — | `--c360-spacing-3` | `--space-3` |
| 4 | 16px | `$spacer` (1rem) | `--c360-spacing-4` | `--space-4` |
| 6 | 24px | `$spacer * 1.5` | `--c360-spacing-6` | `--space-6` |
| 8 | 32px | `$spacer * 2` | `--c360-spacing-8` | `--space-8` |
| 12 | 48px | `$spacer * 3` | `--c360-spacing-12` | `--space-12` |

### Typography scale (all surfaces)

| Level | Kit (`$h*-font-size`) | Product value | Usage |
| --- | --- | --- | --- |
| h1 | `2.25rem` (36px) | 36px bold | Hero / page title (marketing) |
| h2 | `1.875rem` (30px) | 24px semibold | Page title (dashboard) |
| h3 | `1.5rem` (24px) | 20px semibold | Section heading |
| h4 | `1.125rem` (18px) | 18px semibold | Card title, modal title |
| h5 | `1rem` (16px) | 16px medium | Sub-heading, tab label |
| body | `0.875rem` (14px) | 14px regular | Data rows, descriptions |
| small | `0.75rem` (12px) | 12px regular | Captions, metadata, timestamps |
| mono | — | 13px monospace | Email addresses, API keys |

### Border radius scale (kit-aligned)

| Token | Kit equiv | `app` `--c360-radius-*` | `admin` `--radius-*` | `extension` `--c360-radius-*` |
| --- | --- | --- | --- | --- |
| xs / sm | — | `--c360-radius-sm: 6px` | — | `--c360-radius-sm: 4px` |
| md | — | `--c360-radius-md: 10px` | `--radius-md` | `--c360-radius: 6px` |
| lg (card) | `$border-radius: 0.75rem` | `--c360-radius-lg: 0.75rem` **← update** | `--radius-lg: 12px` | `--c360-radius-lg: 12px` **← update** |
| full / pill | — | `--c360-radius-full: 9999px` | — | `--c360-radius-pill: 999px` |

### Shadow scale (kit-aligned)

| Level | Kit reference | `app` | `admin` | `extension` |
| --- | --- | --- | --- | --- |
| Card | `0px 0px 40px 0px rgba(82,63,105,0.1)` | `0 1px 3px rgba(0,0,0,0.08)` + adjust | `card.css` shadow | `0 2px 8px rgba(0,0,0,0.4)` |
| Dropdown | `0 4px 12px rgba(0,0,0,0.12)` | Level 2 | — | — |
| Modal | `0 8px 24px rgba(0,0,0,0.16)` | Level 3 | `modal.css` | — |

---

## Cross-surface control consistency checklist

Use this checklist when reviewing root/app/admin UX parity:

- Inputs have explicit labels, helper/error text, and visible focus states.
- Checkbox and radio controls have keyboard support and clear selected state visuals.
- Progress bars expose deterministic state labels (idle/running/success/failure semantics).
- Tabs preserve active-state visibility and keyboard navigation.
- Graph surfaces provide fallback text/stats when interactive render fails.
- Button variants reflect intent consistently (primary/secondary/destructive/disabled/loading).


---

## Email app docs pack — `contact360.io/email`

### Component highlights
- `components/email-list.tsx` — mailbox fetch orchestration, loading/error/empty state.
- `components/data-table.tsx` — tabs, checkbox selection, pagination, row action dropdown.
- `components/app-sidebar.tsx` — folder navigation and user bootstrap.
- `components/nav-secondary.tsx` — compact secondary nav rail aligned to Radix/shadcn patterns.
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
