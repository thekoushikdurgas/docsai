# extension.server — events boundary (Era 9)

- **Inbound only:** HTTP requests from the gateway or trusted callers.
- **No outbound webhooks** and **no Kafka** from this service.
- **No polling** of external job queues in production — `cmd/worker` is a placeholder.

Async work is limited to **in-request goroutines** via the internal worker pool.

Last updated: 2026-04-15.
