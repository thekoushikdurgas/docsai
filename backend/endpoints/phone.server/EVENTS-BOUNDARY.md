# Events

**phone.server** does not push webhooks to Contact360. Integrations should poll **`GET /jobs/:id/status`** (or use the gateway’s job APIs once wired) for async job progress.
