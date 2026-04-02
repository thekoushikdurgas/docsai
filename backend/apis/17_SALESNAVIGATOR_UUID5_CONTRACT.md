# Sales Navigator UUID5 Contract

This contract freezes identity generation semantics for Sales Navigator ingestion into Connectra.

## Canonical identity keys

- **Company UUID**: UUID5 derived from normalized company identity
  - inputs: normalized `company_name` + normalized `company_url`
- **Contact UUID**: UUID5 derived from normalized person identity
  - inputs: normalized LinkedIn URL + normalized email fallback

## Contract goals

- Deterministic IDs for idempotent upserts
- Stable joins between repeated scrape/save runs
- No duplicate business rows from replayed payloads

## Rules

1. URL normalization must strip query string and trailing slash.
2. Missing values must use consistent placeholders before hashing.
3. Same logical profile payload must produce the same UUID values across retries/chunks.
4. UUID generation logic must remain backward compatible for existing records.

## GraphQL gateway

Browser/extension flows can call `mutation { salesNavigator { saveSalesNavigatorProfiles(...) } }` on the Contact360 gateway; Connectra upserts still follow this UUID5 contract when the downstream `salesnavigator` service processes payloads. Resolver-level fields and env wiring: [23_SALES_NAVIGATOR_MODULE.md](23_SALES_NAVIGATOR_MODULE.md).

## Evidence

- Sales Navigator service save pipeline:
  - `backend(dev)/salesnavigator/app/services/save_service.py`
- UUID helper functions:
  - `backend(dev)/salesnavigator/app/services/sales_navigator/utils.py`
- Idempotency test coverage:
  - `backend(dev)/salesnavigator/tests/test_save_service.py`
