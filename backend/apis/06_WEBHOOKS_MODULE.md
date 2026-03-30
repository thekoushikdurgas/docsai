# Webhooks Module

The Webhooks module defines outbound event subscriptions for tenant-safe, signed callback delivery.
**Era:** `8.x` (Public and private APIs)
**Location:** `app/graphql/modules/webhooks/`

## Overview

- Register callback URLs and event subscriptions per user/workspace
- Sign each delivery with an HMAC secret
- Retry failures with exponential backoff and DLQ handoff
- Enforce strict ownership and secret rotation rules

## Queries and mutations - parameters and return types

| Operation | Parameters | Variable type | Required | Return type | Description |
|---|---|---|---|---|---|
| `listWebhooks` | `input` | `ListWebhooksInput` | No | `WebhookConnection` | Returns paginated webhook subscriptions for current user. |
| `subscribeWebhook` | `input` | `CreateWebhookInput!` | Yes | `Webhook` | Creates a new webhook subscription and returns signing secret once. |
| `deleteWebhook` | `id` | `ID!` | Yes | `Boolean` | Soft-deletes webhook and disables future deliveries. |
| `replayWebhookEvent` | `input` | `ReplayWebhookInput!` | Yes | `WebhookReplayResult` | Replays delivery for audit-safe recovery flows. |

## Delivery Contract

- Header `X-Contact360-Signature: sha256=<hmac>`
- Header `X-Contact360-Event: <event_type>`
- Header `X-Contact360-Delivery-Id: <uuid>`
- Retry schedule: `1m`, `5m`, `15m`, `1h`, `6h` (max 5 attempts)
- After max retry: move to DLQ and emit `webhook.delivery.failed`

## Related Modules

- `20_INTEGRATIONS_MODULE.md` (connector event consumers)
- `18_ANALYTICS_MODULE.md` (delivery dashboards)

## Documentation metadata

- Era: `8.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

