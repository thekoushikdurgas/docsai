-- CRUD examples: subscription_plan_periods — DDL: ../subscription_plan_periods.sql

-- SELECT
SELECT * FROM subscription_plan_periods WHERE plan_tier = :tier;

-- INSERT
INSERT INTO subscription_plan_periods (plan_tier, period, credits, rate_per_credit, price)
VALUES (:tier, 'monthly', 100, 0.01, 9.99);

-- UPDATE
UPDATE subscription_plan_periods SET price = :price, updated_at = NOW() WHERE plan_tier = :tier AND period = :period;

-- DELETE
DELETE FROM subscription_plan_periods WHERE id = :id;
