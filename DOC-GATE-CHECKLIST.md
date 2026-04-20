# Doc update gates (PR checklist)

**Last reviewed:** 2026-04-19

Use this list on every PR that touches **routes, GraphQL, Kafka, auth, satellite env, or VQL**. Full rules: [`DECISIONS-GOVERNANCE.md`](DECISIONS-GOVERNANCE.md).

- [ ] **Route / GraphQL / Kafka / auth:** If this PR changes an **external contract** (HTTP routes, GraphQL fields/inputs, Kafka topics/payloads, JWT/API key/RLS), update [`DECISIONS.md`](DECISIONS.md) in the **same PR**.
- [ ] **Satellite parity:** If routes or env for a satellite/gateway mapping changed, refresh `docs/backend/endpoints/<service>/ROUTES.md` and `AUTH-ENV.md`, update [`backend/endpoints/contact360.io/SATELLITE-PARITY.md`](backend/endpoints/contact360.io/SATELLITE-PARITY.md) for gateway GraphQL aggregation, and update that satellite’s `GATEWAY-PARITY.md` (if present under `docs/backend/endpoints/<service>/`) when GraphQL mapping to that service changes.
- [ ] **VQL converter / Connectra `where` JSON:** If `vql_converter.py` or equivalent changes, triple-sync [`tech/dashboard-graphql-vql.md`](tech/dashboard-graphql-vql.md), [`3.Contact360 contact and company data system/52-app-contacts-vql-filters.md`](3.Contact360%20contact%20and%20company%20data%20system/52-app-contacts-vql-filters.md), and [`docs/contacts-filter-vql-ui.md`](docs/contacts-filter-vql-ui.md).
- [ ] **Gateway GraphQL schema:** If `contact360.io/api/app/graphql/**` changed, regenerate or justify drift for [`backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md`](backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md) per [`backend/endpoints/contact360.io/GRAPHQL-SCHEMA-GENERATION.md`](backend/endpoints/contact360.io/GRAPHQL-SCHEMA-GENERATION.md).

**N/A this PR:** _check the box and write “N/A — docs-only” or similar in the PR description._
