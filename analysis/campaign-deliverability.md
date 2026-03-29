# Campaign Deliverability (10.x)

## Pre-send verification pipeline

- Mailvetter endpoint: `POST /v1/emails/validate-bulk`.
- Required response mapping per recipient: `valid | invalid | catchall`.
- Verification evidence must be stored and linked to `campaign_id`.

## Bounce and complaint classification

- `hard`: immediate suppression, no retry.
- `soft`: bounded retry then suppress.
- `complaint`: immediate suppression + compliance alert.

## CAN-SPAM and unsubscribe mechanics

- Template footer injects `{{.UnsubscribeURL}}` when missing.
- Unsubscribe SLA target: processing within 10 business days.
- Unsubscribe event is immutable in logsapi audit stream.

## DKIM/SPF and sender readiness

- Sender domain checks run before first send of campaign.
- Block send when DNS validation fails.
- Warmup profile controls campaign send rate per domain.

## 10.x patch delivery mapping

- `10.A.5`: deliverability and suppression controls.
- `10.A.7`: compliance and audit closure for opt-out/bounce paths.
