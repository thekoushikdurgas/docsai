-- CRUD examples: token_blacklist — DDL: ../token_blacklist.sql

-- SELECT
SELECT * FROM token_blacklist WHERE token = :token;

-- INSERT
INSERT INTO token_blacklist (token, user_id, expires_at)
VALUES (:token, :user_uuid, :expires_at);

-- UPDATE (tokens usually immutable)
UPDATE token_blacklist SET expires_at = :expires_at WHERE token = :token;

-- DELETE
DELETE FROM token_blacklist WHERE expires_at IS NOT NULL AND expires_at < NOW();
