-- CRUD examples: sessions — DDL: ../sessions.sql

-- SELECT
SELECT * FROM sessions WHERE token_hash = :hash AND is_active = TRUE;

-- INSERT
INSERT INTO sessions (user_id, token_hash, user_agent, ip_address)
VALUES (:user_uuid, :hash, :ua, :ip);

-- UPDATE
UPDATE sessions SET last_activity = NOW() WHERE id = :id;

-- DELETE
DELETE FROM sessions WHERE user_id = :user_uuid OR id = :id;
