# 10.x Era Docs

Execution guide for Contact360 `10.x.x` era delivery.

## Era objective

- Define and deliver a stable era contract across Contract/Service/Surface/Data/Ops tracks.
- Ensure every patch packet carries closeout evidence before release handoff.

## Minor index

| Minor | Title | Status | Doc |
| --- | --- | --- | --- |
| `10.0` | Campaign Bedrock | planned | [`10.0 - Campaign Bedrock`](10.0%20—%20Campaign%20Bedrock.md) |
| `10.1` | Contract Spine | planned | [`10.1 - Contract Spine`](10.1%20—%20Contract%20Spine.md) |
| `10.2` | Audience Graph | planned | [`10.2 - Audience Graph`](10.2%20—%20Audience%20Graph.md) |
| `10.3` | Template Forge | planned | [`10.3 - Template Forge`](10.3%20—%20Template%20Forge.md) |
| `10.4` | Sequence Pulse | planned | [`10.4 - Sequence Pulse`](10.4%20—%20Sequence%20Pulse.md) |
| `10.5` | Deliverability Shield | planned | [`10.5 - Deliverability Shield`](10.5%20—%20Deliverability%20Shield.md) |
| `10.6` | Reliability Mesh | planned | [`10.6 - Reliability Mesh`](10.6%20—%20Reliability%20Mesh.md) |
| `10.7` | Compliance Vault | planned | [`10.7 - Compliance Vault`](10.7%20—%20Compliance%20Vault.md) |
| `10.8` | Performance Lens | planned | [`10.8 - Performance Lens`](10.8%20—%20Performance%20Lens.md) |
| `10.9` | Governance Lock | planned | [`10.9 - Governance Lock`](10.9%20—%20Governance%20Lock.md) |
| `10.10` | Placeholder Policy | planned | [`10.10 - Placeholder Policy`](10.10%20—%20Placeholder%20Policy.md) |

## Patch ladder overview

- `10.0.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.1.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.2.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.3.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.4.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.5.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.6.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.7.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.8.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.9.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `10.10.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom

## Universal task breakdown

- `Task 1 - Contract`: freeze API contracts, auth boundaries, and error envelopes.
- `Task 2 - Service`: validate runtime health and integration behavior.
- `Task 3 - Surface`: verify UI/UX/admin/extension surface behavior.
- `Task 4 - Data`: verify migrations, index mappings, and lineage references.
- `Task 5 - Ops`: verify CI, rollback path, secrets, and runbooks.
- `Task 6 - Evidence`: close patch gates with links in era docs and versions index.

## Stack references

Framework and stack reference material (rename-safe paths under `docs/tech/`):

- [Go/Gin — why & practices](../tech/tech-go-gin-why-practices.md)
- [Go/Gin — 100-point checklist](../tech/tech-go-gin-checklist-100.md)
- [Next.js — why & practices](../tech/tech-nextjs-why-practices.md)
- [Next.js — 100-point checklist](../tech/tech-nextjs-checklist-100.md)
- [PostgreSQL vs Redis (canonical)](../docs/data-stores-postgres.md)


## Cross-links

- [`docs/README.md`](../README.md)
- [`docs/versions.md`](../versions.md)
- [`docs/architecture.md`](../architecture.md)
- [`docs/analysis/README.md`](../analysis/README.md)
## Tasks

### Contract

- ✅ Completed: 📌 Planned: **[emailcampaign]** — Diff and document schema for operations like ConnectraClient, LAMBDA_AI_API_URL, LAMBDA_CONNECTRA_API_URL; align with roadmap | area: `backend-api` | files: `docs/backend/apis/*.md`, `contact360.io/api/app/graphql/schema.py` | reason: Keep GraphQL/REST contracts aligned for era 10.0 patch 0.0.0

### Service

- ✅ Completed: 📌 Planned: **[emailcampaign]** — Service slice: Era 10 scope per docs/codebases/emailcampaign-codebase-analysis.md | area: `backend-api` | files: `contact360.io/api/app/graphql/modules/`, `contact360.io/api/app/clients/` | reason: Implement or verify runtime behavior for Era 10 scope per docs/codebases/emailcampaign-codebase-analysis.md
- ✅ Completed: 📌 Planned: **[jobs]** — Harden primary worker/gateway integration and failure envelopes | area: `backend-api` | files: `docs/codebases/jobs-codebase-analysis.md` | reason: P0 band: critical path and idempotency

### Surface

- ✅ Completed: 📌 Planned: **[appointment360]** — Verify UX for route `/email` and bindings (patch 0.0.0 band 0) | area: `frontend-page` | files: `contact360.io/app/...` | reason: Dashboard/extension surface for era 10 must match gateway contracts

### Data

- ✅ Completed: 📌 Planned: **[emailcampaign]** — Update PostgreSQL/ES/S3 lineage notes if this patch touches persistence or exports | area: `data-lineage` | files: `docs/backend/database/`, `migrations/` | reason: Migrations, indexes, and lineage evidence for this patch

### Ops

- ✅ Completed: 📌 Planned: **[platform]** — Record smoke evidence, rollback, and alerts (patch band 0: charter/P0) | area: `ops` | files: `docs/commands/`, `.github/workflows/` | reason: Smoke, rollback, and observability for patch 0.0.0

