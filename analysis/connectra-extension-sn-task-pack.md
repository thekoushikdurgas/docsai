# Connectra (`contact360.io/sync`) — Era 4.x Extension & Sales Navigator Task Pack

**Service:** `contact360.io/sync` (Connectra)  
**Era:** `4.x` — Extension/SN ingest per [`docs/codebases/connectra-codebase-analysis.md`](../codebases/connectra-codebase-analysis.md) § `4.x` row (*provenance fields and idempotent sync from SN sources*).

---

## Contract track

| Task | Priority |
| --- | --- |
| Lock **SN → Connectra** contact/company payload fields: provenance (`source`, `lead_id`, `search_id`, `data_quality_score`, `connection_degree` where applicable) | P0 |
| Document **conflict / validation** error codes on `POST /contacts/batch-upsert` for SN-sourced batches (operator-readable) | P1 |
| Align UUID5 rules with [`docs/enrichment-dedup.md`](../enrichment-dedup.md) and SN mapper (`salesnavigator` analysis — `linkedin_url` + email recipe) | P0 |
| Record **CORS** posture: today `AllowAllOrigins`; add era note for gateway-only extension traffic vs hardened env | P1 |
| Cross-link REST contracts in `docs/backend/apis/` + endpoint matrix JSON when batch-upsert schema changes | P0 |

---

## Service track

| Task | Priority |
| --- | --- |
| Guarantee **idempotent batch-upsert** for SN: same deterministic UUID → safe retry from `SaveService` / `ConnectraClient` | P0 |
| Verify **parallel write fan-out** (PG + ES + `filters_data`) preserves SN provenance fields on update paths | P0 |
| Add **circuit-breaker friendly** error surfaces for SN Lambda (timeout vs 4xx vs Connectra 5xx) | P1 |
| Expose **health / dependency** signals Connectra uses when SN bulk save degrades (Connectra unavailable) | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Operator visibility: **conflict resolution** summaries (created vs updated vs error) fed back through Appointment360 / dashboard SN panel | P0 |
| Dashboard: surface **ES vs PG drift** hints when SN-sourced contacts fail list/count parity | P1 |
| Document **VQL** expectations for SN-sourced contacts (`source` / provenance filters) | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| **PG + ES parity** for SN rows: mapping updates must land in both stores in one logical upsert | P0 |
| **Drift detection hooks:** align with Connectra queue item “ES–PG reconciliation job” (analysis gaps) — define minimal SN acceptance query set | P1 |
| Preserve **filter_data** facet consistency when SN bulk jobs update company/employer fields | P1 |

---

## Ops track

| Task | Priority |
| --- | --- |
| KPI: **sync conflict auto-resolution success rate** (roadmap **4.3**) — dedup + upsert success without manual fix | P0 |
| Runbook: **ES–PG drift** triage for SN ingestion windows (sample VQL vs PG `uuid` lookups, reindex procedure) | P0 |
| Alerting: bulk-upsert error rate by **source=sales_navigator** / extension session correlation | P1 |
| Release gate: **replay test** evidence — same SN CSV/batch twice → stable UUID counts | P0 |

---

## References

- [docs/backend/database/connectra_data_lineage.md](../backend/database/connectra_data_lineage.md)
- [docs/backend/endpoints/connectra_endpoint_era_matrix.json](../backend/endpoints/connectra_endpoint_era_matrix.json)
- [`docs/codebases/connectra-codebase-analysis.md`](../codebases/connectra-codebase-analysis.md)  
- [`docs/codebases/salesnavigator-codebase-analysis.md`](../codebases/salesnavigator-codebase-analysis.md)  
- [`extension-sync-integrity.md`](extension-sync-integrity.md)  
- [`sales-navigator-ingestion.md`](sales-navigator-ingestion.md)
