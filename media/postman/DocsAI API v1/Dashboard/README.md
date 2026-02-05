# Dashboard

**Note (post refactor):** In the **Django docs app** (mounted at `/docs/`), dashboard list data (pages, endpoints, relationships) is **loaded server-side** in `initial_data` on the dashboard page. The UI does not call list/pagination APIs for the initial load.

- **List APIs** still exist for CRUD and other consumers:
  - Pages: `GET {{base_url}}/docs/api/pages/` (query: `type`, `state`, `search`, `limit`, `offset`, `count=true`)
  - Endpoints: `GET {{base_url}}/docs/api/endpoints/`
  - Relationships: `GET {{base_url}}/docs/api/relationships/`
- The requests in this folder use `/api/v1/dashboard/...` (legacy base path). For the docs app, use `/docs/api/...` and the paths in `contact360/docsai/docs/api.md`.

See `contact360/docsai/docs/api.md` and `routes.md` for current endpoints and routes.
