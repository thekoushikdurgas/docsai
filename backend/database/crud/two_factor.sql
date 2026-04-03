-- CRUD examples: two_factor — DDL: ../two_factor.sql

-- SELECT
SELECT * FROM two_factor WHERE user_id = :user_uuid;

-- INSERT
INSERT INTO two_factor (user_id, secret_hash, verified, enabled)
VALUES (:user_uuid, :secret_hash, FALSE, FALSE);

-- UPDATE
UPDATE two_factor SET enabled = TRUE, verified = TRUE, updated_at = NOW() WHERE user_id = :user_uuid;

-- DELETE
DELETE FROM two_factor WHERE user_id = :user_uuid;
