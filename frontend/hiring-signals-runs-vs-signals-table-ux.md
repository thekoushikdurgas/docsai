# UX audit: Runs tab `Table` vs Signals `HiringSignalsDataTable`

Comparison of **empty states**, **loading**, **density**, and related patterns between [`RunsTab.tsx`](contact360.io/app/src/components/feature/hiring-signals/RunsTab.tsx) (satellite sessions) and [`HiringSignalsDataTable.tsx`](contact360.io/app/src/components/feature/hiring-signals/HiringSignalsDataTable.tsx) (job list). Goal: consistency awareness for future polish — no required code change from this doc alone.

**See also:** [Hiring signals page anatomy](hiring-signals-page-anatomy.md).

## Components in play

| Area | Runs (satellite block) | Signals (main list) |
|------|-------------------------|------------------------|
| Table primitive | [`Table`](contact360.io/app/src/components/ui/Table.tsx) (`c360-table` wrapper) | `@mui/x-data-grid` `DataGrid` + [`C360DataTableShell`](contact360.io/app/src/components/ui/C360DataTableShell.tsx) (`.c360-data-table-shell`) |
| Data scope | Client-paged slice `satellitePaged` from in-memory rows | Server-paged `jobs` from `useHiringSignals` |
| Selection | Not used on Runs `Table` (no `selectedKeys`) | DataGrid `checkboxSelection` + same `selectedKeys` `Set` + `keepNonExistentRowsSelected` |

## Loading

| | Runs `Table` | Signals `HiringSignalsDataTable` |
|---|--------------|----------------------------------|
| **When** | `loading={runsLoading && satelliteRunsRows.length === 0}` | DataGrid `loading` only when `loading && rows.length === 0` (same “no skeleton flicker when rows exist”) |
| **Visual** | Five skeleton rows via `Table` (`c360-skeleton c360-table__skeleton-bar`) | MUI loading overlay (empty list only) |
| **Partial refresh** | If rows already exist, table does **not** show skeleton (only empty vs data) | Same idea: no loading overlay when rows already exist during refresh |

**Takeaway:** Both avoid skeleton/overlay flicker when data is already present. Signals no longer uses custom skeleton `<tr>` rows; behavior matches via DataGrid `loading` gating.

## Empty

| | Runs `Table` | Signals DataGrid |
|---|--------------|------------------|
| **API** | `emptyState={<p>…</p>}` → single cell `c360-table__empty` | Custom `noRowsOverlay` with matching instructional copy |
| **Copy** | “No sessions in this view.” (filter-dependent) | “No job rows yet. Run a scrape…” |
| **Outside table** | Tracked section: paragraph “No tracked scrapes yet.” when `!runsLoading` | N/A (empty only inside table) |

**Takeaway:** Runs uses **two** empty patterns (cards section + table); Signals uses **one** in-grid empty overlay. Both are acceptable; align **tone** (instructional vs terse) if you want one voice.

## Density / compactness

| | Runs | Signals |
|---|------|---------|
| **Row density** | No `comfortable` / `compact` prop on `Table` | DataGrid `density` (`compact` vs `comfortable`) from sidebar |
| **Column width** | Some columns use `min-w` / `max-w` in cell renderers | Title cell `max-width` via CSS (`.c360-hs-title-cell`) |

**Takeaway:** Signals exposes **user-controlled density** (from filter sidebar → page state). Runs does not; add only if product asks for uniform density across tabs.

## Sort

| | Runs `Table` | Signals |
|---|--------------|---------|
| **Sort** | Optional per-column `sortable` → **client-side** sort in `Table` state | **Server** sort via DataGrid sort model + `setFilters` / `sortKey` / `sortOrder` |
| **Runs satellite columns** | Columns are not marked `sortable: true` in the excerpted config | N/A |

**Takeaway:** Different models by design (small local list vs large server list).

## Pagination

| | Runs | Signals |
|---|------|---------|
| **Table block** | `Pagination` under satellite `Table` when filtered count > `RUNS_PAGE_SIZE` | `Pagination` in `DataToolbar` `meta` (same chrome row as scope tabs) when `total > filters.limit` |
| **Page size** | Fixed `RUNS_PAGE_SIZE` (10) for satellite + tracked | Toolbar `Select` 10/25/50/100 + `setPageSize` |

## Recommendations (optional polish)

1. **Empty styling:** Optionally reuse `c360-table__empty` typography class inside Signals `noRowsOverlay` for identical tokens.
2. **Loading visuals:** If designers want parity with Runs skeleton bars, customize DataGrid `loadingOverlay` slot.
3. **Density on Runs:** Only if UX research shows users want the same compact mode on session rows; otherwise leave as-is.
