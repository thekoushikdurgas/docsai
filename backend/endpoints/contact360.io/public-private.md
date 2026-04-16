# Public vs authenticated

## Public (no JWT)

- REST: `/`, `/health`, `/health/*` (as exposed in `main.py`)
- GraphQL: `health.apiMetadata`, `health.apiHealth`, `auth` login/register (and related unauthenticated auth operations per schema)

## Authenticated (Bearer JWT)

- Essentially all other GraphQL fields, including `contacts`, `email`, **`phone`**, `campaignSatellite`, `aiChats`, `admin` (role-gated), etc.

## SuperAdmin-only

- e.g. `health.performanceStats`, many `admin.*` operations — see resolvers in `app/graphql/modules/admin/`.
