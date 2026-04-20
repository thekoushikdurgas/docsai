# HubSpot integration — MVP (Slice I)

**Owner:** integrations · **Last reviewed:** 2026-04-19

## Scope

One **CRM integration** end-to-end: OAuth, contact/company sync, explicit **conflict winner** vs Connectra (document rules per org).

## Flow

1. OAuth install → store refresh token encrypted in gateway/integration store.
2. **Outbound:** Map Connectra/gateway DTOs → HubSpot objects on a schedule or webhook.
3. **Inbound:** HubSpot webhooks → normalize → Kafka or direct gateway handlers → Connectra upsert with **idempotent** keys.
4. **Conflicts:** Last-write-winner or “Connectra wins” — must be **data-driven** per tenant (no silent fork).

## Related

- Public API subset: [`8.Contact360 public and private apis and endpoints/REST-V1-SUBSET.md`](../8.Contact360%20public%20and%20private%20apis%20and%20endpoints/REST-V1-SUBSET.md)
- Billing pointer: Phase 9 `166-billing` when populated — cross-link from Slice B README.
