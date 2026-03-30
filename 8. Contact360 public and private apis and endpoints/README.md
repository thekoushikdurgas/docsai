# 8.x Era Docs

Execution guide for Contact360 `8.x.x` era delivery.

## Era objective

- Define and deliver a stable era contract across Contract/Service/Surface/Data/Ops tracks.
- Ensure every patch packet carries closeout evidence before release handoff.

## Minor index

| Minor | Title | Status | Doc |
| --- | --- | --- | --- |
| `8.0` | API Era Foundation | planned | [`8.0 - API Era Foundation`](8.0%20—%20API%20Era%20Foundation.md) |
| `8.1` | Telemetry Instrumentation | planned | [`8.1 - Telemetry Instrumentation`](8.1%20—%20Telemetry%20Instrumentation.md) |
| `8.2` | Ingestion Quality Gate | planned | [`8.2 - Ingestion Quality Gate`](8.2%20—%20Ingestion%20Quality%20Gate.md) |
| `8.3` | Private Contract Lock | planned | [`8.3 - Private Contract Lock`](8.3%20—%20Private%20Contract%20Lock.md) |
| `8.4` | Public Surface Launch | planned | [`8.4 - Public Surface Launch`](8.4%20—%20Public%20Surface%20Launch.md) |
| `8.5` | Compatibility Guardrail | planned | [`8.5 - Compatibility Guardrail`](8.5%20—%20Compatibility%20Guardrail.md) |
| `8.6` | Webhook Fabric | planned | [`8.6 - Webhook Fabric`](8.6%20—%20Webhook%20Fabric.md) |
| `8.7` | Partner Identity Mesh | planned | [`8.7 - Partner Identity Mesh`](8.7%20—%20Partner%20Identity%20Mesh.md) |
| `8.8` | Reporting Plane | planned | [`8.8 - Reporting Plane`](8.8%20—%20Reporting%20Plane.md) |
| `8.9` | API Release Candidate | planned | [`8.9 - API Release Candidate`](8.9%20—%20API%20Release%20Candidate.md) |
| `8.10` | API Era Buffer | planned | [`8.10 - API Era Buffer`](8.10%20—%20API%20Era%20Buffer.md) |

## Patch ladder overview

- `8.0.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.1.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.2.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.3.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.4.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.5.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.6.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.7.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.8.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.9.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `8.10.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom

## Universal task breakdown

- `Task 1 - Contract`: freeze API contracts, auth boundaries, and error envelopes.
- `Task 2 - Service`: validate runtime health and integration behavior.
- `Task 3 - Surface`: verify UI/UX/admin/extension surface behavior.
- `Task 4 - Data`: verify migrations, index mappings, and lineage references.
- `Task 5 - Ops`: verify CI, rollback path, secrets, and runbooks.
- `Task 6 - Evidence`: close patch gates with links in era docs and versions index.

## Cross-links

- [`docs/README.md`](../README.md)
- [`docs/versions.md`](../versions.md)
- [`docs/architecture.md`](../architecture.md)
- [`docs/analysis/README.md`](../analysis/README.md)
## Tasks

### Contract

- ✅ Completed: 📌 Planned: **[appointment360]** — Diff and document schema for operations like ConnectraClient, LAMBDA_AI_API_URL, LAMBDA_CONNECTRA_API_URL; align with roadmap | area: `backend-api` | files: `docs/backend/apis/*.md`, `contact360.io/api/app/graphql/schema.py` | reason: Keep GraphQL/REST contracts aligned for era 8.0 patch 0.0.0

### Service

- ✅ Completed: 📌 Planned: **[appointment360]** — Service slice: - [ ] 🟡 In Progress: broad GraphQL capability exposure exists for internal/private use. | area: `backend-api` | files: `contact360.io/api/app/graphql/modules/`, `contact360.io/api/app/clients/` | reason: Implement or verify runtime behavior for - [ ] 🟡 In Progress: broad GraphQL capability exposure exists for internal/priva
- ✅ Completed: 📌 Planned: **[logsapi]** — Harden primary worker/gateway integration and failure envelopes | area: `backend-api` | files: `docs/codebases/logsapi-codebase-analysis.md` | reason: P0 band: critical path and idempotency

### Surface

- ✅ Completed: 📌 Planned: **[jobs]** — Verify UX for route `/` and bindings (patch 0.0.0 band 0) | area: `frontend-page` | files: `contact360/dashboard/app/page.tsx` | reason: Dashboard/extension surface for era 8 must match gateway contracts

### Data

- ✅ Completed: 📌 Planned: **[appointment360]** — Update PostgreSQL/ES/S3 lineage notes if this patch touches persistence or exports | area: `data-lineage` | files: `docs/backend/database/`, `migrations/` | reason: Migrations, indexes, and lineage evidence for this patch

### Ops

- ✅ Completed: 📌 Planned: **[platform]** — Record smoke evidence, rollback, and alerts (patch band 0: charter/P0) | area: `ops` | files: `docs/commands/`, `.github/workflows/` | reason: Smoke, rollback, and observability for patch 0.0.0

