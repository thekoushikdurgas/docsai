-- CRUD examples: campaign_templates — DDL: ../campaign_templates.sql

-- SELECT
SELECT * FROM campaign_templates WHERE user_id = :user_uuid::uuid;

-- INSERT
INSERT INTO campaign_templates (user_id, name, body_html)
VALUES (:user_uuid::uuid, :name, :html);

-- UPDATE
UPDATE campaign_templates SET subject = :sub, updated_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM campaign_templates WHERE id = :id AND user_id = :user_uuid::uuid;
