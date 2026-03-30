---
title: "Endpoint specs ↔ database snapshots & lineage"
---

# Endpoint ↔ database linking conventions

Use this document when authoring or reviewing `docs/backend/endpoints/*_graphql.md` and when interpreting **`db_tables_read`** / **`db_tables_write`** fields. It complements [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).

## GraphQL operation → endpoint filename

- **Canonical lookup:** [index.md](index.md) — table column **`path`** is `graphql/<OperationName>` (PascalCase, matches the schema operation name).
- **Resolved file:** the **`markdown`** column links to `*.md` (e.g. `graphql/GetBilling` → `get_billing_graphql.md`).
- **Superset index:** [endpoints_index.md](endpoints_index.md) lists additional generated specs; merge lookups if an operation appears only there.
- **Naming quirks:** some files use explicit prefixes (`mutation_*_graphql.md`, `query_*_graphql.md`) while others use `get_*_graphql.md` or operation-derived stems. **Do not guess** — always resolve via the index table.
- **Relative path to SQL snapshots** (from any file in `docs/backend/endpoints/`):

  `../database/tables/<table_name>.sql`

## Era tags on endpoints

Eras follow [docs/version-policy.md](../../version-policy.md) (`0.x`–`10.x`). Each endpoint spec’s **Lifecycle** table includes **`era`** (e.g. `3.x`).

| Era tag | Theme (summary) |
| --- | --- |
| `0.x` | Foundation — health, bootstrap, shell |
| `1.x` | User / billing / credit |
| `2.x` | Email finder & verifier flows |
| `3.x` | Contacts & companies / VQL / files |
| `4.x` | Extension & Sales Navigator |
| `5.x` | AI workflows |
| `6.x` | Reliability & scaling / analytics |
| `7.x` | Deployment / RBAC / admin |
| `8.x` | Public & private APIs / webhooks |
| `9.x` | Ecosystem & productization |
| `10.x` | Email campaigns |

## `db_tables_read` / `db_tables_write` scope

### Appointment360 gateway PostgreSQL

Tables that live in the **gateway** Postgres (and are snapshotted in this repo) should be referenced as:

- `` `table_name` `` with a link to [../database/tables/](../database/tables/) when `tables/<table_name>.sql` exists.

See [../database/tables/README.md](../database/tables/README.md) for the inventory.

### Connectra-owned tables (no snapshot here)

Endpoints that delegate to **contact360.io/sync** often list logical tables such as:

- `contacts`, `companies`, `filters`, `filters_data`, `contacts_index`

These are stored in **Connectra’s** PostgreSQL + Elasticsearch stack, not in the gateway snapshot folder. This repo does **not** include `tables/contacts.sql` for that reason.

**Authoritative docs:** [../database/connectra_data_lineage.md](../database/connectra_data_lineage.md) — use it for schema/lineage for those stores instead of expecting a `docs/backend/database/tables/*.sql` file.

### External and auxiliary stores

| Store | Typical use | Lineage / notes |
| --- | --- | --- |
| **Amazon S3** | Uploads, exports, artifacts | [../database/s3storage_data_lineage.md](../database/s3storage_data_lineage.md) |
| **Elasticsearch** | Connectra search indices | [connectra_data_lineage.md](../database/connectra_data_lineage.md) |
| **Redis** (if listed) | Caching / rate limits | Covered per service in lineage docs |
| **Logs pipeline** | Auditable events | [../database/logsapi_data_lineage.md](../database/logsapi_data_lineage.md) |

## Related hubs

- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md) — gateway flow and downstream services.
- [../database/README.md](../database/README.md) — database documentation index (if present).
