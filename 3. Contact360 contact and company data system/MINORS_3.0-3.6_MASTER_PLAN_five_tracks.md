# Master plan — minors `3.0`–`3.6` (five-track matrix)

**Gates:** Ship after **`1.2` + `2.4`** close per roadmap. **Task pack:** [`connectra-contact-company-task-pack.index.md`](connectra-contact-company-task-pack.index.md).

| Minor | Contract | Service | Surface | Data | Ops |
| --- | --- | --- | --- | --- | --- |
| **3.0 Twin Ledger** | Dual-store GraphQL ops ↔ Connectra list/count/batch-upsert frozen in [`03`/`04` modules](../backend/graphql.modules/README.md) | `connectra_client` + two-phase read proven in staging | Contacts/companies tables smoke in app | PG + ES lineage in [`connectra_data_lineage.md`](../backend/database/connectra_data_lineage.md) | Health checks for sync + ES cluster |
| **3.1 VQL Engine** | VQL filter AST + error envelope documented | `vql_converter.py` + Connectra `VQLQuery` parity tests | Filter chips / builder bound to GraphQL | ES query mapping versioned | Golden-file + fuzz runs in CI |
| **3.2 Gateway Mirror** | Gateway field names match Connectra DTOs | Resolver delegation paths audited | No duplicate fetches (batch list) | Cache keys documented | Shadow traffic / diff sampling |
| **3.3 Search Quality** | Ranking/boost knobs in contract | ES analyzers + reindex playbook | UX for relevance feedback (optional) | Index mapping changelog | Benchmark SLO dashboard |
| **3.4 Dashboard UX** | Saved search + export GraphQL stable | Pagination cursors end-to-end | [`contacts_page`/`companies_page`](../frontend/pages/README.md) polish | N/A | Feature flags for beta columns |
| **3.5 Import-Export** | Jobs mutations + Connectra import/export limits | `contact360.io/jobs` processors idempotent | Progress UI + error rows | `scheduler_jobs` checkpoint fields | Operator runbook for stuck jobs |
| **3.6 SN Ingestion** | Extension payload → Connectra mapper | Chunk upload + dedup | SN save flows | Provenance columns populated | Rate limit + abuse metrics |

Each row decomposes into patch ladders already described in the corresponding minor `.md` file; this matrix is the **cross-minor planning view** only.
