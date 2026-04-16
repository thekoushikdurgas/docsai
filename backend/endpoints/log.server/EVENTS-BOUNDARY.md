# log.server — events (Kafka vs push)

## Inbound

- The **gateway** and other services **push** logs via HTTP (`POST /logs`, `POST /logs/batch`). There is **no inbound Kafka** consumer in this service.

## Outbound

- **No Kafka** or webhooks are emitted from log.server for log lines.
- **S3** is the durable sink for **CSV** snapshots; **TTL sweep** deletes old objects.

## Polling

- Not required for ingestion. Admin UIs may **poll** GraphQL (`admin.logs`) which calls the gateway client, which calls the HTTP API.

Last updated: 2026-04-15.
