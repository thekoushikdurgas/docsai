# Webhooks (gateway status)

## Current state

The Contact360 GraphQL gateway (`contact360.io/api`) **does not** expose a `webhooks` module under `app/graphql/modules/`. There are **no** webhook subscription queries or mutations in the Strawberry schema, and **no** HTTP webhook receiver routes in `app/main.py`.

Shared code exists only for **outbound signing helpers** (for potential future use), e.g. `app/utils/webhook_signature.py`.

## Implications for docs and clients

- Do **not** expect GraphQL operations such as `listWebhooks` or `subscribeWebhook` on this service until a module is added and registered in `app/graphql/schema.py`.
- Product integrations that consume events should follow **`20_INTEGRATIONS_MODULE.md`** and any service-specific contracts; this file documents **gateway reality only**.

## If / when a module is introduced

Document here:

- Root field name (`Query` / `Mutation` namespace).
- Env vars (secrets, HMAC, retry).
- Delivery headers and retry policy.

## Related

- `00_SERVICE_MESH_CONTRACTS.md` — downstream HTTP clients and env vars.
- `20_INTEGRATIONS_MODULE.md` — integration-facing contracts.
