---
id: 0.7.2.4
title: Phase 1–11 dependency-ordered handoff roadmap
phase: 0.Foundation and pre-product stabilization and codebase setup
owner: platform
last_reviewed: 2026-04-19
status: populated
flow_refs: []
schema_refs: []
---

# Phase 1–11 — handoff roadmap (dependency order)

This is the **sequencing** for work after Phase 0 foundation — **not** an implementation commitment. Anchor decisions stay in [`DECISIONS.md`](../../DECISIONS.md) and [`OPEN-DECISIONS-RESOLVED.md`](../../OPEN-DECISIONS-RESOLVED.md).

| Order | Phase(s) | Focus | Depends on |
| ----- | -------- | ----- | ---------- |
| 1 | **3 + 4** | Connectra / VQL + extension capture | Foundation gateway + Connectra spine |
| 2 | **1** | BillingPort + credits | Usage signals from data plane |
| 3 | **2** | Email / phone enrichment | Phase 3 entities; **TRAI DND** per [`DECISIONS.md`](../../DECISIONS.md) |
| 4 | **10** | Campaign + CQL (`campaign.server`) | Audiences / credits / outbound surface |
| 5 | **5** | AI workflows (`ai.server`) | Planner; gateway JWT / allowlist / SSE per **topic G** in [`OPEN-DECISIONS-RESOLVED.md`](../../OPEN-DECISIONS-RESOLVED.md) |
| 6 | **8** | Public REST v1 + OpenAPI | Gateway-shaped DTOs; [`REST-V1-SUBSET.md`](../../8.Contact360%20public%20and%20private%20apis%20and%20endpoints/REST-V1-SUBSET.md) |
| 7 | **6 + 7** (parallel) | SLOs / runbooks + ECS/EC2 hardening | [`DEPLOYMENT-MATRIX.md`](../../DEPLOYMENT-MATRIX.md); trim Kubernetes-only stubs if unused |
| 8 | **9** | CRM / iPaaS integrations | REST v1 (Phase 8) |
| 9 | **11** | Lead scoring + recommendations | Events; ownership with CRM/Connectra per [`LEAD-ENRICHMENT-SPLIT.md`](../../backend/endpoints/email.server/LEAD-ENRICHMENT-SPLIT.md) |

## Related

- Phase index: [`PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md)
- Foundation readiness: [`03-foundation-readiness-checklist.md`](03-foundation-readiness-checklist.md)
