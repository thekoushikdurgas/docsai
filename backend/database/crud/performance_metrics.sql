-- CRUD examples: performance_metrics — DDL: ../performance_metrics.sql

-- SELECT
SELECT * FROM performance_metrics WHERE user_id = :user_uuid ORDER BY timestamp DESC LIMIT 100;

-- INSERT
INSERT INTO performance_metrics (user_id, metric_name, metric_value, timestamp, metric_metadata)
VALUES (:user_uuid, 'LCP', 2.5, NOW(), '{}'::jsonb);

-- UPDATE
UPDATE performance_metrics SET metric_value = :val WHERE id = :id;

-- DELETE
DELETE FROM performance_metrics WHERE user_id = :user_uuid AND created_at < NOW() - INTERVAL '90 days';
