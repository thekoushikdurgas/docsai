-- Subscription Plans Table
-- Subscription plan tiers

CREATE TABLE IF NOT EXISTS subscription_plans (
    tier VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_subscription_plans_tier ON subscription_plans (tier);
CREATE INDEX IF NOT EXISTS idx_subscription_plans_category ON subscription_plans (category);
CREATE INDEX IF NOT EXISTS idx_subscription_plans_is_active ON subscription_plans (is_active);
