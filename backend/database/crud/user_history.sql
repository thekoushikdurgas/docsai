-- CRUD examples: user_history — DDL: ../user_history.sql

-- SELECT
SELECT * FROM user_history WHERE user_id = :user_uuid ORDER BY created_at DESC LIMIT 50;

-- INSERT
INSERT INTO user_history (user_id, event_type, ip, country, city)
VALUES (:user_uuid, 'login'::user_history_event_type, :ip, :country, :city);

-- UPDATE (append-only in many apps — updates uncommon)
UPDATE user_history SET device = :device WHERE id = :id;

-- DELETE
DELETE FROM user_history WHERE user_id = :user_uuid AND created_at < NOW() - INTERVAL '1 year';
