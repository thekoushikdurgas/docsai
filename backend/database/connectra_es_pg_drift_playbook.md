# Connectra ES-PG Drift Playbook

This playbook is the `0.7` baseline for reporting drift between PostgreSQL (source of truth) and Elasticsearch indexes (`contacts_index`, `companies_index`).

## Goal

- Detect UUID drift in both directions:
  - present in PostgreSQL, missing in Elasticsearch
  - present in Elasticsearch, missing in PostgreSQL
- Produce a repeatable report for operations review.
- Keep reconciliation manual in `0.7`; automation can land in later minors.

## Scope

- PostgreSQL tables: `contacts`, `companies`
- Elasticsearch indexes: `contacts_index`, `companies_index`
- Identity key: `uuid`

## Preconditions

- Read access to PostgreSQL and Elasticsearch.
- API/service credentials loaded from environment.
- A stable snapshot window (avoid running during active bulk migrations if possible).

## Steps

1. Export UUIDs from PostgreSQL:
   - `SELECT uuid FROM contacts WHERE deleted_at IS NULL;`
   - `SELECT uuid FROM companies WHERE deleted_at IS NULL;`
2. Export UUIDs from Elasticsearch:
   - use `_source: ["id"]` scroll or paginated search over both indexes.
3. Normalize datasets:
   - lowercase UUIDs
   - deduplicate
   - sort
4. Compute set differences:
   - `pg_minus_es`
   - `es_minus_pg`
5. Record summary metrics:
   - total PG UUID count
   - total ES UUID count
   - missing counts and sample IDs

## Report Format

Capture results in markdown or JSON with:

- timestamp (UTC)
- environment (`dev`, `staging`, `prod`)
- entity (`contacts`, `companies`)
- counts: `pg_total`, `es_total`, `pg_minus_es_count`, `es_minus_pg_count`
- sample IDs (first 20 each side)
- operator notes (suspected cause)

## Repair Guidance (Manual, Report-First)

- If `pg_minus_es > 0`:
  - reindex affected UUID rows from PostgreSQL to Elasticsearch.
- If `es_minus_pg > 0`:
  - verify if records are soft-deleted in PostgreSQL.
  - if stale in ES, delete stale ES documents.
- Re-run the report after repair and attach before/after metrics.

## Operational Notes

- Keep threshold alerts simple in `0.7` (manual review).
- Proposed escalation threshold:
  - warning: drift > 0.1% of total
  - critical: drift > 1%
- Preserve reports in runbook evidence for `0.10` health gate.
