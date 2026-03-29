# Enrichment and deduplication (Connectra-related)

## Deterministic IDs (UUID v5)

| Entity | Formula | Purpose |
| --- | --- | --- |
| Contact | `UUID5(firstName + lastName + linkedinURL)` | Idempotent contact upsert key |
| Company | `UUID5(name + linkedinURL)` | Idempotent company upsert key |
| Filter facet row | `UUID5(filterKey + service + value)` | Stable facet dedup across writes |

**Deduplication**

- Ingestion-level dedupe/merge for external sources (e.g. Sales Navigator) is implemented in `backend(dev)/salesnavigator/` (see roadmap stage 3.2 / Era 4). Connectra stores the resolved entity after upstream logic runs.

## Parallel write model

`BulkUpsertToDb` writes concurrently to:

1. PostgreSQL contacts
2. Elasticsearch contacts
3. PostgreSQL companies
4. Elasticsearch companies
5. `filters_data` metadata store

This model maximizes throughput but requires parity checks for ES/PG consistency.

## Filter-data derivation pattern

- Filter definitions (`filters`) declare keys and services.
- Incoming entity fields are projected into `filters_data` values.
- Each value receives deterministic UUID5 to avoid duplicate facet rows.
- Downstream filter sidebar and query-builder options read from this store.

## Reconciliation

Operational parity between PostgreSQL and Elasticsearch is maintained by dual writes in `BulkUpsertToDb` (see `connectra-service.md`). Any backfill/reindex or replay process should include post-run parity evidence.
