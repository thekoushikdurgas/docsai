# Integrations Module

The Integrations module manages external CRM and automation connector lifecycle.
**Era:** `9.x`
**Location:** `app/graphql/modules/integrations/`

## Operations

- `listIntegrations(input: ListIntegrationsInput): IntegrationConnection`
- `connectIntegration(input: ConnectIntegrationInput!): Integration`
- `disconnectIntegration(id: ID!): Boolean`
- `syncContacts(input: SyncIntegrationInput!): IntegrationSyncJob`

## Supported providers

- `salesforce`
- `hubspot`
- `zapier`
- `pipedrive`
- `close`

## Security and tenancy

- Token fields encrypted at rest
- Tenant scope required for all reads and writes
- OAuth callback state includes nonce and expiry

## Documentation metadata

- Era: `8.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

