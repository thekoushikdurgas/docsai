-- CRUD examples: subscription_plans — DDL: ../subscription_plans.sql

-- SELECT
SELECT * FROM subscription_plans WHERE is_active = TRUE;

-- INSERT
INSERT INTO subscription_plans (tier, name, category)
VALUES (:tier, :name, :category);

-- UPDATE
UPDATE subscription_plans SET is_active = FALSE, updated_at = NOW() WHERE tier = :tier;

-- DELETE
DELETE FROM subscription_plans WHERE tier = :tier;
