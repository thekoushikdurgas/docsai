-- CRUD examples: notifications — DDL: ../notifications.sql

-- SELECT
SELECT * FROM notifications WHERE user_id = :user_uuid AND read = FALSE ORDER BY created_at DESC;

-- INSERT
INSERT INTO notifications (user_id, type, priority, title, message)
VALUES (:user_uuid, 'system'::notification_type, 'medium'::notification_priority, :title, :message);

-- UPDATE
UPDATE notifications SET read = TRUE, read_at = NOW() WHERE id = :id AND user_id = :user_uuid;

-- DELETE
DELETE FROM notifications WHERE id = :id;
