# Data tables inventory (`contact360.io/app`)

Factual snapshot of HTML `<table>` usage and table-oriented components. Regenerate counts with ripgrep when the app changes significantly.

**See also:** [Hiring signals page anatomy](hiring-signals-page-anatomy.md) (layout slots and data flow for the main hiring-signals route).

## Counts

| Metric | Value |
|--------|------:|
| Literal `<table` opening tags (`.tsx` / `.jsx`) | 22 |
| Distinct source files containing `<table` | 20 |
| Files matching `*Table*.tsx` | 9 |

## Files with `*Table*.tsx`

| Path |
|------|
| `contact360.io/app/src/components/ui/C360DataTableShell.tsx` |
| `contact360.io/app/src/components/feature/hiring-signals/HiringSignalsDataTable.tsx` |
| `contact360.io/app/src/components/feature/companies/CompaniesDataTable.tsx` |
| `contact360.io/app/src/components/feature/files/FilesDataTable.tsx` |
| `contact360.io/app/src/components/feature/contacts/ContactsDataTable.tsx` |
| `contact360.io/app/src/components/feature/jobs/JobsDataTable.tsx` |
| `contact360.io/app/src/components/feature/companies/CompanyContactsTable.tsx` |
| `contact360.io/app/src/components/ui/DataTable.tsx` |
| `contact360.io/app/src/components/ui/Table.tsx` |

## `<table` by area

### Primary data grids (feature)

- `src/components/feature/hiring-signals/HiringSignalsDataTable.tsx` — **MUI `@mui/x-data-grid`** (no literal `<table>`; sits inside `C360DataTableShell`)
- `src/components/feature/companies/CompaniesDataTable.tsx` — **MUI `@mui/x-data-grid`** (companies list route; `C360DataTableShell` + `C360MuiThemeProvider`)
- `src/components/feature/contacts/ContactsDataTable.tsx` — **MUI `@mui/x-data-grid`** (contacts list route; `C360DataTableShell` + `C360MuiThemeProvider`; expanded details via `ContactDetailPanel` `layout="block"` below the grid)
- `src/components/feature/files/FilesDataTable.tsx` (1)
- `src/components/feature/jobs/JobsDataTable.tsx` (1)
- `src/components/feature/companies/CompanyContactsTable.tsx` (1)

### Dashboard routes (inline tables)

- `app/(dashboard)/campaigns/page.tsx` (1)
- `app/(dashboard)/sales-navigator/page.tsx` (1)

### Feature tabs / panels

- `src/components/feature/activities/SavedSearchesTab.tsx` (1)
- `src/components/feature/usage/FeatureOverviewPanel.tsx` (2)
- `src/components/feature/email/EmailPatternsTab.tsx` (1)
- `src/components/feature/email/EmailBulkVerifierTab.tsx` (1)
- `src/components/feature/email/EmailBulkFinderTab.tsx` (1)
- `src/components/feature/profile/ProfileApiKeysTab.tsx` (1)
- `src/components/feature/billing/BillingInvoiceList.tsx` (1)

### Files / S3 modals

- `src/components/feature/files/S3FileJobsModal.tsx` (1)
- `src/components/feature/files/S3FileDetailModal.tsx` (2)
- `src/components/feature/files/S3FilePreviewModal.tsx` (1)
- `src/components/feature/files/S3FileSchemaModal.tsx` (1)

### Shared UI and primitives

- `src/components/ui/DataTable.tsx` (1)
- `src/components/ui/Table.tsx` (1)
- `src/components/ui/C360DataTableShell.tsx` (wrapper for native `<table>` grids; CSS `27-data-table-shell.css`)
- `src/components/shared/Skeleton.tsx` (1)
- `src/components/shared/InvoiceCard.tsx` (1)

## Notes

- Calendar-style grids may use component names such as `DatePicker.TableRow`; those are not counted here unless they render a literal `<table>`.
- Hiring Signals, **Companies** list, and **Contacts** list use **MUI DataGrid** ([`HiringSignalsDataTable.tsx`](contact360.io/app/src/components/feature/hiring-signals/HiringSignalsDataTable.tsx), [`CompaniesDataTable.tsx`](contact360.io/app/src/components/feature/companies/CompaniesDataTable.tsx), [`ContactsDataTable.tsx`](contact360.io/app/src/components/feature/contacts/ContactsDataTable.tsx)); companies list mirrors contacts for server sort, facet combobox + infinite scroll, toolbar page size, and bulk delete; shared column ids in [`companiesTableModel.ts`](contact360.io/app/src/components/feature/companies/companiesTableModel.ts). Regenerate `<table` counts when adding/removing literal tables elsewhere.
- Design reference for a MUI-based grid lives in `docs/frontend/ideas/mydesigns/table.md`; other production tables often use `c360-*` tokens and native `<table>` or shared `DataTable` / `Table` / `C360DataTableShell`.
