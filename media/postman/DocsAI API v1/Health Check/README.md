# Health Check

**Note (post refactor):** In the **Django docs app** (mounted at `/docs/`), health and stats are **no longer exposed as JSON APIs**. They are server-rendered only in the dashboard. The requests in this folder target `/api/v1/health/` (legacy/Lambda-style base path).

- For the **docs app** (`{{base_url}}/docs/`): use the dashboard page; health is in the page context. There is no `GET /docs/api/health/` or `GET /docs/api/stats/`.
- If you use a **separate API** that still exposes `/api/v1/health/`, the requests in this folder apply to that service.

See `contact360/docsai/docs/api.md` for the current docs app API surface.
