-- CRUD examples: ai_chats — DDL: ../ai_chats.sql

-- SELECT
SELECT * FROM ai_chats WHERE uuid = :chat_uuid OR user_id = :user_uuid ORDER BY updated_at DESC NULLS LAST;

-- INSERT
INSERT INTO ai_chats (id, uuid, user_id, title, messages)
VALUES (:id, :uuid, :user_uuid, :title, '[]'::jsonb);

-- UPDATE
UPDATE ai_chats SET messages = messages || :msg::jsonb, updated_at = NOW() WHERE uuid = :chat_uuid;

-- DELETE
DELETE FROM ai_chats WHERE uuid = :chat_uuid AND user_id = :user_uuid;
