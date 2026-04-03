# Sales Navigator integration (extension + workers)

Harvest, chunk upload, and LinkedIn/Sales Navigator–adjacent flows are served from **`EC2/extension.server`** (`contact360.io/extension`) and related paths, with persistence and search delegated to **Connectra** and the **gateway** for GraphQL-facing features.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Extension / SN row in the service registry |
| [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md) | SN-related operations → storage |
| [salesnavigator_endpoint_era_matrix.md](../endpoints/salesnavigator_endpoint_era_matrix.md) | HTTP route inventory by era |
| [salesnavigator_data_lineage.md](../database/salesnavigator_data_lineage.md) | SN-owned / mirrored data |

### GraphQL modules

- [`graphql.modules/23_SALES_NAVIGATOR_MODULE.md`](../graphql.modules/23_SALES_NAVIGATOR_MODULE.md)
- [`graphql.modules/21_LINKEDIN_MODULE.md`](../graphql.modules/21_LINKEDIN_MODULE.md)

### Also in `docs/backend/endpoints/`

- **[README.md](../endpoints/README.md)** — how matrices and `index.md` relate to extension traffic.

## Role

- Extension auth, scrape/harvest, chunk ingest, telemetry hooks, and dashboard integration points documented per matrix and module.

## Related

- Connectra upserts: [connectra.api.md](connectra.api.md)
- Runtime risks and gaps: [salesnavigator-codebase-analysis.md](../../codebases/salesnavigator-codebase-analysis.md), [extension-codebase-analysis.md](../../codebases/extension-codebase-analysis.md)
