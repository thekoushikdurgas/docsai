-- CRUD examples: campaign_sequences — DDL: ../campaign_sequences.sql

-- SELECT
SELECT * FROM campaign_sequences WHERE campaign_id = :campaign_id ORDER BY step_order;

-- INSERT
INSERT INTO campaign_sequences (campaign_id, step_order, delay_days, template_id)
VALUES (:campaign_id, 1, 0, NULL);

-- UPDATE
UPDATE campaign_sequences SET delay_days = :days WHERE id = :id;

-- DELETE
DELETE FROM campaign_sequences WHERE id = :id;
