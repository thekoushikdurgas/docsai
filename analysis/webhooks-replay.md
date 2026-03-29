# Webhooks Replay (8.x)

## Service Contracts

### mailvetter
- Signature: `HMAC-SHA256` in `X-Webhook-Signature`
- Secret isolation: `WEBHOOK_SECRET_KEY` must not reuse `API_SECRET_KEY`
- Event identity: use `job_id` as replay-safe `event_id`
- Retry and DLQ tracking via `jobs.webhook_sent` event stream

### emailcampaign
- Events: `campaign.created`, `campaign.completed`, `recipient.unsubscribed`
- Store subscriptions in `webhook_subscriptions`
- Track attempts in `webhook_delivery_log`

### jobs (tkdjob)
- Callback URL contract for completion/failure
- Job timeline is the canonical audit trail for callback lifecycle

## Endpoint Matrix References
- `docs/backend/endpoints/mailvetter_endpoint_era_matrix.json`
- `docs/backend/endpoints/emailcampaign_endpoint_era_matrix.json`
