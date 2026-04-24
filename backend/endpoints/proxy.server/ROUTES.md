# proxy.server — routes (canonical)

Authoritative copy with examples: [`../../../../unihost/proxy.server/docs/ROUTES.md`](../../../../unihost/proxy.server/docs/ROUTES.md).

Summary:

- `GET /health`, `GET /health/ready` — no API key
- `GET|POST|PUT|DELETE /api/v1/proxies...` — proxy CRUD + health-check enqueue
- `POST /api/v1/verify`, `POST /api/v1/verify/bulk` — Reacher bridge
- `GET /api/v1/verify/jobs/:id`, `.../results`
- `GET /api/v1/metrics/pool`, `GET /api/v1/metrics/proxies/:id`
- `GET /api/v1/jobs`, `GET /api/v1/jobs/:id/status`
