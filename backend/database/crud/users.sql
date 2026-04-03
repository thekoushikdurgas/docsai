-- CRUD examples: users — DDL: ../users.sql
-- Replace :uuid, :email, etc. with real values.

-- SELECT
SELECT id, uuid, email, name, is_active, created_at FROM users WHERE uuid = :user_uuid LIMIT 1;

-- INSERT (application usually hashes password)
INSERT INTO users (id, uuid, email, hashed_password, name, is_active)
VALUES (gen_random_uuid()::text, :uuid, :email, :hashed_password, :name, TRUE)
RETURNING id, uuid;

-- UPDATE
UPDATE users SET name = :name, updated_at = NOW() WHERE uuid = :user_uuid;

-- DELETE (cascades to dependent tables)
DELETE FROM users WHERE uuid = :user_uuid;
