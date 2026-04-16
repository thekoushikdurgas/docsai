# ai.server — persistence (Era 11)

## Optional Postgres

When **`DATABASE_URL`** is set, [`internal/chats/postgres.go`](../../../EC2/ai.server/internal/chats/postgres.go) ensures:

- **`ai_chats`** — `id` (text PK), `title`, `created_at`, `updated_at`
- **`ai_chat_messages`** — `id`, `chat_id` (FK), `role`, `content`, `created_at`

If `DATABASE_URL` is unset, **in-memory** chat store is used (no persistence).

## Redis

**Asynq** task queue only — not a source of truth for chat content.

Last updated: 2026-04-15.
