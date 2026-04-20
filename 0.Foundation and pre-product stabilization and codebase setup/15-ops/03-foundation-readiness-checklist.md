---
id: 0.7.2.3
title: Foundation readiness checklist
phase: 0.Foundation and pre-product stabilization and codebase setup
owner: platform
last_reviewed: 2026-04-19
status: populated
flow_refs: ["flow1"]
schema_refs: []
---

# Foundation readiness checklist

Track **foundation slice** exit criteria (doc gates, as-built map, FLOW-1 docs, flow dedup, CI, Connectra health). Update this table when items flip.

**Legend:** 🟢 Done · 🟡 Partial / in progress · 🔴 Not met / blocked

| # | Criterion | Status | Evidence / notes |
|---|-------------|--------|-------------------|
| M0 | **Doc gates** documented and visible: **PR template** + [`DOC-GATE-CHECKLIST.md`](../../DOC-GATE-CHECKLIST.md) (DECISIONS / satellite parity / VQL triple-sync / GRAPHQL-SCHEMA) | 🟢 | [`.github/pull_request_template.md`](../../../.github/pull_request_template.md); Phase 0 [README](../README.md) § Doc update gates |
| M1 | **As-built map** landed; Phase 0 apps/services/packages stubs reconciled | 🟢 | [`02-architecture/04-as-built-map.md`](../02-architecture/04-as-built-map.md); `index.json` **`populated`** for mapped sections |
| M2 | **FLOW-1** documented end-to-end: create + list + `filterData.total` + `X-Request-ID` | 🟢 | [`08-flows/02-contact-create-flow-v0.md`](../08-flows/02-contact-create-flow-v0.md), [`03-contact-list-flow-v0.md`](../08-flows/03-contact-list-flow-v0.md); code refs in each file |
| M3 | **Flows deduplicated** — one narrative per FLOW in `flows/` + `08-flows/README.md`; **`flow_refs`** in phase indexes resolve | 🟢 | [`08-flows/README.md`](../08-flows/README.md); [`scripts/verify-index-json-paths.py`](../../scripts/verify-index-json-paths.py) exits 0 |
| CI | **`main` green** for monorepo entrypoints: `api-ci.yml`, `app-ci.yml`, `django-ci.yml`, `extension-ci.yml`, satellite `deploy.yml` | 🟡 | See Phase 0 [README](../README.md) CI table — **verify in GitHub Actions** on your target branch |
| Ops | **`satelliteHealth`** GraphQL probe returns **ok** for Connectra (dev/staging) | 🟡 | Run authenticated `health { satelliteHealth { … } }` against env per [`OBSERVABILITY-BASELINE.md`](../../OBSERVABILITY-BASELINE.md) |

## Commands (optional)

- Index + flow ref validation (phase folders `0`–`11` only):

  ```bash
  python docs/scripts/verify-index-json-paths.py
  ```

## Cross-links

- [`DOC-HYGIENE-CHECKLIST.md`](../../DOC-HYGIENE-CHECKLIST.md) — periodic link checks
- **Phase handoff (1–11):** [`04-phase-roadmap-handoff.md`](04-phase-roadmap-handoff.md)
