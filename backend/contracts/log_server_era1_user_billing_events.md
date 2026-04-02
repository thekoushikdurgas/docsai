# log.server — Era 1.x user / billing / credit event baseline

Gateway and workers SHOULD emit structured rows to **`EC2/log.server`** (`POST /logs` or `/logs/batch`) using the existing envelope:

| Field | Type | Notes |
| --- | --- | --- |
| `bucket` | string | Namespace: `user`, `auth`, `billing`, `usage`, `admin`. |
| `level` | string | `info`, `warn`, `error`. |
| `message` | string | Short human-readable summary. |
| `meta` | string | **JSON object serialized as a string** — machine fields below. |
| `created_at` | ISO8601 | Set by server if omitted on ingest. |

## Recommended `meta` JSON (1.x)

All keys are optional unless the event type requires them. Use snake_case.

### Authentication

- `event`: `login_success` | `login_failure` | `logout` | `token_refresh` | `session_revoked`
- `user_id`, `email` (opaque id preferred in shared logs)
- `ip`, `user_agent` (if available)

### Billing / credits

- `event`: `payment_submitted` | `payment_approved` | `payment_declined` | `credits_adjusted`
- `user_id`, `amount_minor`, `currency`, `reference`
- `admin_actor_id` when an admin adjusts credits

### Usage

- `event`: `credit_deducted` | `feature_gate_blocked`
- `user_id`, `feature`, `credits_delta`

**Contract version:** bump when adding required fields; document in [`docs/backend/endpoints/EC2_GO_SATELLITE_ROUTES.md`](../endpoints/EC2_GO_SATELLITE_ROUTES.md) if the HTTP ingest path changes.
