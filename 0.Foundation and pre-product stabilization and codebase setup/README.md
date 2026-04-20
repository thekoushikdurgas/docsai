# Phase 0 — Foundation (entry)

**Owner:** platform · **Last reviewed:** 2026-04-19

**As-built map (reconciles stub names with `contact360.io/*` + `EC2/*`):** [`02-architecture/04-as-built-map.md`](02-architecture/04-as-built-map.md).

This folder holds the **vision, flows, and structural backlog** for Contact360. Authoritative architecture choices live in [`../DECISIONS.md`](../DECISIONS.md). Phase navigation and maintenance tasks: [`../PHASE-DOCS-INDEX.md`](../PHASE-DOCS-INDEX.md).

## Canonical flows (FLOW-1…5)

| Flow | Doc | Flowchart / diagram |
| ---- | --- | ------------------- |
| 1 Contact creation | [`flows/FLOW-1-contact-creation.md`](flows/FLOW-1-contact-creation.md) | [`../flowchart/`](../flowchart/) (contacts/VQL where applicable) |
| 2 Email enrichment | [`flows/FLOW-2-email-enrichment.md`](flows/FLOW-2-email-enrichment.md) | PRD PNG + [`../flowchart/extension-capture.md`](../flowchart/extension-capture.md) (enrichment paths) |
| 3 AI / RAG | [`flows/FLOW-3-ai-hybrid-rag.md`](flows/FLOW-3-ai-hybrid-rag.md) | PRD PNG |
| 4 Campaign | [`flows/FLOW-4-campaign-execution.md`](flows/FLOW-4-campaign-execution.md) | PRD PNG |
| 5 Extension enrich | [`flows/FLOW-5-extension-enrich.md`](flows/FLOW-5-extension-enrich.md) | [`../flowchart/extension-capture.md`](../flowchart/extension-capture.md) |

**Rule:** Prefer **one narrative** in `flows/` plus **one diagram** under `flowchart/`; avoid duplicating route tables — link to [`../backend/endpoints/`](../backend/endpoints/) instead.

## CI entrypoints (monorepo)

| Area | Workflow / path | Notes |
| ---- | ----------------- | ----- |
| API gateway | [`contact360.io/api/.github/workflows/api-ci.yml`](../../contact360.io/api/.github/workflows/api-ci.yml) | Strawberry GraphQL, Alembic |
| Web app | [`contact360.io/app/.github/workflows/app-ci.yml`](../../contact360.io/app/.github/workflows/app-ci.yml) | Next.js |
| Admin | [`contact360.io/admin/.github/workflows/django-ci.yml`](../../contact360.io/admin/.github/workflows/django-ci.yml) | Django |
| Extension (root) | [`.github/workflows/extension-ci.yml`](../../.github/workflows/extension-ci.yml) | Chrome MV3 |
| Deploy helpers | [`.github/workflows/deploy-*.yml`](../../.github/workflows/) | sync, email, AI, campaign satellites |
| EC2 satellites | `EC2/*/.github/workflows/deploy.yml` per repo | Connectra, extension, email, phone, s3storage, log, AI |

## Doc update gates

**PR checklist (copy/tick):** [`../DOC-GATE-CHECKLIST.md`](../DOC-GATE-CHECKLIST.md).

1. Any change to **HTTP routes**, **GraphQL fields**, or **Kafka/event payloads** touching multiple services → update [`../DECISIONS.md`](../DECISIONS.md) in the **same PR** (see [`../DECISIONS-GOVERNANCE.md`](../DECISIONS-GOVERNANCE.md)).
2. Satellite / gateway mapping → refresh endpoint docs and [`../backend/endpoints/contact360.io/SATELLITE-PARITY.md`](../backend/endpoints/contact360.io/SATELLITE-PARITY.md) as needed; VQL changes → triple-sync per [`../DECISIONS-GOVERNANCE.md`](../DECISIONS-GOVERNANCE.md).
3. Gateway schema drift → regenerate or diff [`../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md`](../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md) (see [`../backend/endpoints/contact360.io/GRAPHQL-SCHEMA-GENERATION.md`](../backend/endpoints/contact360.io/GRAPHQL-SCHEMA-GENERATION.md)).
4. New phase markdown promoted from `stub` → `populated` requires **owner + last-reviewed** in the file (per [`../PHASE-DOCS-INDEX.md`](../PHASE-DOCS-INDEX.md)).

## Related

- Deployment topology (ECS-first): [`../DEPLOYMENT-MATRIX.md`](../DEPLOYMENT-MATRIX.md)
- Observability baseline: [`../OBSERVABILITY-BASELINE.md`](../OBSERVABILITY-BASELINE.md)
- Resolved open questions (slice unblockers): [`../OPEN-DECISIONS-RESOLVED.md`](../OPEN-DECISIONS-RESOLVED.md)

## Appendix — phase 1–11 handoff sequence

After foundation, follow **dependency order** in [`15-ops/04-phase-roadmap-handoff.md`](15-ops/04-phase-roadmap-handoff.md) (Phase **3+4 → 1 → 2 → 10 → 5 → 8**; then **6+7** in parallel; **9**; **11**). Details and anchors are in that file.
