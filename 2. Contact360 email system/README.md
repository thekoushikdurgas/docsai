# 2.x Era Docs

Execution guide for Contact360 `2.x.x` era delivery.

## Era objective

- Define and deliver a stable era contract across Contract/Service/Surface/Data/Ops tracks.
- Ensure every patch packet carries closeout evidence before release handoff.

## Minor index

| Minor | Title | Status | Doc |
| --- | --- | --- | --- |
| `2.0` | Email Foundation | planned | [`2.0 - Email Foundation`](2.0%20—%20Email%20Foundation.md) |
| `2.1` | Finder Engine | planned | [`2.1 - Finder Engine`](2.1%20—%20Finder%20Engine.md) |
| `2.2` | Verifier Engine | planned | [`2.2 - Verifier Engine`](2.2%20—%20Verifier%20Engine.md) |
| `2.3` | Results Engine | planned | [`2.3 - Results Engine`](2.3%20—%20Results%20Engine.md) |
| `2.4` | Bulk Processing | planned | [`2.4 - Bulk Processing`](2.4%20—%20Bulk%20Processing.md) |
| `2.5` | Mailbox Core | planned | [`2.5 - Mailbox Core`](2.5%20—%20Mailbox%20Core.md) |
| `2.6` | Provider Harmonization | planned | [`2.6 - Provider Harmonization`](2.6%20—%20Provider%20Harmonization.md) |
| `2.7` | Mailvetter Hardening | planned | [`2.7 - Mailvetter Hardening`](2.7%20—%20Mailvetter%20Hardening.md) |
| `2.8` | Bulk Observability | planned | [`2.8 - Bulk Observability`](2.8%20—%20Bulk%20Observability.md) |
| `2.9` | Email Credit & Audit Maturity | planned | [`2.9 - Email Credit & Audit Maturity`](2.9%20—%20Email%20Credit%20&%20Audit%20Maturity.md) |
| `2.10` | Email System Exit Gate | planned | [`2.10 - Email System Exit Gate`](2.10%20—%20Email%20System%20Exit%20Gate.md) |

## Patch ladder overview

- `2.0.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.1.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.2.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.3.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.4.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.5.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.6.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.7.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.8.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.9.x`: Void, Seed, Sprout, Roots, Soil, Rain, Stem, Branch, Leaf, Bloom
- `2.10.x`: Inventory, Probe, Benchmark, Certify, Harden, Document, Freeze, Tag, Promote, Exit

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

- ✅ Completed: 📌 Planned: **[appointment360]** — Diff and document schema for operations like ConnectraClient, LAMBDA_AI_API_URL, LAMBDA_CONNECTRA_API_URL; align with roadmap | area: `backend-api` | files: `docs/backend/apis/*.md`, `contact360.io/api/app/graphql/schema.py` | reason: Keep GraphQL/REST contracts aligned for era 2.0 patch 0.0.0

### Service

- ✅ Completed: 📌 Planned: **[appointment360]** — Service slice: - [x] ✅ Completed: email finder/verifier and job orchestration modules are integrated. | area: `backend-api` | files: `contact360.io/api/app/graphql/modules/`, `contact360.io/api/app/clients/` | reason: Implement or verify runtime behavior for - [x] ✅ Completed: email finder/verifier and job orchestration modules are integ
- ✅ Completed: 📌 Planned: **[mailvetter]** — Harden primary worker/gateway integration and failure envelopes | area: `backend-api` | files: `docs/codebases/mailvetter-codebase-analysis.md` | reason: P0 band: critical path and idempotency

### Surface

- ✅ Completed: 📌 Planned: **[emailapis]** — Verify UX for route `/email` and bindings (patch 0.0.0 band 0) | area: `frontend-page` | files: `contact360.io/app/...` | reason: Dashboard/extension surface for era 2 must match gateway contracts

### Data

- ✅ Completed: 📌 Planned: **[appointment360]** — Update PostgreSQL/ES/S3 lineage notes if this patch touches persistence or exports | area: `data-lineage` | files: `docs/backend/database/`, `migrations/` | reason: Migrations, indexes, and lineage evidence for this patch

### Ops

- ✅ Completed: 📌 Planned: **[platform]** — Record smoke evidence, rollback, and alerts (patch band 0: charter/P0) | area: `ops` | files: `docs/commands/`, `.github/workflows/` | reason: Smoke, rollback, and observability for patch 0.0.0

