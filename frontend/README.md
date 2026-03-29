# Frontend Documentation Hub

Central repository for Contact360 UI inventories, design systems, and backend bindings across the 11-era roadmap.

## Project Structure

- **[pages/index.md](pages/index.md)** — Canonical registry of all 56+ frontend pages.
- **[pages/DESIGN_SYMBOLS.md](pages/DESIGN_SYMBOLS.md)** — Standardized layout and control notation.
- **[pages/admin_surface.md](pages/admin_surface.md)** — Django super-admin and DocsAI hub.
- `docs/` — Component, design, and service binding references.
- `excel/` — Machine-readable inventories for architectural audit.

## Codebase Hosts

| Host | Codebase | Stack |
| --- | --- | --- |
| `contact360.io/app` | **app** | Next.js Dashboard SPA |
| `contact360.io/root` | **root** | Next.js Marketing & Docs Shell |
| `contact360.io/email` | **email** | Next.js Mailhub Client |
| `contact360.io/admin` | **admin** | Django Operators Surface |

## Documentation Protocol

1. **JSON First**: Define routes and metadata in `*_page.json`.
2. **Standardize**: Run `python json_to_markdown.py` to generate page specs.
3. **Audit**: Apply [DESIGN_SYMBOLS.md](pages/DESIGN_SYMBOLS.md) and standardized **Navigation** handoffs.
4. **Link**: Run `python link_endpoint_specs.py` to bind UI to GraphQL contracts.
5. **Augment**: Run `augment_page_specs.py` for global parity.

## Cross-links

- [Main Documentation README](../../README.md)
- [Frontend Registry](pages/index.md)
- [Design Symbols](pages/DESIGN_SYMBOLS.md)
- [Service Topology](../../backend/endpoints/SERVICE_TOPOLOGY.md)
