# DocsAI API Reference

This document describes **all API endpoints** in the DocsAI project. Base URL: `{{base_url}}` (e.g. `http://localhost:8000`).

**Summary:**

- **`/api/v1/`** – Documentation REST API (health, pages, endpoints, relationships, postman, dashboard). Used by the dashboard and Swagger/OpenAPI.
- **`/docs/api/`** – Documentation app AJAX APIs (draft, relationships CRUD, media-manager lists, media files, operations).
- **`/durgasman/api/`** – Durgasman (Postman-like) APIs: collections, requests, environments, history, mocks, analyze, execute.
- **`/ai/api/`** – AI chat completion.

**OpenAPI:** Schema at `/api/schema/`. Interactive docs: `/api/docs/` (custom), `/api/swagger/`, `/api/redoc/`.

---

## 1. OpenAPI / schema (root)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/schema/` | OpenAPI schema (Spectacular) |
| GET | `/api/docs/` | Custom API docs (Swagger-style UI) |
| GET | `/api/swagger/` | Spectacular Swagger UI |
| GET | `/api/redoc/` | ReDoc UI |

---

## 2. Documentation REST API v1 — `/api/v1/`

All return JSON. Used for dashboard data and documented in Swagger.

### 2.1 Health & service info

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/` | Service info |
| GET | `/api/v1/health/` | Full health (app, DB, cache, storage, external) |
| GET | `/api/v1/health/database/` | Database health |
| GET | `/api/v1/health/cache/` | Cache health |
| GET | `/api/v1/health/storage/` | Storage health |

### 2.2 Docs / meta

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/docs/endpoint-stats/` | Per-endpoint request counts, last_called_at |
| GET | `/api/v1/docs/endpoint-stats-by-user-type/` | Endpoint stats by user type (query: `user_type`, `limit`, `format=graph`) |

### 2.3 Pages (GET only, under `/api/v1/pages/`)

List, by-type (docs/marketing/dashboard, generic), by-state, by-user-type; detail and sub-resources: `access-control`, `sections`, `components`, `endpoints`, `versions`. See `apps/documentation/api/v1/pages_urls.py`.

### 2.4 Endpoints (GET only, under `/api/v1/endpoints/`)

List, by-api-version (v1/v4/graphql, count, stats, by-method), by-method (GET/POST/QUERY/MUTATION, count, stats), by-state, by-lambda; `api-versions`, `methods`; detail and sub-resources: `pages`, `access-control`, `lambda-services`, `files`, `methods`, `used-by-pages`, `dependencies`. See `apps/documentation/api/v1/endpoints_urls.py`.

### 2.5 Relationships (GET only, under `/api/v1/relationships/`)

List, usage-types, usage-contexts; by-page, by-endpoint, by-usage-type, by-usage-context, by-state, by-lambda, by-invocation-pattern, by-postman-config; performance (slow, errors); detail and sub-resources. See `apps/documentation/api/v1/relationships_urls.py`.

### 2.6 Postman (GET only, under `/api/v1/postman/`)

List, by-state; detail and sub-resources: `collection`, `environments`, `environments/<env_name>`, `mappings`, `mappings/<mapping_id>`, `test-suites`, `test-suites/<suite_id>`, `access-control`. See `apps/documentation/api/v1/postman_urls.py`.

### 2.7 Dashboard (pagination)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/dashboard/pages/` | Paginated pages for dashboard |
| GET | `/api/v1/dashboard/endpoints/` | Paginated endpoints |
| GET | `/api/v1/dashboard/relationships/` | Paginated relationships |
| GET | `/api/v1/dashboard/postman/` | Paginated postman configs |

---

## 3. Documentation app AJAX APIs — under `/docs/api/`

All under the documentation app; require a logged-in session.

### 3.1 Draft & relationships (forms / AJAX)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/docs/api/endpoints/draft/` | Endpoint draft (auto-save) |
| POST | `/docs/api/pages/draft/` | Page draft (auto-save) |
| POST | `/docs/api/relationships/create/` | Create relationship |
| POST/PUT | `/docs/api/relationships/<relationship_id>/update/` | Update relationship |
| POST/DELETE | `/docs/api/relationships/<relationship_id>/delete/` | Delete relationship |

