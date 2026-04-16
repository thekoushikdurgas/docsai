# Gateway boundary

The Python gateway is the **only** GraphQL surface for browsers and first-party clients. It:

1. Owns **Postgres** CRM tables (users, billing, jobs, idempotency, uploads, notifications, …).
2. Proxies to **Connectra** (contacts/companies VQL, jobs).
3. Proxies **email.server** / **phone.server** (finder, verify, patterns, jobs).
4. Proxies **ai.server** (chats, Gemini helpers, VQL parse).
5. Proxies **s3storage.server** (multipart, presign, analysis).
6. Proxies **log.server** (ingest/query) when logging is enabled.
7. Proxies **extension.server** via Sales Navigator client (save-profiles / scrape).
8. Proxies **campaign.server** (campaigns, sequences, templates, CQL).

No Kafka from gateway; optional Mongo log handler pushes to logs satellite over HTTP.
