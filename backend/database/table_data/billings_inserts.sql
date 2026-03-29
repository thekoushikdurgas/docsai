-- =====================================================
-- INSERT STATEMENTS FOR SUBSCRIPTION PLANS
-- =====================================================
-- Note: Insert subscription_plans first (parent table)

INSERT INTO subscription_plans (tier, name, category, is_active, created_at, updated_at) VALUES
('5k', '5k Credits Tier', 'STARTER', TRUE, '2025-11-27 17:03:26.132824 +00:00', NULL),
('25k', '25k Credits Tier', 'STARTER', TRUE, '2025-11-27 17:03:26.132824 +00:00', NULL),
('100k', '100k Credits Tier', 'PROFESSIONAL', TRUE, '2025-11-27 17:03:26.132824 +00:00', NULL),
('500k', '500k Credits Tier', 'PROFESSIONAL', TRUE, '2025-11-27 17:03:26.132824 +00:00', NULL),
('1M', '1M Credits Tier', 'BUSINESS', TRUE, '2025-11-27 17:03:26.132824 +00:00', NULL),
('5M', '5M Credits Tier', 'BUSINESS', TRUE, '2025-11-27 17:03:26.132824 +00:00', NULL),
('10M', '10M Credits Tier', 'ENTERPRISE', TRUE, '2025-11-27 17:03:26.132824 +00:00', NULL);

-- =====================================================
-- INSERT STATEMENTS FOR SUBSCRIPTION PLAN PERIODS
-- =====================================================
-- Note: Insert after subscription_plans (foreign key dependency)
-- Note: id column is SERIAL (auto-increment), so we don't specify it

INSERT INTO subscription_plan_periods (plan_tier, period, credits, rate_per_credit, price, savings_amount, savings_percentage, created_at, updated_at) VALUES
('5k', 'monthly', 5000, 0.002000, 10.00, NULL, NULL, '2025-11-27 17:03:26.803685 +00:00', NULL),
('5k', 'quarterly', 15000, 0.001800, 27.00, 3.00, 10, '2025-11-27 17:03:26.803685 +00:00', NULL),
('5k', 'yearly', 60000, 0.001600, 96.00, 24.00, 20, '2025-11-27 17:03:26.803685 +00:00', NULL),
('25k', 'monthly', 25000, 0.001200, 30.00, NULL, NULL, '2025-11-27 17:03:27.458154 +00:00', NULL),
('25k', 'quarterly', 75000, 0.001080, 81.00, 9.00, 10, '2025-11-27 17:03:27.458154 +00:00', NULL),
('25k', 'yearly', 300000, 0.000960, 288.00, 72.00, 20, '2025-11-27 17:03:27.458154 +00:00', NULL),
('100k', 'monthly', 100000, 0.000990, 99.00, NULL, NULL, '2025-11-27 17:03:28.105454 +00:00', NULL),
('100k', 'quarterly', 300000, 0.000891, 267.00, 30.00, 10, '2025-11-27 17:03:28.105454 +00:00', NULL),
('100k', 'yearly', 1200000, 0.000792, 950.00, 238.00, 20, '2025-11-27 17:03:28.105454 +00:00', NULL),
('500k', 'monthly', 500000, 0.000398, 199.00, NULL, NULL, '2025-11-27 17:03:28.758083 +00:00', NULL),
('500k', 'quarterly', 1500000, 0.000358, 537.00, 60.00, 10, '2025-11-27 17:03:28.758083 +00:00', NULL),
('500k', 'yearly', 6000000, 0.000318, 1910.00, 478.00, 20, '2025-11-27 17:03:28.758083 +00:00', NULL),
('1M', 'monthly', 1000000, 0.000299, 299.00, NULL, NULL, '2025-11-27 17:03:29.412532 +00:00', NULL),
('1M', 'quarterly', 3000000, 0.000269, 807.00, 90.00, 10, '2025-11-27 17:03:29.412532 +00:00', NULL),
('1M', 'yearly', 12000000, 0.000239, 2870.00, 718.00, 20, '2025-11-27 17:03:29.412532 +00:00', NULL),
('5M', 'monthly', 5000000, 0.000200, 999.00, NULL, NULL, '2025-11-27 17:03:30.062823 +00:00', NULL),
('5M', 'quarterly', 15000000, 0.000180, 2697.00, 300.00, 10, '2025-11-27 17:03:30.062823 +00:00', NULL),
('5M', 'yearly', 60000000, 0.000160, 9590.00, 2398.00, 20, '2025-11-27 17:03:30.062823 +00:00', NULL),
('10M', 'monthly', 10000000, 0.000160, 1599.00, NULL, NULL, '2025-11-27 17:03:30.725713 +00:00', NULL),
('10M', 'quarterly', 30000000, 0.000144, 4317.00, 480.00, 10, '2025-11-27 17:03:30.725713 +00:00', NULL),
('10M', 'yearly', 120000000, 0.000128, 15350.00, 3838.00, 20, '2025-11-27 17:03:30.725713 +00:00', NULL);

-- =====================================================
-- INSERT STATEMENTS FOR ADDON PACKAGES
-- =====================================================
-- Note: Independent table, can be inserted in any order

INSERT INTO addon_packages (id, name, credits, rate_per_credit, price, is_active, created_at, updated_at) VALUES
('small', 'Small', 5000, 0.002000, 10.00, TRUE, '2025-11-27 17:03:31.394296 +00:00', NULL),
('basic', 'Basic', 25000, 0.001200, 30.00, TRUE, '2025-11-27 17:03:31.394296 +00:00', NULL),
('standard', 'Standard', 100000, 0.000990, 99.00, TRUE, '2025-11-27 17:03:31.394296 +00:00', NULL),
('plus', 'Plus', 500000, 0.000398, 199.00, TRUE, '2025-11-27 17:03:31.394296 +00:00', NULL),
('pro', 'Pro', 1000000, 0.000299, 299.00, TRUE, '2025-11-27 17:03:31.394296 +00:00', NULL),
('advanced', 'Advanced', 5000000, 0.000200, 999.00, TRUE, '2025-11-27 17:03:31.394296 +00:00', NULL),
('premium', 'Premium', 10000000, 0.000160, 1599.00, TRUE, '2025-11-27 17:03:31.394296 +00:00', NULL);