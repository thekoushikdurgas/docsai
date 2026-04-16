# campaign.server — ecosystem boundary (Era 2)

- **Owns:** Postgres `campaigns`, `recipients`, `templates`, `sequences`, `sequence_steps`, `suppression_list`; S3 objects for templates; Redis Asynq queues.
- **Calls:** **sync.server (Connectra)** for `GET /contacts/{uuid}` when enrolling a sequence step; optional **email.server** / **phone.server** HTTP clients for future enrichment; **S3** via AWS SDK for template storage.
- **Does not own:** CRM tenancy (gateway JWT); Kafka topics.
