Postman collection for DocsAI (contact360/docsai).

**Base URL**: {{base_url}}
**Local**: http://127.0.0.1:8000

**Routing note**: This project currently mounts the REST API directly at `/api/v1/` (it does NOT mount the `apps.api` gateway at `/api/*`).

**Authentication**: Most `/api/v1/` endpoints are public; many `/docs/api/*` endpoints may require session login.

## REST API v1 (mounted)
- **Health**: root, health, database, cache, storage.
- **Docs/meta**: `/api/v1/docs/endpoint-stats/`.
- **Pages, Endpoints, Relationships, Postman**: list, filters, detail, sub-resources.
- **Dashboard**: paginated lists.

## Documentation internal JSON APIs (mounted)
- **Statistics** (`/docs/api/statistics/`)
- **Dashboard** (`/docs/api/dashboard/`) including graph

**Counts**: 98 GET endpoints under `/api/v1/` plus additional JSON endpoints under `/docs/api/*`.