# Connectra data lineage (contacts / companies / search)

**Service:** `contact360.io/sync` (Go) — PostgreSQL authoritative rows + Elasticsearch query/index plane.

## Scope

- Physical tables and indices live **outside** the gateway `docs/backend/database/*.sql` snapshot; this document is the **contract authority** for Connectra-owned storage referenced by [`03_CONTACTS_MODULE.md`](../graphql.modules/03_CONTACTS_MODULE.md) and [`04_COMPANIES_MODULE.md`](../graphql.modules/04_COMPANIES_MODULE.md).

## Lineage notes

- **Dual write:** upserts land in PG then ES (ordering and failure handling per Connectra implementation).
- **VQL:** translated to ES query + PG hydration — see `contact360.io/sync` and [`connectra-codebase-analysis.md`](../../codebases/connectra-codebase-analysis.md).

## Related

- [`connectra_endpoint_era_matrix.md`](../endpoints/connectra_endpoint_era_matrix.md)
- Imported analysis: [`EC2/sync.server/docs/imported/analysis/connectra-contact-company-task-pack.md`](../../../EC2/sync.server/docs/imported/analysis/connectra-contact-company-task-pack.md)

*Extend this stub with table/index names and migration pointers when promoting Connectra schema docs into `docs/`.*
