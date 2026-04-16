# email.server — Connectra (sync.server) integration

The **email finder** path queries the **Connectra** HTTP API before pattern generation and verification.

## Client

[`internal/clients/connectra_client.go`](../../../../EC2/email.server/internal/clients/connectra_client.go)

- **Method:** `POST`
- **Path:** `/contacts/` (relative to `CONNECTRA_BASE_URL`)
- **Headers:** `Content-Type: application/json`, **`X-API-Key: CONNECTRA_API_KEY`**
- **Body:** JSON payload built in [`fetchFromConnectra`](../../../../EC2/email.server/internal/services/email_finder_service.go) (search-style contact query; mirrors gateway “search contacts raw” behavior).

## Configuration

Set in `.env` or process environment:

- `CONNECTRA_BASE_URL` — e.g. `http://<sync-server-host>:8000` or mapped port (see [sync.server DEPLOY](../sync.server/DEPLOY.md)).
- `CONNECTRA_API_KEY` — must match sync.server’s expected API key.
- `CONNECTRA_TIMEOUT`, `CONNECTRA_RETRY_ATTEMPTS`, `CONNECTRA_RETRY_DELAY` — tune outbound reliability.

## Failure modes

- **Timeout:** Finder logs a warning and continues with pattern + generator + verification (see [`FindEmails`](../../../../EC2/email.server/internal/services/email_finder_service.go)).
- **No hit:** Pipeline proceeds to pattern DB + email generator + race verification.

## Data ownership

- **Contacts/companies of record:** sync.server (Postgres + OpenSearch).
- **email.server** does not write back to Connectra from finder; it only **reads** to short-circuit when a match exists.
