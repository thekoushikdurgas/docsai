# GraphQL schema

- **Composition:** `app/graphql/schema.py` — root `Query` + `Mutation` aggregate modules.
- **Library:** Strawberry (`strawberry.fastapi.GraphQLRouter` on `/graphql`).
- **Extensions:** `QueryComplexityExtension`, `QueryTimeoutExtension` (`app/graphql/extensions.py`).
- **Scalars:** `app/graphql/scalars.py` (`SCALAR_MAP`).

### New / notable fields (Era 0–11)

- **`phone`:** `PhoneQuery` / `PhoneMutation` — phone.server parity with email finder/verify/patterns.
- **`health.satelliteHealth`:** list of `{ name, configured, status, detail }` for configured satellites.
- **`campaignSatellite`:** `campaign`, `sequenceSteps`, `cqlParse`, `cqlValidate`, `campaignTemplate`, `renderTemplatePreview` plus existing list fields.
