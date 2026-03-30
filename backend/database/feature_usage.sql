-- Feature Usage Table
-- Feature usage tracking per user

CREATE TABLE IF NOT EXISTS feature_usage (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    feature feature_type NOT NULL,
    used INTEGER NOT NULL DEFAULT 0,
    "limit" INTEGER NOT NULL DEFAULT 0,
    period_start TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    period_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_feature_usage_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE,
    CONSTRAINT uq_feature_usage_user_feature UNIQUE (user_id, feature)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_feature_usage_user_id ON feature_usage (user_id);
CREATE INDEX IF NOT EXISTS idx_feature_usage_feature ON feature_usage (feature);
CREATE INDEX IF NOT EXISTS idx_feature_usage_user_feature ON feature_usage (user_id, feature);
CREATE INDEX IF NOT EXISTS idx_feature_usage_period_start ON feature_usage (period_start);
