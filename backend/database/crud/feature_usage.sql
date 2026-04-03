-- CRUD examples: feature_usage — DDL: ../feature_usage.sql

-- SELECT
SELECT * FROM feature_usage WHERE user_id = :user_uuid AND feature = 'AI_CHAT'::feature_type;

-- INSERT
INSERT INTO feature_usage (user_id, feature, used, "limit", period_start, period_end)
VALUES (:user_uuid, 'AI_CHAT'::feature_type, 0, 100, NOW(), NOW() + INTERVAL '30 days')
ON CONFLICT (user_id, feature) DO UPDATE SET used = feature_usage.used + 1, updated_at = NOW();

-- UPDATE
UPDATE feature_usage SET used = used + 1, updated_at = NOW() WHERE user_id = :user_uuid AND feature = 'AI_CHAT'::feature_type;

-- DELETE
DELETE FROM feature_usage WHERE user_id = :user_uuid;
