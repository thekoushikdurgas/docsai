# extension.server — persistence (Era 11)

**extension.server** does **not** host a CRM database. It is stateless aside from in-flight request memory.

- **Profiles** persist only after **`POST /internal/extension/upsert-bulk`** on **sync.server** (Postgres + OpenSearch). See [`sync.server-schema.md`](./sync.server-schema.md).

## Optional index (sync.server `contacts`)

For strict **one row per LinkedIn URL** when email is absent, apply the optional migration (commented) in [`EC2/sync.server/migrations/002_contacts_linkedin_url_unique_optional.sql`](../../EC2/sync.server/migrations/002_contacts_linkedin_url_unique_optional.sql) after data cleanup.

Last updated: 2026-04-15.
