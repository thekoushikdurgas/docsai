-- CRUD examples: integrations — DDL: ../integrations.sql

-- SELECT
SELECT * FROM integrations WHERE user_id = :user_uuid::uuid;

-- INSERT
INSERT INTO integrations (user_id, provider, config)
VALUES (:user_uuid::uuid, 'hubspot'::integration_provider, '{}'::jsonb);

-- UPDATE
UPDATE integrations SET access_token_enc = :tok, expires_at = :exp, updated_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM integrations WHERE id = :id;
