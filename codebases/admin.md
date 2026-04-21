# Codebase: `contact360.io/admin` (DocsAI / internal admin console)

**Role:** Internal operator UI at `admin.contact360.io` (Django).  
**Primary integration:** `POST /graphql` on the API gateway with `Authorization: Bearer <JWT>` from the operator session.  
**Docs index:** [`PHASE-DOCS-INDEX.md`](../PHASE-DOCS-INDEX.md) · **Admin GraphQL contract:** [`../backend/endpoints/contact360.io/ADMIN-MODULE.md`](../backend/endpoints/contact360.io/ADMIN-MODULE.md)

## Stack

- Python / Django, session-based operator identity (`apps.core`)
- Shared HTTP client: `apps/core/services/graphql_client.py` → gateway
- SuperAdmin product flows: `apps/admin_ops` → `admin.*` GraphQL (see ADMIN-MODULE)

## Sub-apps and phase mapping (roadmap)

| Django app | URL prefix | Primary phase | Notes |
| ---------- | ---------- | ------------- | ----- |
| `core` | `/` | 0 | Login, dashboard shell |
| `admin_ops` | `/admin/` | 1 (+ ops) | Users, jobs, logs, billing, storage, system status |
| `documentation` | `/docs/`, `api/v1/` | 0, 8 | Docs portal and internal REST |
| `graph` | `/graph/` | 0, 3 | Relationship graph (gateway) |
| `roadmap` | `/roadmap/` | 0 | Roadmap hub |
| `architecture` | `/architecture/` | 0 | Architecture hub |
| `analytics` | `/analytics/` | 6 | Observability tiles (target) |
| `operations` | `/operations/` | 6 | Ops hub |
| `ai_agent` | `/ai/` | 5 | AI chat — non-streaming via gateway `aiChats.*`; SSE still TBD |
| `knowledge` | `/knowledge/` | 5 | Knowledge base UI (gateway `knowledge.*` CRUD) |
| `page_builder` | `/page-builder/` | 0, 8 | Page specs + storage |
| `json_store` | `/json-store/` | 0 | JSON documents + storage |
| `durgasman` | `/durgasman/` | 8 | API collections / request runner |
| `durgasflow` | `/durgasflow/` | 9 | Workflow automation (ORM) |
| `codebase` | `/codebase/` | 0 | Codebase scanner (stub/WIP) |
| `templates_app` | `/templates/` | 0 | Templates index |

Phases **2, 3, 4, 10, 11** add operator views under `admin_ops` (satellite job monitors, read-only CRM tools, campaign CQL lab, etc.) per product roadmap.

## Gateway GraphQL used by the admin UI (beyond `admin.*`)

| Namespace | Example fields | Admin surface |
| --------- | -------------- | ------------- |
| `contacts` | `contacts(query:)` | `/admin/ops/contacts-explorer/` |
| `campaignSatellite` | `cqlParse`, `cqlValidate`, `renderTemplatePreview` | `/admin/ops/campaign-cql/` |
| `aiChats` | `aiChats`, `createAIChat`, `sendMessage` | `/ai/` chat + sessions |
| `health` | `satelliteHealth`, `apiMetadata` | Analytics tiles, system status |
| `s3` | `deleteFile` | Optional `ADMIN_STORAGE_VIA_GATEWAY` deletes for `json_store` / `page_builder` |

## CI

- [`contact360.io/admin/.github/workflows/django-ci.yml`](../../contact360.io/admin/.github/workflows/django-ci.yml)

## Deployment

- See [`../DEPLOYMENT-MATRIX.md`](../DEPLOYMENT-MATRIX.md) — Admin row (ECS, gateway auth).
