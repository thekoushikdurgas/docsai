# Design symbols (Contact360 pages)

Shared visual tokens and icon conventions for dashboard and marketing pages documented under [`docs/frontend/pages/`](README.md). Use these names when aligning Figma ↔ code and when writing new page specs.

## Status & emphasis

| Symbol | Meaning | Typical usage |
| --- | --- | --- |
| **Primary** | Main CTA, high emphasis | Single primary button per view |
| **Secondary** | Alternate action | Outline or ghost button |
| **Destructive** | Irreversible or data loss | Delete, revoke, disconnect |
| **Success** | Completed / healthy | Toasts, badges, inline alerts |
| **Warning** | Attention needed | Low credit, approaching limit |
| **Error** | Failed / blocked | Form errors, API failures |
| **Info** | Neutral context | Hints, empty states |

## Layout regions

| Region | Role |
| --- | --- |
| **App shell** | Sidebar + top bar + content grid (dashboard) |
| **Page header** | Title, breadcrumbs, primary actions |
| **Data panel** | Tables, cards, filters |
| **Drawer / modal** | Focused subflows without route change |

## Data density

- **Comfortable** — default dashboard spacing.
- **Compact** — dense tables and admin-style lists.

## Icons

- Prefer the project icon set already used in `contact360.io/app` (Lucide / custom SVG sprite if configured).
- **Do not** invent new metaphors for the same action (e.g. one trash icon for delete everywhere).

## Accessibility

- Interactive targets ≥ 44×44 px where possible.
- Pair color-only states with text or icons (success/error not color-only).

## Cross-links

- [`README.md`](README.md) — pages inventory
- [`index.md`](index.md) — generated or hand-maintained index when present
