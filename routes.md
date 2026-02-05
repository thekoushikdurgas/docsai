# DocsAI Routes Reference

All web routes are defined in `docsai/urls.py` and included app URLconfs. Base URL: `{{base_url}}` (e.g. `http://localhost:8000`).

---

## 1. Root-level (no prefix)

| Route | Purpose |
|-------|---------|
| `.well-known/appspecific/com.chrome.devtools.json` | Chrome DevTools; returns 204 |
| `favicon.ico` | Favicon; returns 204 |
| `^.+\.worker\.js\.map$` (regex) | Suppress worker source map 404; returns 204 |
| `/` | Core dashboard |
| `login` | Redirect → `/login/` |
| `login/` | Login |
| `register/` | Register |
| `logout/` | Logout |

---

## 2. `/docs/` — Documentation app

**Dashboard / health / info**

- `/docs/`, `/docs/pages/`, `/docs/endpoints/`, `/docs/relationships/` → documentation dashboard (tabs)
- `/docs/health/` → redirect to dashboard `?tab=health`
- `/docs/service-info/` → service info
- `/docs/docs/endpoint-stats/` → redirect to `/api/docs/`
- `/docs/statistics/` → statistics
- `/docs/routes-overview/` → routes overview

**Pages:** statistics, format, types; by-type (docs, marketing, dashboard, generic); by-state; by-user-type; `<page_id>/sections`, components, endpoints, versions, access-control, detail; list, create, detail, edit, update, delete. Draft API: `/docs/api/pages/draft/`.

**Endpoints:** statistics, format, api-versions, methods; by-api-version (v1, v4, graphql, generic); by-method (GET, POST, QUERY, MUTATION, generic); by-state; by-lambda; `<endpoint_id>/pages`, access-control, lambda-services, files, methods, used-by-pages, dependencies, detail; list, create, detail, edit, delete. Draft API: `/docs/api/endpoints/draft/`.

**Relationships:** statistics, format, graph, usage-types, usage-contexts; by-page, by-endpoint, by-usage-type, by-usage-context; by-state, by-lambda, by-invocation-pattern, by-postman-config; performance (slow, errors); `<relationship_id>/access-control`, data-flow, performance, dependencies, postman, detail; list, create, detail, edit, delete. APIs: `/docs/api/relationships/create/`, `.../update/`, `.../delete/`.

**Postman:** statistics, format; by-state; `<config_id>/collection`, environments, mappings, test-suites, access-control, detail; create, detail, edit, delete.

**Index & dashboard:** index/pages|endpoints|relationships|postman (validate, list); dashboard/pages|endpoints|relationships|postman.

**Media:** manager; preview, viewer, form (create, edit), delete; file `<path>/analyze`, validate, generate-json, upload-s3. APIs under `/docs/api/media-manager/` and `/docs/api/media/` (see [api.md](./api.md)).

**Operations:** dashboard; analyze, validate, generate-json, generate-postman, upload, seed, workflow, status; tasks, tasks/<task_id>. APIs: `/docs/api/operations/upload-file-list/<resource_type>/`, `upload-to-s3/<resource_type>/`.

**Legacy:** list, `<page_id>/`, create, `<page_id>/update`, `<page_id>/delete`.

**Redirects:** All `/docs/media-manager/*` paths redirect to the corresponding `/docs/*` routes.

---

## 3. `/durgasman/`

| Path | Purpose |
|------|---------|
| `/durgasman/` | Dashboard |
| `/durgasman/design/` | Design dashboard |
| `/durgasman/collection/<collection_id>/` | Collection detail |
| `/durgasman/import/` | Import UI |
| `/durgasman/api/collections/` | List collections |
| `/durgasman/api/collections/<collection_id>/requests/` | Requests in collection |
| `/durgasman/api/requests/<request_id>/` | Request detail |
| `/durgasman/api/environments/` | Environments |
| `/durgasman/api/history/` | History |
| `/durgasman/api/mocks/` | Mocks |
| `/durgasman/api/analyze/` | Analyze response |
| `/durgasman/api/execute/` | Execute request |

---

## 4. Other app prefixes

| Prefix | Purpose |
|--------|---------|
| `/analytics/` | Analytics dashboard |
| `/ai/` | AI agent: chat, sessions, session detail, `api/chat/` |
| `/codebase/` | Codebase dashboard, scan, analyses/<id>, files, dependencies, patterns |
| `/tasks/` | Task list, create, detail, start, complete, edit |
| `/media/` | Media app list |
| `/graph/` | Graph visualization |
| `/tests/` | Test runner dashboard |
| `/accessibility/` | Accessibility dashboard |
| `/roadmap/` | Roadmap dashboard |
| `/postman/` | Postman app: homepage, dashboard |
| `/templates/` | Templates list |
| `/architecture/` | Architecture (blueprint) view |
| `/database/` | Database schema view |
| `/json-store/` | JSON store list |
| `/operations/` | Operations app dashboard |
| `/page-builder/` | Page builder editor |
| `/knowledge/` | Knowledge: list, create, detail, edit, delete, search |
| `/admin/` | App admin: users, user-history, statistics, logs (bulk-delete, update, delete), system-status, settings |

---

## 5. `/api/v1/` — Documentation REST API

Health, docs meta, pages, endpoints, relationships, postman, dashboard (pagination). All GET except as used by dashboard. See [api.md](./api.md) for full list.

---

## 6. `/api/` — OpenAPI / schema

| Path | Purpose |
|------|---------|
| `/api/schema/` | OpenAPI schema (Spectacular) |
| `/api/docs/` | Custom API docs (Swagger-style) |
| `/api/swagger/` | Spectacular Swagger UI |
| `/api/redoc/` | ReDoc UI |

---

## 7. `/durgasflow/`

Dashboard, hub, workflows; workflow create, detail, edit, delete, execute, activate, deactivate; editor (by workflow, new); executions, execution detail; credentials, credential create/detail/delete; templates, template use; import/n8n/<path>; webhook/<workflow_id>/<webhook_path>.

---

## 8. Static and media (DEBUG only)

When `DEBUG=True`, static and media files are served from `STATIC_URL` and `MEDIA_URL`.

---

## Related docs

- **API endpoints (full list):** [api.md](./api.md)
- **Quick reference:** [routes.txt](../routes.txt)
- **Commands:** [commands.md](./commands.md)
