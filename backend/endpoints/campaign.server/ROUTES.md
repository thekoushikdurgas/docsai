# campaign.server — route inventory (Era 0)

Source: [`EC2/campaign.server/api/router.go`](../../../../EC2/campaign.server/api/router.go).

## Public

| Method | Path | Notes |
|--------|------|--------|
| GET | `/health` | Liveness |
| GET | `/health/ready` | DB ping |
| GET | `/unsub` | Unsubscribe (JWT query `token`) |

## Authenticated (`X-API-Key` = `CAMPAIGN_API_KEY` or `ADMIN_API_KEY`)

### Gateway parity ([`CampaignServiceClient`](../../../../contact360.io/api/app/clients/campaign_service_client.py))

| Group | Methods |
|--------|---------|
| `/campaigns` | GET, POST |
| `/campaigns/:id` | GET, DELETE |
| `/campaigns/:id/stats` | GET |
| `/campaigns/:id/pause` | POST |
| `/campaigns/:id/resume` | POST |
| `/sequences` | GET, POST |
| `/sequences/:id` | GET, DELETE |
| `/sequences/:id/pause` | POST |
| `/sequences/:id/resume` | POST |
| `/sequences/:id/steps` | POST |
| `/sequences/:id/steps/:step_id` | PUT, DELETE |
| `/sequences/:id/trigger` | POST (body `{"contact_uuid"}`) |
| `/campaign-templates` | GET, POST (JSON or multipart) |
| `/campaign-templates/:id` | GET, PUT, DELETE |
| `/campaign-templates/:id/preview` | POST |

### CQL

| Method | Path |
|--------|------|
| POST | `/cql/parse` |
| POST | `/cql/validate` |

### Legacy

| Method | Path |
|--------|------|
| POST | `/campaign` |
| GET | `/campaign/:id/stats` |
| GET | `/list/mailbox`, `/list/inbox`, `/body/:uid` |

## Asynq worker

Task types: `campaign:send` (legacy), `campaign:email`, `campaign:phone`, `campaign:linkedin`, `campaign:sequence_step`. Concurrency: `WORKER_CONCURRENCY` (default **10**).

Last updated: 2026-04-15.
