---
id: 0.1.2.4
title: As-built repository map (gateway, apps, EC2 satellites)
phase: 0.Foundation and pre-product stabilization and codebase setup
owner: platform
last_reviewed: 2026-04-19
status: populated
flow_refs: ["flow1", "flow5"]
schema_refs: []
---

# As-built repository map

**Source of truth:** This doc reconciles Phase 0 **stub names** (`apps/web`, `services/crm-service`, …) with **actual** roots in the monorepo: `contact360.io/*` (Python/TypeScript apps) and `EC2/*` (Go satellites). Authoritative contracts: [`DECISIONS.md`](../../DECISIONS.md), gateway [`backend/endpoints/contact360.io/`](../../backend/endpoints/contact360.io/).

## Top-level layout

| Phase 0 notion | Real path (repo root) | Stack / role |
| -------------- | -------------------- | ------------ |
| `services/api-gateway` (`0.2.2.1`) | [`contact360.io/api`](../../../contact360.io/api) | FastAPI + Strawberry GraphQL, JWT + RLS, upstream satellite clients |
| `apps/web` (`0.2.1.1`) | [`contact360.io/app`](../../../contact360.io/app) | Next.js dashboard |
| `apps/admin` (`0.2.1.2`) | [`contact360.io/admin`](../../../contact360.io/admin) | Django admin |
| `apps/extension` (`0.2.1.4`) | [`contact360.extension`](../../../contact360.extension) (MV3); see also [`frontend/extension/`](../../frontend/extension/) and [`flowchart/extension-capture.md`](../../flowchart/extension-capture.md) | Chrome MV3 side panel + service worker |
| `services/crm-service` (`0.2.2.3`) | [`EC2/sync.server`](../../../EC2/sync.server) (Connectra) | Contact/company VQL, batch-upsert |
| `services/email-service` (`0.2.2.4`) | [`EC2/email.server`](../../../EC2/email.server) | Email satellite |
| `services/phone-service` (`0.2.2.5`) | [`EC2/phone.server`](../../../EC2/phone.server) | Phone / SMS satellite |
| `services/campaign-service` (`0.2.2.6`) | [`EC2/campaign.server`](../../../EC2/campaign.server) | Campaigns / CQL |
| `services/ai-agent-service` (`0.2.2.7`) | [`EC2/ai.server`](../../../EC2/ai.server) | AI / chats satellite |
| `services/file-service` (`0.2.2.10`) | [`EC2/s3storage.server`](../../../EC2/s3storage.server) | Uploads / S3-style API; admin logs via [`EC2/log.server`](../../../EC2/log.server) |
| Extension GraphQL / Sales Navigator | [`EC2/extension.server`](../../../EC2/extension.server) | LinkedIn / preview pipeline to gateway |
| `services/auth-service` (`0.2.2.2`) | **No standalone repo** | JWT issuance/session patterns in **gateway** + Django **admin**; RLS via `SET LOCAL` in API |

**Not yet a dedicated deployable** (keep Phase 0 stubs): `services/analytics-service` (`0.2.2.8`), `services/integration-service` (`0.2.2.9`), `apps/mcp-ui` (`0.2.1.3`) — align future work with [`DEPLOYMENT-MATRIX.md`](../../DEPLOYMENT-MATRIX.md).

## Documentation links per service

| Satellite / tier | `docs/backend/endpoints/` | Notes |
| ---------------- | ------------------------- | ----- |
| Gateway | [`contact360.io/`](../../backend/endpoints/contact360.io/) | `ROUTES.md`, `GRAPHQL-SCHEMA.md`, `SATELLITE-PARITY.md` |
| Connectra | [`sync.server/`](../../backend/endpoints/sync.server/) | Batch-upsert, VQL |
| email.server | [`email.server/`](../../backend/endpoints/email.server/) | |
| phone.server | [`phone.server/`](../../backend/endpoints/phone.server/) | |
| campaign.server | [`campaign.server/`](../../backend/endpoints/campaign.server/) | |
| ai.server | [`ai.server/`](../../backend/endpoints/ai.server/) | |
| extension.server | [`extension.server/`](../../backend/endpoints/extension.server/) | |
| s3storage.server | [`s3storage.server/`](../../backend/endpoints/s3storage.server/) | |
| log.server | [`log.server/`](../../backend/endpoints/log.server/) | |

## Packages (`0.2.3.*`)

| Stub | Reality |
| ---- | ------- |
| `packages/shared-types` | Types live **in app and API code** (TypeScript/Python); no root `packages/shared-types` yet — treat stub as **future** npm workspace package if/when extracted. |
| `packages/shared-events` | Same — Kafka/event shapes documented under [`DECISIONS.md`](../../DECISIONS.md) / service `EVENTS-BOUNDARY.md` where present. |
| `packages/shared-db` (Prisma) | **Future or alternate** — current DB access is SQLAlchemy/Alembic (API), Django (admin), Connectra (sync.server). Do **not** assume a root Prisma package. |
| `packages/ui` | Shared UI may live under `contact360.io/app` components; no separate `packages/ui` at repo root today — **future**. |

## Cross-links

- CI entrypoints: [Phase 0 README](../README.md) table
- Extension capture diagram: [`flowchart/extension-capture.md`](../../flowchart/extension-capture.md)
- Connectra UUID5: `EC2/sync.server/docs/EXTENSION_SCRAPER_UUID5.md` (repo path)
