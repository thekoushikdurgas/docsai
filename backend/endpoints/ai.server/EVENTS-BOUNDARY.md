# ai.server — events boundary (Era 9)

- **Inbound:** HTTP from gateway and trusted callers.
- **Async:** Asynq tasks in **Redis** (`REDIS_ADDR`); no Kafka.
- **No outbound webhooks** from this service.
- **No polling** of external job queues in the API process — workers consume Asynq only.

Last updated: 2026-04-15.
