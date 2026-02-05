# Media Alignment – Task Breakdown

Master plan and smaller tasks for aligning `media/endpoints`, `media/postman`, and `media/relationship` with appointment360 and the JSON model specs (`endpoints_json_models.md`, `postman_json_models.md`, `relationship_json_models.md`).

---

## Phase 0: Foundation (convention and inventory)

| Task | Description | Status |
|------|-------------|--------|
| 0.1 | Decide endpoint_id convention (e.g. query_*/mutation_* or mixed) | Done – documented in MEDIA_CONVENTIONS.md |
| 0.2 | Decide endpoint_path convention (graphql/OperationName) | Done – documented |
| 0.3 | Build canonical operation list from appointment360 | Done – used in fill_endpoint_service_files.py |
| 0.4 | Build endpoint_path ↔ endpoint_id map | Done – media/endpoints/index.json |
| 0.5 | Document relationship directory (media/relationship) | Done – MEDIA_CONVENTIONS.md |

---

## Phase 1: media/endpoints (endpoints_json_models.md)

| Task | Description | Status |
|------|-------------|--------|
| 1.1 | Normalize endpoint_id and _id in every endpoint JSON | Deferred – current mixed convention kept for backward compatibility |
| 1.2 | Set service_file (and router_file) for every doc | Done – 66 files filled via fill_endpoint_service_files.py |
| 1.3 | Set service_methods (and repository_methods) | Done – filled with resolver names |
| 1.4 | Validate used_by_pages (usage_type, usage_context, page_count) | Done – normalize_endpoints_to_spec.py |
| 1.5 | Add missing endpoint docs for backend ops | Done – 156 docs; audit reports 0 missing for audited ops |
| 1.6 | Remove or redirect obsolete endpoint docs | Not required |
| 1.7 | Regenerate endpoints index (index.json, endpoints_index.json) | Done – via normalize_endpoints_to_spec.py |

---

## Phase 2: media/postman (postman_json_models.md)

| Task | Description | Status |
|------|-------------|--------|
| 2.1 | Validate contact360.json (PostmanConfiguration, metadata) | Done – structure conforms |
| 2.2 | Align endpoint_mappings.endpoint_id with media/endpoints | Done – 4 mappings reference valid endpoint_id |
| 2.3 | Ensure postman_request_id exists on collection items | Done – 4 dashboard requests have matching ids |
| 2.4 | Ensure test_suites reference valid mapping_ids | Done |
| 2.5 | (Optional) Add endpoint_mappings for more endpoints | Pending – only 4 of 156 endpoints have mappings |
| 2.6 | (Optional) Align collection folders with modules | Pending |
| 2.7 | Update media/postman index | Pending – run normalize_media_indexes if needed |

---

## Phase 3: media/relationship (relationship_json_models.md)

| Task | Description | Status |
|------|-------------|--------|
| 3.1 | Use canonical endpoint_path in all relationships | Done – by-page uses paths from pages; aliases in fill script |
| 3.2 | Populate endpoint_reference for every relationship | Done – 112 entries via fill_relationship_endpoint_refs.py |
| 3.3 | Populate postman_reference where mapping exists | Done – dashboard 4 have postman_reference |
| 3.4 | Apply to all by-page files | Done – 33 files updated |
| 3.5 | Update sync_pages_to_relationships.py | Done – fills endpoint_reference and postman_reference from index/postman |
| 3.6 | (Optional) Normalize pages uses_endpoints to canonical paths | Pending |
| 3.7 | Regenerate by-endpoint from by-page | Done – rebuild_relationships_index_from_by_page.py |
| 3.8 | Remove/rename obsolete by-endpoint files | Done – 3 stale files removed |
| 3.9 | Regenerate relationship index and relationships_index | Done |
| 3.10 | Validate EnhancedRelationship (required fields, enums) | Done – normalize_media_relationships if needed |

---

## Phase 4: Cross-cutting and media (top level)

| Task | Description | Status |
|------|-------------|--------|
| 4.1 | Verify relationship postman_reference vs Postman configs | Done – dashboard refs match contact360.json |
| 4.2 | Align media/pages uses_endpoints with canonical paths | Pending – optional |
| 4.3 | Regenerate media indexes | Done – endpoints and relationship indexes rebuilt |
| 4.4 | Update ENDPOINTS_AUDIT.md, DASHBOARD_ALIGNMENT.md | Done – audit regenerated; dashboard doc already current |

---

## Phase 5: Validation and normalization

