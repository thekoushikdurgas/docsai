# proxy.server — events boundary

Canonical: [`../../../../unihost/proxy.server/docs/EVENTS-BOUNDARY.md`](../../../../unihost/proxy.server/docs/EVENTS-BOUNDARY.md).

- No Kafka; Asynq + HTTP only; poll `/api/v1/jobs/:id/status` for async verify.
