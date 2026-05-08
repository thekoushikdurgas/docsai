# Radio vs Select patterns (`contact360.io/app`)

Repo-wide scan for **mutually exclusive choices** implemented as **`Radio` / `RadioGroup`** vs **`Select`**, with notes for **filter UX** consistency. Scan method: ripgrep for `RadioGroup`, `@/components/ui/Radio`, and raw `type="radio"` (excluding `Radio.tsx` implementation).

**See also:** [Hiring signals page anatomy](hiring-signals-page-anatomy.md) (where radios appear in hiring flows vs filter `Select`s).

## Kit primitives

- **Radio:** [`components/ui/Radio.tsx`](contact360.io/app/src/components/ui/Radio.tsx) — `Radio` + `RadioGroup` (cloned children get shared `name` / value handling).
- **Data-driven helper:** [`components/ui/RadioGroup.tsx`](contact360.io/app/src/components/ui/RadioGroup.tsx) — `options` array → radios.
- **Select:** [`components/ui/Select.tsx`](contact360.io/app/src/components/ui/Select.tsx) — used heavily in filters and toolbars.

## Where `Radio` / `RadioGroup` (kit) is used

| Location | Use case |
|----------|----------|
| [`RunScrapeModal.tsx`](contact360.io/app/src/components/feature/hiring-signals/RunScrapeModal.tsx) | Scrape source: Manual / API / Cron |
| [`BillingCheckoutWizard.tsx`](contact360.io/app/src/components/feature/billing/BillingCheckoutWizard.tsx) | Plan vs add-on; nested plan choice |
| [`S3FileUploadModal.tsx`](contact360.io/app/src/components/feature/files/S3FileUploadModal.tsx) | Upload mode |
| [`UploadGatewayTab.tsx`](contact360.io/app/src/components/feature/files/UploadGatewayTab.tsx) | Gateway path `upload/` vs `exports/` |
| [`app/(dashboard)/ui-kit/page.tsx`](contact360.io/app/app/(dashboard)/ui-kit/page.tsx) | Component gallery |

**Hiring signals filters:** [`HiringSignalsFilterSidebar.tsx`](contact360.io/app/src/components/feature/hiring-signals/HiringSignalsFilterSidebar.tsx) does **not** import `Radio`; multi-option facets use **`Select`** (and token comboboxes / `Input`). Radios appear in hiring **only** inside **`RunScrapeModal`**, not the filter rail.

## Raw `type="radio"` (non-kit or legacy)

| File | Notes |
|------|--------|
| [`HiringSignalsExportModal.tsx`](contact360.io/app/src/components/feature/hiring-signals/HiringSignalsExportModal.tsx) | Export intent options |
| [`PhoneFinderSingleTab.tsx`](contact360.io/app/src/components/feature/phone/PhoneFinderSingleTab.tsx) | Small binary/trio choice |
| [`EmailFinderSingleTab.tsx`](contact360.io/app/src/components/feature/email/EmailFinderSingleTab.tsx) | Same pattern |
| [`VqlFormParts.tsx`](contact360.io/app/src/components/vql/VqlFormParts.tsx) | Form part |
| [`FilterSection.tsx`](contact360.io/app/src/components/patterns/FilterSection.tsx) | Pattern-level radio in filter UI |

These are candidates to **migrate to `Radio` / `RadioGroup`** over time for a11y and styling consistency.

## Radix context menu

[`ContextMenu.tsx`](contact360.io/app/src/components/ui/ContextMenu.tsx) exports `ContextMenuRadioGroup` / `ContextMenuRadioItem` — menu-specific, not the same as page-level `RadioGroup`.

## Heuristic (when to use which)

| Prefer **Radio** (visible group) | Prefer **Select** |
|----------------------------------|-------------------|
| 2–5 options, all should be visible without opening a menu | Many options, long labels, or space-constrained |
| Choice changes infrequently and is central to the step (wizard, modal) | Filter dimensions with “Any” + long option lists |
| Legal/marketing needs to show all choices at once | Numeric or enum lists aligned with backend (`JobListFilters`) |

**Filters (hiring, contacts, etc.):** `Select` + “Any” sentinel is the dominant pattern; **do not** switch to radios unless the option set is tiny and UX asks for always-visible choices.

## Consistency follow-ups (optional)

1. **Export modal:** Evaluate replacing native radios with `RadioGroup` for keyboard roving + shared styling with `RunScrapeModal`.
2. **FilterSection:** If used in multiple features, align with kit `Radio` for focus ring and label association.
3. **No change required** for `HiringSignalsFilterSidebar` unless product spec demands visible radio groups for specific facets.
