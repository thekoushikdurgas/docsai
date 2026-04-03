-- CRUD examples: user_profiles — DDL: ../user_profiles.sql

-- SELECT
SELECT * FROM user_profiles WHERE user_id = :user_uuid LIMIT 1;

-- INSERT
INSERT INTO user_profiles (user_id, role, credits, subscription_plan)
VALUES (:user_uuid, 'FreeUser', 50, 'free')
ON CONFLICT (user_id) DO NOTHING;

-- UPDATE
UPDATE user_profiles SET credits = credits - 1, updated_at = NOW() WHERE user_id = :user_uuid;

-- DELETE (usually cascades from users; direct delete rare)
DELETE FROM user_profiles WHERE user_id = :user_uuid;
