# Extension / Connectra sync integrity (roadmap stage 4.3)

This doc ties **extension + Sales Navigator** ingestion to **Connectra** bulk upsert semantics: deterministic keys, server-side dedup, and observable reconciliation.

**Cross-references:** [`docs/codebases/extension-codebase-analysis.md`](../codebases/extension-codebase-analysis.md) (`profileMerger`, `lambdaClient`) · [`docs/codebases/salesnavigator-codebase-analysis.md`](../codebases/salesnavigator-codebase-analysis.md) (`SaveService`, extraction, `ConnectraClient`) · [`docs/codebases/connectra-codebase-analysis.md`](../codebases/connectra-codebase-analysis.md) (batch-upsert, UUID5) · [`docs/enrichment-dedup.md`](../enrichment-dedup.md).

## Idempotency token (client / batch)

- **Stable logical batch:** Callers should treat each “save” attempt as a batch with a **client-generated idempotency key** (e.g. extension session id + monotonic batch sequence, or hash of ordered `profile_url` list) carried on the request where the API contract allows (`X-Idempotency-Key` / body field — align with OpenAPI when formalized).
- **Purpose:** Correlates retries after Lambda cold start or network failure so operators can prove “one user action → one downstream outcome” in logs (`X-Request-Id` + idempotency key).
- **Connectra alignment:** Even without a chunk token, **deterministic UUID5** at persistence (`linkedin_url + email`, company UUID from name+URL) ensures **replay-safe upserts** for the same canonical profile (see below).

## Conflict resolution sequence (SaveService → completeness → Connectra)

End-to-end order:

1. **Extension** — `profileMerger.deduplicateProfiles`: groups by `profile_url`, **completeness score** decides field-level merge before HTTP.
2. **Sales Navigator `SaveService`** (`save_service.py`) — **`deduplicate_profiles`** (normalized `profile_url` / `linkedin_sales_url`): keeps **most-complete** profile; chunks (~500) with limited parallelism; aggregates per-chunk Connectra results.
3. **`ConnectraClient.batch_upsert`** — deterministic contact/company UUIDs (UUID5); parallel company + contact bulk writes.
4. **Connectra `BulkUpsert`** — PostgreSQL + Elasticsearch + `filter_data` fan-out; same IDs on retry → **upsert idempotency**.

Field-level lineage for “who won” merges is primarily enforced in **SaveService** + merger before Connectra sees the row.

## Reconciliation evidence

- **Response counts:** Compare input profile cardinality to **`saved_count`** / `contacts_created` / `contacts_updated` (and `errors[]`) returned from `POST /v1/save-profiles` and propagated to dashboard/extension UI (`SNSaveSummaryCard` patterns in SN analysis).
- **Logs:** Emit structured **`sn.sync.conflict_resolved`** (or equivalent) when dedup prefers one profile variant over another so support can answer “why did my row look like X?”
- **Dashboard / jobs:** Align sync status surfaces with Connectra write outcomes and extension provenance jobs (`contact360.io/jobs`) where extension-origin saves are tracked.

## Replay semantics

- **Re-sending the same batch** after partial failure: merged profiles produce the **same UUID5 keys** → Connectra upserts are **safe** (update-in-place, no duplicate contacts for the same canonical identity).
- **Partial chunk failure:** Retry only failed chunks; UUID stability avoids double-create when a chunk is replayed.
- **Extension retry:** `lambdaClient` serial queue + backoff should not change dedup keys; merger output should be identical for the same DOM snapshot.

## Idempotent bulk writes (Connectra)

- Connectra **`BulkUpsert`** writes PostgreSQL + Elasticsearch + `filter_data` in parallel (`contact360.io/sync`).
- Deterministic IDs: contacts from **firstName + lastName + linkedInURL** (see Connectra analysis; SN path uses harvested `linkedin_url` / email in UUID5 recipe in SN analysis).

## Related era work

- Chunk-level idempotency tokens are flagged as a **future hardening** item in SN analysis (duplicate saves on blind Lambda retry) — design **4.3** KPIs assuming current UUID5 + SaveService dedup as the baseline.


## References

- [docs/backend/endpoints/connectra_endpoint_era_matrix.json](../backend/endpoints/connectra_endpoint_era_matrix.json)


## Replay decision tree

1. Check whether idempotency token exists for the original batch.
2. Retry only failed chunks when token and chunk state are available.
3. Compare saved_count and reconciliation outputs against expected input count.
4. If UUID/reconciliation drift remains, escalate to manual merge runbook.
