# Logs API (`logs.api`)

Structured log ingest and query surfaces used by the gateway, workers, and admin for auditability and observability.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Logging pipeline position |
| [logsapi_endpoint_era_matrix.md](../endpoints/logsapi_endpoint_era_matrix.md) | Routes and era maturity |
| [logsapi_data_lineage.md](../database/logsapi_data_lineage.md) | Storage and retention model |
| [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md) | Gateway log mutations ↔ tables |

### Also in `docs/backend/endpoints/`

- **[README.md](../endpoints/README.md)** — matrix ↔ codebase mapping (includes `logsapi`).
- **[endpoints_index.md](../endpoints/endpoints_index.md)** — [logsapi_endpoint_era_matrix.md](../endpoints/logsapi_endpoint_era_matrix.md) in supplemental indexes; [index.md](../endpoints/index.md) for `graphql/CreateLog`, batch log mutations, and related `*_graphql.md` specs.

## Role

- Ingest from multiple producers; supports batch APIs consumed via gateway mutations such as `graphql/CreateLog` / batch variants—see [index.md](../endpoints/index.md).

## Peer services

- **Appointment360** — emits user- and system-facing events from resolvers.
- **Admin** — Django operator views may call logs clients ([admin.api.md](admin.api.md)).
- **Contact AI** — may emit telemetry to logging pipeline where integrated.
