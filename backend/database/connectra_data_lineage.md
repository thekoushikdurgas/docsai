# connectra data lineage (PostgreSQL + Elasticsearch)

## Storage model

- Hybrid model:

  - PostgreSQL as canonical row store (`contacts`, `companies`, `jobs`, `filters`, `filters_data`)
  - Elasticsearch as query/search index (`contacts_index`, `companies_index`)

- Runtime: `contact360.io/sync` (`Connectra`) with VQL query conversion and dual-write behavior.

## Core lineage entities

- Contact identity: deterministic UUID5 (`firstName + lastName + linkedinURL`)
- Company identity: deterministic UUID5 (`name + linkedinURL`)
- Filter facet identity: deterministic UUID5 (`filterKey + service + value`)
- Job identity/state: `OPEN`, `IN_QUEUE`, `PROCESSING`, `COMPLETED`, `FAILED`, `RETRY_IN_QUEUED`

## Read/write lineage pattern

### Read

1. VQL compiled to Elasticsearch query.
2. ES returns ordered IDs/cursors.
3. PG hydrates full rows by UUID.
4. Optional PG company populate for contact responses.

### Write

`batch-upsert` fans out concurrently to:

1. PG contacts
2. ES contacts index
3. PG companies
4. ES companies index
5. PG `filters_data`

## Era lineage concerns

- `0.x`: service/bootstrap contract and index baseline
- `1.x`: query/export volume lineage tied to billing/credit
- `2.x`: CSV import/export and job-state lineage
- `3.x`: VQL taxonomy freeze and ES/PG parity checks
- `4.x`: SN/source provenance and replay-safe upsert lineage
- `5.x`: AI enrichment field and confidence lineage
- `6.x`: reliability/SLO and retry-path evidence
- `7.x`: RBAC, audit, and tenant-isolation lineage
- `8.x`: versioned API and partner-access lineage
- `9.x`: entitlement/quota and tenant telemetry lineage
- `10.x`: campaign audience/suppression compliance lineage

## Operational checks

- ES/PG parity checks after bulk upsert and backfills
- `filters_data` derivation consistency against configured filter keys
- Job retry state transition correctness
- Query latency and error-rate evidence on contacts/companies list and count
- Drift playbook: `docs/backend/database/connectra_es_pg_drift_playbook.md`

## References

- `docs/codebases/connectra-codebase-analysis.md`
- `docs/3. Contact360 contact and company data system/connectra-service.md`
- `docs/3. Contact360 contact and company data system/vql-filter-taxonomy.md`
