# Contact360 Admin (Next.js)

Internal admin panel for Contact360 operators. UI matches `contact360.io/app` (c360 design system). Backend: **`contact360.io/api`** GraphQL (`/graphql`), same as the user app.

## Run locally

1. Start the API gateway (default `http://127.0.0.1:8001/graphql`). Ensure `ALLOWED_ORIGINS` includes `http://localhost:3001`.
2. `cp .env.example .env.local`
3. `npm install` && `npm run dev` (port **3001**)

Dev rewrites `/graphql` → `GRAPHQL_UPSTREAM_URL` (see `next.config.ts`).

## Auth

Sign in with a gateway user whose role is `Admin` or `SuperAdmin`. Login sends `pageType: "admin"` so the API rejects non-admin roles server-side.

## Production (EC2 / PM2)

**Dedicated admin host** (recommended): `18.207.217.168`, domain `admin.contact360.io`, PM2 port **3000**.

| Process              | Port | PM2 name                 | Host |
| -------------------- | ---- | ------------------------ | ---- |
| Admin (production)   | 3000 | `contact360-admin`       | `18.207.217.168` |
| User app (local dev) | 3000 | `contact360-dashboard`   | separate app EC2 |
| Admin (local dev)    | 3001 | —                        | `npm run dev` |

If admin shares a host with the dashboard, use admin on **3001** and dashboard on **3000** — see [deploy/COEXISTENCE.md](deploy/COEXISTENCE.md).

1. `cp .env.production.example .env.production` — set `NEXT_PUBLIC_GRAPHQL_URL`, `PORT=3000`
2. `bash deploy/ec2-deploy.sh`
3. Install nginx: `deploy/ec2-nginx-admin.conf` → `admin.contact360.io`

See [deploy/README.md](deploy/README.md), [deploy/EC2-ADMIN-HOST.md](deploy/EC2-ADMIN-HOST.md), and monorepo workflow `.github/workflows/deploy-contact360-admin.yml`.

## Scripts

| Command            | Description                          |
| ------------------ | ------------------------------------ |
| `codebase.bat`     | Windows full local audit: clean, install, codegen, typecheck, lint, build; optional dev |
| `npm run ci`       | lint + typecheck + build             |
| `npm run health:smoke` | API `/health` check (set `API_HEALTH_URL`) |
| `npm run codegen`  | GraphQL schema types (API must be up) |

## Docker

```bash
docker compose -f docker-compose.prod.yml up --build
```

Maps host port **3000** (production). Local dev remains **3001** via `npm run dev`.

## UI / CSS sync with app

The admin app copies the c360 design system from `contact360.io/app` (`app/css/*`). When the dashboard UI kit changes, diff or re-copy CSS partials into `contact360.io/admin/app/css/`. React primitives live in `src/components/ui/` (synced from app; admin-specific: `MuiDataGrid`, `Spinner`).

Visit `/ui-kit` locally to verify Tabs, Progress, Checkbox, Radio, and ContextMenu.

## DocsAI parity migration

Legacy Django DocsAI: [`contact360.io/1`](../1/README.md). This Next app is the migration target.

- `npm run parity:matrix` → [`docs/frontend/pages/admin-parity-matrix.json`](../../docs/frontend/pages/admin-parity-matrix.json)
- [deploy/COEXISTENCE.md](deploy/COEXISTENCE.md) · [docs/FEATURE_CHECKLIST.md](docs/FEATURE_CHECKLIST.md)
- Decommission: [`docs/runbooks/decommission-django-docsai.md`](../../docs/runbooks/decommission-django-docsai.md)

Iframe routes (`/docs`, `/durgasflow`, …) use `NEXT_PUBLIC_LEGACY_DOCSAI_URL`. BFF: `/api/docsai/*`.