| Task | Description | Status |
|------|-------------|--------|
| 5.1 | Run endpoint validation (validate_endpoint_data) | Pending – run via Django/app when persisting |
| 5.2 | Run Postman validation (validate_postman_configuration_data) | Pending – run via Django when loading config |
| 5.3 | Run relationship validation (validate_relationship_data) | Pending – run via Django when persisting |
| 5.4 | Run normalize commands (normalize_media_files, normalize_media_indexes) | Done – pages/endpoints/relationships normalized; indexes regenerated |
| 5.5 | Re-run ENDPOINTS_AUDIT | Done – audit script run; 0 no service_file |

---

## Smaller tasks (actionable list)

**Completed in this session:**

1. Create MEDIA_CONVENTIONS.md (endpoint_id, endpoint_path, relationship dir, usage enums).
2. Create fill_endpoint_service_files.py (path+method → appointment360 module/resolver).
3. Fill service_file and service_methods for 66 endpoint JSONs; add GetVQLHealth/GetVQLStats mapping.
4. Run normalize_endpoints_to_spec.py (used_by_pages, page_count, regenerate index).
5. Create fill_relationship_endpoint_refs.py (endpoint_reference, postman_reference from index/postman).
6. Add path aliases for relationship ↔ endpoint path mismatches.
7. Run fill_relationship_endpoint_refs.py --write (33 by-page files, 112 endpoint_reference entries).
8. Run rebuild_relationships_index_from_by_page.py (index, relationships_index, 102 by-endpoint files).
9. Update sync_pages_to_relationships.py to fill endpoint_reference and postman_reference from index/postman.
10. Run audit_endpoints_vs_backend.py (regenerate ENDPOINTS_AUDIT.md; 0 no service_file).
11. Update ENDPOINTS_AUDIT.md with document count and recent changes note.
12. Create TASK_BREAKDOWN.md (this file).
13. Make EndpointRef.endpoint_state optional (default "development") in Pydantic so relationship JSON validates without endpoint_state in endpoint_reference.
14. Run normalize_media_relationships --write (242 items, 0 errors).
15. Run normalize_media_indexes --write (lightweight indexes, pages_index, endpoints_index, relationship index, relationships_index, n8n index).

**Remaining (optional or run in Django context):**

- **Postman:** Add more endpoint_mappings for other endpoints (2.5); align collection folders with modules (2.6).
- **Pages:** Normalize media/pages uses_endpoints to canonical endpoint_path (3.6, 4.2).
- **Validation at persist:** Run validate_endpoint_data / validate_postman_configuration_data / validate_relationship_data when saving via Django app (5.1–5.3).

**Smaller task breakdown for optional work:**

| # | Task | Scope |
|---|------|--------|
| O1 | Add endpoint_mappings in contact360.json for high-traffic endpoints | Pick N endpoints from endpoints_index; add mapping_id, endpoint_id, postman_request_id (create request in collection). |
| O2 | Normalize pages uses_endpoints to canonical graphql/OperationName | Script: read media/pages/*.json, resolve path via endpoints index, write back. |
| O3 | Wire validation into Django save flows | On endpoint/postman/relationship create/update, call the corresponding validate_*_data before persisting. |

---

## Scripts reference

| Script | Purpose |
|--------|---------|
| `scripts/fill_endpoint_service_files.py [--write]` | Fill missing service_file and service_methods in media/endpoints/*.json from backend map. |
| `scripts/normalize_endpoints_to_spec.py` | Normalize endpoint JSONs to spec; set page_count; rebuild index.json and endpoints_index.json. |
| `scripts/fill_relationship_endpoint_refs.py [--write]` | Fill endpoint_reference and postman_reference in media/relationship/by-page/*.json. |
| `scripts/sync_pages_to_relationships.py` | Sync media/pages → by-page; now fills endpoint_reference and postman_reference when path matches. |
| `scripts/rebuild_relationships_index_from_by_page.py` | Rebuild relationship/index.json, relationships_index.json, and by-endpoint/*.json from by-page. |
| `scripts/audit_endpoints_vs_backend.py` | Regenerate media/ENDPOINTS_AUDIT.md from endpoints_index.json. |

**Suggested workflow after changing pages or endpoints:**

1. `python scripts/sync_pages_to_relationships.py`
2. `python scripts/fill_relationship_endpoint_refs.py --write`
3. `python scripts/rebuild_relationships_index_from_by_page.py`
4. If endpoint docs changed: `python scripts/normalize_endpoints_to_spec.py` then `python scripts/audit_endpoints_vs_backend.py`
