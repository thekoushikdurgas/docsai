-- CRUD examples: user_activities — DDL: ../user_activities.sql

-- SELECT
SELECT * FROM user_activities WHERE user_id = :user_uuid ORDER BY created_at DESC LIMIT 100;

-- INSERT
INSERT INTO user_activities (user_id, service_type, action_type, status, result_count)
VALUES (:user_uuid, 'email'::activity_service_type, 'verify'::activity_action_type, 'success'::activity_status, 1);

-- UPDATE
UPDATE user_activities SET status = 'failed'::activity_status, error_message = :err WHERE id = :id;

-- DELETE
DELETE FROM user_activities WHERE id = :id;
