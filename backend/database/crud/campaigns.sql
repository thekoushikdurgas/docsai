-- CRUD examples: campaigns — DDL: ../campaigns.sql

-- SELECT
SELECT * FROM campaigns WHERE user_id = :user_uuid::uuid;

-- INSERT
INSERT INTO campaigns (user_id, name, status, audience_filter)
VALUES (:user_uuid::uuid, :name, 'draft'::campaign_status, '{}'::jsonb);

-- UPDATE
UPDATE campaigns SET status = 'scheduled'::campaign_status, scheduled_at = :at WHERE id = :id;

-- DELETE
DELETE FROM campaigns WHERE id = :id;
