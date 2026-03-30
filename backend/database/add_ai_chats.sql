-- Migration: add ai_chats for Contact AI (contact.ai) microservice
-- Safe to run on existing DBs: uses IF NOT EXISTS.
-- Apply after users table exists. Aligns with app.models.ai_chat.AIChat.

CREATE TABLE IF NOT EXISTS ai_chats (
    id TEXT PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    user_id TEXT NOT NULL REFERENCES users (uuid) ON DELETE CASCADE,
    title VARCHAR(255) DEFAULT '',
    messages JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_ai_chats_user_id ON ai_chats (user_id);
CREATE INDEX IF NOT EXISTS idx_ai_chats_created_at ON ai_chats (created_at);
CREATE INDEX IF NOT EXISTS idx_ai_chats_updated_at ON ai_chats (updated_at);

COMMENT ON TABLE ai_chats IS 'AI chat threads per user; REST API: backend(dev)/contact.ai';
COMMENT ON COLUMN ai_chats.uuid IS 'Public chat id used in API paths and responses';
COMMENT ON COLUMN ai_chats.messages IS 'JSON array of {sender, text, contacts?} message objects';
