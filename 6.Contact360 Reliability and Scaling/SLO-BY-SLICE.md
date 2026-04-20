# SLO targets by vertical slice

**Owner:** SRE · **Last reviewed:** 2026-04-19  
**Companion:** [`../OBSERVABILITY-BASELINE.md`](../OBSERVABILITY-BASELINE.md), [`../DEPLOYMENT-MATRIX.md`](../DEPLOYMENT-MATRIX.md).

| Slice | Indicator | Target (initial) |
| ----- | ----------- | ---------------- |
| **A — Foundation** | Gateway availability | 99.5% monthly |
| **C — Contacts list** | `filterData` + list GraphQL p95 | \< 800 ms (warm) |
| **D — SN save** | End-to-end save p95 (gateway → extension.server → Connectra) | \< 5 s per chunk |
| **E — Enrichment** | Job completion p95 (single contact) | \< 30 s (provider-dependent) |
| **H — Campaign** | Send tick processing backlog | \< 5 min lag at P95 |
| **G — AI** | SSE time-to-first-token p95 | \< 2 s |

Revise after production telemetry; link runbooks when SLO burn breaches.
