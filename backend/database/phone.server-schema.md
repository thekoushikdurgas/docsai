# phone.server — Postgres reference

## `phoneapi_jobs`

Defined in [`EC2/phone.server/migrations/001_phoneapi_jobs.sql`](../../EC2/phone.server/migrations/001_phoneapi_jobs.sql). Column `total_emails` is legacy naming from the email stack; counts generic job rows.

## Other tables

GORM may manage `email_patterns`, `email_finder_cache`, etc. (same schema family as email satellite). See [`email.server-schema.md`](email.server-schema.md) for the parallel pattern; align migrations for production as needed.

## Redis

Asynq queues and `job:{id}:*` keys — see [`DEPLOY.md`](../endpoints/phone.server/DEPLOY.md).
