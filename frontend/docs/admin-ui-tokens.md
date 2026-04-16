# Django admin UI tokens (contact360.io/admin)

The DocsAI admin uses **server-rendered Django templates** and static CSS under `contact360.io/admin/static/admin/css/`.

## Canonical files

| File | Role |
|------|------|
| `contact360.io/admin/static/admin/css/design-tokens.css` | `--c360-*` variables; aligned with Dashboard UI kit palette |
| `contact360.io/admin/static/admin/css/components/shell-eatio.css` | App shell / sidebar |
| `contact360.io/admin/static/admin/css/components/form-inputs.css` | Inputs, checkbox/radio |
| `contact360.io/admin/static/admin/css/components/graph.css` | Graph/codebase visualizations |

## Cross-reference

- **User web app (Next.js):** `contact360.io/app/app/css/dashboard-kit.css` — same design language; different stack (CSS layers vs Django staticfiles).
- **Kit ideas:** `docs/frontend/ideas/Dashboard ui kit/`.
