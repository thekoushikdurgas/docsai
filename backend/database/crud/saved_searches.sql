-- CRUD examples: saved_searches — DDL: ../saved_searches.sql

-- SELECT
SELECT * FROM saved_searches WHERE user_id = :user_uuid ORDER BY updated_at DESC NULLS LAST;

-- INSERT
INSERT INTO saved_searches (user_id, name, type, filters)
VALUES (:user_uuid, :name, 'contact'::saved_search_type, '{}'::json);

-- UPDATE
UPDATE saved_searches SET use_count = use_count + 1, last_used_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM saved_searches WHERE id = :id AND user_id = :user_uuid;
