# Connectra contact-company task pack (`3.x`)

## Scope

Deliver core **VQL search**, **enrichment**, **deduplication**, and **dual-store integrity** for contacts and companies (`contact360.io/sync`).

## Core tasks

- **Contract:** Freeze VQL filter taxonomy and operator mapping for contacts and companies — keep aligned with [`vql-filter-taxonomy.md`](vql-filter-taxonomy.md) and gateway `vql_converter.py`.  
- **Service:** Harden `ListByFilters`, `CountByFilters`, and `batch-upsert` for deterministic behavior — see [`connectra-service.md`](connectra-service.md).  
- **Database:** Enforce **PG + ES** parity checks and deterministic **UUID5** rules for contacts, companies, and filter facets — [`enrichment-dedup.md`](enrichment-dedup.md).  
- **Flow:** Validate **two-phase read** and **five-store parallel write** diagrams against runtime behavior.  
- **Release gate evidence:** Relevance tests, **P95 latency** evidence, and **dedup consistency** report.

---

## Execution queue (from [`docs/codebases/connectra-codebase-analysis.md`](../codebases/connectra-codebase-analysis.md))

1. **Persistent queue backing** — replace single in-memory queue behavior that can lose pending work on process crash; align with `version_3.7` / ops runbooks.  
2. **ES–PG reconciliation job** — scheduled drift diagnostics with diff sets and optional repair hooks (`version_3.7`).  
3. **Per-tenant rate limiting + API key scope model** — move beyond global key + coarse limits (`version_3.9`).  
4. **Contract-parity tests** — VQL operators, filter metadata, and `get_field_type()` edge cases (`version_3.1`).  
5. **Batch-upsert idempotency evidence** — golden replays proving same payload → stable UUID list + no duplicate facet rows (`version_3.2`, `3.7`).

## Additional hardening (codebase risks)

- **CORS:** `AllowAllOrigins` / overly broad posture — tighten for hardened environments per deployment era.  
- **Observability:** Correlate **request id** from gateway through Connectra on list/count/upsert paths.

## Root/Admin surface contributions (era sync)

- **`contact360.io/root`**: product and feature pages that communicate contact/company data value and data-quality flows through tabs/cards/table demos.  
- **`contact360.io/admin`**: contact/company documentation and relationship-graph governance surfaces (`relationship-graph-viewer.js`, docs dashboards and related templates).

---

## Extension surface contributions (era sync)

### Era 3.x — Contact & Company Data

**`extension/contact360` profile capture pipeline:**

- `utils/profileMerger.js` — `deduplicateProfiles()`, `mergeProfiles()`, `scoreProfile()` fully implemented  
- `utils/lambdaClient.js` — `saveProfiles()` core flow: chunk → fetch → `POST /v1/save-profiles`  
- Lambda SN API relays profiles to Connectra **`/contacts/bulk`** and **`/companies/bulk`** (verify against deployed routes in `connectra-service.md`)  
- `profile_url` used as dedup key; completeness score gates merge decisions  

**Tasks:**

- [ ] Validate dedup ratio reporting (log `duplicate_count` per session)  
- [ ] Confirm `pruneProfile()` strips all `null`/`undefined` before submission  
- [ ] Verify Connectra bulk path correctly handles extension-sourced profile objects  
- [ ] Add `source="sales_navigator"` provenance tag to all contacts from extension  

## Completion gate

- [ ] One **golden search** (complex VQL) + **count** pair passes with trace id end-to-end.  
- [ ] Reconciliation or sampling shows **ES/PG** within agreed drift threshold after bulk upsert test.  
- [ ] Idempotency replay artifact attached for `batch-upsert` representative fixture.
