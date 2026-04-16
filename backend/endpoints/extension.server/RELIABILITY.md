# extension.server — health and reliability (Era 6)

## Health

- **`GET /health`** — returns **200** with `status: ok` (no dependency checks in extension itself).

## Connectra client

[`internal/connectra/client.go`](../../../../EC2/extension.server/internal/connectra/client.go): HTTP timeout **60s**; up to **4** retries on transport errors and **5xx/429** with backoff.

## Limits

- Save path processes profiles in chunks of **500** per Connectra POST.
- Gateway client validates **≤ 1000** profiles per `save_profiles` call ([`sales_navigator_client.py`](../../../../contact360.io/api/app/clients/sales_navigator_client.py)).

## Tracing

Gin default logger only — no **`X-Request-ID`** middleware in extension (optional future alignment with sync.server).

Last updated: 2026-04-15.
