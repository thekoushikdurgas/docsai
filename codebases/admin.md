# Codebase: `contact360.io/admin` (Contact360 Admin — Next.js)

**Role:** Internal operator UI at `admin.contact360.io` (Next.js, production port **3000** on EC2 `18.207.217.168`; local dev **3001**).  
**Legacy full DocsAI:** Django app at [`contact360.io/1`](../contact360.io/1/README.md) (Gunicorn ~8000) — kept in parallel until parity matrix is 100% implemented.  
**Primary integration:** `POST /graphql` on [`contact360.io/api`](../../contact360.io/api/README.md) with operator JWT (`pageType: "admin"` on login).

**Docs:** [`PHASE-DOCS-INDEX.md`](../PHASE-DOCS-INDEX.md) · [`ADMIN-MODULE.md`](../backend/endpoints/contact360.io/ADMIN-MODULE.md) · [Parity matrix](../frontend/pages/admin-parity-matrix.md)

## Stack

- Next.js 16 (App Router), React 19, MUI DataGrid, c360 CSS from `contact360.io/app`
- GraphQL client: `src/lib/graphqlClient.ts` → gateway
- No local database; all data via API gateway

## Legacy Django (`contact360.io/1`)

| Concern | Django prefix | Next status |
| ------- | ------------- | ----------- |
| Operator admin | `/admin/` | Migrated to Next (`/users`, `/billing`, …) |
| Documentation platform | `/docs/`, `/api/v1/` | BFF proxy + `/docs/*` shells (see admin `app/api/docsai`) |
| Automation | `/durgasflow/`, `/durgasman/`, `/page-builder/` | Legacy iframe/proxy routes until Phase 5 UI port |

Regenerate route parity: `node contact360.io/admin/scripts/generate-parity-matrix.mjs`

## Next.js route map (operator console)

| Area | Routes | GraphQL |
| ---- | ------ | ------- |
| Core | `/dashboard`, `/login`, `/settings` | `auth`, `admin.userStats` |
| Users & billing | `/users`, `/users/[id]`, `/billing/*` | `admin.*`, `billing.*` |
| Operations | `/jobs`, `/jobs/tickets`, `/ops/*` | `admin`, `jobs`, `contacts`, `campaignSatellite` |
| Platform | `/logs`, `/storage`, `/ai/*`, `/knowledge/*`, `/health`, `/analytics`, `/audit` | `admin`, `s3`, `aiChats`, `knowledge`, `health` |
| Documentation | `/docs/*` | BFF → Django REST + gateway where available |
| Legacy tools | `/durgasflow`, `/durgasman`, … | Proxy to Django |

## CI & deploy

- CI: `npm run ci` in `contact360.io/admin`
- Deploy: [`contact360.io/admin/deploy/README.md`](../../contact360.io/admin/deploy/README.md), workflow `.github/workflows/deploy-contact360-admin.yml`
- Coexistence nginx: [`contact360.io/admin/deploy/COEXISTENCE.md`](../../contact360.io/admin/deploy/COEXISTENCE.md)

## Related

- User app: [`contact360.io/app`](../../contact360.io/app/README.md)
- API gateway: [`contact360.io/api`](../../contact360.io/api/README.md)
- Django DocsAI (legacy): [`contact360.io/1`](../../contact360.io/1/README.md)
