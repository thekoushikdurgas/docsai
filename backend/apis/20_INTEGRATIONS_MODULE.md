# Integrations (gateway status)

## Current state

The Contact360 GraphQL gateway (`contact360.io/api`) **does not** implement an `integrations` module. There is **no** `app/graphql/modules/integrations/` package and no `integrations` field on the root `Query` / `Mutation` in `app/graphql/schema.py`.

The historical operation list below is a **placeholder** for a future CRM connector surface.

## Placeholder operations (not implemented)

- `listIntegrations(input: ListIntegrationsInput): IntegrationConnection`
- `connectIntegration(input: ConnectIntegrationInput!): Integration`
- `disconnectIntegration(id: ID!): Boolean`
- `syncContacts(input: SyncIntegrationInput!): IntegrationSyncJob`

## Related

- [06_WEBHOOKS_MODULE.md](06_WEBHOOKS_MODULE.md) — outbound webhooks not implemented on the gateway either.
- [00_SERVICE_MESH_CONTRACTS.md](00_SERVICE_MESH_CONTRACTS.md) — HTTP clients that *do* exist today.

When an integrations module ships, replace this stub with: resolver paths, auth, `Settings` env vars, and data stores.
