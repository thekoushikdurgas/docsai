# Connectra contact/company task pack — doc index

The authoritative **Connectra contact + company** analysis lives next to the sync server (imported analysis). Use it when planning **`3.0`–`3.6`** work and when reconciling GraphQL ↔ Connectra ↔ ES/PG.

| Copy | Path |
| --- | --- |
| **Monorepo (sync.server)** | [`EC2/sync.server/docs/imported/analysis/connectra-contact-company-task-pack.md`](../../../EC2/sync.server/docs/imported/analysis/connectra-contact-company-task-pack.md) |
| **Root docs mirror** (if present) | [`contact360.io/root/docs/imported/analysis/connectra-contact-company-task-pack.md`](../../../contact360.io/root/docs/imported/analysis/connectra-contact-company-task-pack.md) |

## How to use with era `3.x`

1. Read gaps in the task pack (VQL, batch-upsert, pagination, provenance columns).
2. Map each gap to a **minor** in [`MINORS_3.0-3.6_MASTER_PLAN_five_tracks.md`](MINORS_3.0-3.6_MASTER_PLAN_five_tracks.md).
3. Update [`docs/backend/graphql.modules/03_CONTACTS_MODULE.md`](../backend/graphql.modules/03_CONTACTS_MODULE.md) and [`04_COMPANIES_MODULE.md`](../backend/graphql.modules/04_COMPANIES_MODULE.md) when contracts change.
