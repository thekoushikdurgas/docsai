# Frontend page specs (`docs/frontend/pages/`)

Markdown inventory for Contact360 **UI routes** across **app**, **root**, **email**, and (documented) **admin**.

| File | Role |
| --- | --- |
| [index.md](index.md) | **Master registry:** all pages, era map (0.x–10.x), **Mermaid navigation graphs**, cross-host handoffs, admin surface summary |
| [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md) | **Symbol glossary:** `[L]`, `[T]`, `(btn)`, `(pb)`, `{GQL}`, etc. — layout + controls + data |
| [admin_surface.md](admin_surface.md) | **Django DocsAI** (`contact360.io/admin`) — era map, symbols, Mermaid, URL prefixes |
| `*_page.md` | One spec per logical page (tabs, tables, hooks, services, flows from prior JSON export) |

## Codebases

- **`contact360.io/app`** — Dashboard Next.js app; most `*_page.md` entries.
- **`contact360.io/root`** — Marketing and public docs shell.
- **`contact360.io/email`** — Mailhub (`mailhub_*_page.md`).
- **`contact360.io/admin`** — Django DocsAI; see **Admin** section in [index.md](index.md) (add `admin_*_page.md` when you need per-route specs).

## Maintenance

1. Edit the relevant `*_page.md` (or add a new one) and update the table in [index.md](index.md).
2. Keep [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md) in sync when you introduce new layout or control patterns.
3. Regenerate **Era coverage**, **Page design (symbols)**, **Navigation**, and **Backend API documentation** footers on all Next/Mailhub specs:

   `python augment_page_specs.py`

   Run from repo root (`python docs/frontend/pages/augment_page_specs.py`) or from `docs/frontend/pages/`.

4. Regenerate **GraphQL → endpoint spec** link tables (`AUTO:endpoint-links`) after backend operation or page-spec changes:

   `python link_endpoint_specs.py`

   Run from repo root (`python docs/frontend/pages/link_endpoint_specs.py`) or from `docs/frontend/pages/`. See [../backend/endpoints/ENDPOINT_DATABASE_LINKS.md](../backend/endpoints/ENDPOINT_DATABASE_LINKS.md) for operation naming and database scope.

5. Django admin: edit [admin_surface.md](admin_surface.md) or add `admin_*_page.md` for per-route depth.

## Related docs

- `docs/frontend/docs/`, `docs/frontend/components.md` (if present)
- Era folders `docs/0.` … `docs/10.` for product-phase tasks
