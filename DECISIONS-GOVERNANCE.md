# DECISIONS.md governance

**Last reviewed:** 2026-04-19

## Rule

Any PR that changes an **external contract** must update [`DECISIONS.md`](DECISIONS.md) in the **same PR**:

- New or renamed **HTTP** routes on a satellite or gateway
- New or renamed **GraphQL** fields, inputs, or breaking behavior
- **Kafka** topic names or **event payload** shapes referenced across services
- **Auth** model changes (JWT claims, API key headers, RLS session variables)

## Satellite parity

After changing a satellite’s routes or env:

1. Update the service’s `ROUTES.md` / `AUTH-ENV.md` under `docs/backend/endpoints/<service>/`.
2. Refresh [`backend/endpoints/contact360.io/SATELLITE-PARITY.md`](backend/endpoints/contact360.io/SATELLITE-PARITY.md) and the affected satellite’s `GATEWAY-PARITY.md` (when present under `docs/backend/endpoints/<service>/`) if GraphQL mapping to that service changes.

## VQL triple sync

When `vql_converter.py` changes Connectra `where` JSON:

1. Update [`tech/dashboard-graphql-vql.md`](tech/dashboard-graphql-vql.md).
2. Align Phase 3 app doc [`3.Contact360 contact and company data system/52-app-contacts-vql-filters.md`](3.Contact360%20contact%20and%20company%20data%20system/52-app-contacts-vql-filters.md) and `docs/docs/contacts-filter-vql-ui.md` as needed.
