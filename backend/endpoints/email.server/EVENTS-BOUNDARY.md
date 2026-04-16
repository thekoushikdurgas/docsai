# email.server — events and webhooks

**email.server** does **not** emit Kafka events or Contact360 webhooks for job completion.

- **Gateway polling:** The Contact360 API resolves `statusPayload` for `scheduler_jobs` rows with `source_service = email_server` by calling **`GET /jobs/:id/status`** on the satellite (see [`jobs` GraphQL module](../../../../contact360.io/api/app/graphql/modules/jobs/types.py)).
- **No outbound “job done” HTTP callback** is defined in this repo; integrations should poll via the gateway or call the satellite status endpoint with the same API key.

If you add webhooks later, document them here and in [`docs/DECISIONS.md`](../../DECISIONS.md).
