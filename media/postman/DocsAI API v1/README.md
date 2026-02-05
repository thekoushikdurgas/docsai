Postman collection for DocsAI (contact360/docsai) Documentation API – Django service parity with Lambda Documentation API.

**Base URL**: `{{base_url}}`  
**Local**: http://localhost:8000

---

## Django docs app (mounted at `/docs/`)

When running the **Django documentation app** (mounted at `/docs/`):

- **Docs API base**: `{{base_url}}/docs/api/` (e.g. Pages list: `GET {{base_url}}/docs/api/pages/`).
- **Health and stats**: No longer exposed as JSON APIs. They are server-rendered only in the dashboard. Do not use `GET /docs/api/health/` or `GET /docs/api/stats/` (removed).
- **Dashboard**: List data (pages, endpoints, relationships) is loaded server-side in `initial_data`; list APIs remain available for CRUD and other consumers.

See **contact360/docsai/docs/api.md** and **contact360/docsai/docs/routes.md** for the current docs app API and routes.

**Environment**: Use `DocsAI - Local` (or similar); set `base_url` to your server (e.g. `http://127.0.0.1:8000`). For docs app requests, use URL `{{base_url}}/docs/api/...`.

---

## Legacy / Lambda-style API (this collection)

The requests in this folder use the **`/api/v1/`** base path (Lambda-style). Use them when targeting a service that still exposes that surface.

### REST API v1 (legacy paths)

- **Health Check**: Service info and health (root, health, database, cache, storage, external API). *In the Django docs app these are not exposed; health is server-rendered only.*
- **Pages API** (`/api/v1/pages/`) – List, format, statistics, types, by-type, by-state, page detail, sub-resources.
- **Endpoints API** (`/api/v1/endpoints/`) – List, api-versions, methods, by-api-version, by-method, detail, etc.
- **Relationships API** (`/api/v1/relationships/`) – List, graph, statistics, by-page, by-endpoint, detail, etc.
- **Postman API** (`/api/v1/postman/`) – List, statistics, by-state, detail, collection, environments, mappings, test-suites.
- **Index Management** (`/api/v1/index/`) – Read and validate index for pages, endpoints, relationships, postman.
- **Dashboard API** (`/api/v1/dashboard/`) – Paginated list for pages, endpoints, relationships, postman. *In the Django docs app, dashboard list data is server-rendered; use `/docs/api/pages/` etc. for list APIs.*

**Authentication**: Django docs app requires a logged-in session for `/docs/api/*`. Lambda-style endpoints may be public depending on deployment.
