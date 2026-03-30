-- Subscription Plan Periods Table
-- Pricing periods (monthly, quarterly, yearly) for subscription plans

CREATE TABLE IF NOT EXISTS subscription_plan_periods (
    id SERIAL PRIMARY KEY,
    plan_tier VARCHAR(50) NOT NULL,
    period VARCHAR(20) NOT NULL,
    credits INTEGER NOT NULL,
    rate_per_credit NUMERIC(10, 6) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    savings_amount NUMERIC(10, 2),
    savings_percentage INTEGER,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_subscription_plan_periods_plan_tier FOREIGN KEY (plan_tier) REFERENCES subscription_plans(tier) ON DELETE CASCADE,
    CONSTRAINT uq_subscription_plan_periods_unique UNIQUE (plan_tier, period)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_subscription_plan_periods_plan_tier ON subscription_plan_periods (plan_tier);
CREATE INDEX IF NOT EXISTS idx_subscription_plan_periods_period ON subscription_plan_periods (period);
CREATE UNIQUE INDEX IF NOT EXISTS idx_subscription_plan_periods_unique ON subscription_plan_periods (plan_tier, period);
