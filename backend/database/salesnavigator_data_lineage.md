# Sales Navigator — data lineage (Connectra contact/company)

**Scope:** Fields produced or enriched by Sales Navigator ingestion (`contact360.extension` FastAPI → Connectra bulk upsert). Planning artifact; validate against live Connectra schema and `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md`.

**Endpoint metadata:** `docs/backend/endpoints/salesnavigator_endpoint_era_matrix.json`

---

## Provenance (required SN context)

These fields tie a contact back to SN capture context and downstream features (campaign audience, analytics).

| Field | Type (logical) | Source | Notes |
| --- | --- | --- | --- |
| `source` | string | Constant | Always `sales_navigator` for SN-derived rows. |
| `lead_id` | string | SN URL / scrape context | Sales Navigator lead identifier extracted from profile/search context. |
| `search_id` | string | SN search session | Identifies the search/list context when bulk-captured. |
| `data_quality_score` | number (0–100) | Service | Completeness / quality score from mapper (`profileMerger` / backend). |
| `connection_degree` | string | SN profile | e.g. `1st`, `2nd`, `3rd` — SN relationship depth. |

---

## Identity and URLs

| Field | Notes |
| --- | --- |
| `uuid` | Deterministic UUID5 from `linkedin_url` + `email` (see module doc). |
| `linkedin_sales_url` | Raw SN profile URL. |
| `linkedin_url` | Normalized public LinkedIn URL when derivable. |

---

## Downstream reads

- **Dashboard / Connectra:** contacts and companies lists filtered by `source=sales_navigator`.
- **Era 10.x:** campaign audience provenance expects `lead_id` / `search_id` where available.
- **Era 5.x / AI:** `data_quality_score` and field completeness inform AI eligibility.

---

## Cross-references

- `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md` — REST schemas and field mapping table.
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md` — era delivery index.
- `docs/codebases/extension-codebase-analysis.md` — extension transport and shell gaps.
- `docs/frontend/docs/salesnavigator-ui-bindings.md` — UI bindings and implementation status.
