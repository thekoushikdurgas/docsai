# Events boundary

- **No outbound Kafka** from the gateway in the current codebase.
- **SSE:** `AIServerClient.send_message_stream` consumes **HTTP chunked/SSE** from ai.server (`/api/v1/ai-chats/{id}/message/stream`). The default GraphQL `sendMessage` mutation uses the **non-streaming** JSON endpoint for simplicity.
- **Queues:** Satellites (email, phone, campaign, s3storage, log) use **Redis/Asynq** on their side; gateway only polls job status where applicable.
- **Idempotency / abuse:** Backed by **Postgres** tables in the gateway DB.
