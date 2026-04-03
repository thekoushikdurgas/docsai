# Appointment360 GraphQL gateway (`contact360.io/api`)

Python GraphQL API — primary product gateway for dashboard, extension, and workers. Resolvers delegate to Connectra, EC2 satellites, and internal modules.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Gateway row in the service registry |
| [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md) | GraphQL operations → logical tables / workers |
| [appointment360_endpoint_era_matrix.md](../endpoints/appointment360_endpoint_era_matrix.md) | Operation inventory by era |
| [appointment360_data_lineage.md](../database/appointment360_data_lineage.md) | RDS tables owned by the gateway / shared product plane |

### Also in `docs/backend/endpoints/`

- **[README.md](../endpoints/README.md)** — operation JSON and matrix layout.
- **[endpoints_index.md](../endpoints/endpoints_index.md)** — master inventory.
- **[index.md](../endpoints/index.md)** — `graphql/OperationName` → file map.

### GraphQL modules

- Deep contracts: [`docs/backend/graphql.modules/`](../graphql.modules/README.md) — `01`–`29` module docs and era task packs.

## Role

- Auth, billing, usage, jobs orchestration, uploads, AI chats, campaigns, and all product GraphQL operations surfaced to clients.

## Related

- Async jobs surface: [jobs.api.md](jobs.api.md)
- Connectra data plane: [connectra.api.md](connectra.api.md)
- Runtime analysis: [appointment360-codebase-analysis.md](../../codebases/appointment360-codebase-analysis.md)
