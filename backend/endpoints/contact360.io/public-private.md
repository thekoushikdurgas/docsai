# Public vs authenticated

**Last reviewed:** 2026-04-19 — anchor: [`DECISIONS.md`](../../DECISIONS.md) § GraphQL status.

## Public (no JWT)

- REST: `/`, `/health`, `/health/*` (as exposed in `main.py`)
- GraphQL: `health.apiMetadata`, `health.apiHealth`, `auth` login/register (and related unauthenticated auth operations per schema)

## Authenticated (Bearer JWT) — product API

- Essentially all other GraphQL fields, including `contacts`, `email`, **`phone`**, `campaignSatellite`, `aiChats`, `admin` (role-gated), etc.
- **Partners / automation** should use the **public REST v1** surface (OpenAPI) when shipped — GraphQL remains **first-class for dashboard + extension** only.

## SuperAdmin-only

- e.g. `health.performanceStats`, many `admin.*` operations — see resolvers in `app/graphql/modules/admin/`.

## Public REST (future / v1 subset)

- **Policy:** REST + OpenAPI for **external** integrations; **never** expose satellite base URLs or API keys to partners ([`8.Contact360 public and private apis and endpoints/REST-V1-SUBSET.md`](../../../8.Contact360%20public%20and%20private%20apis%20and%20endpoints/REST-V1-SUBSET.md)).
- **Shape:** **Gateway-shaped CRM DTOs** (stable JSON resources), not raw Connectra payloads — see [`OPEN-DECISIONS-RESOLVED.md`](../../../OPEN-DECISIONS-RESOLVED.md).

## Schema reference automation

- Regenerate [`GRAPHQL-SCHEMA.md`](GRAPHQL-SCHEMA.md) when Strawberry types change — see [`GRAPHQL-SCHEMA-GENERATION.md`](GRAPHQL-SCHEMA-GENERATION.md).
