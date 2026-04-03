-- CRUD examples: user_scraping — DDL: ../user_scraping.sql

-- SELECT
SELECT * FROM user_scraping WHERE user_id = :user_uuid ORDER BY timestamp DESC LIMIT 50;

-- INSERT
INSERT INTO user_scraping (user_id, timestamp, version, source, search_context)
VALUES (:user_uuid, NOW(), '1.0', 'sales_navigator', '{}'::jsonb);

-- UPDATE
UPDATE user_scraping SET search_context = :ctx::jsonb WHERE id = :id;

-- DELETE
DELETE FROM user_scraping WHERE id = :id;
