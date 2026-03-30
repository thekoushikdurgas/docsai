# Connectra email-system task pack (`2.x`)

Grounded in [`docs/codebases/connectra-codebase-analysis.md`](../codebases/connectra-codebase-analysis.md).

## Codebase file map (high-value for 2.x bulk CSV)

| Area | Paths (start here) | Notes |
| --- | --- | --- |
| Service root | `contact360.io/sync` | Connectra service folder |
| Contacts/companies APIs | `/contacts`, `/companies`, `/common` routes | Bulk upsert + jobs surfaces |
| Streaming CSV ingestion | `io.Pipe()`-based streams | `2.x` bulk stability requirement (multi-GB without memory spikes) |
| Job engine | `OPEN → IN_QUEUE → PROCESSING → COMPLETED|FAILED → RETRY_IN_QUEUED` | In-memory queue durability is a known gap |
| Deterministic IDs | UUID5 keys | Idempotency for batch upsert + retries |

## Scope

Support bulk CSV-driven email workflows that rely on Connectra ingestion and retrieval.

## Email field lineage (what Connectra must preserve for `2.x`)

Connectra is not the email “engine” in `2.x`, but it becomes a downstream consumer/producer of email fields during ingestion/enrichment. For `2.x` bulk workflows, ensure the following contact/company fields are treated as stable and queryable:

- `contacts.email`
- `contacts.email_status` (must preserve canonical vocabulary; no ad-hoc renames)
- company/domain linkage fields used by finder (`domain`, company identifiers)

## Small tasks

- **Contract:** Freeze CSV column mapping contract for contacts/companies fields used in finder/verifier workflows.
- **Service:** Validate `common/jobs` + `common/batch-upsert` paths for large import/export flows.
- **Database:** Ensure `jobs`, `filters`, and `filters_data` writes remain consistent with batch ingestion.
- **Flow:** Confirm streaming CSV (`io.Pipe`) path can process multi-GB inputs without memory spikes.
- **Release gate evidence:** Throughput benchmark, failed-row retry behavior, and job status integrity evidence.

## Root/Admin surface contributions (era sync)

- **`contact360.io/root`**: landing-level email workflows messaging and interaction modules (`EmailFinderSection`, `AIWriterSection`, supporting selectors/progress storytelling).
- **`contact360.io/admin`**: documentation dashboard and endpoint/docs management for email-system surfaces, including relationship graph visibility for docs operations.
