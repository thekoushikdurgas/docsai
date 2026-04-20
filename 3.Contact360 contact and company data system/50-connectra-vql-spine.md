# Connectra + VQL spine (identity order)

**Owner:** crm-platform · **Last reviewed:** 2026-04-19  
**Slice C** — populate deeper stubs in this order: **identity + dedupe + merge → companies → activities (storage) → import → search**.

## Anchors

- **System of record:** Connectra (`sync.server`) — UUID5 parity; batch-upsert ordering — [`docs/DECISIONS.md`](../DECISIONS.md).
- **Gateway `where` JSON:** only from [`contact360.io/api/app/utils/vql_converter.py`](../../../contact360.io/api/app/utils/vql_converter.py).
- **Dashboard triple sync:** [`docs/tech/dashboard-graphql-vql.md`](../tech/dashboard-graphql-vql.md) ↔ this phase ↔ [`52-app-contacts-vql-filters.md`](52-app-contacts-vql-filters.md) ↔ [`docs/docs/contacts-filter-vql-ui.md`](../docs/contacts-filter-vql-ui.md).

## `filterData` / `total`

- **`total`** must reflect the **global** match count when Connectra returns it — not only page length — see `DECISIONS.md` § Dashboard contacts list filters.

## Batch upsert

- HTTP contract and schema notes: [`docs/backend/database/sync.server-schema.md`](../backend/database/sync.server-schema.md)
- Postman: [`EC2/sync.server/docs/postman/README.md`](../../EC2/sync.server/docs/postman/README.md)
