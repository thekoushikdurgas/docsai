-- CRUD examples: api_keys — DDL: ../api_keys.sql

-- SELECT
SELECT id, name, key_prefix, read_access, write_access, created_at FROM api_keys WHERE user_id = :user_uuid;

-- INSERT
INSERT INTO api_keys (user_id, name, key_hash, key_prefix, read_access, write_access)
VALUES (:user_uuid, :name, :key_hash, :prefix, TRUE, FALSE);

-- UPDATE
UPDATE api_keys SET last_used_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM api_keys WHERE id = :id AND user_id = :user_uuid;
