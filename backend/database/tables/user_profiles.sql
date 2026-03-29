-- User Profiles Table
-- Extended user information and billing details
drop table public.user_profiles;

CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    job_title VARCHAR(255),
    bio TEXT,
    timezone VARCHAR(100),
    avatar_url TEXT,
    notifications JSON DEFAULT '{}',
    role VARCHAR(50) DEFAULT 'Member',
    -- Billing fields
    credits INTEGER NOT NULL DEFAULT 0,
    subscription_plan VARCHAR(50) DEFAULT 'free',
    subscription_period VARCHAR(20) DEFAULT 'monthly',
    subscription_status VARCHAR(50) DEFAULT 'active',
    subscription_started_at TIMESTAMP WITH TIME ZONE,
    subscription_ends_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_user_profiles_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE UNIQUE INDEX IF NOT EXISTS ix_user_profiles_user_id ON user_profiles (user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles (user_id);