### 3.2 Media Manager dashboard (lists / stats)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/docs/api/media-manager/pages/` | Pages list for dashboard |
| GET | `/docs/api/media-manager/endpoints/` | Endpoints list |
| GET | `/docs/api/media-manager/relationships/` | Relationships list |
| GET | `/docs/api/media-manager/postman/` | Postman list |
| GET | `/docs/api/media-manager/statistics/` | Statistics |
| GET | `/docs/api/media-manager/health/` | Health |

### 3.3 Media files

| Method | Path | Description |
|--------|------|-------------|
| GET | `/docs/api/media/files/` | List files |
| POST | `/docs/api/media/files/create/` | Create file |
| GET | `/docs/api/media/sync-status/` | Sync status |
| POST | `/docs/api/media/bulk-sync/` | Bulk sync |
| POST | `/docs/api/media/indexes/regenerate/pages/` | Regenerate pages index |
| POST | `/docs/api/media/indexes/regenerate/endpoints/` | Regenerate endpoints index |
| POST | `/docs/api/media/indexes/regenerate/postman/` | Regenerate postman index |
| POST | `/docs/api/media/indexes/regenerate/relationships/` | Regenerate relationships index |
| POST | `/docs/api/media/indexes/regenerate/all/` | Regenerate all indexes |
| GET | `/docs/api/media/files/<path:file_path>/` | Get file |
| PUT/PATCH | `/docs/api/media/files/<path:file_path>/update/` | Update file |
| DELETE | `/docs/api/media/files/<path:file_path>/delete/` | Delete file |
| POST | `/docs/api/media/sync/<path:file_path>/` | Sync single file |

### 3.4 Operations

| Method | Path | Description |
|--------|------|-------------|
| POST | `/docs/api/operations/upload-file-list/<resource_type>/` | Upload file list |
| POST | `/docs/api/operations/upload-to-s3/<resource_type>/` | Upload to S3 |

---

## 4. Durgasman — under `/durgasman/api/`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/durgasman/api/collections/` | List collections |
| GET | `/durgasman/api/collections/<collection_id>/requests/` | Requests in collection |
| GET | `/durgasman/api/requests/<request_id>/` | Request detail |
| GET | `/durgasman/api/environments/` | Environments |
| GET | `/durgasman/api/history/` | History |
| GET | `/durgasman/api/mocks/` | Mocks |
| POST | `/durgasman/api/analyze/` | Analyze response |
| POST | `/durgasman/api/execute/` | Execute request |

---

## 5. AI Agent — under `/ai/api/`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/ai/api/chat/` | Chat completion (AI) |

---

## 6. Unmounted APIs (not exposed at root)

The central API gateway (`apps.api.urls`) is **not** included in the root URLconf. The following are **defined but not mounted**:

- **`/api/ai/`** – chat, sessions, session detail (from `apps.ai_agent.api.urls`).
- **`/api/knowledge/`** – list, search, detail, update, delete, create (from `apps.knowledge.api.urls`).
- **`/api/tasks/`** – TaskViewSet REST (from `apps.tasks.api.urls`).
- **`/api/durgasflow/`** – workflows, executions, nodes, credentials, templates, stats (from `apps.durgasflow.api.urls`).

The **AI** app's exposed API is under **`/ai/api/chat/`** (from `apps.ai_agent.urls`), not `/api/ai/`.

---

## 7. Authentication

- **`/api/v1/*`** – Typically allowed for dashboard and tooling; check project auth middleware/settings.
- **`/docs/api/*`** – Require a logged-in session (Django auth). Use the same session/cookies as the docs dashboard.
- **`/durgasman/api/*`**, **`/ai/api/*`** – Follow app-level auth (session or token as configured).

---

## 8. Related docs

- **Web routes (all URLs):** [routes.md](./routes.md)
- **Quick reference:** [routes.txt](../routes.txt)
- **Commands:** [commands.md](./commands.md)
