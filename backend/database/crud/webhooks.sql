-- CRUD examples: webhooks — DDL: ../webhooks.sql

-- SELECT
SELECT * FROM webhooks WHERE user_id = :user_uuid::uuid AND active = TRUE;

-- INSERT
INSERT INTO webhooks (user_id, url, events, secret_hash)
VALUES (:user_uuid::uuid, :url, ARRAY['campaign.sent']::text[], :secret_hash);

-- UPDATE
UPDATE webhooks SET active = FALSE, updated_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM webhooks WHERE id = :id;
