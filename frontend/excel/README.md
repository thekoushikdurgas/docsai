# Excel / CSV exports (`docs/frontend/excel/`)

CSV files here are **exports of page inventory metadata** (for spreadsheets, reviews, or one-off analysis). They are **derived artifacts** — not the canonical source for routes or code paths.

**Canonical documentation** for frontend routing and features:

- **`docs/frontend.md`** — dashboard, marketing, DocsAI, extension
- **`docs/frontend/pages/`** — JSON page specs and `pages_index.json`

---

## Files (naming pattern)

Exports use a shared prefix with category suffixes, for example:

| File pattern | Typical contents |
| --- | --- |
| `* - Title.csv` | Page titles / labels |
| `* - Product.csv` | Product-area grouping |
| `* - Dashboard.csv` | Dashboard-only rows |
| `* - Marketing.csv` | Marketing-site rows |
| `* - Docs.csv` | Docs / DocsAI-related rows |

Exact filenames may include export timestamps, e.g. `pages_export_2026-03-15 (6) - Dashboard.csv`.

## Folder reality snapshot

- Current exports include five CSV files: `Title`, `Product`, `Dashboard`, `Marketing`, and `Docs`.
- These represent one export batch and should be regenerated when page metadata changes.

---

## Naming

- CSV exports: batch prefix + ` - Category.csv` (Title, Product, Dashboard, Marketing, Docs); timestamps optional in filename.

## Structure contract

- Derived only from [`../pages/`](../pages/) and related JSON; never edit CSV as source of truth for routes.

## File index

- See **Files (naming pattern)** and **Folder reality snapshot** above; regenerate as a set when page metadata changes.

## When to regenerate

Regenerate CSVs when:

- Major page additions/removals ship (`docs/roadmap.md` / `docs/versions.md` cuts)
- You need a stakeholder review of **surface coverage** by era (`0.x`–`10.x` per **`docs/version-policy.md`**)

---

## Version era alignment

These exports do **not** encode SemVer by row automatically. Map rows to Contact360 eras using the tables in:

- **`docs/frontend/README.md`** (era → surfaces)
- **`docs/frontend/pages/README.md`** (example `page_id` per era)

## Normalized export field contract

When generating CSV exports, include these columns (or closest equivalents):

- `page_id`
- `surface` (`root` / `app` / `admin`)
- `route`
- `era`
- `introduced_in`
- `tabs`
- `buttons`
- `input_boxes`
- `checkboxes`
- `radios`
- `progress_bars`
- `graphs`
- `components`
- `hooks`
- `services`
- `contexts`
- `backend_bindings`
- `data_sources`

This keeps spreadsheet review aligned with `docs/frontend/pages/` JSON metadata and the tri-surface model.

---

## Related

- **`docs/flowchart.md`** — request flow across UI and gateway  
- **`docs/docsai-sync.md`** — if page metadata is mirrored into Django constants

## Manual export workflow

1. Update JSON metadata in `docs/frontend/pages/`.
2. Regenerate CSV exports in this folder from JSON source.
3. Spot-check at least one row each for `root`, `app`, and `admin`.
4. Validate era and UI-element fields are populated for the changed pages.
